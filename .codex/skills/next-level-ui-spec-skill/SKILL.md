---
name: next-level-ui-spec-skill
description: Use this skill when implementing or reviewing Spark-style mobile or web UI that must follow strict design tokens, design spec, design review rules, and automated self-check guards. Covers mobile Compose token usage, web CSS variable and Tailwind semantic token usage, icon rules, guard-driven validation, and when to stop for missing tokens.
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

Required behavior:

- identify whether the task is `mobile`, `web`, or `both`
- never mix mobile token naming with web token naming
- stop if the requested visual value is outside the spec
- run `../../../src/next-level-ui-spec-skill/scripts/run_design_guards.sh` after UI edits
