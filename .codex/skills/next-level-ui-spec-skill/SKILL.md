---
name: next-level-ui-spec-skill
description: Use this skill when implementing or reviewing mobile or web UI with editable example design specs plus strictly enforced design rules and automated self-check guards. Covers mobile Compose token usage, web CSS variable and Tailwind semantic token usage, icon rules, and guard-driven validation.
---

# Next Level UI Spec Skill

This repository keeps the canonical installable skill under `../../../src/next-level-ui-spec-skill/`.

For `mobile/` tasks, read:

- `../../../src/next-level-ui-spec-skill/references/spark-mobile-design-spec.md`
- `../../../src/next-level-ui-spec-skill/references/spark-mobile-design-rules.md`
- `../../../src/next-level-ui-spec-skill/scripts/mobile_design_spec_guard.py`

For `web/` tasks, read:

- `../../../src/next-level-ui-spec-skill/references/spark-web-design-spec.md`
- `../../../src/next-level-ui-spec-skill/references/spark-web-design-rules.md`
- `../../../src/next-level-ui-spec-skill/scripts/web_design_spec_guard.py`

Spec handling:

- treat the bundled design specs as editable examples
- users may change spec parameters directly
- users may provide custom spec files through `NEXT_LEVEL_UI_SPEC_MOBILE_SPEC_PATH` and `NEXT_LEVEL_UI_SPEC_WEB_SPEC_PATH`

Required behavior:

- identify whether the task is `mobile`, `web`, or `both`
- never mix mobile token naming with web token naming
- treat rules and guard scripts as mandatory and strict
- stop if the requested visual value is outside the active spec
- run `../../../src/next-level-ui-spec-skill/scripts/run_design_guards.sh` after UI edits
