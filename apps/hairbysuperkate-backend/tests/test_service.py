import unittest

from hbs_backend import BackendConfig, InMemorySyncStore, SuperkateSyncService


AUTH = "Bearer local-test-token"
BUSINESS = "hair-by-superkate"


CUSTOMER = {
    "localId": "local-customer-test-1",
    "name": "  Test Client  ",
    "email": " TEST.CLIENT@EXAMPLE.TEST ",
    "createdAt": "2026-07-08T18:00:00Z",
    "updatedAt": "2026-07-08T18:00:00Z",
    "deletedAt": None,
}


APPOINTMENT = {
    "localId": "local-appt-test-1",
    "customerLocalId": "local-customer-test-1",
    "clientNameSnapshot": "Test Client",
    "appointmentDate": "2026-07-08",
    "hourlyRateCents": 8000,
    "timeSpentMinutes": 90,
    "productCostCents": 1500,
    "appointmentTotalCents": 13500,
    "createdAt": "2026-07-08T18:05:00Z",
    "updatedAt": "2026-07-08T18:05:00Z",
    "deletedAt": None,
}


class SuperkateSyncServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = SuperkateSyncService(
            config=BackendConfig(env="test"),
            store=InMemorySyncStore(),
        )

    def test_health_has_no_secret_database_url(self):
        response = self.service.health()
        self.assertTrue(response["success"])
        self.assertEqual(response["data"]["service"], "hair-by-superkate-sync")
        self.assertEqual(response["data"]["mode"], "local-test")
        self.assertNotIn("databaseUrl", response["data"])

    def test_bootstrap_requires_auth(self):
        with self.assertRaises(PermissionError):
            self.service.bootstrap(authorization=None)
        response = self.service.bootstrap(authorization=AUTH)
        self.assertTrue(response["success"])
        self.assertEqual(response["data"]["businessSlug"], BUSINESS)
        self.assertFalse(response["data"]["features"]["directEmailSend"])
        self.assertFalse(response["data"]["features"]["analytics"])

    def test_push_customer_normalizes_email_and_returns_server_id(self):
        response = self.service.push(
            {"businessSlug": BUSINESS, "customers": [CUSTOMER], "appointments": []},
            authorization=AUTH,
        )
        self.assertTrue(response["success"])
        accepted = response["data"]["accepted"]["customers"][0]
        self.assertEqual(accepted["name"], "Test Client")
        self.assertEqual(accepted["email"], "test.client@example.test")
        self.assertTrue(accepted["serverId"].startswith("srv_customer_"))
        self.assertEqual(accepted["ownerUserId"], "test-owner-superkate")

    def test_push_appointment_recomputes_total_and_links_customer(self):
        response = self.service.push(
            {"businessSlug": BUSINESS, "customers": [CUSTOMER], "appointments": [APPOINTMENT]},
            authorization=AUTH,
        )
        appointment = response["data"]["accepted"]["appointments"][0]
        self.assertEqual(appointment["appointmentTotalCents"], 13500)
        self.assertTrue(appointment["customerServerId"].startswith("srv_customer_"))

    def test_mismatched_appointment_total_is_rejected(self):
        bad = dict(APPOINTMENT, appointmentTotalCents=999)
        response = self.service.push(
            {"businessSlug": BUSINESS, "customers": [], "appointments": [bad]},
            authorization=AUTH,
        )
        self.assertEqual(response["data"]["accepted"]["appointments"], [])
        rejected = response["data"]["rejected"][0]
        self.assertEqual(rejected["code"], "VALIDATION_ERROR")
        self.assertEqual(rejected["field"], "appointmentTotalCents")

    def test_tombstoned_customer_does_not_delete_appointment(self):
        self.service.push(
            {"businessSlug": BUSINESS, "customers": [CUSTOMER], "appointments": [APPOINTMENT]},
            authorization=AUTH,
        )
        tombstone = dict(
            CUSTOMER,
            name="Test Client",
            email=None,
            updatedAt="2026-07-08T19:00:00Z",
            deletedAt="2026-07-08T19:00:00Z",
        )
        self.service.push(
            {"businessSlug": BUSINESS, "customers": [tombstone], "appointments": []},
            authorization=AUTH,
        )
        pulled = self.service.pull(business_slug=BUSINESS, after_version=0, authorization=AUTH)
        self.assertEqual(len(pulled["data"]["customers"]), 1)
        self.assertEqual(len(pulled["data"]["appointments"]), 1)
        self.assertIsNotNone(pulled["data"]["customers"][0]["deletedAt"])

    def test_cross_business_access_is_rejected(self):
        response = self.service.push(
            {"businessSlug": "not-hair-by-superkate", "customers": [CUSTOMER], "appointments": []},
            authorization=AUTH,
        )
        self.assertFalse(response["success"])
        self.assertEqual(response["code"], "VALIDATION_ERROR")

    def test_reset_route_is_local_test_only(self):
        self.service.push(
            {"businessSlug": BUSINESS, "customers": [CUSTOMER], "appointments": []},
            authorization=AUTH,
        )
        response = self.service.reset_test_data(authorization=AUTH)
        self.assertTrue(response["success"])
        self.assertEqual(response["data"]["serverVersion"], 0)

        production = SuperkateSyncService(
            config=BackendConfig(env="production"),
            store=InMemorySyncStore(),
        )
        blocked = production.reset_test_data(authorization=AUTH)
        self.assertFalse(blocked["success"])
        self.assertEqual(blocked["code"], "NOT_AVAILABLE")


if __name__ == "__main__":
    unittest.main()
