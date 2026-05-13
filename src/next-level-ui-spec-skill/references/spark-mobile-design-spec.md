# Spark_ScientificResearch Design Spec

> 本规范是 AI 与 Hook 必读文档。所有 UI 实现必须**严格调用 token**，禁止硬编码值。
> 所有「使用规则」+「使用示例」必须深刻记忆并落地到代码中‼️
> 平台：iOS / Android（移动端 375×812 基线）。所有 token 命名遵循 **驼峰式（camelCase）**，可被映射为 React Native theme / Flutter ThemeData / SwiftUI ColorAsset。

---

## 目录

1. [设计说明](#0-设计说明foundations)
2. [颜色系统](#1-颜色系统)
3. [文字系统](#2-文字系统)
4. [圆角系统](#3-圆角系统)
5. [边框线系统](#4-边框线系统)
6. [间距系统](#5-间距系统)
7. [透明度系统](#6-透明度系统)
8. [阴影系统](#7-阴影系统)
9. [组件规范](#8-组件规范)
10. [图标库](#9-图标库)
11. [AI 协同约定](#10-ai-协同约定)

---

## 0. 设计说明（Foundations）

| 项目 | 值 |
|---|---|
| 设计画板 | iPhone 375×812（statusBar 44 + navBar 44 + safeArea 34） |
| 字体族 | 系统默认字体（Compose 使用 `FontFamily.Default`） |
| 主题模式 | **Light / Dark 双模** — 通过 `MODE` collection 在两个 modeId 之间切换 |
| Token 分层 | `Primatives`（数值原子：radius / dividerWidth）→ `Spacing`（间距）→ `MODE`（语义色 + opacity，含双模）→ `TextStyles`（14 个）+ `EffectStyles`（4 个） |
| Token 命名规则 | 全部 **驼峰式**（camelCase）：`colors.brand`、`radius.md`、`spacing.s4`、`textStyle.bodySm`、`shadow.inputLight` |

**应用范围**：移动端业务页面（首页、写作流程、研读搜索流程、侧滑窗等所有 7 个 section）+ 基础组件库（150 个）+ 业务组件库（163 个）。

### 0.1 强制实现约束（AI / Hook / Review 统一执行）

- 业务组件中的图标只能通过统一入口 `SparkIcons.*` 引用。
- 禁止在业务组件中直接使用 `Icons.*`、`Res.drawable.*`、`painterResource(Res.drawable.xxx)`。
- SVG 原文件统一存放在 `mobile/shared/src/commonMain/composeResources/drawable/`。
- 图标代码入口统一维护在 `mobile/shared/src/commonMain/kotlin/com/iflytek/spark/shared/core/icon/SparkIcons.kt`。
- 业务组件中的颜色、字号、字重、行高、字间距、圆角、描边宽度、阴影、透明度、间距、图标尺寸、布局尺寸都必须走 token。
- 浅色 / 暗色模式只允许通过 `SparkMobileTheme` token 切换；禁止组件内部写 `if (isDarkTheme)` 后手动切换颜色。
- 组件允许引用的视觉 token 入口仅限：
  - `SparkMobileTheme.colors.*`
  - `SparkMobileTheme.textStyle.*`
  - `SparkMobileTheme.spacing.*`
  - `SparkMobileTheme.radius.*`
  - `SparkMobileTheme.dividerWidth.*`
  - `SparkMobileTheme.shadow.*`
  - `SparkMobileTheme.iconSize.*`
  - `SparkMobileTheme.layout.*`

---

## 1. 颜色系统

### 1.1 使用规则（非常重要⚠️ 通读并理解⚠️）

- 每个语义色都有 light/dark 双映射，**必须调用 token**，永远不可输出硬编码⚠️ 调用硬编码会导致暗色模式下无法切换⚠️
- **同一页面主题色 `colors.brand` 使用不超过 3 处**，保持视觉焦点⚠️ 避免大面积使用 brand 色造成视觉粘腻⚠️
- `colors.brand` 应用于：主操作按钮（提交/确认/发送）、激活态/选中态、链接、focus 描边、可点击的强调元素⚠️
- `colors.state.danger` 仅用于：删除/移除/警告操作、错误提示文本、必填星标⚠️
- `colors.state.success` 仅用于：成功 toast、success 图标/校验通过⚠️
- 容器层级：页面背景 `colors.background.*` < 卡片底色 `colors.block.*`；不可错配⚠️
- 文字层级：标题 `primary` → 副文 `secondary` → 占位/禁用 `tertiary` → 反白 `quaternary`，依次降级⚠️
- 底层动效组件（Lottie / shader / 粒子系统 / Skia）的内部插值色、噪声色不属于页面 token；但页面层传入这些组件的颜色 props，仍必须来自 design token‼️

### 1.2 使用示例（非常重要⚠️ 通读并理解⚠️）

✅ 正确示例
```tsx
// React Native
backgroundColor: theme.colors.brand
color: theme.colors.foreground.primary

// SwiftUI
.background(Color.brand)
.foregroundColor(.foregroundPrimary)

// Flutter
color: AppColors.brand
```

❌ 错误示例
```tsx
backgroundColor: '#1F69FF'           // 硬编码 hex
color: '#1B1C21'                     // 硬编码 hex
backgroundColor: 'rgba(31,105,255,0.85)'  // 硬编码 RGBA
```

### 1.3 色彩系统

#### 1.3.1 主题色（Brand）

| 语义 | Light | Dark | Token 路径 |
|---|---|---|---|
| 品牌主色 | `#1F69FF` | `#185EEC` | `colors.brand` |

#### 1.3.2 背景色（Background — 页面级）

| 语义 | Light | Dark | Token 路径 |
|---|---|---|---|
| 页面主背景 | `#F3F8FF` | `#0D0D0D` | `colors.background.primary` |
| 次级背景（分组段） | `#F0F4F9` | `#111111` | `colors.background.secondary` |

#### 1.3.3 容器底色（Block — 组件级 fill）

| 语义 | Light | Dark | Token 路径 |
|---|---|---|---|
| 一级容器（card / input / button-secondary / FormDatePicker  / drag / FloatingWindow / FormInput / FormSelect / FormTextArea / SearchBar / TagButton） | `#FFFFFF` | `#1D1D1D` | `colors.block.primary` |
| 嵌套容器（card 内 card） | `#F0F2F6` | `#1B1B1B` | `colors.block.secondary` |
| 浮层容器（dropdown / popover / drawer / modal） | `#FFFFFF` | `#222222` | `colors.block.tertiary` |

#### 1.3.4 文字色（Foreground）

| 语义 | Light | Dark | Token 路径 |
|---|---|---|---|
| 一级文字（标题、正文） | `#1B1C21` | `#D9D9D9` | `colors.foreground.primary` |
| 二级文字（描述、辅助） | `#696E81` | `#A0A4B0` | `colors.foreground.secondary` |
| 三级文字（占位、弱提示） | `#A3A9B9` | `#6C6F79` | `colors.foreground.tertiary` |
| 反白文字（深色背景上） | `#FFFFFF` | `#FFFFFF` | `colors.foreground.quaternary` |

#### 1.3.5 状态色（State）

| 语义 | Light | Dark | Token 路径 |
|---|---|---|---|
| 成功 | `#2CA13D` | `#219432` | `colors.state.success` |
| 危险/错误 | `#F14B43` | `#E1372E` | `colors.state.danger` |

#### 1.3.6 边框线色（Divider）

| 语义 | Light | Dark | Token 路径 |
|---|---|---|---|
| 分割线/边框 | `#E4E3F0` | `#2D2D2D` | `colors.divider` |

> 强调态描边（focus / selected）用 `colors.brand` 替换。

---

## 2. 文字系统

### 2.1 使用规则（非常重要⚠️ 通读并理解⚠️）

#### 2.1.1 必须遵守✅
- 页面级主标题语义只能有一个，使用 `textStyle.heading1`
- 标题层级不能跳级：`heading1` → `heading2` → `heading3` 依次递进
- 标题默认展示一行（非 hero 区），常规页面标题不应自然折成两行
- 正文统一用 `textStyle.bodySm`（默认）；阅读型大段落用 `textStyle.bodyLg`；不要混用
- 按钮文字统一用 `textStyle.bodySm`
- 表单 Label 统一用 `textStyle.bodySmAccent`（Medium）
- 输入框 placeholder 统一用 `textStyle.bodySm`
- 错误提示统一用 `textStyle.bodySm` + `colors.state.danger`
- 辅助说明、时间、状态文字用 `textStyle.caption`
- 角标/徽标数字用 `textStyle.tiny`（10px，1% 字间距）

#### 2.1.2 禁止❌
- 不能跳级：`heading1` 直接接 `heading3`⚠️
- 不能用 `heading*` 写正文⚠️
- 不能用 `body*` 写主标题⚠️
- 不能用裸字号（`fontSize: 18`）跳过语义层⚠️
- 不能让 `heading1/2/3` 默认折两行⚠️
- 不能在按钮文字中使用 `heading*` 或 `caption`⚠️
- 正文字重不能超过 Medium（`500`），禁止 Bold/Black⚠️

#### 2.1.3 可执行检查规则（供 AI 与 Hook 严格执行）

##### A. 标题层级规则
- 页面级主标题只允许使用 `textStyle.heading1`，每页仅 1 次
- 二级（卡片/section 标题）只允许使用 `textStyle.heading2` 或 `textStyle.bodyTitle`
- 三级（卡片内分组标题）只允许使用 `textStyle.heading3`
- 标题层级必须逐级递进，禁止跳级
- 禁止 `heading1 → heading3`
- 禁止 `heading2 → 跳过 → 直接正文`

##### B. 标题与无障碍语义映射（移动端通用建议）
- `textStyle.heading1` → 节点 `accessibilityRole: 'header'` + 视为页面 H1 级
- `textStyle.heading2` / `textStyle.bodyTitle` → H2 级 header
- `textStyle.heading3` → H3 级 header
- 禁止普通 Text 节点承担页面主标题语义而不带 header 无障碍角色

##### C. 正文规则
- 默认正文用 `textStyle.bodySm`（14/22 Regular）
- 阅读型长文用 `textStyle.bodyLg`（15/26 Regular），用于文章/段落正文
- 列表项标题用 `textStyle.bodyTitle`（16/24 Medium）
- 列表项正文、按钮文字、表单输入文字统一 `textStyle.bodySm`
- 同一信息块内禁止混用 `bodySm` 与 `bodyLg`
- 禁止用 `heading*` 充当正文
- 禁止用 `bodyLgAccent` / `bodySmAccent` 作为大段正文（强调用，非阅读用）

##### D. 按钮文字规则
- 所有按钮主文字必须使用 `textStyle.bodySm`
- `Button` 组件内 `label` slot 必须使用 `textStyle.bodySm`
- 禁止按钮主文字使用 `heading*` / `caption` / `mini`
- 图标按钮（仅图标无文字）允许省略文本节点

##### E. 表单文字规则
- 字段 label 统一用 `textStyle.bodySmAccent`（14 Medium）
- 输入框 placeholder 统一用 `textStyle.bodySm` + `colors.foreground.tertiary`
- 输入框值（已填）用 `textStyle.bodySm` + `colors.foreground.primary`
- 帮助文字、错误提示统一用 `textStyle.bodySm`（错误色用 `colors.state.danger`）
- 表单分组标题用 `textStyle.heading3`
- 必填星标颜色用 `colors.state.danger`（**注意：当前 Figma 中部分组件用了硬编码 `#FF3838`，新代码必须改为 token**）
- 禁止字段 label 使用 `bodySm`（无强调）或 `caption`

##### F. 辅助信息规则
- 时间、状态说明、次级提示、图片描述统一用 `textStyle.caption`
- 章节前缀、分类前缀、超小标签统一用 `textStyle.captionAccent` 或 `textStyle.tinyAccent`
- 角标数字、徽标数字统一用 `textStyle.tiny`
- 禁止把 `caption` 用作主要正文
- 禁止把 `tiny` 用作可读正文（仅角标/极小标识）

##### G. 字重规则
- `heading1` / `heading2` / `heading3` / `bodyTitle` / `*Accent` 系列 → 必须 `500`（Medium）
- `bodyLg` / `bodySm` / `mini` / `caption` / `tiny` → 必须 `400`（Regular）
- 字面值映射：Medium = `500`，Regular = `400`
- 禁止自行加 `fontWeight: 'bold'` / `fontWeight: '700'` / `fontWeight: '900'`
- 禁止正文使用 Medium 以上字重

##### H. 裸 token 禁止规则
- 禁止直接使用 `fontSize: <数值>`
- 禁止跳过语义层使用裸字号 token
- 必须优先使用语义类：`heading1` `heading2` `heading3` `bodyTitle` `bodyLg` `bodyLgAccent` `bodySm` `bodySmAccent` `mini` `miniAccent` `caption` `captionAccent` `tiny` `tinyAccent`

##### I. Hook 检查约定
以下写法可被 Hook 直接判定为违规：
- 标题文本使用裸 `fontSize: <num>`
- 按钮文本使用 `caption` / `heading*`
- 正文使用 `heading*`
- 表单 label 不使用 `bodySmAccent`
- 帮助文字 / 错误提示不使用 `bodySm`
- 同一页面出现多个 `heading1`
- 相邻标题层级跳级
- 必填星标使用硬编码 `#FF3838`（必须改 `colors.state.danger`）

### 2.2 文字规范（Text Style 表）

> 字体族统一使用系统默认字体；Compose 代码使用 `FontFamily.Default`。letterSpacing 默认 `0`（仅 `tiny` 系列为 `1%`）。

#### 2.2.1 语义命名

| 语义 | Token 路径 | 字号 token | 字重 | 场景 |
|---|---|---|---|---|
| 一级标题 | `textStyle.heading1` | `fontSize.h1` | `500` | 页面主标题（每页 1 次） |
| 二级标题 | `textStyle.heading2` | `fontSize.h2` | `500` | 卡片 / section 标题 |
| 三级标题 | `textStyle.heading3` | `fontSize.h3` | `500` | 卡片内分组标题 |
| 列表项标题 | `textStyle.bodyTitle` | `fontSize.bodyTitle` | `500` | List item 标题 |
| 阅读正文（强调） | `textStyle.bodyLgAccent` | `fontSize.bodyLg` | `500` | 大正文强调 |
| 阅读正文 | `textStyle.bodyLg` | `fontSize.bodyLg` | `400` | 文章正文、阅读区 |
| 默认正文（强调） | `textStyle.bodySmAccent` | `fontSize.bodySm` | `500` | 表单 label、按钮强调 |
| 默认正文 | `textStyle.bodySm` | `fontSize.bodySm` | `400` | **默认**：按钮、输入、列表正文 |
| 信息强调 | `textStyle.miniAccent` | `fontSize.mini` | `500` | 次级标识、tag |
| 信息文字 | `textStyle.mini` | `fontSize.mini` | `400` | 辅助说明、metadata |
| 标签强调 | `textStyle.captionAccent` | `fontSize.caption` | `500` | 章节前缀、分类标签 |
| 标签文字 | `textStyle.caption` | `fontSize.caption` | `400` | 时间、状态、图片说明 |
| 极小标签强调 | `textStyle.tinyAccent` | `fontSize.tiny` | `500` | 角标 + 强调 |
| 极小数字 | `textStyle.tiny` | `fontSize.tiny` | `400` | 徽标数字、角标 |

#### 2.2.2 字号 Token 定义

| Token 路径 | 字号 | 行高 | letterSpacing |
|---|---|---|---|
| `fontSize.h1` | 18 | 28 | 0 |
| `fontSize.h2` | 16 | 28 | 0 |
| `fontSize.h3` | 15 | 26 | 0 |
| `fontSize.bodyTitle` | 16 | 24 | 0 |
| `fontSize.bodyLg` | 15 | 26 | 0 |
| `fontSize.bodySm` | 14 | 22 | 0 |
| `fontSize.mini` | 13 | 22 | 0 |
| `fontSize.caption` | 12 | 18 | 0 |
| `fontSize.tiny` | 10 | 12 | 1% |

#### 2.2.3 字重 Token

| Token | 名称 |
|---|---|
| `400` | Regular |
| `500` | Medium |

> Spark 不使用 SemiBold(600) / Bold(700)。

---

## 3. 圆角系统

### 3.1 使用规范（非常重要⚠️ 通读并理解⚠️）

#### 3.1.1 可执行检查规则（供 AI 与 Hook 严格执行）

##### A. 组件圆角映射
| 组件 | Token 路径 | 值 |
|---|---|---|
| 按钮（Button lg/md） | `radius.md` | 12 |
| 输入框（FormInput / FormDatePicker） | `radius.md` | 12 |
| 卡片（Card） | `radius.md` 或 `radius.lg` | 12 / 16 |
| Sheet / Drawer 顶部 | `radius.lg` | 16 |
| 弹窗 / Dialog / Modal | `radius.xl` | 24 |
| 下拉菜单 / Popover | `radius.md` | 12 |
| Toast / Tooltip | `radius.sm` | 10 |
| Chip / 选中标签（content-Tag-Button） | `radius.sm` | 10 |
| 小 chip / Skill button（input-Skill-button） | `radius.xs` | 8 |
| Badge（数字徽标、胶囊 tag） | `radius.full` | 9999 |
| 头像 / 圆形按钮 / 圆形图标按钮 | `radius.full` | 9999 |

##### B. 禁止规则
- 禁止按钮使用 `radius.full`，除非是图标按钮 / 纯圆形按钮
- 禁止卡片使用 `radius.xs`（过小）
- 禁止弹窗使用 `radius.full` 或 `radius.xs`
- 禁止 chip / Tag 使用 `radius.lg` 或更大值（破坏胶囊感）
- 禁止任意值：`borderRadius: 14`
- 禁止硬编码：`borderRadius: 12`（必须用 token 引用）

##### C. 嵌套规则
- 同一组件内：内层圆角 ≤ 外层圆角
- 同一组件内：圆角应统一，不允许混用多个语义层（如外圆角 `radius.md` 内部 chip 强行 `radius.xl`）
- 纯装饰性嵌套元素若无必要，不应额外设置圆角

##### D. Hook 检查约定
以下写法可被 Hook 直接判定为违规：
- 出现裸数值 `borderRadius: <num>`
- `Button` 使用非 `radius.md`（例外：图标按钮 + `radius.full`）
- `FormInput` 使用非 `radius.md`
- `Badge` / `Tag` 使用非 `radius.full`、`radius.sm`、`radius.xs`
- `Modal` / `Dialog` 使用非 `radius.xl`

### 3.2 圆角样式表

| Token 路径 | 值 | 应用 |
|---|---|---|
| `radius.xs` | 8 | 小 chip、icon button、skill 按钮 |
| `radius.sm` | 10 | 大 chip、Tag、Toast、Tooltip |
| `radius.md` | 12 | **默认**：按钮、输入框、卡片、Popover |
| `radius.lg` | 16 | 大卡片、Sheet 顶部、Drawer |
| `radius.xl` | 24 | 弹窗、Dialog、浮层容器 |
| `radius.full` | 9999 | 胶囊按钮、Badge、头像、圆形 |

---

## 4. 边框线系统

### 4.1 使用规范（非常重要⚠️ 通读并理解⚠️）

#### 4.1.1 必须遵守✅
- 默认描边宽度 `dividerWidth.w1`（1），适用于列表分割、卡片描边、按钮 secondary、表单输入框各状态描边
- 强调态描边（focus / selected / error）保持宽度 `dividerWidth.w1`（1），**只换色不加粗** — 用 `colors.brand` 或 `colors.state.danger`
- 加粗描边 `dividerWidth.w2`（2）用于 tab indicator、选中态指示条等装饰元素，以及**首页输入框 ChatBoxIndexInterface**（核心入口的视觉强调，含渐变描边）
- 描边颜色默认 `colors.divider`，激活态用 `colors.brand`，错误态用 `colors.state.danger`

#### 4.1.2 禁止❌
- 禁止裸数值 `borderWidth: 1`（必须用 token 引用）
- 禁止描边宽度大于 2（除非有特殊设计批准）
- 禁止用 `dividerWidth.w2` 作为常规组件（按钮 / 卡片 / 普通输入框）描边（视觉过重，仅装饰指示条与首页输入框）
- 禁止描边颜色使用 `foreground.*` 系列

#### 4.1.3 可执行检查规则
##### A. 组件描边映射
| 组件 | 描边宽度 | 描边颜色 |
|---|---|---|
| Button secondary | `dividerWidth.w1` | `colors.divider` |
| FormInput default | 无描边或 `dividerWidth.w1` | `colors.divider` |
| FormInput focus | `dividerWidth.w1` | `colors.brand` |
| FormInput error | `dividerWidth.w1` | `colors.state.danger` |
| ChatBoxIndexInterface | `dividerWidth.w2` | 渐变描边（特殊案例） |
| List divider | `dividerWidth.w1` | `colors.divider` |
| Tab indicator | `dividerWidth.w2` | `colors.brand` |
| Card 描边 | `dividerWidth.w1` | `colors.divider` |

##### B. Hook 检查约定
- 出现裸数值 `borderWidth: <num>`
- 描边颜色使用 `foreground.*`
- secondary 按钮缺失描边

### 4.2 边框线样式表

| Token 路径 | 值 | 应用 |
|---|---|---|
| `dividerWidth.w1` | 1 | **默认**：列表分割、卡片描边、按钮 secondary |
| `dividerWidth.w2` | 2 | tab indicator、强调装饰条、首页输入框 ChatBoxIndexInterface |

---

## 5. 间距系统

### 5.1 使用规范（非常重要⚠️ 通读并理解⚠️）

#### 5.1.1 Token 表（白名单）

| Token 路径 | 值 |
|---|---|
| `spacing.s0` | 0 |
| `spacing.s1` | 4 |
| `spacing.s2` | 8 |
| `spacing.s3` | 12 |
| `spacing.s4` | 16 |
| `spacing.s5` | 20 |
| `spacing.s6` | 24 |
| `spacing.s8` | 32 |
| `spacing.s10` | 40 |
| `spacing.s12` | 48 |
| `spacing.s14` | 56 |
| `spacing.s16` | 64 |

> ⚠️ **注意**：Spacing 不连续（缺 s7、s9、s11、s13、s15）。AI 不可自行新增中间值。

#### 5.1.2 可执行检查规则（供 AI 与 Hook 严格执行）

##### A. 间距白名单
仅允许使用 token 表中的值。任意 `padding / margin / gap` 必须从下列中选择：
`s0` `s1` `s2` `s3` `s4` `s5` `s6` `s8` `s10` `s12` `s14` `s16`

##### B. 固定场景映射（基于真实组件实测）

| 场景 | 取值 | Token |
|---|---|---|
| 图标与文字之间 | 4 | `spacing.s1` |
| 按钮内 padding（lg） | V 12 / H 16 | `spacing.s3` / `spacing.s4` |
| 按钮内 padding（md） | V 8 / H 16 | `spacing.s2` / `spacing.s4` |
| 按钮内 icon 与 label gap | 4 | `spacing.s1` |
| 输入框内 padding | V 16 / H 20 | `spacing.s4` / `spacing.s5` |
| 输入框内 label 与 content gap | 16 | `spacing.s4` |
| 输入框 label 内 文字与必填星 gap | 4 | `spacing.s1` |
| Error message 与 input gap | 4 | `spacing.s1` |
| 大 Chip 内 padding（content-Tag-Button） | H 20 | `spacing.s5` |
| 大 Chip 内 gap | 4 | `spacing.s1` |
| 小 Chip 内 padding（input-Skill-button） | V 4 / H 8 | `spacing.s1` / `spacing.s2` |
| ChatBox 容器内 V padding | 12 | `spacing.s3` |
| ChatBox 内子模块 gap | 12 | `spacing.s3` |
| 容器内 H padding（chatbox 内层） | 12 | `spacing.s3` |
| 卡片内 padding（默认） | 16 | `spacing.s4` |
| 卡片之间 gap | 12 ~ 16 | `spacing.s3` / `spacing.s4` |
| 列表项之间 gap | 8 ~ 12 | `spacing.s2` / `spacing.s3` |
| 表单字段之间 gap | 16 | `spacing.s4` |
| Section 之间 gap | 24 ~ 32 | `spacing.s6` / `spacing.s8` |
| 页面 H 边距（默认） | 16 | `spacing.s4` |
| 页面 V 边距（顶部首屏） | 16 ~ 24 | `spacing.s4` / `spacing.s6` |
| 弹窗 / Dialog 内 padding | 20 ~ 24 | `spacing.s5` / `spacing.s6` |
| Toast / Tooltip 内 padding | V 8 / H 12 | `spacing.s2` / `spacing.s3` |

##### C. 布局语义常量（不属于通用 spacing 白名单，但合规）
以下为 iOS 移动端固定布局常量，可被代码以独立常量引用：

| Token 路径 | 值 |
|---|---|
| `layout.statusBarHeight` | 44 |
| `layout.navBarHeight` | 44 |
| `layout.totalHeaderHeight` | 88 |
| `layout.homeIndicatorHeight` | 34 |
| `layout.screenPaddingH` | 16（= `spacing.s4`） |

##### D. 禁止规则
- 禁止使用 token 白名单之外的 spacing（如 5、6、7、9、10、11、13、14、15、17、18…）
- 禁止任意值：`padding: 18` / `gap: 13`
- 禁止硬编码：`padding: 24` / `marginTop: 14`
- 禁止子层级间距大于父层级间距
- 禁止卡片内 padding 大于页面 padding（视觉破坏）

##### E. Hook 检查约定
以下写法可被 Hook 直接判定为违规：
- 任意 `padding / margin / gap` 数值不在白名单内
- 出现裸数值 `padding: <num>` / `gap: <num>`（除布局常量）

---

## 6. 透明度系统

### 6.1 使用规范（非常重要⚠️ 通读并理解⚠️）

> Light 模式以白色（`#FFFFFF`）为基色，Dark 模式以黑色（`#0D0D0D`）为基色，仅 alpha 不同。常用于遮罩、毛玻璃、悬浮态、品牌色叠加。

#### 6.1.1 Token 表

| Token 路径 | Alpha | 应用 |
|---|---|---|
| `colors.opacity.o5` | 0.05 | 极弱 hover 高亮 |
| `colors.opacity.o10` | 0.10 | hover 态、轻遮罩 |
| `colors.opacity.o15` | 0.15 | press 态、状态 badge 底色 |
| `colors.opacity.o75` | 0.75 | 半透明遮罩、毛玻璃 |
| `colors.opacity.o85` | 0.85 | 重遮罩、品牌 chip 叠加层（与 brand 复合） |
| `colors.opacity.o90` | 0.90 | 顶层 dialog 遮罩 |
| `colors.opacity.o95` | 0.95 | 接近不透明（防穿透） |

#### 6.1.2 必须遵守✅
- 半透明遮罩、悬浮态、状态 badge 底色 **必须**通过 `colors.opacity.*` token 实现
- 品牌色淡化（如 brand chip 底色）= `colors.brand` 上叠加 `colors.opacity.o85`（实测组件做法）
- 状态 badge 底色 = `colors.state.success` / `colors.state.danger` 上叠加 `colors.opacity.o15`

#### 6.1.3 禁止❌
- 禁止手写 alpha：RGBA 字面量、`#1F69FF85` 八位 hex
- 禁止跳过 token，自定义 alpha 值（如 0.2、0.3、0.4 不在 token 表中）
- 禁止用 `colors.opacity.*` 作为可见文字（极不可读）
- 禁止用 `colors.opacity.*` 作为按钮主底色（应使用实色）

#### 6.1.4 Hook 检查约定
- 出现 RGBA 字面量
- 出现非 token alpha 值（如 0.2、0.3、0.4、0.6、0.8）
- Text 节点使用 `colors.opacity.*` 作为颜色

---

## 7. 阴影系统

### 7.1 使用规范（非常重要⚠️ 通读并理解⚠️）

#### 7.1.1 必须遵守✅
- 浮窗、抽屉、弹出层可用阴影
- 输入框激活态可用 `shadow.inputLight` / `shadow.inputDark`（按当前主题选）
- 表单 / 输入框 focus 态**不使用阴影环**，仅通过 `dividerWidth.w1` + `colors.brand` 的描边表达（输入框的 `shadow.input*` 只是 hover/活跃悬浮感，不属于焦点环）

#### 7.1.2 禁止❌
- 除浮窗 / 抽屉 / 输入框激活态外，其他场景**禁止**使用阴影
- 禁止硬编码 `shadowOffset` / `shadowRadius` / `shadowOpacity` 数值
- 禁止使用非 token 的阴影值

#### 7.1.3 可执行检查规则

##### A. 允许使用阴影的场景（白名单）
- `Popover` / `PopoverContent`
- `DropdownMenu`
- `Dialog` / `Modal`
- `Sheet` / `Drawer`
- `Tooltip`
- `Toast`（短暂浮层）
- `FormInput` / `ChatBoxIndexInterface` 激活态（特殊：用 `shadow.inputLight` / `shadow.inputDark`）

##### B. 禁止使用阴影的场景
- 普通页面容器
- 普通卡片（Card 默认无阴影，只描边）
- Section 块
- Button（默认无阴影）
- Badge / Tag
- 静态信息块

##### C. Hook 检查约定
- 在普通 View / Card / Button / Badge 上出现 shadow token
- 在白名单外组件上出现 `shadowColor` / `shadowOffset` / `shadowRadius`
- 出现裸数值 `shadowOffset: { width: 0, height: 4 }` 等任意值

### 7.2 阴影 Token 表

| Token 路径 | 颜色 × Alpha | Offset (x, y) | Blur | Spread | 应用 |
|---|---|---|---|---|---|
| `shadow.inputLight` | `#1F69FF` × 0.16 | (0, 4) | 16 | 0 | 浅色模式输入框激活/悬浮 |
| `shadow.inputDark` | `#000000` × 0.16 | (0, 4) | 16 | 0 | 深色模式输入框激活/悬浮 |

> 注：`shadow.inputLight` / `shadow.inputDark` 应通过当前主题模式自动二选一。

---

## 8. 组件规范

> 以下组件 spec 来自 Figma 真实组件的 token 绑定（实测，非主观推断）。AI 在生成代码时**必须**严格匹配这些 token 组合。

### 8.1 Button（按钮）

#### 8.1.1 变体维度
- `theme`: `primary` | `secondary` | `danger` | `textAccent` | `textSecondary` | `icon`
- `state`: `enabled` | `loading` | `disable`
- `size`: `lg`（46 高）| `md`（38 高）

#### 8.1.2 通用规则（所有变体）
| 属性 | 值 |
|---|---|
| 圆角 | `radius.md`（12） |
| Padding（lg） | V `spacing.s3` / H `spacing.s4`（12 / 16） |
| Padding（md） | V `spacing.s2` / H `spacing.s4`（8 / 16） |
| Icon 与 label gap | `spacing.s1`（4） |
| 文字 style | `textStyle.bodySm` |
| 描边宽度（如有） | `dividerWidth.w1` |

#### 8.1.3 颜色映射

| theme | 背景 | 文字色 | 描边 |
|---|---|---|---|
| `primary` | `colors.brand` | `colors.foreground.quaternary` | 无 |
| `secondary` | `colors.block.primary` | `colors.foreground.primary` | `colors.divider` (1) |
| `danger` | `colors.state.danger` | `colors.foreground.quaternary` | 无 |
| `textAccent` | 透明 | `colors.brand` | 无 |
| `textSecondary` | 透明 | `colors.foreground.secondary` | 无 |
| `icon` | 透明 | 继承父级 | 无 |

#### 8.1.4 状态变化
- `loading`：保持背景色不变，label 替换为 loading 旋转图标，不改变高度
- `disable`：背景与文字降不透明度（推荐用 `colors.opacity.*` 叠加方式或专用 disabled token）

### 8.2 ButtonGroup（按钮组）

| 属性 | 值 |
|---|---|
| 容器 padding | V 0 / `spacing.s3` 底部 / H `spacing.s4` |
| 子按钮 gap | 10（**特殊：不在 spacing 白名单**）— 建议代码统一为 `spacing.s2` |
| 内部按钮 | 实例引用 Button（默认 lg） |
| 数量 | 通常 2 个（左 secondary / 右 primary） |

### 8.3 FormInput（表单输入框）

#### 8.3.1 变体维度
- `theme`: `default` | `focus` | `disable` | `error`
- `status`: `outline` | `filled`

#### 8.3.2 默认结构
| 属性 | 值 |
|---|---|
| 高度 | 54（无 error）/ 80（含 error message） |
| 圆角 | `radius.md`（12） |
| Padding | V `spacing.s4` / H `spacing.s5`（16 / 20） |
| 内部 gap（label ↔ content） | `spacing.s4`（16） |
| 背景 | `colors.block.primary` |
| Label 文字 | `textStyle.bodySmAccent` + `colors.foreground.primary` |
| Placeholder 文字 | `textStyle.bodySm` + `colors.foreground.tertiary` |
| 已填值文字 | `textStyle.bodySm` + `colors.foreground.primary` |
| 必填星标 | `colors.state.danger`（**注意：当前 Figma 中是 `#FF3838` 硬编码，需迁移**） |
| 必填星与 label gap | `spacing.s1`（4） |

#### 8.3.3 状态变化
| 状态 | 描边 | 阴影 |
|---|---|---|
| `default` | 无 | 无 |
| `focus` | `dividerWidth.w1` + `colors.brand` | `shadow.inputLight` / `shadow.inputDark`（按主题）|
| `disable` | 无 | 无（背景色降阶） |
| `error` | `dividerWidth.w1` + `colors.state.danger` | 无 |

#### 8.3.4 Error 状态额外结构
- Container 改为 vertical layout
- Input 主体下方 gap `spacing.s1`（4）
- Error message 文本：`textStyle.bodySm` + `colors.state.danger`

### 8.4 Card（卡片）

| 属性 | 值 |
|---|---|
| 圆角 | `radius.md`（12）默认；大卡片 `radius.lg`（16） |
| Padding | `spacing.s4`（16）默认 |
| 背景（独立卡片） | `colors.block.primary` |
| 背景（嵌套卡片） | `colors.block.secondary` |
| 描边（如需）| `dividerWidth.w1` + `colors.divider` |
| 阴影 | **无**（除非是浮层卡片） |
| 卡片之间 gap | `spacing.s3`（12） |

### 8.5 Chip / Tag（标签）

#### 8.5.1 大 Chip（content-Tag-Button，26 高）
| 属性 | 值 |
|---|---|
| 圆角 | `radius.sm`（10） |
| Padding | V 0 / H `spacing.s5`（20） |
| Gap（icon ↔ text） | `spacing.s1`（4） |
| 文字 | `textStyle.bodyLg`（15 Regular） |
| 选中态背景 | `colors.brand` × `colors.opacity.o85` 叠加 |
| 选中态文字 | `colors.brand` |

#### 8.5.2 小 Chip（input-Skill-button，26 高）
| 属性 | 值 |
|---|---|
| 圆角 | `radius.xs`（8） |
| Padding | V `spacing.s1` / H `spacing.s2`（4 / 8） |
| Gap | `spacing.s1`（4） |
| 文字 | `textStyle.mini` 或 `textStyle.miniAccent` |
| 描边 | `dividerWidth.w1` |
| 选中态背景 | `colors.brand` × `colors.opacity.o85` |

### 8.6 ChatBoxIndexInterface（首页输入框）

| 属性 | 值 |
|---|---|
| 高度 | 156（withoutPrompt outline）/ 216（filled）/ 214（uploaded） |
| 圆角 | `radius.md`（12） |
| 容器 padding | V `spacing.s3` / H 0（12 / 0） |
| 子模块 gap | `spacing.s3`（12） |
| 描边（outline） | `dividerWidth.w2`（2） |
| 描边（focus） | 渐变描边特殊处理 |
| 阴影（focus） | `shadow.inputLight` / `shadow.inputDark`（按主题） |
| 背景 | `colors.block.primary` |
| 内部 H padding（content） | `spacing.s3`（12） |
| Empty placeholder | `textStyle.bodyLg` + `colors.foreground.tertiary` |

### 8.7 Header / NavBar

| 属性 | 值 |
|---|---|
| StatusBar 高度 | 44（iOS）/ 44（Android） |
| NavBar 高度 | 44（标准）/ 46（chat 场景） |
| 总 Header 高度 | 88（statusBar + navBar） |
| 背景 | `colors.background.primary` 或透明（沉浸式） |
| 标题文字 | `textStyle.heading2` 或 `textStyle.bodyTitle` |
| 返回 / 操作图标 | 24×24，色 `colors.foreground.primary` |

### 8.8 BottomBar / TabBar

| 属性 | 值 |
|---|---|
| HomeIndicator 高度 | 34 |
| TabBar 内 tab 文字 | `textStyle.tinyAccent`（10 Medium） |
| 选中色 | `colors.brand` |
| 未选中色 | `colors.foreground.secondary` |
| 选中态指示条 | `dividerWidth.w2` + `colors.brand` |

---

## 9. 图标库

> 移动端图标系统：以 Lucide 系列为基底（Figma 中实测使用 Lucide Icons）。所有图标必须通过组件实例引用，禁止裸 SVG 字符串 / 原生 Image 组件加载图标。

### 9.0 命名与落库规则

- Figma 图标命名与代码命名保持一致，统一使用 **PascalCase**，例如：`ChevronDown`、`InputboxSend`、`FileText`。
- SVG 文件名使用资源文件规范：**小写下划线**，例如：`chevron_down.svg`、`inputbox_send.svg`、`file_text.svg`。
- 代码调用统一通过 `SparkIcons` 暴露 PascalCase 名称，例如：

```kotlin
val icon = SparkIcons.ChevronDown
Icon(
    painter = painterResource(icon),
    contentDescription = null,
)
```

- 禁止在业务组件中直接引用资源路径：

```kotlin
// ❌ 禁止
painterResource(Res.drawable.chevron_down)
Icons.Outlined.Search
Icons.Filled.ArrowUpward
```

- 允许的唯一业务层引用方式：

```kotlin
// ✅ 允许
painterResource(SparkIcons.Search)
painterResource(SparkIcons.InputboxSend)
```

### 9.0.1 图标落库目录

| 类型 | 路径 |
|---|---|
| SVG 资源目录 | `mobile/shared/src/commonMain/composeResources/drawable/` |
| 图标代码入口 | `mobile/shared/src/commonMain/kotlin/com/iflytek/spark/shared/core/icon/SparkIcons.kt` |

### 9.0.2 图标落库策略（按需优先）

- **默认策略：先写组件，再补图标。**
- 当 AI 或开发开始实现某个 Figma 组件时，必须先检查该组件所需图标是否已经存在于 `SparkIcons.kt`。
- 若图标已存在：直接复用仓库中的图标资源与 `SparkIcons.*` 入口。
- 若图标不存在：仅新增当前组件实际需要的图标，不得顺手批量导入整个 Figma icon 画板。
- 禁止“先把全部 icon 一次性导入仓库，再开始写组件”的工作方式，除非项目明确进入图标资产库建设阶段并单独评审。

执行顺序必须是：

1. 确认要实现的具体 Figma 组件
2. 列出该组件使用到的图标
3. 检查 `SparkIcons.kt` 是否已有对应项
4. 缺失的图标按需新增到 `drawable/` 并注册进 `SparkIcons.kt`
5. 组件代码只引用 `SparkIcons.*`

这样做的目的：

- 降低一次性引入大量无用 SVG 的噪音
- 保证每个新增图标都有明确使用场景
- 降低 review 成本
- 保持设计资源、代码资源和组件实现之间的映射关系清晰

### 9.1 使用规则（非常重要⚠️）

#### 9.1.1 必须遵守✅
- 移动端项目统一使用 Lucide 图标库（与 Figma 一致）
- 图标默认尺寸 24×24（业务级），16×16（紧凑场景），20×20（次紧凑）
- 图标颜色默认继承父元素 `color` / `tintColor`
- 禁用态图标用 `colors.foreground.tertiary`
- 危险态图标用 `colors.state.danger`

#### 9.1.2 禁止❌
- 禁止混用其他图标库（HeroIcons / Phosphor / Tabler / IconPark 等）
- 禁止用原生 Image 组件加载 SVG / PNG 作为图标
- 禁止图标硬编码颜色（除非是 logo / illustration）
- 禁止仅设置 width 不设置 height（或反之）
- 禁止通过父容器尺寸间接控制图标大小
- 禁止在业务组件中直接使用 `Icons.*`
- 禁止在业务组件中直接使用 `painterResource(Res.drawable.*)`

### 9.2 尺寸 Token

| Token 路径 | 尺寸 | 应用 |
|---|---|---|
| `iconSize.xs` | 12×12 | md 按钮内图标、tag 内图标 |
| `iconSize.sm` | 16×16 | lg 按钮内图标、紧凑列表 |
| `iconSize.md` | 20×20 | input 内图标、辅助操作 |
| `iconSize.lg` | 24×24 | **默认**：导航图标、操作按钮、TabBar |
| `iconSize.xl` | 32×32 | 大模块入口、空态图 |

### 9.3 Hook 检查约定
以下写法可被 Hook 直接判定为违规：
- 非 Lucide 来源的图标 import（除项目认可 logo / brand asset）
- 用原生 Image 组件加载 svg / png 作为图标
- 图标 style 仅 width 无 height（或反之）
- 图标硬编码颜色（非 logo 场景）
- `Icons.*`
- `painterResource(Res.drawable.*)`
- 业务组件未通过 `SparkIcons.*` 间接引用图标

### 9.4 暗色模式要求

- 单色线性图标的颜色必须通过 `tint = SparkMobileTheme.colors.*` 控制。
- 多色品牌图标允许使用 `Color.Unspecified` 保留原始 SVG 颜色，但该图标必须经过设计确认且不承担浅色 / 暗色语义切换。
- 任何需要随 Light / Dark 切换的图标，不允许把浅色值固化在组件逻辑里；必须通过 token tint 控制。

---

## 10. AI 协同约定

### 10.1 AI 生成代码时的强制规则

1. **永远从 token 出发**：每写一个数值、每写一个颜色，先查表，找到匹配 token 路径，使用 token；找不到匹配 token 时，先停下询问，不要自创数值
2. **严格匹配组件 spec**：生成 Button / Input / Card / Chip 等组件时，逐字段对照 §8 组件规范，不允许出现"接近但不一致"的样式
3. **暗色模式自动支持**：颜色 token 已含双模，生成代码不需要写两套颜色，只需调用 token；除非组件本身需要主题敏感判断（如 `shadow.inputLight` / `shadow.inputDark`）
4. **禁止内联样式数值**：所有 spacing、radius、color、fontSize、shadow 必须走 token 引用
5. **变体优先 props 化**：组件变体（如 Button 的 theme/state/size）应作为 props，由 token 映射决定最终样式，而非每次重写
6. **图标先落库再写组件**：组件引用图标前，必须先把 SVG 放进 `composeResources/drawable/`，并在 `SparkIcons.kt` 注册
7. **业务组件只能调 `SparkIcons.*`**：禁止在 feature 代码中直接写 `Icons.*` 或 `painterResource(Res.drawable.*)`
8. **图标按需新增**：实现具体组件时，先检查仓库是否已有所需图标；只有缺失时才新增，禁止无场景全量导入

### 10.2 AI 应主动停下询问的情况

- 设计稿出现 token 表外的数值（如 padding 13 / 18）
- 设计稿出现新颜色（不在 §1.3 的 7 类语义色内）
- 设计稿要求新组件，但 §8 没有匹配的 spec
- 出现"特殊状态"（如渐变描边）需要新增 token

### 10.3 文档自检 Checklist

提交代码前，AI 应自检以下 7 条：
- [ ] 所有颜色都使用 token？
- [ ] 所有间距都在白名单内（spacing 表）？
- [ ] 所有圆角都使用 token？
- [ ] 所有字号 / 字重都来自语义 textStyle？
- [ ] 所有阴影只在 §7.1.3.A 白名单组件上出现？
- [ ] 没有硬编码 hex / RGBA / 数值？
- [ ] 暗色模式可正常切换（无硬编码颜色阻断）？

再额外自检以下 4 条：
- [ ] 所有业务图标都来自 `SparkIcons.*`？
- [ ] 没有 `Icons.*`？
- [ ] 没有 `painterResource(Res.drawable.*)`？
- [ ] Light / Dark 两套模式下图标颜色都通过 token 控制？

### 10.4 Token 全局结构（参考实现）

```ts
// 概念性结构 — 供 RN / Flutter / SwiftUI 各自适配
const theme = {
  colors: {
    brand: token('mode.brand'),
    background: { primary, secondary },
    block: { primary, secondary, tertiary },
    foreground: { primary, secondary, tertiary, quaternary },
    state: { success, danger },
    divider: token('mode.divider'),
    opacity: { o5, o10, o15, o75, o85, o90, o95 },
  },
  radius: { xs: 8, sm: 10, md: 12, lg: 16, xl: 24, full: 9999 },
  dividerWidth: { w1: 1, w2: 2 },
  spacing: {
    s0: 0, s1: 4, s2: 8, s3: 12, s4: 16, s5: 20, s6: 24,
    s8: 32, s10: 40, s12: 48, s14: 56, s16: 64,
  },
  iconSize: { xs: 12, sm: 16, md: 20, lg: 24, xl: 32 },
  fontSize: {
    h1: { size: 18, lineHeight: 28 },
    h2: { size: 16, lineHeight: 28 },
    h3: { size: 15, lineHeight: 26 },
    bodyTitle: { size: 16, lineHeight: 24 },
    bodyLg: { size: 15, lineHeight: 26 },
    bodySm: { size: 14, lineHeight: 22 },
    mini: { size: 13, lineHeight: 22 },
    caption: { size: 12, lineHeight: 18 },
    tiny: { size: 10, lineHeight: 12, letterSpacing: 0.1 },
  },
  textStyle: {
    heading1: { ...fontSize.h1, fontWeight: 500 },
    heading2: { ...fontSize.h2, fontWeight: 500 },
    heading3: { ...fontSize.h3, fontWeight: 500 },
    bodyTitle: { ...fontSize.bodyTitle, fontWeight: 500 },
    bodyLg: { ...fontSize.bodyLg, fontWeight: 400 },
    bodyLgAccent: { ...fontSize.bodyLg, fontWeight: 500 },
    bodySm: { ...fontSize.bodySm, fontWeight: 400 },
    bodySmAccent: { ...fontSize.bodySm, fontWeight: 500 },
    mini: { ...fontSize.mini, fontWeight: 400 },
    miniAccent: { ...fontSize.mini, fontWeight: 500 },
    caption: { ...fontSize.caption, fontWeight: 400 },
    captionAccent: { ...fontSize.caption, fontWeight: 500 },
    tiny: { ...fontSize.tiny, fontWeight: 400 },
    tinyAccent: { ...fontSize.tiny, fontWeight: 500 },
  },
  shadow: {
    inputLight: { color: '#1F69FF', alpha: 0.16, x: 0, y: 4, blur: 16, spread: 0 },
    inputDark:  { color: '#000000', alpha: 0.16, x: 0, y: 4, blur: 16, spread: 0 },
  },
  layout: {
    statusBarHeight: 44,
    navBarHeight: 44,
    totalHeaderHeight: 88,
    homeIndicatorHeight: 34,
    screenPaddingH: 16,
  },
}
```

---

**文档结束。**
适用于 AI 直接生成移动端 UI 代码 / 解读 Figma 设计稿 / 校验现有实现。
