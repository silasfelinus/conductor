# Retire WonderLab; keep the voices

**Status:** approved by Silas in-session 2026-08-11
**Project:** kind-robots
**Kind:** software/content migration

Silas directed Kind Robots to retire WonderLab entirely as a product and developer subsystem. Remove the museum routes, component catalog/store/API/build metadata generation, WonderLab-specific CI/contracts/admin review surfaces, and the requirement that orphaned components remain compilable for museum previews. `components/abandonware` may remain in-repo temporarily as excluded source, but the end state is to archive it outside Kind Robots so it cannot affect built chunks.

Preserve the valuable artifact: the 706 polished Bot/Character-authored WonderLab commentary entries. They are not to be retargeted in place. Treat each paired exchange as source material and create a fresh, target-appropriate two-speaker scene on a live reviewable Kind Robots model. The goal is setup/payoff and sharply identifiable voices, not software critique. Existing WonderLab rows/manifests remain intact until the replacement corpus is drafted and approved.

The general review system should become the permanent home. All main reviewable models should expose their `allowReviews` setting from the selected-item/edit experience, and displayed authored reviews must preserve/link the Bot or Character speaker identity.

Publishing the rewritten corpus is a separate human gate because the generated prose becomes outward-facing content. Infrastructure retirement and draft-generation tooling are approved now.
