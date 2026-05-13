---
paths:
  - "mobile/**/*.kt"
  - "mobile/**/*.kts"
---
# Spark Mobile Design Spec 强制规则

> 凡是修改 `mobile/` 下任何 Compose UI / theme / icon / 组件代码，必须严格遵守本规则。
> 本规则与 `design/spark-mobile-design-spec.md`（仓库内规范文件）配套，spec 是唯一事实来源。

## 0. 写代码前必须先读 spec（Hard Requirement）

**触发条件**：本次任务涉及任意以下文件路径：

- `mobile/shared/src/commonMain/**/presentation/**/*.kt`
- `mobile/shared/src/commonMain/**/components/**/*.kt`
- `mobile/shared/src/commonMain/**/core/theme/**/*.kt`
- `mobile/shared/src/commonMain/**/core/icon/**/*.kt`
- `mobile/shared/src/commonMain/composeResources/**`
- 任意其它 `mobile/` 下的 Compose `@Composable` 函数

**强制动作**：在动手写/改任何一行代码 **之前**，按以下顺序执行：

1. 用 Read 工具完整读取 `design/spark-mobile-design-spec.md`（不允许只读片段或跳读，文件不大）。
2. 在该 spec 中定位本次任务相关的章节（§1 颜色 / §2 文字 / §3 圆角 / §4 边框 / §5 间距 / §6 透明度 / §7 阴影 / §8 组件 / §9 图标）。
3. 在回复中向用户简要复述将引用的 token 路径（例：`colors.brand`、`spacing.s4`、`radius.md`），让用户能即时纠偏。
4. 同步阅读 token 实现：`mobile/shared/src/commonMain/kotlin/com/iflytek/spark/shared/core/theme/`（`Color.kt`、`Typography.kt`、`Dimensions.kt`、`Theme.kt`），以及 `core/icon/SparkIcons.kt`，确认 spec 中的 token 在代码中对应的实际命名。

**禁止跳过**：即便对 spec 内容看似熟悉、即便是「微小修改」，仍必须先读。spec 在持续演进，缓存的记忆不可信。

## 1. Token 调用白名单

UI 代码中所有视觉数值，**只允许**通过以下入口取得：

- `SparkMobileTheme.colors.*`
- `SparkMobileTheme.textStyle.*`
- `SparkMobileTheme.spacing.*`
- `SparkMobileTheme.radius.*`
- `SparkMobileTheme.dividerWidth.*`
- `SparkMobileTheme.shadow.*`
- `SparkMobileTheme.iconSize.*`
- `SparkMobileTheme.layout.*`

**绝对禁止**（PostToolUse hook 会扫描并拦截）：

- 硬编码 hex / RGBA：`Color(0xFF1F69FF)`、`Color(red, green, blue)` 写在 UI 代码里（仅 `core/theme/Color.kt` 内部允许）
- 裸 `.dp` / `.sp` 数字：`16.dp`、`14.sp`（仅 `core/theme/Dimensions.kt`、`Typography.kt` 内部允许）
- 裸 `RoundedCornerShape(12.dp)` / `BorderStroke(1.dp, …)` / 自创 `Shadow(…)`
- 透明度直接写 `0.5f`、`alpha = 0.85f`
- 暗色逻辑写 `if (isDarkTheme) … else …`，颜色应由 token 自带双模解决

设计稿出现 spec 外的数值或新颜色 → **停止编码并向用户提问**，请求扩 token 或更新 spec，不允许自创。

## 2. 图标使用规则

- 所有 UI 图标 **必须** 通过 `com.iflytek.spark.shared.core.icon.SparkIcons.*` 引用。
- **禁止** 在 feature / components 代码中出现：
  - `androidx.compose.material.icons.Icons.*`
  - `painterResource(Res.drawable.*)`
  - `Res.drawable.*` 直接引用
- SVG 原文件统一放 `mobile/shared/src/commonMain/composeResources/drawable/`，新增图标时：
  1. 先把 SVG 落到该目录（命名 snake_case）
  2. 在 `SparkIcons.kt` 注册对应 `ImageVector`（命名 PascalCase）
  3. 才能在组件中以 `SparkIcons.XxxYyy` 引用
