---
name: next-level-ui-spec-skill
description: Use this skill when implementing or reviewing Spark-style mobile or web UI that must follow strict design tokens, design spec, design review rules, and automated self-check guards. Covers mobile Compose token usage, web CSS variable and Tailwind semantic token usage, icon rules, guard-driven validation, and when to stop for missing tokens.
---

# Next Level UI Spec Skill

This skill packages Spark-style mobile/web design constraints into a reusable, installable skill.

## Use This Skill For

- editing `mobile/` UI, theme, icon, or component code
- editing `web/` UI, style, icon, or component code
- reviewing token compliance
- diagnosing design-guard failures
- enforcing a "read spec first, then code, then run guards" workflow

## Source Files

Load only the files relevant to the task.

For `mobile/` tasks:

- `references/spark-mobile-design-spec.md`
- `references/spark-mobile-design-rules.md`
- `scripts/mobile_design_spec_guard.py`

For `web/` tasks:

- `references/spark-web-design-spec.md`
- `references/spark-web-design-rules.md`
- `scripts/web_design_spec_guard.py`

## Required Workflow

### 1. Identify the surface

- If the task touches `mobile/`, use only the mobile spec and rules.
- If the task touches `web/`, use only the web spec and rules.
- If the task touches both, treat them as separate systems.
- Never mix mobile token naming with web token naming.

### 2. Read the correct references before editing

- Read the relevant design spec first.
- Then read the matching design rules file.
- If the task involves compliance or review, inspect the matching guard script.

### 3. Follow the correct token system

For `mobile/`, UI values must come from:

- `SparkMobileTheme.colors.*`
- `SparkMobileTheme.textStyle.*`
- `SparkMobileTheme.spacing.*`
- `SparkMobileTheme.radius.*`
- `SparkMobileTheme.dividerWidth.*`
- `SparkMobileTheme.shadow.*`
- `SparkMobileTheme.iconSize.*`
- `SparkMobileTheme.layout.*`
- `SparkIcons.*`

For `web/`, UI values must come from:

- CSS variables like `var(--primary)`, `var(--border)`, `var(--shadow)`
- Tailwind semantic classes like `bg-primary`, `text-foreground`, `border-border`, `rounded-md`, `shadow`
- typography semantic classes like `display`, `heading-1..4`, `body-lg`, `body`, `label`, `caption`, `overline`, `code`, `nav`, `micro`
- Lucide icons via a project icon entrypoint

### 4. Stop when the spec does not cover the request

Stop and ask for a design/token update when:

- a requested color, spacing, radius, opacity, shadow, or typography value is missing from the spec
- a requested component state is not covered by the rules
- the design requires a new semantic token

Do not work around missing tokens with hardcoded values, Tailwind palette colors, arbitrary values, raw `.dp` / `.sp`, or manual dark-mode branches.

### 5. Validate after edits

Run the bundled guards:

```bash
bash scripts/run_design_guards.sh mobile changed
bash scripts/run_design_guards.sh web changed
bash scripts/run_design_guards.sh both staged
```

If the target project is not the current git root, set `NEXT_LEVEL_UI_SPEC_PROJECT_ROOT=/abs/path/to/project`.

## Output Expectations

When using this skill:

- say whether the task is `mobile`, `web`, or `both`
- cite the exact spec/rules files used
- name the token families or semantic classes you are following
- call out missing tokens instead of inventing values
