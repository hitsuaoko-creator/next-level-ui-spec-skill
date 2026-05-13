#!/usr/bin/env python3
"""Spark Web design spec guard.

Scans `web/` UI source files for violations of `design/spark-web-design-spec.md`:
- hardcoded colors (hex / rgb / rgba / hsl / hsla)
- Tailwind arbitrary values (`bg-[#...]`, `p-[18px]`, `rounded-[14px]`, `shadow-[...]`, `text-[15px]`, `w-[16px]`)
- Tailwind palette colors (`bg-blue-500`, `text-gray-900`, etc.)
- raw Tailwind text/font/radius/shadow utilities that should go through semantic classes
- inline style hardcodes (`style={{ color: '#xxx', padding: 24, ... }}`)
- non-lucide icon libraries (`@heroicons`, `react-icons`, `phosphor`, `tabler-icons`, `@iconify`)
- `<img src="*.svg">` used as icons
- manual dark-mode color branches (`if (theme === 'dark')`)

Runs on three modes (mirrors mobile_design_spec_guard.py):
- `--changed` (default): dirty + staged + untracked
- `--staged`: index only (used by pre-commit)
- `--all`: every tracked file
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


SKILL_ROOT = Path(__file__).resolve().parents[1]


def detect_project_root() -> Path:
    env_root = os.environ.get("NEXT_LEVEL_UI_SPEC_PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()

    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return Path(proc.stdout.strip()).resolve()

    return Path.cwd().resolve()


PROJECT_ROOT = detect_project_root()
custom_spec = os.environ.get("NEXT_LEVEL_UI_SPEC_WEB_SPEC_PATH")
if custom_spec:
    SPEC_PATH = Path(custom_spec).resolve()
else:
    SPEC_PATH = PROJECT_ROOT / "design" / "spark-web-design-spec.md"
    if not SPEC_PATH.is_file():
        SPEC_PATH = SKILL_ROOT / "references" / "spark-web-design-spec.md"

SCAN_ROOTS = ("web/",)
UI_EXTENSIONS = {
    ".tsx",
    ".ts",
    ".jsx",
    ".js",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".html",
    ".vue",
    ".svelte",
    ".astro",
    ".mdx",
}
EXCLUDED_PARTS = {
    ".git",
    ".next",
    ".nuxt",
    ".turbo",
    ".vercel",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "public",
    "storybook-static",
}

# Files that legitimately define design tokens or third-party UI primitives.
# We skip them because they're allowed to declare raw values.
TOKEN_DEFINITION_PATTERNS = [
    # Tailwind / PostCSS / build configs
    re.compile(r"(^|/)tailwind\.config\.(ts|js|cjs|mjs)$"),
    re.compile(r"(^|/)postcss\.config\.(ts|js|cjs|mjs)$"),
    re.compile(r"(^|/)vite\.config\.(ts|js|cjs|mjs)$"),
    re.compile(r"(^|/)next\.config\.(ts|js|cjs|mjs)$"),
    # Global / token CSS layers
    re.compile(r"(^|/)styles?/(globals?|tokens?|theme|typography|variables?)\.(css|scss|sass|less)$", re.I),
    re.compile(r"(^|/)(globals?|tokens?|theme|typography|variables?)\.(css|scss|sass|less)$", re.I),
    # shadcn/ui mirror — third-party primitives we don't author
    re.compile(r"(^|/)components/ui/", re.I),
    # Generated / vendored assets
    re.compile(r"(^|/)assets/icons/.+\.svg$", re.I),
]


# Tailwind color palette names (full set, all canonical Tailwind v3+).
TAILWIND_PALETTE_COLORS = (
    "slate|gray|zinc|neutral|stone|"
    "red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose"
)
# Tailwind utility prefixes that take a color suffix.
TAILWIND_COLOR_PREFIXES = (
    "bg|text|border|ring|outline|divide|placeholder|caret|accent|fill|stroke|"
    "from|via|to|shadow|decoration"
)
# Whitelisted Tailwind text-size utilities (raw text-* are forbidden — must go through semantic classes).
# These regex flag any raw text-{xxs,xs,xs-2,sm,md,base,lg,xl,2xl,3xl,4xl,5xl,6xl,7xl,8xl,9xl}.
RAW_TEXT_SIZES = r"text-(?:xxs|xs|xs-2|sm|md|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)\b"
# Spacing whitelist (1-10). Any other numeric Tailwind spacing utility is a violation.
SPACING_PREFIXES = r"(?:p|px|py|pt|pr|pb|pl|ps|pe|m|mx|my|mt|mr|mb|ml|ms|me|gap|gap-x|gap-y|space-x|space-y|inset|inset-x|inset-y|top|right|bottom|left)"
SPACING_INVALID_VALUES = r"(?:0\.5|1\.5|2\.5|3\.5|11|12|14|16|20|24|28|32|36|40|44|48|52|56|60|64|72|80|96)"
# Whitelisted Tailwind radius utilities (rounded-{xs,sm,md,lg,xl,full,none}). Any other rounded-* is a violation.
RAW_RADIUS_INVALID = r"rounded-(?:2xl|3xl)\b"
# Whitelisted Tailwind shadow utility is just `shadow` (single token). Any sized variant is a violation.
RAW_SHADOW_INVALID = r"\bshadow-(?:sm|md|lg|xl|2xl|inner|none)\b"
# Tailwind font weights — only via semantic classes implicitly. Raw font-{bold,extrabold,black,medium} is banned.
RAW_FONT_WEIGHT_INVALID = r"\bfont-(?:medium|bold|extrabold|black)\b"
# Whitelisted opacity steps via `/<num>` syntax (5/10/15/75/85/90/95). Other steps are violations.
TAILWIND_OPACITY_INVALID = r"/(?:0|2[05]|30|3[5]|40|4[5]|50|5[5]|60|6[5]|70|80)\b"

# Icon library imports forbidden in business code.
FORBIDDEN_ICON_IMPORT = (
    r"from\s+['\"](?:"
    r"@heroicons/react(?:/[^'\"]*)?|"
    r"react-icons(?:/[^'\"]*)?|"
    r"phosphor-react|"
    r"@phosphor-icons/react(?:/[^'\"]*)?|"
    r"tabler-icons-react|"
    r"@tabler/icons-react|"
    r"@iconify/react|"
    r"@iconify-icons/[^'\"]*|"
    r"react-feather|"
    r"react-bootstrap-icons"
    r")['\"]"
)


class Rule:
    def __init__(self, code: str, pattern: str, message: str, flags: int = 0):
        self.code = code
        self.pattern = re.compile(pattern, flags)
        self.message = message


# Order matters only insofar as one line can produce multiple violations from
# overlapping rules; we report each match separately so the developer sees the
# full picture.
RULES = [
    # ---- Hardcoded colors ----
    Rule(
        "hardcoded-color-hex",
        r"(?<![A-Za-z0-9_/#-])#[0-9A-Fa-f]{3,8}\b",
        "禁止硬编码颜色；使用 var(--xxx) 或 Tailwind 语义类（如 bg-primary / text-foreground）。",
    ),
    Rule(
        "hardcoded-color-fn",
        r"\b(?:rgba?|hsla?)\s*\(",
        "禁止手写 rgb/rgba/hsl/hsla 颜色；使用 var(--xxx) 或 Tailwind 语义类。透明度通过 /5 /10 /15 /75 /85 /90 /95 表达。",
    ),
    # ---- Tailwind arbitrary value syntax ----
    Rule(
        "tailwind-arbitrary-color",
        r"\b(?:bg|text|border|ring|outline|divide|placeholder|caret|accent|fill|stroke|from|via|to|decoration)-\[(?:#|rgb|rgba|hsl|hsla|var\()",
        "禁止 Tailwind 任意值颜色（如 bg-[#1F69FF] / text-[rgba(...)]）；使用语义类 bg-primary / text-foreground 等。",
    ),
    Rule(
        "tailwind-arbitrary-spacing",
        r"\b" + SPACING_PREFIXES + r"-\[[^\]]+\]",
        "禁止 Tailwind 任意值间距（如 p-[18px] / gap-[13px]）；只能使用白名单 1-10（4-40px）或布局常量 var(--sidebar-width) 等。",
    ),
    Rule(
        "tailwind-arbitrary-radius",
        r"\brounded(?:-[trblse]{1,2})?-\[[^\]]+\]",
        "禁止 Tailwind 任意值圆角（如 rounded-[14px]）；只能使用 rounded-{xs,sm,md,lg,xl,full}。",
    ),
    Rule(
        "tailwind-arbitrary-shadow",
        r"\bshadow-\[[^\]]+\]",
        "禁止 Tailwind 任意值阴影（如 shadow-[0_4px_16px_...]）；只能使用 shadow（= var(--shadow)）。",
    ),
    Rule(
        "tailwind-arbitrary-text-size",
        r"\btext-\[[^\]]*(?:px|rem|em|pt)[^\]]*\]",
        "禁止 Tailwind 任意值字号（如 text-[15px]）；使用语义类 display / heading-1..4 / body / label / caption / nav 等。",
    ),
    Rule(
        "tailwind-arbitrary-size",
        r"\b[wh]-\[[^\]]+\]",
        "禁止 Tailwind 任意值尺寸（如 w-[16px] / h-[20px]）；图标只能用 w-5 h-5 或 w-4 h-4，布局用 var(--xxx) 常量。",
    ),
    # ---- Tailwind palette (skip semantic layer) ----
    Rule(
        "tailwind-palette-color",
        r"\b(?:" + TAILWIND_COLOR_PREFIXES + r")-(?:" + TAILWIND_PALETTE_COLORS + r")-(?:50|100|200|300|400|500|600|700|800|900|950)\b",
        "禁止 Tailwind 调色板（如 bg-blue-500 / text-gray-900）；使用语义类 bg-primary / text-foreground / text-muted-foreground 等。",
    ),
    Rule(
        "tailwind-palette-color-dark-prefix",
        r"\bdark:(?:" + TAILWIND_COLOR_PREFIXES + r")-(?:" + TAILWIND_PALETTE_COLORS + r")-(?:50|100|200|300|400|500|600|700|800|900|950)\b",
        "禁止 dark: 前缀 + Tailwind 调色板（颜色 token 已含双模，应直接用 bg-primary / text-foreground）。",
    ),
    # ---- Tailwind size / weight tokens that bypass semantic layer ----
    Rule(
        "raw-tailwind-text-size",
        r"\b" + RAW_TEXT_SIZES,
        "禁止裸 Tailwind 字号（如 text-sm / text-2xl）；使用语义类 display / heading-1..4 / body-lg / body / label / caption / overline / code / nav / micro。",
    ),
    Rule(
        "invalid-tailwind-radius",
        RAW_RADIUS_INVALID,
        "禁止 rounded-2xl / rounded-3xl；Spark Web 圆角只允许 rounded-{xs,sm,md,lg,xl,full}。",
    ),
    Rule(
        "invalid-tailwind-shadow",
        RAW_SHADOW_INVALID,
        "禁止 shadow-sm / shadow-md / shadow-lg / shadow-xl / shadow-2xl / shadow-inner；Spark Web 只有单一 shadow（= var(--shadow)），仅用于浮层组件。",
    ),
    Rule(
        "invalid-tailwind-font-weight",
        RAW_FONT_WEIGHT_INVALID,
        "禁止 font-medium(500) / font-bold(700) / font-extrabold(800) / font-black(900)；字重通过语义类隐式应用（400 / 600）。",
    ),
    Rule(
        "invalid-tailwind-spacing",
        r"\b" + SPACING_PREFIXES + r"-" + SPACING_INVALID_VALUES + r"\b",
        "禁止白名单外的 Tailwind 间距值；只允许 1-10（4-40px）。",
    ),
    Rule(
        "invalid-tailwind-opacity",
        r"\b(?:bg|text|border|ring|fill|stroke)-[a-z-]+" + TAILWIND_OPACITY_INVALID,
        "禁止白名单外的 Tailwind 透明度；只允许 /5 /10 /15 /75 /85 /90 /95。",
    ),
    # ---- Inline style hardcodes ----
    Rule(
        "inline-style-color-hardcode",
        r"(?:color|background|background-?[Cc]olor|borderColor|border-color|fill|stroke)\s*:\s*['\"]?#[0-9A-Fa-f]{3,8}",
        "禁止 inline style 硬编码颜色；使用 var(--xxx) 或 Tailwind 语义类。",
    ),
    Rule(
        "inline-style-color-fn",
        r"(?:color|background|background-?[Cc]olor|borderColor|border-color|fill|stroke)\s*:\s*['\"]?(?:rgb|rgba|hsl|hsla)\s*\(",
        "禁止 inline style 写 rgb/rgba/hsl 颜色；使用 var(--xxx)。",
    ),
    Rule(
        "inline-style-padding-hardcode",
        r"(?:padding|margin|gap|rowGap|columnGap)\s*:\s*['\"]?\d+(?:\.\d+)?(?:px|rem|em)?['\"]?(?:\s*[,}])",
        "禁止 inline style 硬编码 padding/margin/gap；使用 Tailwind 间距类（p-1..p-10）或 var(--spacing-*)。",
    ),
    Rule(
        "inline-style-font-size",
        r"(?:fontSize|font-size|lineHeight|line-height|letterSpacing|letter-spacing)\s*:\s*['\"]?\d+(?:\.\d+)?(?:px|rem|em|sp|pt)?",
        "禁止 inline style 硬编码字号 / 行高 / 字间距；使用语义类 display / heading-x / body / label / caption 等。",
    ),
    Rule(
        "inline-style-radius",
        r"(?:borderRadius|border-radius)\s*:\s*['\"]?\d+(?:\.\d+)?(?:px|rem|em)?",
        "禁止 inline style 硬编码圆角；使用 rounded-{xs,sm,md,lg,xl,full} 或 var(--rounded-xx)。",
    ),
    Rule(
        "inline-style-shadow",
        r"(?:boxShadow|box-shadow)\s*:\s*['\"]?\d+",
        "禁止 inline style 硬编码 box-shadow；使用 var(--shadow) 或 shadow Tailwind 类，仅在白名单浮层组件上。",
    ),
    Rule(
        "inline-style-opacity",
        r"\bopacity\s*:\s*0?\.\d+",
        "禁止 inline style 硬编码 opacity 数值；使用 Tailwind /5 /10 /15 /75 /85 /90 /95 透明度。",
    ),
    # ---- CSS file hardcodes (allowed only in token-definition layer files; those are excluded) ----
    Rule(
        "css-hardcoded-padding",
        r"^[^/*]*?\b(?:padding|margin|gap|row-gap|column-gap)\s*:\s*[^;\n]*\d+(?:\.\d+)?(?:px|rem|em)\s*;",
        "CSS 中禁止硬编码 padding/margin/gap；使用 var(--spacing-*) 或 Tailwind @apply 语义类。",
    ),
    Rule(
        "css-hardcoded-radius",
        r"^[^/*]*?\bborder-radius\s*:\s*[^;\n]*\d+(?:\.\d+)?(?:px|rem|em)\s*;",
        "CSS 中禁止硬编码 border-radius；使用 var(--rounded-xx)。",
    ),
    Rule(
        "css-hardcoded-shadow",
        r"^[^/*]*?\bbox-shadow\s*:\s*[^;\n]*\d+(?:\.\d+)?(?:px|rem|em)",
        "CSS 中禁止硬编码 box-shadow；使用 var(--shadow)。",
    ),
    Rule(
        "css-hardcoded-font-size",
        r"^[^/*]*?\bfont-size\s*:\s*[^;\n]*\d+(?:\.\d+)?(?:px|rem|em|pt)\s*;",
        "CSS 中禁止硬编码 font-size；使用 var(--text-xx) 或语义类。",
    ),
    # ---- Icon rules ----
    Rule(
        "forbidden-icon-import",
        FORBIDDEN_ICON_IMPORT,
        "禁止引入非 lucide-react 的图标库；统一使用 lucide-react 并通过 @/components/icon/spark-icons re-export。",
    ),
    Rule(
        "img-as-icon",
        r"<img\b[^>]*\bsrc\s*=\s*['\"][^'\"]*\.svg(?:[\"'?])",
        "禁止使用 <img src=\"*.svg\"> 加载图标；统一使用 lucide-react。",
    ),
    Rule(
        "img-as-icon-data-url",
        r"<img\b[^>]*\bsrc\s*=\s*['\"]data:image/svg",
        "禁止使用 <img src=\"data:image/svg...\"> 加载图标；统一使用 lucide-react。",
    ),
    Rule(
        "icon-w6-h6",
        r"\bw-6\s+h-6\b|\bh-6\s+w-6\b",
        "图标尺寸 w-6 h-6（24px）超出默认白名单；只允许 w-5 h-5（20px）或 w-4 h-4（16px）。如需更大尺寸需评审。",
    ),
    # ---- Manual dark mode branching ----
    # Catches `if (theme === 'dark')`, ternaries `theme === 'dark' ? ... : ...`,
    # and string equality checks against 'dark' / 'light' anywhere they appear.
    # Pure Tailwind `dark:` prefix is fine (handled by Tailwind itself), but
    # JS-side branching against the resolved theme name is forbidden.
    Rule(
        "manual-dark-mode-branch",
        r"\b(?:theme|resolvedTheme|currentTheme|colorScheme|colorMode|appearance)\s*===?\s*['\"](?:dark|light)['\"]",
        "禁止手写暗色分支切颜色；颜色 token 已含双模，应直接用 var(--xxx) / Tailwind 语义类自动切换。",
    ),
    Rule(
        "manual-dark-mode-flag",
        r"\b(?:if|when|return)\s*\(\s*(?:isDark|isDarkMode|darkMode)\b",
        "禁止用 isDark / isDarkMode / darkMode 等布尔标志手写暗色分支；颜色 token 已含双模。",
    ),
]


def run_git(args: list[str]) -> list[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def unique_paths(paths: Iterable[str]) -> list[Path]:
    result: list[Path] = []
    seen: set[str] = set()
    for raw_path in paths:
        rel_path = raw_path.strip()
        if not rel_path or rel_path in seen:
            continue
        seen.add(rel_path)
        result.append(PROJECT_ROOT / rel_path)
    return result


def collect_paths(mode: str) -> list[Path]:
    if mode == "all":
        return unique_paths(run_git(["ls-files"]))
    if mode == "staged":
        return unique_paths(run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMR"]))

    changed = run_git(["diff", "--name-only", "--diff-filter=ACMR"])
    staged = run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    untracked = run_git(["ls-files", "--others", "--exclude-standard"])
    return unique_paths([*changed, *staged, *untracked])


def relative_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def is_token_definition_file(rel_path: str) -> bool:
    return any(pattern.search(rel_path) for pattern in TOKEN_DEFINITION_PATTERNS)


def is_scannable(path: Path) -> bool:
    if not path.is_file():
        return False

    rel_path = relative_path(path)
    if not rel_path.startswith(SCAN_ROOTS):
        return False
    if path.suffix not in UI_EXTENSIONS:
        return False
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return False
    if is_token_definition_file(rel_path):
        return False
    return True


def strip_inline_noise(line: str) -> str:
    # Strip trailing line comments (JS/TS/CSS/HTML alike). The guard is a
    # safety net, not a language parser; this is intentionally conservative.
    stripped = line.split("//", 1)[0]
    stripped = stripped.split("/*", 1)[0]
    stripped = stripped.split("<!--", 1)[0]
    return stripped


def scan_file(path: Path) -> list[str]:
    violations: list[str] = []
    rel_path = relative_path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return violations

    lines = text.splitlines()
    for line_number, line in enumerate(lines, start=1):
        check_line = strip_inline_noise(line)
        stripped = check_line.strip()
        if not stripped:
            continue

        for rule in RULES:
            if rule.pattern.search(check_line):
                snippet = stripped
                if len(snippet) > 160:
                    snippet = snippet[:157] + "..."
                violations.append(
                    f"{rel_path}:{line_number}: [{rule.code}] {rule.message}\n"
                    f"  > {snippet}"
                )
    return violations


def print_header() -> None:
    print("Spark web design spec guard failed.", file=sys.stderr)
    try:
        spec_display = SPEC_PATH.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        spec_display = str(SPEC_PATH)
    print(f"Spec: {spec_display}", file=sys.stderr)
    print("Guard: src/next-level-ui-spec-skill/scripts/web_design_spec_guard.py", file=sys.stderr)
    print(
        "Fix: replace hardcoded values with var(--xxx) / Tailwind semantic classes "
        "(bg-primary, text-foreground, rounded-md, p-4, shadow), and use semantic "
        "typography classes (display, heading-1..4, body, label, caption, nav, etc.). "
        "All icons must come from lucide-react; do not use heroicons / phosphor / "
        "tabler-icons / iconify or <img src=\"*.svg\">.",
        file=sys.stderr,
    )
    print(file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Spark Web UI code against the Spark web design spec tokens."
    )
    parser.add_argument(
        "--mode",
        choices=("changed", "staged", "all"),
        default="changed",
        help="changed scans dirty/untracked files, staged scans the commit index, all scans tracked files.",
    )
    parser.add_argument("--changed", action="store_const", const="changed", dest="mode")
    parser.add_argument("--staged", action="store_const", const="staged", dest="mode")
    parser.add_argument("--all", action="store_const", const="all", dest="mode")
    args = parser.parse_args()

    if not SPEC_PATH.is_file():
        print("Spark web design spec is missing.", file=sys.stderr)
        print(
            "Expected NEXT_LEVEL_UI_SPEC_WEB_SPEC_PATH, "
            "design/spark-web-design-spec.md in the target project, "
            "or the bundled reference inside the installed skill.",
            file=sys.stderr,
        )
        return 1

    files = [path for path in collect_paths(args.mode) if is_scannable(path)]
    violations: list[str] = []
    for path in files:
        violations.extend(scan_file(path))

    if violations:
        print_header()
        print("\n\n".join(violations), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
