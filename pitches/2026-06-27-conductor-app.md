# Pitch: Conductor App — native mobile/desktop client
date: 2026-06-27
project-target: conductor
status: awaiting-silas

## The idea
A native app (Flutter recommended for write-once cross-platform) that gives
Silas a polished UI for the Conductor system:
- Login via kind_robots auth (JWT / session token)
- Dashboard: active projects, open todos, agent status
- Create/edit todos and notes on the go
- Push notifications for agent completions, blocked tasks, PRs needing review
- Art generation requests from the phone camera or prompt
- Quick voice-to-todo (pairs with Alexa Integration)

Flutter chosen because: one codebase → iOS + Android + macOS + web; Dart is
strongly typed and straightforward; the kind_robots REST API is all we need.

## Why it's worth doing
The workspace page is admin-only and browser-only. A phone app makes Conductor
accessible from anywhere — logging a todo during a walk, checking agent status
from a coffee shop, approving a PR from the couch.

## Rough effort
medium-large (Flutter app shell + API client + push notifications)

## Key pieces
1. Flutter project scaffold in a new `conductor-app/` repo or subdir
2. Dart API client wrapping kind_robots REST endpoints
3. Auth flow: login screen → JWT stored in secure storage
4. Home screen: project cards, todo list, agent status feed
5. Push: integrate with a notification service (FCM or self-hosted ntfy)

## Suggested first task
Scaffold the Flutter project and implement the auth flow + home dashboard
reading from `/api/conductor/projects` and `/api/todos`.
