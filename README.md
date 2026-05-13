# Next Level UI Spec Skill

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Codex](https://img.shields.io/badge/Codex-Supported-0A7BFF)
![Claude](https://img.shields.io/badge/Claude-Supported-7C3AED)
![Install](https://img.shields.io/badge/Install-bash-brightgreen)

A reusable AI skill that packages editable example design specs plus strict design rules and self-check guards into an installable bundle.

It is intended for teams that want strict design-token enforcement for:

- Kotlin Compose mobile UI
- React/Tailwind/shadcn-style web UI
- design review and self-check workflows
- guard-based validation before commit

## Contract

- The bundled design specs are examples and templates.
- Users can edit the parameters in those spec files.
- Users can also create their own spec documents derived from the examples.
- The rules files and self-check guards are the mandatory enforcement layer and should be followed strictly.

## Structure

```text
src/next-level-ui-spec-skill/
  SKILL.md
  references/
  scripts/
.claude/skills/next-level-ui-spec-skill/
.codex/skills/next-level-ui-spec-skill/
skill.json
install-skill.sh
```

`src/next-level-ui-spec-skill/` is the canonical install source.

## Install

Install for Codex:

```bash
bash install-skill.sh codex
```

Install for Claude:

```bash
bash install-skill.sh claude
```

Install for both:

```bash
bash install-skill.sh both
```

## Use

After installation, ask the agent to use `next-level-ui-spec-skill` when working on tokenized UI work.

If you want to run the guards manually against a project:

```bash
NEXT_LEVEL_UI_SPEC_PROJECT_ROOT=/abs/path/to/project \
bash src/next-level-ui-spec-skill/scripts/run_design_guards.sh both staged
```

The target project is expected to use `mobile/` and/or `web/` directories.

Spec resolution order:

1. `NEXT_LEVEL_UI_SPEC_MOBILE_SPEC_PATH` / `NEXT_LEVEL_UI_SPEC_WEB_SPEC_PATH`
2. project-local `design/spark-mobile-design-spec.md` / `design/spark-web-design-spec.md`
3. the bundled example specs in this skill

That means you can:

- keep the bundled example specs as-is
- edit the bundled example spec parameters
- create your own project spec files and point the guards at them

The rules files and guard scripts remain the strict enforcement layer in all cases.

## Publish To GitHub

```bash
git init
git add .
git commit -m "feat: add next-level-ui-spec-skill"
git branch -M main
git remote add origin https://github.com/<your-account>/next-level-ui-spec-skill.git
git push -u origin main
```

## License

This project is released under the `MIT` license. See [LICENSE](LICENSE).
