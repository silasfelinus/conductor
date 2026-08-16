# Conductor App — Store Readiness Checklist

Date: 2026-08-16
Task: conductor-app/t-010
Status: prep-only — nothing submitted; several items explicitly need Silas

This is the "prepare, do NOT submit" checklist t-010 asked for. It inventories what's
already in place, what this cycle shipped, and what only Silas can decide or provide
(Apple/Google developer accounts, signing secrets, and the actual submit action are
all outside what an agent should do unattended).

## 1. Bundle identifiers

Already set and consistent between platforms:

- Android `applicationId`: `org.kindrobots.conductor_app` (`android/app/build.gradle.kts`)
- iOS `PRODUCT_BUNDLE_IDENTIFIER`: `org.kindrobots.conductorApp` (`ios/Runner.xcodeproj/project.pbxproj`)

No action needed here — both resolve under the `org.kindrobots` reverse-DNS namespace
already used elsewhere. Confirm these match whatever App Store Connect / Play Console
app records Silas creates (or has already created) before the first real upload.

## 2. Signing

**Gap found, not fixed by this cycle — needs Silas.** `android/app/build.gradle.kts`'s
`release` build type still signs with the debug keystore:

```kotlin
buildTypes {
    release {
        // TODO: Add your own signing config for the release build.
        signingConfig = signingConfigs.getByName("debug")
    }
}
```

This is fine for `flutter run --release` locally but cannot ship to Play Console as-is.
Needed before a real release build:

- A production upload keystore (`keytool -genkey ...`) generated and kept **out of
  source control** — store it in a password manager or CI secret store, not this repo.
  Losing it means losing the ability to update the app under the same listing, so this
  is a one-way door: Play App Signing (Google holds the real signing key, you keep an
  upload key) is the safer default over classic self-managed signing.
- A `key.properties`-style file (gitignored) wired into `build.gradle.kts`'s
  `signingConfigs.release`, following the standard Flutter Android deploy docs pattern.
- On iOS: an Apple Developer Program enrollment, a distribution certificate, and an App
  Store provisioning profile, managed through Xcode/Fastlane or manually in App Store
  Connect. None of this can be generated without Silas's Apple ID and paid enrollment.

Nothing secret-bearing belongs in this repo or in agent hands — this section is
guidance/checklist only, not something to automate further without Silas providing the
actual credentials through his own channel.

## 3. Privacy nutrition labels

Local mode collects nothing — no account, no network calls, no analytics. That's the
easy case for both stores' privacy questionnaires.

Server modes (hosted `kindrobots.org` or self-hosted) do involve an account. The
authoritative inventory of what a kind_robots account holds is the same list the
server's own account-deletion path purges (see §4) — useful raw material for filling in
Apple's "data types collected" / Play's Data Safety form:

| Category | Examples | Linked to identity? | Used for tracking? |
|---|---|---|---|
| Account info | username, email, role | Yes | No |
| User content | projects, dreams, characters, scenarios, art collections/images, prompts, chats | Yes | No |
| App activity | reactions, karma/mana transaction ledgers, achievement records | Yes | No |
| Social | relations/friends, referrals, notifications | Yes | No |

None of this is sold, shared with third parties for advertising, or used for
cross-app tracking — the app makes API calls only to the server the user explicitly
configured (hosted, self-hosted, or none in local mode). This table is a starting
draft, not a filed submission; Silas should review it against the actual current
`User`-linked Prisma models before it goes into either store's form, since kind_robots'
schema can drift from this snapshot.

There is no dedicated in-app or hosted privacy-policy document yet. Both stores require
a reachable privacy-policy URL before submission — this is a real gap, tracked here
rather than fixed silently, since it's Silas's call whether it lives on kindrobots.org
or as a standalone page.

## 4. Account deletion flow

**Shipped this cycle.** Apple requires apps with account creation to offer in-app
account deletion, not just deactivation. `apps/conductor/lib/features/settings/settings_screen.dart`
now has a "Delete account" tile (destructive styling, confirmation dialog, only shown
when signed into a real server account — not shown in local mode, which has no account
to delete). It calls the server's existing `DELETE /api/users/:id` self-delete path
(`AuthController.deleteAccount()` in `lib/features/auth/auth_controller.dart`), which
kind_robots already implements as a real hard-delete cascade
(`server/utils/userPurge.ts`'s `deleteUserWithOwnedData`) covering every table in the
§3 inventory. On success the app resets to the welcome screen, same as "Switch server
mode." Covered by `test/auth_controller_test.dart` (delete call fires with the right
user id and resets local state; no request is made when nobody is signed in).

No further action needed here for store readiness — the flow exists, is destructive
only after explicit confirmation, and matches Apple's discoverability requirement
(Settings, not buried in a support-ticket flow).

## 5. TestFlight / internal-track plan

Draft, not yet executed:

1. **Internal testing first.** Play Console "Internal testing" track and TestFlight
   internal testing (up to 100 users, no App Review needed) — just Silas and anyone he
   adds by email/Apple ID.
2. **Smoke checklist per build:** onboarding → pick server mode → sign in (hosted) →
   browse projects/todos → sign out → delete-account round trip against a disposable
   test account (never a real one) → local-mode path with no server configured.
3. **Escalate to external/beta testing** only after internal builds are stable across
   at least one Android + one iOS device, and only on Silas's call.
4. **Versioning:** bump `pubspec.yaml`'s `version: 0.1.0+1` build number per upload;
   keep the semantic version at `0.x` until this checklist's gaps are closed.

## Summary — what's still needs-human

- Production Android keystore + Play App Signing enrollment (§2)
- iOS Distribution certificate + provisioning profile, Apple Developer Program
  enrollment (§2)
- A reachable privacy-policy URL for both store listings (§3)
- Reviewing the §3 data-safety table against the live Prisma schema before filing it
- Actually running the TestFlight/internal-track plan (§5) and the real store
  submissions — explicitly out of scope for this task per its own note

Everything else in the "prepare" list (bundle ids, account-deletion flow, a concrete
data-collection inventory, and a testing plan) is done or drafted above.
