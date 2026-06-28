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

export const seedData: SeedData = {
  customers: [
    { id: 'cus-rivera', displayName: 'Maya Rivera', email: 'maya@example.test', phone: '555-0101', status: 'active', notes: 'Dummy customer for local development only.', createdAt: now, updatedAt: now },
    { id: 'cus-chen', displayName: 'Theo Chen', email: 'theo@example.test', phone: '555-0102', status: 'lead', createdAt: now, updatedAt: now },
  ],
  properties: [
    { id: 'prop-rivera-home', customerId: 'cus-rivera', label: 'Home yard', streetAddress: '101 Example Lane', city: 'Eureka', state: 'CA', postalCode: '95501', yardSize: 'medium', access: 'gate-code', accessNotes: 'Gate code stored as dummy text only.', serviceNotes: 'Check side yard behind garage.', isPrimary: true, createdAt: now, updatedAt: now },
  ],
  pets: [
    { id: 'pet-rivera-poppy', customerId: 'cus-rivera', propertyId: 'prop-rivera-home', name: 'Poppy', species: 'dog', breed: 'Labrador mix', temperament: 'friendly', createdAt: now, updatedAt: now },
  ],
  servicePlans: [
    { id: 'plan-rivera-weekly', customerId: 'cus-rivera', propertyId: 'prop-rivera-home', status: 'active', frequency: 'weekly', preferredWeekday: 'tuesday', basePriceCents: 2500, addOnPriceCents: 500, currency: 'USD', startsOn: '2026-07-01', notes: 'Dummy weekly plan for schema testing.', createdAt: now, updatedAt: now },
  ],
  visits: [
    { id: 'visit-rivera-2026-07-07', servicePlanId: 'plan-rivera-weekly', customerId: 'cus-rivera', propertyId: 'prop-rivera-home', scheduledFor: '2026-07-07T16:00:00Z', status: 'scheduled', createdAt: now, updatedAt: now },
  ],
  draftInvoices: [
    { id: 'inv-rivera-july-draft', customerId: 'cus-rivera', periodStart: '2026-07-01', periodEnd: '2026-07-31', subtotalCents: 2500, adjustmentCents: 0, totalCents: 2500, currency: 'USD', status: 'draft', lineItems: [{ id: 'line-rivera-visit-2026-07-07', invoiceId: 'inv-rivera-july-draft', visitId: 'visit-rivera-2026-07-07', description: 'Weekly yard cleanup — dummy line item', quantity: 1, unitPriceCents: 2500, totalCents: 2500 }], createdAt: now, updatedAt: now },
  ],
}
