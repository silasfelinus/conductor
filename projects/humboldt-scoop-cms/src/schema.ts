export type CustomerStatus = 'lead' | 'active' | 'paused' | 'archived'
export type PropertyAccess = 'gate-code' | 'unlocked' | 'key-on-file' | 'appointment-only'
export type PetTemperament = 'friendly' | 'shy' | 'protective' | 'unknown'
export type ServiceFrequency = 'weekly' | 'twice-weekly' | 'biweekly' | 'monthly' | 'one-time'
export type ServicePlanStatus = 'draft' | 'active' | 'paused' | 'cancelled'
export type VisitStatus = 'scheduled' | 'completed' | 'skipped' | 'cancelled'
export type YardSize = 'small' | 'medium' | 'large' | 'extra-large'

export type Customer = {
  id: string
  displayName: string
  email: string
  phone: string
  status: CustomerStatus
  notes?: string
  createdAt: string
  updatedAt: string
}

export type Coordinates = {
  lat: number
  lng: number
}

export type Property = {
  id: string
  customerId: string
  label: string
  streetAddress: string
  city: string
  state: string
  postalCode: string
  yardSize: YardSize
  access: PropertyAccess
  accessNotes?: string
  serviceNotes?: string
  isPrimary: boolean
  /** Dummy coordinates only — no real addresses are geocoded. Null until seeded. */
  coordinates?: Coordinates
  createdAt: string
  updatedAt: string
}

export type Pet = {
  id: string
  customerId: string
  propertyId: string
  name: string
  species: 'dog' | 'cat' | 'other'
  breed?: string
  temperament: PetTemperament
  notes?: string
  createdAt: string
  updatedAt: string
}

export type ServicePlan = {
  id: string
  customerId: string
  propertyId: string
  status: ServicePlanStatus
  frequency: ServiceFrequency
  preferredWeekday: 'monday' | 'tuesday' | 'wednesday' | 'thursday' | 'friday' | 'saturday' | 'sunday'
  basePriceCents: number
  addOnPriceCents: number
  currency: 'USD'
  startsOn: string
  endsOn?: string
  notes?: string
  createdAt: string
  updatedAt: string
}

export type Visit = {
  id: string
  servicePlanId: string
  customerId: string
  propertyId: string
  scheduledFor: string
  completedAt?: string
  status: VisitStatus
  crewNotes?: string
  customerVisibleNotes?: string
  bagsUsed?: number
  createdAt: string
  updatedAt: string
}

export type DraftInvoice = {
  id: string
  customerId: string
  periodStart: string
  periodEnd: string
  subtotalCents: number
  adjustmentCents: number
  totalCents: number
  currency: 'USD'
  status: 'draft' | 'void'
  lineItems: DraftInvoiceLineItem[]
  createdAt: string
  updatedAt: string
}

export type DraftInvoiceLineItem = {
  id: string
  invoiceId: string
  visitId?: string
  description: string
  quantity: number
  unitPriceCents: number
  totalCents: number
}

export type SeedData = {
  customers: Customer[]
  properties: Property[]
  pets: Pet[]
  servicePlans: ServicePlan[]
  visits: Visit[]
  draftInvoices: DraftInvoice[]
}

const now = '2026-06-26T09:22:00Z'

// Dummy, approximate single-point coordinates for named Humboldt County sample
// areas (matching route-cards/SPEC.md's existing sample neighborhoods) -- not
// geocoded from real customer addresses, and not precise to any real property.
const DUMMY_AREA_COORDINATES: Record<string, Coordinates> = {
  eureka: { lat: 40.8021, lng: -124.1637 },
  cutten: { lat: 40.7629, lng: -124.1462 },
  hendersonCenter: { lat: 40.7975, lng: -124.152 },
  myrtletown: { lat: 40.8129, lng: -124.1275 },
  fortuna: { lat: 40.5982, lng: -124.1573 },
}

