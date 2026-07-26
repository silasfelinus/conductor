import type { Coordinates, YardSize } from '../schema.js'

export type StopCandidate = {
  customerId: string
  customerName: string
  visitId: string
  propertyId: string
  propertyLabel: string
  neighborhood: string
  yardSize: YardSize
  coordinates: Coordinates | null
}

export type LockedStop = {
  customerId: string
  /** 0-based position among stops only (start/end are not part of this index space). */
  position: number
}

export type ExplicitSelection = {
  mode: 'explicit'
  customerIds: string[]
}

export type FillToNSelection = {
  mode: 'fill-to-n'
  count: number
  sortBy?: 'earliest-due' | 'proximity'
}

export type Selection = ExplicitSelection | FillToNSelection

export type RoutePlanFilter = {
  neighborhood?: string
  frequency?: string
}

export type RoutePlanRequest = {
  date: string
  filter?: RoutePlanFilter
  selection: Selection
  start: Coordinates & { label?: string }
  end?: Coordinates & { label?: string }
  locked?: LockedStop[]
  crewStartTime?: string
}

export type ExcludedCustomer = {
  customerId: string
  customerName: string
  reason: string
}

export type DistanceMatrix = {
  distancesMeters: number[][]
  durationsSeconds: number[][]
}

export type RouteGeometry = {
  polyline: string | null
  instructions: string[]
}

export interface RouteMatrixProvider {
  readonly name: string
  getMatrix(points: Coordinates[]): Promise<DistanceMatrix>
  getRouteGeometry(orderedPoints: Coordinates[]): Promise<RouteGeometry>
}

export type PlannedStop = {
  sequence: number
  customerId: string
  customerName: string
  propertyLabel: string
  neighborhood: string
  coordinates: Coordinates
  locked: boolean
  legDistanceMeters: number
  legDurationSeconds: number
  cumulativeDistanceMeters: number
  cumulativeDurationSeconds: number
  eta: string
}

export type RoutePlanResponse = {
  date: string
  routingProvider: string
  start: Coordinates & { label?: string }
  end: Coordinates & { label?: string }
  stops: PlannedStop[]
  totals: {
    distanceMeters: number
    durationSeconds: number
    estimatedFinishTime: string
  }
  warnings: string[]
  excluded: ExcludedCustomer[]
  instructions: string[]
}
