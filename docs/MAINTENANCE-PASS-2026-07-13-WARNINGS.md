# Roadmap Maintenance — Warning Cleanup

This pass resolves the 15 advisory findings from the first portfolio audit without erasing useful history:

- completed and approved historical gates no longer count as current throughput warnings;
- intentional soft checkpoints are explicit with `soft_gate: true`;
- `stakes: needs-human` is recognized as a real hard-gate marker;
- the abandoned `art-generator-connect/t-019` claim was reset to `ready` after branch and PR searches found no live work;
- `engagement` moved from `active` to `finished` because all tasks are done;
- `ruler-hooked` received an active override so its ready tasks are selectable.

The generated audit reports zero errors and zero warnings.
