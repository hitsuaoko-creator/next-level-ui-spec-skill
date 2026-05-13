#!/usr/bin/env python3

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
SPEC_PATH = PROJECT_ROOT / "design" / "spark-mobile-design-spec.md"
if not SPEC_PATH.is_file():
    SPEC_PATH = SKILL_ROOT / "references" / "spark-mobile-design-spec.md"

SCAN_ROOTS = ("mobile/",)
UI_EXTENSIONS = {
    ".kt",
    ".kts",
    ".swift",
    ".tsx",
    ".ts",
    ".jsx",
    ".js",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".vue",
    ".dart",
}
EXCLUDED_PARTS = {
    ".git",
    ".gradle",
    ".next",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "Pods",
    "DerivedData",
}

TOKEN_DEFINITION_PATTERNS = [
    re.compile(r"(^|/)(SparkDesignTokens|DesignTokens|Tokens|Theme|AppTheme)\.(kt|kts|ts|tsx|swift|dart)$", re.I),
    re.compile(r"(^|/)(theme|tokens|design-system|designsystem)/", re.I),
    re.compile(r"(^|/)SparkIcons\.kt$", re.I),
]


class Rule:
    def __init__(self, code: str, pattern: str, message: str, flags: int = re.I):
        self.code = code
        self.pattern = re.compile(pattern, flags)
        self.message = message


RULES = [
    Rule(
        "direct-compose-icons",
        r"\bIcons\.",
        "业务组件禁止直接使用 Compose 内置 Icons.*；请改为统一图标入口 SparkIcons.*。",
    ),
    Rule(
        "direct-drawable-resource",
        r"painterResource\s*\(\s*Res\.drawable\.",
        "业务组件禁止直接引用 Res.drawable.*；请通过 SparkIcons.* 统一调取图标。",
    ),
    Rule(
        "hardcoded-color-hex",
        r"(?<![A-Za-z0-9_])#[0-9A-Fa-f]{3,8}\b",
        "禁止硬编码颜色；使用 design/spark-mobile-design-spec.md 中的 colors.* token。",
    ),
    Rule(
        "hardcoded-color-fn",
        r"\b(?:rgba?|hsla?)\s*\(",
        "禁止手写 rgb/rgba/hsl/hsla；透明度必须使用 colors.opacity.* token。",
    ),
    Rule(
        "hardcoded-compose-color",
        r"\bColor\s*\(\s*0x[0-9A-Fa-f_]+",
        "禁止 Compose 中硬编码 Color(0x...)；使用 Spark design token。",
    ),
    Rule(
        "hardcoded-font-size",
        r"(?:fontSize|font-size|lineHeight|line-height|letterSpacing|letter-spacing)\s*[:=]\s*['\"]?\d+(?:\.\d+)?(?:px|sp|em|rem)?",
        "字号、行高、字间距必须使用 textStyle.* 语义 token。",
    ),
    Rule(
        "hardcoded-sp",
        r"\b\d+(?:\.\d+)?\.sp\b",
        "禁止裸 .sp 字号；使用 textStyle.heading1/bodySm/caption 等语义 token。",
    ),
    Rule(
        "invalid-font-weight",
        r"\bFontWeight\.(?:SemiBold|Bold|ExtraBold|Black|W[6-9]00)\b|fontWeight\s*[:=]\s*['\"]?(?:600|700|800|900|bold|semibold)",
        "Spark 只允许 Regular(400) / Medium(500)，正文不得使用 Bold/SemiBold。",
    ),
    Rule(
        "hardcoded-spacing-css",
        r"\b(?:padding|margin|gap|row-gap|column-gap|inset|top|right|bottom|left)\s*:\s*[^;\n]*\d+(?:\.\d+)?(?:px|dp|rem|em)",
        "padding/margin/gap 等间距必须使用 spacing.* 白名单 token。",
    ),
    Rule(
        "hardcoded-spacing-compose",
        r"\b(?:padding|offset|Spacer|height|width)\s*\([^)\n]*\d+(?:\.\d+)?\.dp",
        "Compose 间距/尺寸不要写裸 .dp；优先映射 spacing.* / layout.* / 组件 token。",
    ),
    Rule(
        "hardcoded-radius",
        r"\b(?:borderRadius|border-radius|RoundedCornerShape|cornerRadius)\s*[:=(]\s*[^;\n)]*\d+(?:\.\d+)?(?:px|dp)?",
        "圆角必须使用 radius.* token，禁止 borderRadius / RoundedCornerShape 裸数值。",
    ),
    Rule(
        "hardcoded-border-width",
        r"\b(?:borderWidth|border-width|BorderStroke)\s*[:=(]\s*[^;\n)]*\d+(?:\.\d+)?(?:px|dp)?",
        "描边宽度必须使用 dividerWidth.w1/w2 token。",
    ),
    Rule(
        "hardcoded-shadow",
        r"\b(?:box-shadow|shadowOffset|shadowRadius|shadowOpacity)\b|\bshadow\s*\([^)\n]*\d",
        "阴影只能在规范白名单组件上使用 shadow.* token。",
    ),
    Rule(
        "hardcoded-opacity",
        r"\b(?:opacity|alpha)\s*[:=(]\s*0?\.\d+",
        "透明度必须使用 colors.opacity.* token，禁止自定义 alpha。",
    ),
    Rule(
        "manual-dark-mode-color-branch",
        r"\bif\s*\([^)\n]*(?:isDark|darkTheme|isSystemInDarkTheme)[^)\n]*\)\s*[^{\n]*Color\s*\(",
        "禁止在组件内手写暗色分支切颜色；请统一通过 SparkMobileTheme.colors.* token 切换。",
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
    # Keep this intentionally simple. The guard is a safety net, not a language parser.
    return line.split("//", 1)[0].split("/*", 1)[0]


def scan_file(path: Path) -> list[str]:
    violations: list[str] = []
    rel_path = relative_path(path)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return violations

    for line_number, line in enumerate(lines, start=1):
        check_line = strip_inline_noise(line)
        if not check_line.strip():
            continue

        for rule in RULES:
            if rule.pattern.search(check_line):
                snippet = check_line.strip()
                if len(snippet) > 160:
                    snippet = snippet[:157] + "..."
                violations.append(
                    f"{rel_path}:{line_number}: [{rule.code}] {rule.message}\n"
                    f"  > {snippet}"
                )
    return violations


def print_header() -> None:
    print("Spark mobile design spec guard failed.", file=sys.stderr)
    try:
        spec_display = SPEC_PATH.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        spec_display = str(SPEC_PATH)
    print(f"Spec: {spec_display}", file=sys.stderr)
    print("Guard: src/next-level-ui-spec-skill/scripts/mobile_design_spec_guard.py", file=sys.stderr)
    print(
        "Fix: replace hardcoded style values with colors.*, textStyle.*, spacing.*, "
        "radius.*, dividerWidth.*, shadow.*, iconSize.*, or layout.* tokens; "
        "route all business icons through SparkIcons.* only.",
        file=sys.stderr,
    )
    print(file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mobile UI code against Spark mobile design tokens.")
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
        print("Spark mobile design spec is missing.", file=sys.stderr)
        print(
            "Expected either design/spark-mobile-design-spec.md in the target project "
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