- 图标尺寸只能用 `SparkMobileTheme.iconSize.*`（`xs/sm/md/lg/xl`）。
- 按需新增：实现具体组件前先扫一遍 `SparkIcons.kt` 是否已有目标图标，缺失才新增；不要批量预导入。

## 3. 组件实现约束

- 写新组件前，先在 `design/spark-mobile-design-spec.md` §8 中查找是否已有对应规范（Button / ButtonGroup / FormInput / Card / Chip / ChatBoxIndexInterface / Header / TabBar）。
- 若 spec 已有：逐字段对照实现，禁止「接近但不一致」。
- 若 spec 无：停下询问用户，要求补 spec / token；不要自创组件 spec。
- 组件变体（如 `theme` / `state` / `size`）必须以 `enum` + props 表达，由 token 映射决定样式，不要在调用方层层重写。
- 颜色、间距、圆角、字体的取值放在 composable 顶部统一从 `SparkMobileTheme.*` 解出，再传入子组件，便于审查。

## 4. 提交前自检 Checklist

修改完成后，务必逐条核对（对应 spec §10.3）：

- [ ] 所有颜色都用了 `SparkMobileTheme.colors.*`？
- [ ] 所有间距都来自 `SparkMobileTheme.spacing.*`（白名单：s0/s1/s2/s3/s4/s5/s6/s8/s10/s12/s14/s16）？
- [ ] 所有圆角都用了 `SparkMobileTheme.radius.*`？
- [ ] 所有字号 / 字重都来自 `SparkMobileTheme.textStyle.*`？
- [ ] 所有阴影都来自 `SparkMobileTheme.shadow.*`，并且只用在 spec §7 白名单组件上？
- [ ] 没有任何硬编码 hex / RGBA / 裸 `.dp` / 裸 `.sp` / 裸 alpha float？
- [ ] 暗色模式可正常切换（无硬编码颜色阻断）？
- [ ] 所有图标都来自 `SparkIcons.*`？
- [ ] 没有 `Icons.*`、`painterResource(Res.drawable.*)`？
- [ ] Light / Dark 两套模式下图标颜色都通过 token 控制？

未通过任意一项 → 返回修改，不要交付。

## 5. 配套机制（自动校验，不可绕过）

以下机制会在编辑后自动执行，输出违例必须先修复再继续：

- `scripts/hooks/mobile_design_spec_guard.py`：扫描 `mobile/` UI 代码中的硬编码与非法 token 引用。
- `.claude/hooks/ai_runtime_guard.sh` → `scripts/hooks/ai_runtime_guard.py`：注入 spec 约束、PostToolUse / Stop 阶段做自查。
- `.githooks/pre-commit` → `scripts/hooks/pre-commit.sh`：提交前最后一道闸。
- 新 clone 后必须执行 `bash scripts/install-hooks.sh` 启用 git hook。

如果任何一道闸报错，**优先修代码** 而不是修 hook；只有规则本身确有问题、且与用户对齐后，才能调整 spec / hook。

## 6. 越界行为（Block 级）

以下任何一种情况都属于规则违反，发现立即停手并向用户报告：

- 在 UI 代码里直接写硬编码颜色 / 数值 / 字号
- 在 feature / components 里使用 `Icons.*` 或 `Res.drawable.*`
- 用 `if (isDarkTheme)` 之类条件分支替代 token 双模
- 引入 spec 之外的新组件或新视觉规则却没先和用户对齐
- 跳过 §0「写代码前先读 spec」直接动手

## 参考

- 规范源文件：`design/spark-mobile-design-spec.md`
- Token 实现：`mobile/shared/src/commonMain/kotlin/com/iflytek/spark/shared/core/theme/`
- 图标实现：`mobile/shared/src/commonMain/kotlin/com/iflytek/spark/shared/core/icon/SparkIcons.kt`
- 自动校验脚本：`scripts/hooks/mobile_design_spec_guard.py`
- 顶层项目说明：`CLAUDE.md` / `AGENTS.md`（亦记录了同一约束）
