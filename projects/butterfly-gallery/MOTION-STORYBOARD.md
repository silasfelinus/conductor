# Butterfly Gallery Motion Storyboard

Status: implementation contract for `butterfly-gallery/t-012`

This storyboard refines the approved stage contract into deterministic UI beats. It does not introduce a second visual direction. The static warehouse, convex funnel, five left preset bins, central frame, right rail, foreground pile, and animation-layer ordering remain owned by `APPROVED-STAGE-SPEC.md`.

## Motion principles

- Sorting is always usable before, during, and after animation. Motion never owns application state.
- User artwork remains a normal DOM image. The stretch-and-snap effect is CSS/Web Animations motion on a transient proxy, never a generated video containing the user's image.
- First-visit theater is short, skippable, and remembered only for the intended browser session.
- Ambient actors are separate from this intro. The intro may cue their layer slots, but it must not require rendered mascot clips to complete.
- `prefers-reduced-motion: reduce` bypasses squash/stretch, falling piles, and mascot motion. It uses a short fade/scale and lands directly in the same steady-state DOM.

## State model

The existing gallery scene state remains authoritative. The intro adds no parallel queue or persistence model.

1. `loading`: data/store initialization. No intro motion yet.
2. `intro-ready`: first eligible visit after data is ready. The steady-state stage is already mounted underneath.
3. `intro-playing`: optional non-blocking vignette. Skip is visible and keyboard reachable.
4. `ready`: normal sorting stage. This is also the immediate destination for returning sessions, reduced-motion users, errors, or Skip.
5. `drop-transition`: transient selected-image proxy animates from funnel to frame while the real selected image is prepared underneath.
6. `ready`: proxy is removed; real image owns the frame.

Any error during animation cancels the proxy/intro and returns to `ready`. Animation failure must never strand the scene in a hidden or disabled state.

## Session memory

Use `sessionStorage`, not durable account state, for the intro-played marker. Suggested key: `butterfly-gallery:intro-played:v1`.

- Read once after client hydration.
- If present, enter `ready` without intro.
- Set it when the intro completes naturally or the user chooses Skip.
- Do not set it merely because loading failed before the intro could begin.
- Version the key when the intro contract changes materially so a future intentionally-new vignette can play once without clearing unrelated storage.

Reduced-motion users should enter `ready` immediately and may set the session marker so the full intro does not suddenly play later in the same session if OS settings change.

## First-visit intro, target 2.4 to 3.2 seconds

The intro is a garnish, not a loading screen. The real stage is mounted from frame one.

### Beat 0: room already usable, 0 to 150 ms

The warehouse stage is visible immediately. Controls may finish hydration normally. A compact `Skip intro` control appears in a stable location that does not move the central artwork or bins.

### Beat 1: trapdoor cue, 150 to 550 ms

A ceiling/trapdoor DOM layer above the top runway gives one quick open/jolt cue. Keep it graphic and simple: hinge/open transform plus a small shadow change. Do not animate the entire room or camera.

If no dedicated trapdoor art exists, a CSS/DOM panel is sufficient. The intro must not wait on asset generation.

### Beat 2: picture tumble, 500 to 1,650 ms

Three to five decorative frame proxies fall toward the foreground pile on slightly staggered paths. They are non-interactive clones/placeholders, not additional ArtImages and not changes to queue ordering.

- Keep trajectories deterministic and bounded inside the stage.
- Use modest rotation and stagger, not physics simulation.
- Frames terminate behind/into the existing foreground pile and are removed.
- The actual pile DOM does not jump, reorder, or gain fake records.
- No butterfly or robot is required for this beat.

### Beat 3: settle, 1,650 to 2,250 ms

The trapdoor closes or exits. A tiny pile-settle nudge may occur on the pile container, but its final geometry must be byte-for-byte the ordinary steady-state layout, not an intro-only alternate composition.

### Beat 4: handoff, by 3,200 ms maximum

Remove intro-only proxies, hide Skip, mark the session intro as played, and enter `ready`. Ambient runway/butterfly/robot schedulers may begin independently after this handoff.

Hard timeout: regardless of animation events, the intro must self-complete by 3.2 seconds. `animationend` is an optimization, not the only escape hatch.

## Skip behavior

Skip is available from the moment `intro-playing` begins.

- Button and keyboard activation call one idempotent `finishIntro()` path.
- Cancel all intro animations/timers.
- Remove transient trapdoor/frame proxies.
- Restore final transforms/opacity synchronously.
- Set the session marker.
- Enter `ready` without waiting for an animation callback.
- Do not alter selected image, filters, bins, queue order, or pending curation actions.

