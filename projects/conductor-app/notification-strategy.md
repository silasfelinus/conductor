# Conductor App — Notification Strategy

Date: 2026-07-03
Task: conductor-app/t-004
Status: design-only; no live notification service configured

## Recommendation

Use a staged notification model:

1. **MVP: local polling + local notifications**
2. **Operator/admin layer: in-app Agent Ops inbox and badge counts**
3. **Later: server push with FCM/APNs only after real usage proves which events matter**

This keeps the first app useful without adding a backend push service, device-token storage, Apple/Google notification setup, or any background task assumptions that would be brittle before the app has stable daily use.

## Events worth notifying on

The app should notify only for state changes that require action or reassurance:

| Event | User value | MVP behavior | Later push behavior |
|---|---|---|---|
| New `needs-human` roadmap task | Silas/operator action required | Local notification if count increases during refresh | Push to admins/operators |
| New blocked/failed Worker task | Something needs triage | In-app badge; local notification only if newly blocked | Push to admins/operators |
| Worker/Reviewer PR merged | Reassurance that automation moved forward | In-app activity item; optional quiet local notification | Optional digest push |
| New high-priority Todo/HONEYDO | User action requested | Local notification if assigned to signed-in user | Push to owning user |
| Art request queued/ready | Creative workflow update | In-app badge only for MVP | Push only when generated asset is ready |
| Pitch awaiting vote | Approval/review needed | In-app badge | Push to admins/operators |

Do **not** notify for every task status change, every roadmap refresh, every chat message, or every generated log line. Notification spam is how apps earn the sacred uninstall speedrun achievement.

## MVP architecture

### Foreground refresh

The app already needs a refresh loop for dashboard freshness. Reuse it:

- On app launch: fetch `/api/users/me`, `/api/conductor/projects`, and `/api/todos`.
- While foregrounded: refresh every 5 minutes.
- On pull-to-refresh or returning from background: refresh immediately.
- Diff the newly fetched snapshot against the last local snapshot.
- Emit a local notification only when an actionable count increases.

Recommended local snapshot fields:

```json
{
  "lastRefreshAt": "2026-07-03T21:14:34-07:00",
  "needsHumanKeys": ["global-ui/t-008", "digital-storefront/t-002"],
  "blockedTaskKeys": [],
  "openHighTodoIds": [123],
  "awaitingPitchSlugs": ["example-pitch"],
  "queuedArtRequestKeys": ["project:pinball-hero:hero"]
}
```

Use stable keys, not counts alone, so the app can identify what is new and avoid repeat notifications for the same item.

### Local notifications

Use `flutter_local_notifications` for MVP local alerts.

Suggested channels/categories:

| Channel | Android importance | iOS interruption | Examples |
|---|---|---|---|
| `agent_ops` | high | active | needs-human task, blocked automation |
| `todos` | default | active | high-priority HONEYDO/Todo |
| `creative_queue` | low | passive | art request queued/ready |
| `digests` | low | passive | daily/weekly summary later |

Default all but `agent_ops` to quiet. Let the Settings screen toggle each channel.

### Badge counts

Badges are more important than push for this app. The dashboard should show:

- `Needs review`: count of `needs-human` tasks visible to the operator/admin layer.
- `Blocked`: count of blocked or stale claimed tasks.
- `Todos`: count of open high-priority user todos.
- `Art queue`: count of queued/in-progress art requests if the app can read them.

For non-admin users, hide Agent Ops badges entirely and only show user-owned Todos/Dream project activity.

## Background behavior

Do not rely on continuous background polling for MVP.

Mobile OS background behavior is intentionally inconsistent:

- iOS limits arbitrary background timers.
- Android varies by OEM battery policy.
- Flutter background fetch plugins add platform complexity and still do not guarantee timely delivery.

MVP rule: notifications are best-effort while the app is foregrounded or recently resumed. The UI should never promise instant alerts.

## Server push: deferred design

Add real push only after the app has a stable event model.

### Proposed server-side pieces

- `PushDevice` table or equivalent:
  - `id`
  - `userId`
  - `platform` (`IOS`, `ANDROID`, `WEB` later)
  - `provider` (`FCM`, `APNS`)
  - `tokenHash`
  - encrypted token value if needed
  - `enabledChannels`
  - `createdAt`, `lastSeenAt`, `revokedAt`
- `POST /api/push/register-device`
- `DELETE /api/push/register-device/:id`
- `PATCH /api/push/preferences`
- server-side event emitter for actionable events only

### Security boundaries

- Push tokens are user-scoped.
- No admin token ships in the app.
- Server checks the signed-in user's role before sending admin/operator event details.
- Notification bodies should avoid secrets, private file contents, raw roadmap notes, or production data.
- For sensitive events, send a generic notification like: "Conductor needs review" and load detail only after app auth.

### Push providers

| Provider | Pros | Cons | Recommendation |
|---|---|---|---|
| Firebase Cloud Messaging | Works for Android and can bridge iOS; common Flutter path | Requires Firebase project setup and device-token backend | Best later default |
| Direct APNs + FCM split | More control | More platform-specific code and credential handling | Overkill early |
| Email digest | Easy operational fallback | Not native/mobile; inbox noise | Good companion, not primary app notification |
| GitHub notification reliance | Already exists for PRs | Not user-friendly for app-only users | Operator-only fallback |

## Notification copy

Keep copy short and action-oriented:

- `Conductor needs review: 2 tasks are waiting on you.`
- `Worker cycle finished: alexa-integration/t-007 is done.`
- `High-priority Honeydo: approve the route card spec.`
- `Art queue update: pinball-hero hero request is ready to review.`

Avoid long roadmap notes in notifications. Deep-link into the relevant screen.

## Deep links

Design route targets now, even if push waits:

| Target | App route |
|---|---|
| Project detail | `/projects/:slug` |
| Task detail | `/projects/:slug/tasks/:taskId` |
| Approvals queue | `/approvals` |
| Todo detail | `/todos/:id` |
| Art queue item | `/art/queue/:key` |
| Settings notifications | `/settings/notifications` |

## Implementation outline

1. Add a notification preference model in local app state.
2. Add a refresh snapshot service that computes stable event keys.
3. Add a diff function:
   - previous snapshot
   - current snapshot
   - enabled channels
   - returns notification intents
4. Add local notification adapter with channel setup.
5. Add badge count selectors for dashboard cards.
6. Add Settings toggles for notification channels.
7. Add tests for diff behavior so old items do not re-notify.

## Verification checklist

- First app launch with existing `needs-human` tasks does not spam all historical tasks.
- A newly appearing `needs-human` task triggers one local notification.
- Re-refreshing without changes triggers no duplicate notification.
- Clearing or completing a task updates the badge count.
- Non-admin user mode hides Agent Ops notifications.
- Local-only mode keeps all notifications local and never contacts a push service.
- App resume refresh updates badges before showing stale alerts.

## Decision

Choose **local polling + local notifications + badges for MVP**.

Defer FCM/APNs push until:

- the app has active users beyond Silas/operator testing,
- event types have been proven useful,
- the server-side auth boundaries are stable,
- and there is a clear reason instant background delivery matters.

This gives the app useful awareness immediately without creating an early push-infrastructure swamp. Tiny swamp avoided. Heroic, honestly.