export const seedData: SeedData = {
  customers: [
    { id: 'cus-rivera', displayName: 'Maya Rivera', email: 'maya@example.test', phone: '555-0101', status: 'active', notes: 'Dummy customer for local development only.', createdAt: now, updatedAt: now },
    { id: 'cus-chen', displayName: 'Theo Chen', email: 'theo@example.test', phone: '555-0102', status: 'lead', createdAt: now, updatedAt: now },
    { id: 'cus-park', displayName: 'Jordan Park', email: 'jordan@example.test', phone: '555-0103', status: 'active', notes: 'Dummy customer for route-planner testing.', createdAt: now, updatedAt: now },
    { id: 'cus-nguyen', displayName: 'Lin Nguyen', email: 'lin@example.test', phone: '555-0104', status: 'active', notes: 'Dummy customer for route-planner testing.', createdAt: now, updatedAt: now },
    { id: 'cus-brooks', displayName: 'Sam Brooks', email: 'sam@example.test', phone: '555-0105', status: 'active', notes: 'Dummy customer for route-planner testing.', createdAt: now, updatedAt: now },
    { id: 'cus-alvarez', displayName: 'Dana Alvarez', email: 'dana@example.test', phone: '555-0106', status: 'active', notes: 'Dummy customer for route-planner testing, no coordinates on file (tests the missing-coordinates exclusion path).', createdAt: now, updatedAt: now },
  ],
  properties: [
    { id: 'prop-rivera-home', customerId: 'cus-rivera', label: 'Home yard', streetAddress: '101 Example Lane', city: 'Eureka', state: 'CA', postalCode: '95501', yardSize: 'medium', access: 'gate-code', accessNotes: 'Gate code stored as dummy text only.', serviceNotes: 'Check side yard behind garage.', isPrimary: true, coordinates: DUMMY_AREA_COORDINATES.eureka, createdAt: now, updatedAt: now },
    { id: 'prop-park-duplex-b', customerId: 'cus-park', label: 'Duplex yard B', streetAddress: '204 Example Court', city: 'Myrtletown', state: 'CA', postalCode: '95503', yardSize: 'small', access: 'unlocked', serviceNotes: 'Shared fence line with unit A -- stay on the B side.', isPrimary: true, coordinates: DUMMY_AREA_COORDINATES.myrtletown, createdAt: now, updatedAt: now },
    { id: 'prop-nguyen-home', customerId: 'cus-nguyen', label: 'Home yard', streetAddress: '77 Example Ave', city: 'Cutten', state: 'CA', postalCode: '95534', yardSize: 'large', access: 'key-on-file', serviceNotes: 'Large back acreage; two dogs, keep gate double-latched.', isPrimary: true, coordinates: DUMMY_AREA_COORDINATES.cutten, createdAt: now, updatedAt: now },
    { id: 'prop-brooks-patio', customerId: 'cus-brooks', label: 'Back patio run', streetAddress: '15 Example Way', city: 'Henderson Center', state: 'CA', postalCode: '95501', yardSize: 'small', access: 'appointment-only', serviceNotes: 'Small fenced run plus gravel strip; skip raised garden beds.', isPrimary: true, coordinates: DUMMY_AREA_COORDINATES.hendersonCenter, createdAt: now, updatedAt: now },
    { id: 'prop-alvarez-home', customerId: 'cus-alvarez', label: 'Home yard', streetAddress: '9 Example Rd', city: 'Fortuna', state: 'CA', postalCode: '95540', yardSize: 'medium', access: 'gate-code', serviceNotes: 'Coordinates not yet on file for this property.', isPrimary: true, createdAt: now, updatedAt: now },
  ],
  pets: [
    { id: 'pet-rivera-poppy', customerId: 'cus-rivera', propertyId: 'prop-rivera-home', name: 'Poppy', species: 'dog', breed: 'Labrador mix', temperament: 'friendly', createdAt: now, updatedAt: now },
    { id: 'pet-park-mochi', customerId: 'cus-park', propertyId: 'prop-park-duplex-b', name: 'Mochi', species: 'dog', breed: 'corgi', temperament: 'shy', createdAt: now, updatedAt: now },
    { id: 'pet-nguyen-rex', customerId: 'cus-nguyen', propertyId: 'prop-nguyen-home', name: 'Rex', species: 'dog', breed: 'shepherd mix', temperament: 'protective', createdAt: now, updatedAt: now },
    { id: 'pet-brooks-tofu', customerId: 'cus-brooks', propertyId: 'prop-brooks-patio', name: 'Tofu', species: 'cat', temperament: 'unknown', createdAt: now, updatedAt: now },
    { id: 'pet-alvarez-biscuit', customerId: 'cus-alvarez', propertyId: 'prop-alvarez-home', name: 'Biscuit', species: 'dog', breed: 'beagle', temperament: 'friendly', createdAt: now, updatedAt: now },
  ],
  servicePlans: [
    { id: 'plan-rivera-weekly', customerId: 'cus-rivera', propertyId: 'prop-rivera-home', status: 'active', frequency: 'weekly', preferredWeekday: 'tuesday', basePriceCents: 2500, addOnPriceCents: 500, currency: 'USD', startsOn: '2026-07-01', notes: 'Dummy weekly plan for schema testing.', createdAt: now, updatedAt: now },
    { id: 'plan-park-biweekly', customerId: 'cus-park', propertyId: 'prop-park-duplex-b', status: 'active', frequency: 'biweekly', preferredWeekday: 'tuesday', basePriceCents: 2000, addOnPriceCents: 0, currency: 'USD', startsOn: '2026-07-01', createdAt: now, updatedAt: now },
    { id: 'plan-nguyen-weekly', customerId: 'cus-nguyen', propertyId: 'prop-nguyen-home', status: 'active', frequency: 'weekly', preferredWeekday: 'tuesday', basePriceCents: 3200, addOnPriceCents: 500, currency: 'USD', startsOn: '2026-07-01', createdAt: now, updatedAt: now },
    { id: 'plan-brooks-weekly', customerId: 'cus-brooks', propertyId: 'prop-brooks-patio', status: 'active', frequency: 'weekly', preferredWeekday: 'tuesday', basePriceCents: 2200, addOnPriceCents: 0, currency: 'USD', startsOn: '2026-07-01', createdAt: now, updatedAt: now },
    { id: 'plan-alvarez-monthly', customerId: 'cus-alvarez', propertyId: 'prop-alvarez-home', status: 'active', frequency: 'monthly', preferredWeekday: 'tuesday', basePriceCents: 2500, addOnPriceCents: 0, currency: 'USD', startsOn: '2026-07-01', createdAt: now, updatedAt: now },
  ],
  visits: [
    { id: 'visit-rivera-2026-07-07', servicePlanId: 'plan-rivera-weekly', customerId: 'cus-rivera', propertyId: 'prop-rivera-home', scheduledFor: '2026-07-07T16:00:00Z', status: 'scheduled', createdAt: now, updatedAt: now },
    { id: 'visit-rivera-2026-07-28', servicePlanId: 'plan-rivera-weekly', customerId: 'cus-rivera', propertyId: 'prop-rivera-home', scheduledFor: '2026-07-28T16:00:00Z', status: 'scheduled', createdAt: now, updatedAt: now },
    { id: 'visit-park-2026-07-28', servicePlanId: 'plan-park-biweekly', customerId: 'cus-park', propertyId: 'prop-park-duplex-b', scheduledFor: '2026-07-28T16:00:00Z', status: 'scheduled', createdAt: now, updatedAt: now },
    { id: 'visit-nguyen-2026-07-28', servicePlanId: 'plan-nguyen-weekly', customerId: 'cus-nguyen', propertyId: 'prop-nguyen-home', scheduledFor: '2026-07-28T16:00:00Z', status: 'scheduled', createdAt: now, updatedAt: now },
    { id: 'visit-brooks-2026-07-28', servicePlanId: 'plan-brooks-weekly', customerId: 'cus-brooks', propertyId: 'prop-brooks-patio', scheduledFor: '2026-07-28T16:00:00Z', status: 'scheduled', createdAt: now, updatedAt: now },
    { id: 'visit-alvarez-2026-07-28', servicePlanId: 'plan-alvarez-monthly', customerId: 'cus-alvarez', propertyId: 'prop-alvarez-home', scheduledFor: '2026-07-28T16:00:00Z', status: 'scheduled', createdAt: now, updatedAt: now },
  ],
  draftInvoices: [
    { id: 'inv-rivera-july-draft', customerId: 'cus-rivera', periodStart: '2026-07-01', periodEnd: '2026-07-31', subtotalCents: 2500, adjustmentCents: 0, totalCents: 2500, currency: 'USD', status: 'draft', lineItems: [{ id: 'line-rivera-visit-2026-07-07', invoiceId: 'inv-rivera-july-draft', visitId: 'visit-rivera-2026-07-07', description: 'Weekly yard cleanup — dummy line item', quantity: 1, unitPriceCents: 2500, totalCents: 2500 }], createdAt: now, updatedAt: now },
  ],
}