Pressing Escape may invoke Skip while the intro is active, provided it does not conflict with an open dialog or existing app-level Escape behavior.

## Selected-image funnel transition

This transition is separate from the first-visit intro and may run whenever selection advances after a successful sort.

### Geometry

Measure the funnel mouth and central frame with `getBoundingClientRect()` after the selected image is known. Animate a fixed-position proxy so layout does not reflow. The destination rectangle is derived from the frame's actual rendered content box, preserving the image's true aspect ratio with the same fit policy as the final display.

If either rectangle is unavailable, dimensions are zero, or the page becomes hidden, skip directly to the final selected image.

### Full-motion keyframes, target 420 to 560 ms

1. **Emerge, 0 to 18%**: proxy starts centered just inside/below the convex funnel mouth at roughly normal proportions, slightly smaller than destination width.
2. **Stretch, 18 to 58%**: proxy travels downward while vertical scale exaggerates to roughly `1.7–2.2`; horizontal scale may compress mildly (`0.88–0.96`). Transform origin stays near top center so it reads as being pulled from the funnel.
3. **Snap, 58 to 82%**: proxy reaches the frame and recoils past neutral, for example vertical `0.88–0.94` with horizontal `1.03–1.07`.
4. **Settle, 82 to 100%**: proxy returns to neutral scale at the exact destination rectangle. Crossfade to the real selected image and remove the proxy.

Use easing with a fast middle and short overshoot, not spring physics that can run unpredictably. The final frame must always use the image's true aspect ratio. The distortion exists only on the transient proxy.

### Interruption rules

- A new selection cancels the old proxy and starts from the newest selection only.
- Sorting actions do not wait for the visual proxy to finish persisting.
- Route leave, tab hide, resize invalidating geometry, or component unmount cancels cleanly.
- Never queue multiple drop transitions. Latest selection wins.

## Reduced-motion variant

When `prefers-reduced-motion: reduce` is active:

- Do not play the trapdoor tumble sequence.
- Do not run ambient mascot loops from this page's motion controller.
- Do not vertically stretch/squash artwork.
- For a new selected image, use a 120 to 180 ms opacity fade plus optional scale from `0.98` to `1` directly in the central frame.
- Preserve the same selected-image timing and application state. Reduced motion changes presentation only.
- Skip remains available if any intro affordance is shown, but the preferred behavior is to enter `ready` immediately.

Listen for media-query changes while mounted. If reduced motion becomes active mid-animation, cancel current animation and commit the final steady state immediately.

## Accessibility and interaction contract

- Intro-only elements are `aria-hidden` unless they are controls. Decorative falling frames must never enter the accessibility tree.
- `Skip intro` has an ordinary button role and visible focus treatment.
- Do not steal focus when the intro starts or ends.
- Do not announce every animation beat. Existing gallery status announcements should describe meaningful sorting/selection changes, not theater.
- Pointer, touch, and keyboard curation paths remain available throughout. If a transient proxy visually crosses controls, it uses `pointer-events: none`.

## Layer ownership

Use the approved layer stack without shortcuts:

- trapdoor and falling-frame intro proxies: transient scene layer above static stage but below global app header;
- selected-image drop proxy: approved transient drop layer above pile/controls, `pointer-events: none`;
- top runway actors: their own clipped surface behind the funnel;
- lower-right robot: behind foreground pile;
- left butterfly: foreground above bins;
- blank-state loop: inside central display only while no ArtImage is selected.

No intro actor is baked into the warehouse background.

## Implementation acceptance checklist

The implementation following this storyboard is complete when:

- first eligible visit can play once and returning navigation in the same session does not replay it;
- Skip immediately lands on the exact normal stage and is keyboard accessible;
- a hard timeout prevents a stuck intro;
- decorative tumble proxies never mutate queue data;
- selected-image entry measures funnel/frame geometry and uses one cancelable transient proxy;
- full motion visibly stretches vertically then snaps to the true aspect ratio;
- reduced motion uses only a brief fade/scale and cancels any in-flight exaggerated motion;
- hidden/unmounted/error states cancel timers and animations cleanly;
- sorting actions and persisted state never depend on animation completion;
- the final DOM/layout after any path is the same steady-state gallery stage.

## Handoff to motion tasks

`t-013` may now create shot lists/jobs for the independent runway, left-butterfly, robot, and blank-state assets without redefining intro timing. `t-015` owns implementation of the first-visit orchestration. `t-017` owns the selected-image stretch-and-snap micro-interaction. Both implementation tasks should treat this storyboard and `APPROVED-STAGE-SPEC.md` together as the motion contract.
