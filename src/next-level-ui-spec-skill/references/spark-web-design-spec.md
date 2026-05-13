# Spark_ScientificResearch Web Design Spec

- 以下三句话是核心思想，非常重要‼️一定要熟读并理解‼️
- 这是一份基于 **shadcn/ui** 制定的设计规范，我们在利用这套规范生成设计时一定要严格调用「token」，调用以下我写的「**css 变量**」，不要输出硬编码‼️
- 一定要熟读并深刻记住每个系统的「使用规则」和「使用示例」‼️
- 要做成响应式网页，桌面端基线 **1440×798**‼️

> Figma 设计系统由 **Mode 集合**（语义层 token）+ **Theme 集合**（实际颜色定义，分 light / dark）组成，是标准 shadcn/ui 风格。所有 token 在 `web/src/styles/globals.css` 中以 CSS 变量形式落地，业务代码必须通过 `var(--xxx)` 或 Tailwind 语义类（如 `bg-primary`、本质也是 `var(--primary)`）调用。

———————————————————————————————————————————————————————————————————————————————————————————

## 目录

1. [颜色系统](#1-颜色系统)
2. [文字系统](#2-文字系统)
3. [圆角系统](#3-圆角系统)
4. [阴影系统](#4-阴影系统)
5. [间距系统](#5-间距系统)
6. [布局系统](#6-布局系统)
7. [组件规范](#7-组件规范)
8. [图标库](#8-图标库)
9. [AI 协同约定](#9-ai-协同约定)

———————————————————————————————————————————————————————————————————————————————————————————

## 1. 颜色系统

-----

### 1.1 使用规则（非常重要‼️熟读并理解‼️）

- 每个颜色都支持 light 和 dark 双模映射，一定要调用 token 并严格输出成「**css 变量**」，千万不可以输出硬编码‼️如果你调用的是硬编码，那么在切换 light / dark 模式时，颜色不会发生变化‼️
- 在单个页面中主题色 `primary` 使用不超过 3 处，保持视觉焦点‼️避免大面积使用主题色 `primary`，以免造成视觉疲劳‼️
- 主题色 `primary` 应用于：主要操作按钮（提交 / 确认 / 发送）、重要信息高亮（选中状态、活动 tab）、关键链接和可点击强调元素‼️
- 状态色 `destructive` 仅用于：删除 / 移除 / 警告操作、错误提示文字、必填星标‼️
- 容器层级关系（**自外而内**）：屏幕背景 `background` → 一级卡片 `card` / 浮层 `popover` → 弱化嵌套 `muted` / 强调态 `accent`，不可错配‼️
- 文字层级：`foreground`（标题、正文）→ `muted-foreground`（描述、占位、辅助）→ `*-foreground` 系列（反白文字，如 `primary-foreground` / `destructive-foreground`），依次降级‼️
- 侧边栏自成一套色板（`sidebar` / `sidebar-foreground` / `sidebar-primary` / `sidebar-accent` 等），不与主内容区颜色混用‼️
- 多色背景色 + 多色文字色，可以用于 `Badge` / `Tag` 标签的语义化取色（业务待补，见 §1.4）‼️
- 底层动效组件（canvas / shader / WebGL / 粒子系统）的内部插值色、渐变采样色、噪声色不属于页面 token 自查范围；但页面层传入这些组件的颜色 props，仍必须来自 design token / css 变量‼️

-----

### 1.2 使用示例（非常重要‼️熟读并理解‼️）

✅ 正确示例
```css
background: var(--primary);
color: var(--primary-foreground);
border: 1px solid var(--border);
box-shadow: var(--shadow);
```

```tsx
<button style={{ background: 'var(--primary)', color: 'var(--primary-foreground)' }}>提交</button>

// Tailwind 语义类同样合规（其底层就是 var(--xxx)）：
<button className="bg-primary text-primary-foreground">提交</button>
<aside className="bg-sidebar text-sidebar-foreground border-r border-sidebar-border">目录</aside>
```

❌ 错误示例
```css
background: #615FFF;                    /* 硬编码 hex */
background: rgba(97, 95, 255, 0.85);    /* 硬编码 RGBA */
color: #1B1C21;                         /* 硬编码 hex */
```

```tsx
<button className="bg-[#615FFF]">提交</button>      // Tailwind 任意值
<button className="bg-blue-600">提交</button>        // 跳过语义层，直接用 Tailwind 调色板
<div className="text-gray-900 dark:text-white">     // 手写双模分支，应直接用 text-foreground
```

-----

### 1.3 色彩系统

#### 1.3.1 主题色

| 语义层 | light 映射色 | dark 映射色 | Token | CSS 变量 |
|---|---|---|---|---|
| 主题色 | `#615fff` | `#7B61FF` | `primary` | `var(--primary)` |
| 主题色之上文字 | `#FFFFFF` | `#FFFFFF` | `primary-foreground` | `var(--primary-foreground)` |

#### 1.3.2 背景色

| 语义层 | light 映射色 | dark 映射色 | Token | CSS 变量 |
|---|---|---|---|---|
| 屏幕背景色 | `#FFFFFF` | `#0D0D0D` | `background` | `var(--background)` |
| 一级卡片背景色（card / 表格行 / 列表项） | `#FFFFFF` | `#1D1D1D` | `card` | `var(--card)` |
| 浮层背景色（dialog / popover / dropdown / tooltip / drawer） | `#FFFFFF` | `#222222` | `popover` | `var(--popover)` |
| 二级嵌套背景色（muted 区块 / tag 底 / 占位区） | `#F0F4F9` | `#1B1B1B` | `muted` | `var(--muted)` |
| 强调态背景色（hover / selected 弱态） | `#F4F4F5` | `#262626` | `accent` | `var(--accent)` |
| 次级按钮背景色 | `#F4F4F5` | `#262626` | `secondary` | `var(--secondary)` |

#### 1.3.3 文字色

| 语义 | light 映射色 | dark 映射色 | Token | CSS 变量 |
|---|---|---|---|---|
| 主文字（标题、正文） | `#1B1C21` | `#D9D9D9` | `foreground` | `var(--foreground)` |
| 一级卡片上文字 | `#171717` | `#D9D9D9` | `card-foreground` | `var(--card-foreground)` |
| 浮层上文字 | `#171717` | `#D9D9D9` | `popover-foreground` | `var(--popover-foreground)` |
| 弱化文字（描述、占位、辅助） | `#828287` | `#A0A4B0` | `muted-foreground` | `var(--muted-foreground)` |
| 强调态文字 | `#52525C` | `#D9D9D9` | `accent-foreground` | `var(--accent-foreground)` |
| 次级按钮文字 | `#52525C` | `#D9D9D9` | `secondary-foreground` | `var(--secondary-foreground)` |
| 失败 / 危险文字 | `#EC003F` | `#E1372E` | `destructive` | `var(--destructive)` |

#### 1.3.4 状态色（背景 + 反白文字）

| 语义 | light 映射色 | dark 映射色 | Token | CSS 变量 |
|---|---|---|---|---|
| 失败 / 危险背景 | `#EC003F` | `#E1372E` | `destructive` | `var(--destructive)` |
| 失败 / 危险背景之上文字 | `#FFFFFF` | `#FFFFFF` | `destructive-foreground` | `var(--destructive-foreground)` |

> ⚠️ 当前 Figma 设计系统**未定义** `success` / `warning` / `info` 语义 token。如业务需要（成功 toast、警告条、提示），AI 必须先停下询问由设计补充 token，**不得**自行用 Tailwind 调色板（`bg-green-500` 等）兜底。

#### 1.3.5 边框 / 输入框 / 焦点环

| 语义 | light 映射色 | dark 映射色 | Token | CSS 变量 |
|---|---|---|---|---|
| 通用边框（卡片、列表、分割线） | `#E4E4E7` | `#2D2D2D` | `border` | `var(--border)` |
| 输入框边框 | `#E4E4E7` | `#2D2D2D` | `input` | `var(--input)` |
| 焦点环 / 选中描边 | `#615FFF` | `#7B61FF` | `ring` | `var(--ring)` |

#### 1.3.6 侧边栏专属色（Spark Web 桌面端核心结构）

> 侧边栏自成一套色板，与主内容区视觉分离。**不允许**用主内容区色 token 给侧边栏上色。

| 语义 | light 映射色 | dark 映射色 | Token | CSS 变量 |
|---|---|---|---|---|
| 侧边栏背景 | `rgba(244, 244, 245, 0.60)` | `#171717` | `sidebar` | `var(--sidebar)` |
| 侧边栏主文字 | `#1B1C21` | `#D9D9D9` | `sidebar-foreground` | `var(--sidebar-foreground)` |
| 侧边栏 nav 选中态背景 | `#FFFFFF` | `#262626` | `sidebar-primary` | `var(--sidebar-primary)` |
| 侧边栏 nav 选中态文字 | `#171717` | `#FFFFFF` | `sidebar-primary-foreground` | `var(--sidebar-primary-foreground)` |
| 侧边栏 nav hover 态背景 | `#F4F4F5` | `#1F1F1F` | `sidebar-accent` | `var(--sidebar-accent)` |
| 侧边栏 nav hover 态文字 | `#52525C` | `#D9D9D9` | `sidebar-accent-foreground` | `var(--sidebar-accent-foreground)` |
| 侧边栏分割线 | `#E4E4E7` | `#2D2D2D` | `sidebar-border` | `var(--sidebar-border)` |
| 侧边栏焦点环 | `#615FFF` | `#7B61FF` | `sidebar-ring` | `var(--sidebar-ring)` |

#### 1.3.7 图表色（数据可视化专用）

| 语义 | Token | CSS 变量 |
|---|---|---|
| 第 1 系列 | `chart-1` | `var(--chart-1)` |
| 第 2 系列 | `chart-2` | `var(--chart-2)` |
| 第 3 系列 | `chart-3` | `var(--chart-3)` |
| 第 4 系列 | `chart-4` | `var(--chart-4)` |
| 第 5 系列 | `chart-5` | `var(--chart-5)` |

> 图表色仅用于折线图 / 柱图 / 饼图 / 进度条等数据可视化场景，**禁止**用于普通 UI 元素。具体 hex 值由设计在 Figma Theme 集合中定义。

#### 1.3.8 阴影色

| 语义 | Token | light 模式色值 | dark 模式色值 | CSS 变量 |
|---|---|---|---|---|
| 阴影色 | `shadow` | `0 1.5px 5px rgba(63, 63, 70, 0.06), 0 1px 1px rgba(63, 63, 70, 0.06)` | `0 1.5px 5px rgba(0, 0, 0, 0.16), 0 1px 1px rgba(0, 0, 0, 0.12)` | `var(--shadow)` |

> 当前设计稿里的 light 浮层阴影已经不是早期蓝色辉光，而是中性灰双层阴影；`var(--shadow)` 可以是多层 box-shadow 字符串。

-----

### 1.4 Badge / Tag 颜色可执行检查规则（供 AI 与 Hook 严格执行）

> ⚠️ 当前 Figma 设计系统**未定义**多色语义 badge token（红 / 橙 / 黄 / 绿 / 青 / 蓝 / 紫）。
>
> 业务上若需要彩色 badge（如「已完成 / 进行中 / 待审核」状态徽标，或文档类型分类），AI 必须停下询问，请设计先在 Figma 中补充以下 token：
> - `red-background` + `red-foreground`
> - `orange-background` + `orange-foreground`
> - `yellow-background` + `yellow-foreground`
> - `green-background` + `green-foreground`
> - `cyan-background` + `cyan-foreground`
> - `blue-background` + `blue-foreground`
> - `purple-background` + `purple-foreground`
>
> 设计补充后，按以下规则执行：

#### A. 允许的背景色
Badge / Tag 只能使用以下背景 token：`red-background` / `orange-background` / `yellow-background` / `green-background` / `cyan-background` / `blue-background` / `purple-background`

#### B. 允许的文字色
Badge / Tag 只能使用以下文字 token：`red-foreground` / `orange-foreground` / `yellow-foreground` / `green-foreground` / `cyan-foreground` / `blue-foreground` / `purple-foreground`

#### C. 配对规则
- `red-background` 只能搭配 `red-foreground`
- `orange-background` 只能搭配 `orange-foreground`
- `yellow-background` 只能搭配 `yellow-foreground`
- `green-background` 只能搭配 `green-foreground`
- `cyan-background` 只能搭配 `cyan-foreground`
- `blue-background` 只能搭配 `blue-foreground`
- `purple-background` 只能搭配 `purple-foreground`

#### D. 禁止规则
- Badge / Tag 禁止使用中性色（`muted` / `accent`）替代语义色
- Badge / Tag 禁止使用硬编码颜色
- Badge / Tag 禁止背景色和文字色跨色系混搭

#### E. Hook 检查约定
以下写法可被 Hook 直接判定为违规：
- `Badge` / `Tag` 使用非白名单背景色
- `Badge` / `Tag` 使用非白名单文字色
- `Badge` / `Tag` 的背景色与文字色不成对
- `Badge` / `Tag` 出现硬编码颜色

———————————————————————————————————————————————————————————————————————————————————————————

## 2. 文字系统

-----

### 2.1 使用规则（让 AI 不乱用）（非常重要‼️熟读并理解‼️）

#### 2.1.1 必须遵守✅
- 页面级主标题语义只能有一个，使用 `display`，每页仅 1 次
- 标题层级不能跳级，`heading-1` → `heading-2` → `heading-3` → `heading-4` 依次递进
- 标题默认展示一行；常规标题不应自然折成两行
- 正文统一用 `body`；阅读型大段长文用 `body-lg`，不要混用
- 按钮文字统一用 `body`
- 表单字段标签统一用 `label`
- 输入框 placeholder 统一用 `body`
- 帮助文字 / 错误提示统一用 `caption`
- 辅助说明、时间、状态文字用 `caption`
- 章节前缀 / 分类标签用 `overline`
- 顶栏导航文字 / 侧边栏 nav item 文字统一用 `nav`
- 代码片段统一用 `code`
- 角标 / 徽标数字统一用 `micro`

#### 2.1.2 禁止❌
- 不能跳级（`heading-1` 直接接 `heading-3`）‼️
- 不能用 `display` 做卡片标题、弹窗标题、表单标题‼️
- 不能用裸 token（`text-2xl` / `text-sm` / `text-xs`）跳过语义层直接使用‼️
- 不能用 `heading-*` 做正文‼️
- 正文字重不能超过 `400`‼️
- 不能让 `heading-1` / `heading-2` / `heading-3` / `heading-4` 默认自动折成两行‼️
- 不能在按钮文字中使用 `heading-*` / `label` / `caption`‼️
- 不能把 `caption` 当作主要正文使用‼️
- 不能把 `overline` 当作按钮文字 / 正文使用‼️
- 不能把 `micro` 当作可读正文使用（仅角标 / 极小标识）‼️
- 不能把 `nav` 当作按钮文字 / 正文 / 标题使用‼️

> Spark Web 没有营销首屏 / 落地页场景，因此**不引入** `hero-display` / `section-display` / `lead` / `metric-number` 这类大字号语义。如未来增加营销页，需先停下补 token 与字号 scale。

#### 2.1.3 可执行检查规则（供 AI 与 Hook 严格执行）

##### A. 标题层级规则
- 页面主标题只允许使用 `display`，每页仅 1 次
- 一级标题只允许使用 `heading-1`
- 二级标题只允许使用 `heading-2`
- 三级标题只允许使用 `heading-3`
- 四级标题只允许使用 `heading-4`
- 标题层级必须逐级递进，不允许跳级
- 禁止 `display → heading-2`（中间应有 `heading-1` 过渡，或主标题语义就用 `heading-1`）
- 禁止 `heading-1 → heading-3`
- 禁止 `heading-2 → heading-4`

##### B. 标题与 HTML 标签映射规则
- `display` / `heading-1` → 必须包裹在 `<h1>`
- `heading-2` → `<h2>`
- `heading-3` → `<h3>`
- `heading-4` → `<h4>`
- 如果使用了 `<h1>` / `<h2>` / `<h3>` / `<h4>` 标签，则其 class 语义必须与标题层级一致
- 禁止 `<h1>` 搭配 `heading-3`
- 禁止 `<h2>` 搭配 `heading-4`
- 禁止普通 `<div>` / `<span>` / `<p>` 冒充页面主标题后再使用错误语义类

##### C. 正文规则
- 默认正文只能使用 `body`
- 大段长文（论文 / 文章正文段落 / 阅读模式）才允许使用 `body-lg`
- 列表项正文、卡片描述、普通说明文字统一使用 `body`
- 禁止在同一信息块中混用 `body` 和 `body-lg`
- 禁止用 `heading-*` 充当正文
- 禁止用 `display` 充当卡片标题、正文标题、说明文字

##### D. 按钮文字规则
- 所有按钮文字必须使用 `body`
- `<button>` 标签内的主文字必须使用 `body`
- shadcn `<Button>` 组件内的主文字必须使用 `body`
- 禁止按钮主文字使用 `heading-*` / `label` / `caption` / `overline` / `nav`
- 图标按钮如果无文字，可不适用本条；但只要出现文字，仍必须使用 `body`

##### E. 表单文字规则
- 字段名 / 表单标签统一使用 `label`
- 输入框 placeholder 统一使用 `body` + `text-muted-foreground`
- 输入框值（已填）统一使用 `body` + `text-foreground`
- 帮助文字统一使用 `caption` + `text-muted-foreground`
- 错误提示统一使用 `caption` + `text-destructive`
- 表单分组标题统一使用 `heading-4`
- 必填星标颜色用 `text-destructive`
- 禁止字段名使用 `body`（无强调）或 `caption`
- 禁止错误提示使用 `body` 或 `label`

##### F. 辅助信息规则
- 时间、状态说明、次级提示、图片说明统一使用 `caption`
- 章节前缀、分类前缀、短标签标题（全大写或带颜色）使用 `overline`
- 代码片段统一使用 `code`
- 顶栏导航 / 侧边栏 nav item 文字统一使用 `nav`
- 角标 / 徽标数字使用 `micro`
- 禁止把 `caption` 用作主要正文
- 禁止把 `overline` 用作按钮文字或正文
- 禁止把 `micro` 用作可读正文（仅角标 / 极小标识）

##### G. 字重规则
- `display` / `heading-1` / `heading-2` / `heading-3` / `heading-4` 只能使用 `600`
- `nav` 只能使用 `600`
- `label` 只能使用 `600`
- `overline` 只能使用 `600`
- `body-lg` / `body` / `caption` / `code` / `micro` 只能使用 `400`
- 正文字重禁止超过 `400`
- 禁止自行写 `font-bold`（700）/ `font-extrabold`（800）/ `font-black`（900）
- 禁止正文使用 `600`

##### H. 裸 token 禁止规则
- 禁止直接使用 `text-2xl` `text-xl` `text-lg` `text-md` `text-sm` `text-xs` `text-xxs` 作为最终语义输出
- 禁止使用 `text-[15px]` `text-[24px]` 等任意值
- 禁止 `style={{ fontSize: 14 }}` 内联样式
- 必须优先使用语义类：`display` / `heading-1` / `heading-2` / `heading-3` / `heading-4` / `body-lg` / `body` / `label` / `caption` / `overline` / `code` / `nav` / `micro`

##### I. Hook 检查约定
以下写法可被 Hook 直接判定为违规：
- 标题文本使用裸 `text-*` 类
- 按钮文本使用 `label` / `caption` / `heading-*` / `overline` / `nav`
- 正文使用 `heading-*`
- 同一页面出现多个 `display`
- 相邻标题层级跳级
- 表单 label 不使用 `label`
- 帮助文字 / 错误提示不使用 `caption`
- 顶栏 / 侧边栏 nav 文字使用裸字号或 `body`
- 常规标题显式使用多行写法（`whitespace-normal` / `line-clamp-2+`）
- Hook 只检查页面、布局、业务 UI 输出层；不直接检查动效底层 shader / canvas 数学实现内部的颜色计算与插值公式

##### J. 标题单行规则
- `heading-1` / `heading-2` / `heading-3` / `heading-4` 默认单行展示
- 页面标题、卡片标题、列表标题、弹窗标题、表单组标题默认单行展示
- 默认标题应使用单行裁切、单行省略或等效 no-wrap 策略
- 多行标题必须是明确的设计决定，不能因为默认布局自然折行

-----

### 2.2 文字规范

#### 2.2.1 语义命名

| 语义名 | 字号 token | 字重 token | 场景 |
|---|---|---|---|
| display | `text-2xl` | 600 | 页面最大主标题，每页只出现一次 |
| heading-1 | `text-2xl` | 600 | 一级标题，section 标题（与 display 同尺寸，但允许多次） |
| heading-2 | `text-xl` | 600 | 二级标题，卡片标题、面板标题 |
| heading-3 | `text-lg` | 600 | 三级标题，弹窗标题、Drawer 标题 |
| heading-4 | `text-md` | 600 | 四级标题，表单组标题、列表项标题 |
| body-lg | `text-md` | 400 | 大段正文，论文 / 文章阅读区 |
| body | `text-sm` | 400 | 默认正文，列表项、按钮文字、输入框文字、卡片描述 |
| label | `text-sm` | 600 | 表单字段标签 |
| caption | `text-xs` | 400 | 辅助说明、时间戳、图片描述、帮助文字、错误提示 |
| overline | `text-xs` | 600 | 分类标签、章节前缀（全大写或带颜色） |
| code | `text-sm` | 400 | 代码片段，等宽字体（`font-mono`） |
| nav | `text-sm` | 600 | 顶栏导航 / 侧边栏 nav item 文字 |
| micro | `text-xxs` | 400 | 角标、徽标数字 |

#### 2.2.2 字号 Token 定义

| Token | 字号 | 行高 | letterSpacing | CSS 变量 |
|---|---|---|---|---|
| `text-xxs` | 10px | 12px | 0 | `var(--text-xxs)` |
| `text-xs` | 12px | 16px | 0 | `var(--text-xs)` |
| `text-xs-2` | 13px | 18px | 0 | `var(--text-xs-2)` |
| `text-sm` | 14px | 20px | 0 | `var(--text-sm)` |
| `text-md` | 16px | 24px | 0 | `var(--text-md)` |
| `text-lg` | 18px | 28px | 0 | `var(--text-lg)` |
| `text-xl` | 20px | 28px | 0 | `var(--text-xl)` |
| `text-2xl` | 24px | 32px | 0 | `var(--text-2xl)` |

> 注：Tailwind 默认 `text-base` = 16px；Spark Web 项目使用 `text-md` 替代 `text-base`，与 Figma `font/size/text-md` token 同名对齐。`tailwind.config.ts` 中显式定义 `md: ['16px', '24px']`。

#### 2.2.3 字重 Token

| Token | 名称 |
|---|---|
| `400` | normal |
| `600` | semibold |

> Spark Web 使用 shadcn 标准字重：标题 / label / nav / overline 用 `600`，正文 / 辅助 / 代码 / 角标用 `400`。**不使用** `500`（medium）/ `700`（bold）/ `900`（black）。

#### 2.2.4 字体族

```css
/* 中英文系统字体栈 */
--font-sans: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei",
             "Segoe UI", Roboto, sans-serif;
/* 等宽字体（用于 code） */
--font-mono: "SFMono-Regular", Menlo, Consolas, "Liberation Mono", monospace;
```

———————————————————————————————————————————————————————————————————————————————————————————

## 3. 圆角系统

### 3.1 使用规范（非常重要‼️熟读并理解‼️）

#### 3.1.1 可执行检查规则（供 AI 与 Hook 严格执行）

##### A. 组件圆角映射

| 组件 | 圆角 | CSS 变量 |
|---|---|---|
| Checkbox / 方形微控件 | `4px` | `var(--radius-square)` |
| Input / Select / Textarea / Datepicker / Radio Group Item / Sidebar option item | `15.2px` | `var(--rounded-xs)` |
| Tabs / Segmented 内层激活项 | `17.2px` | `var(--radius-tab-item)` |
| Footer action Button / Tabs 外层轨道 / Sidebar 历史项 / Icon Button 外壳 | `19.2px` | `var(--rounded-md)` |
| Dialog / Modal / AlertDialog / Sheet / Drawer / 大型白色浮层 | `27.2px` | `var(--rounded-xl)` |
| Add Button / TopBar pill Button / Service pill / Switch / Badge / Avatar / 圆形按钮 | `rounded-full` | `var(--rounded-full)` |
| Table / TableRow / TableCell | 不带圆角（`rounded-none`） | — |

##### B. 禁止规则
- 禁止继续沿用旧 spec 的 `2 / 4 / 6 / 8 / 12` 线性圆角梯度
- 禁止把所有 Button 一律写成 `rounded-md`
- 禁止把 Input / Select / Textarea 写成旧 spec 的 `6px`
- 禁止 Dialog / Modal 使用 `15.2px` / `19.2px` / `rounded-full`
- 禁止 Tabs 内层激活项和外层轨道共用同一圆角值
- 禁止未核实的组件脑补成 `rounded-lg = 8px`
- 禁止使用 `rounded-2xl` / `rounded-3xl` 等 Tailwind 默认更大值
- 禁止 `rounded-[14px]` / `rounded-[10px]` 等任意值
- 禁止 `style={{ borderRadius: 12 }}` / `border-radius: 12px` 硬编码

##### C. 嵌套规则
- 同一个组件内，内层圆角必须 ≤ 外层圆角
- 同一个组件内圆角应统一，不允许混用多个无语义层级（如外层 `rounded-xl` 内部强行 `rounded-full`）
- 纯装饰性嵌套元素若无必要，不应额外设置圆角

##### D. Hook 检查约定
以下写法可被 Hook 直接判定为违规：
- 出现 `rounded-2xl` / `rounded-3xl` / `rounded-[<num>]`
- 出现 `style={{ borderRadius: <num> }}` / `border-radius: <num>px` 硬编码
- Footer action Button 使用非 `19.2px`
- Add / pill Button 使用非 `rounded-full`
- `<Input>` / `<Select>` / `<Textarea>` / Datepicker / Radio Group Item 使用非 `15.2px`
- Tabs 内层激活项使用非 `17.2px`
- `<Dialog>` / `<Modal>` / `<Drawer>` / `<Sheet>` 使用非 `27.2px`
- Checkbox / 方形微控件使用非 `4px`

-----

### 3.2 圆角样式

| Token / 场景 | 值 | CSS 变量 |
|---|---|---|
| `radius-square`（checkbox / 方形微控件） | 4px | `var(--radius-square)` |
| `rounded-xs`（input / radio / sidebar option） | 15.2px | `var(--rounded-xs)` |
| `radius-tab-item`（tabs 内层激活项） | 17.2px | `var(--radius-tab-item)` |
| `rounded-md`（按钮 / tabs 轨道 / list shell） | 19.2px | `var(--rounded-md)` |
| `rounded-xl`（modal / dialog / large surface） | 27.2px | `var(--rounded-xl)` |
| `rounded-full` | 9999px | `var(--rounded-full)` |

> 当前主路径设计稿已经不是旧 spec 的 `2 / 4 / 6 / 8 / 12` 半径体系。经 Figma 主路径节点回查，当前有效圆角是 `4 / 15.2 / 17.2 / 19.2 / 27.2 / 9999`。未读到独立 `rounded-lg` 变量时，禁止自行脑补旧值。

———————————————————————————————————————————————————————————————————————————————————————————

## 4. 阴影系统

### 4.1 使用规范（非常重要‼️熟读并理解‼️）

#### 4.1.1 必须遵守✅
- 浮窗、抽屉、弹窗、ChatBox 输入框 focus 态 可用阴影
- 输入框 focus 态**不使用阴影环**，仅通过 `border` + `var(--ring)` 描边表达
- 卡片默认无阴影；只有「浮起卡片」（如 hero chat box、悬浮态选中卡片）才允许 `var(--shadow)`

#### 4.1.2 禁止❌
- 除浮窗 / 抽屉 / 弹窗 / 浮起卡片外，其他场景**禁止**使用阴影
- 禁止硬编码 `box-shadow: 0 4px 16px rgba(...)` 数值
- 禁止使用非 `var(--shadow)` 的阴影值
- 禁止 `shadow-[<value>]` Tailwind 任意值语法

#### 4.1.3 阴影可执行检查规则（供 AI 与 Hook 严格执行）

##### A. 唯一允许使用阴影的组件
以下场景允许使用 `shadow` / `var(--shadow)`：
- `Popover` / `PopoverContent`
- `DropdownMenu` / `DropdownMenuContent`
- `Dialog` / `DialogContent`
- `AlertDialog` / `AlertDialogContent`
- `Sheet` / `SheetContent`
- `Drawer` / `DrawerContent`
- `Tooltip` / `TooltipContent`
- `Toast` / `Sonner`（短暂浮层）
- `ChatBoxIndexInterface` 激活 / focus 态（业务组件）
- `Sidebar` nav item 选中态（轻微浮起表达「卡片浮于侧栏」）

##### B. 禁止规则
- 普通页面容器禁止使用阴影
- 普通卡片（`<Card>` 默认）禁止使用阴影
- section 禁止使用阴影
- `<Button>` 禁止使用阴影
- `<Badge>` / `<Tag>` 禁止使用阴影
- 静态信息块禁止使用阴影
- 表格行 / 列表项禁止使用阴影
- 输入框 focus 态禁止使用阴影（用 ring 描边代替）
- 禁止硬编码 `box-shadow`
- 禁止使用非 `var(--shadow)` 的阴影值

##### C. Hook 检查约定
以下写法可被 Hook 直接判定为违规：
- 在普通 `<div>` / `<section>` / `<Card>` / `<Button>` / `<Badge>` 上出现 `shadow-*` 类
- 在白名单外组件上出现 `var(--shadow)`
- 出现 `box-shadow: ...` 硬编码
- 出现 `shadow-[<value>]` 任意值

-----

### 4.2 阴影 Token 表

| 语义 | Token | light 模式色值 | dark 模式色值 | CSS 变量 |
|---|---|---|---|---|
| 阴影色 | `shadow` | `0 1.5px 5px rgba(63, 63, 70, 0.06), 0 1px 1px rgba(63, 63, 70, 0.06)` | `0 1.5px 5px rgba(0, 0, 0, 0.16), 0 1px 1px rgba(0, 0, 0, 0.12)` | `var(--shadow)` |

> ⚠️ Spark Web 仅定义**单一阴影 token**。所有需要浮起感的浮层组件统一使用 `var(--shadow)`，**禁止**自行新增 `shadow-sm` / `shadow-md` / `shadow-lg` 等多级阴影。如业务确实需要分级阴影，先停下询问由设计补充。

———————————————————————————————————————————————————————————————————————————————————————————

## 5. 间距系统

### 5.1 使用规范（非常重要‼️熟读并理解‼️）

#### 5.1.1 Token

| Token | 值 | Tailwind 类 | CSS 变量 |
|---|---|---|---|
| Spacing 1 | 4px | `gap-1` `p-1` `m-1` | `var(--spacing-1)` |
| Spacing 2 | 8px | `gap-2` `p-2` `m-2` | `var(--spacing-2)` |
| Spacing 3 | 12px | `gap-3` `p-3` `m-3` | `var(--spacing-3)` |
| Spacing 4 | 16px | `gap-4` `p-4` `m-4` | `var(--spacing-4)` |
| Spacing 5 | 20px | `gap-5` `p-5` `m-5` | `var(--spacing-5)` |
| Spacing 6 | 24px | `gap-6` `p-6` `m-6` | `var(--spacing-6)` |
| Spacing 7 | 28px | `gap-7` `p-7` `m-7` | `var(--spacing-7)` |
| Spacing 8 | 32px | `gap-8` `p-8` `m-8` | `var(--spacing-8)` |
| Spacing 9 | 36px | `gap-9` `p-9` `m-9` | `var(--spacing-9)` |
| Spacing 10 | 40px | `gap-10` `p-10` `m-10` | `var(--spacing-10)` |

#### 5.1.2 可执行检查规则（供 AI 与 Hook 严格执行）

##### A. 间距白名单
仅允许使用以下 spacing token：`1` / `2` / `3` / `4` / `5` / `6` / `7` / `8` / `9` / `10`

对应值：
- `1 = 4px`
- `2 = 8px`
- `3 = 12px`
- `4 = 16px`
- `5 = 20px`
- `6 = 24px`
- `7 = 28px`
- `8 = 32px`
- `9 = 36px`
- `10 = 40px`

##### A-1. 布局语义 token（不属于通用 spacing 白名单，但允许通过 css 变量调用）

> 桌面端固定布局常量，Spark Web 项目专用。

| Token | 值 | CSS 变量 | 应用 |
|---|---|---|---|
| `sidebar-width` | 220px | `var(--sidebar-width)` | 侧边栏固定宽度 |
| `sidebar-collapsed-width` | 64px | `var(--sidebar-collapsed-width)` | 侧边栏折叠宽度 |
| `top-bar-height` | 44px | `var(--top-bar-height)` | 顶栏固定高度 |
| `content-padding-h` | 75px | `var(--content-padding-h)` | 主内容区内部水平 padding |
| `content-padding-top` | 32px | `var(--content-padding-top)` | 主内容区内部顶部 padding |

##### B. 固定场景映射（基于 Figma 实测）

- 图标与文字之间只能使用 `gap-1` 或 `gap-2`（4 / 8）
- 按钮内 padding 只能使用 `px-4 py-2`（16 / 8）
- 按钮内 icon 与 label gap 只能使用 `gap-2`（8）
- 输入框内 padding 只能使用 `px-3 py-2`（12 / 8）
- label 与输入框之间只能使用 `gap-2`（8）
- 帮助文字 / 错误提示与输入框之间只能使用 `mt-1` 或 `mt-2`（4 / 8）
- 表单字段之间只能使用 `gap-4`（16）
- 卡片内 padding 只能使用 `p-4` 或 `p-6`（16 / 24）
- 卡片之间 gap 只能使用 `gap-3` 或 `gap-4`（12 / 16）
- 列表项之间 gap 只能使用 `gap-2` 或 `gap-3`（8 / 12）
- Section 之间 gap 只能使用 `gap-6` 或 `gap-8`（24 / 32）
- 弹窗内 padding 只能使用 `p-6`（24）
- 弹窗 footer 与 body gap 只能使用 `gap-4` 或 `gap-6`（16 / 24）
- Toast / Tooltip 内 padding 只能使用 `px-3 py-2`（12 / 8）
- Tag / Chip 内 padding 只能使用 `px-2 py-1`（8 / 4）
- Sidebar nav item padding 只能使用 `px-3 py-2`（12 / 8）
- Sidebar 同 section 内 nav item gap 只能使用 `gap-1`（4）
- Sidebar 不同 section 之间 gap 只能使用 `gap-3` 或 `gap-4`（12 / 16）
- Sidebar 顶部 logo 区 padding 只能使用 `p-3`（12）
- 顶栏内 padding 只能使用 `px-4`（16）
- 表格 cell padding 只能使用 `px-4 py-3`（16 / 12）
- 主内容区 H 边距只能使用 `var(--content-padding-h)`（75px，桌面端固定常量）
- 主内容区顶部 padding 只能使用 `var(--content-padding-top)`（32px，桌面端固定常量）
- 顶栏高度只能使用 `var(--top-bar-height)`（44px）
- 侧边栏宽度只能使用 `var(--sidebar-width)`（220px）

##### C. 禁止规则
- 禁止使用白名单之外的 spacing token
- 禁止使用 `gap-0` `gap-0.5` `gap-1.5` `gap-2.5` `gap-11` `gap-12` `gap-14` `gap-16` 等非白名单值
- 禁止使用 `p-[13px]` `gap-[18px]` 等任意值
- 禁止硬编码 `padding: 18px` `margin: 14px` `gap: 22px`
- 禁止卡片内 padding 大于页面 padding
- 禁止同一列表或 grid 中混用 gap
- 禁止子层级间距大于父层级间距

##### D. Hook 检查约定
- CSS 属性 `padding` / `margin` / `gap` 的值必须优先使用规范中的 CSS 变量或对应 Tailwind token
- `sidebar-width` / `top-bar-height` / `content-padding-h` 等布局语义 token 不视为硬编码违规
- 以下写法可被 Hook 直接判定为违规：
  - 任意 `p-[...]` `m-[...]` `gap-[...]` `space-*-[...]`
  - 出现不在白名单内的 `p-*` `px-*` `py-*` `m-*` `mt-*` `mb-*` `gap-*`（除布局常量）
  - 直接写死 px 数值，如 `padding: 24px` / `style={{ padding: 24 }}`

———————————————————————————————————————————————————————————————————————————————————————————

## 6. 布局系统

> Web 端是桌面布局：固定 sidebar + 固定 top bar + 主内容区。与移动端单列垂直滚动布局完全不同。所有 Spark Web 业务页面**必须**遵循此外框结构。

### 6.1 设计基线

| 项 | 值 |
|---|---|
| 设计画板 | 1440 × 798 |
| 侧边栏宽度 | `var(--sidebar-width)` = 220px |
| 顶栏高度 | `var(--top-bar-height)` = 44px |
| 主内容区宽度 | 1220px（1440 - 220） |
| 主内容区水平 padding | `var(--content-padding-h)` = 75px |
| 主内容区顶部 padding | `var(--content-padding-top)` = 32px |
| 实际内容最大宽度 | 1070px（1220 - 75 × 2） |

### 6.2 整体框架（推荐 flex 实现）

```tsx
<div className="flex min-h-screen bg-background text-foreground">
  <aside
    className="shrink-0 border-r border-sidebar-border bg-sidebar text-sidebar-foreground"
    style={{ width: 'var(--sidebar-width)' }}
  >
    {/* Sidebar */}
  </aside>
  <main className="flex-1 flex flex-col min-w-0">
    <header
      className="shrink-0 flex items-center justify-between border-b border-border bg-background px-4"
      style={{ height: 'var(--top-bar-height)' }}
    >
      {/* Top bar */}
    </header>
    <div
      className="flex-1 overflow-auto"
      style={{ padding: 'var(--content-padding-top) var(--content-padding-h)' }}
    >
      {/* Page content */}
    </div>
  </main>
</div>
```

### 6.3 响应式断点

| 断点 | 像素 | 场景 |
|---|---|---|
| `sm:` | ≥ 640px | 不在主要支持范围（移动端独立设计） |
| `md:` | ≥ 768px | 平板（仅做不破坏式降级） |
| `lg:` | ≥ 1024px | 笔记本最小宽度 |
| `xl:` | ≥ 1280px | 笔记本 / 桌面常规 |
| `2xl:` | ≥ 1440px | **默认设计基线** |

> 当前 v2.1 设计稿基于 1440 桌面单点设计。需要适配小屏 / 平板 / 移动时，AI 必须先停下询问，由设计补充对应断点的尺寸 / 排版规范。

———————————————————————————————————————————————————————————————————————————————————————————

## 7. 组件规范

本项目基于 [shadcn/ui](https://ui.shadcn.com/docs/components) 组件库，UI 库源码自维护副本（`web/src/components/ui/`）。Figma 设计系统的 `科研助手全面改版` 库 = shadcn/ui 标准组件 + Spark 业务定制变体。

### 7.1 使用原则

- 实现任何 UI 组件前，**先查 shadcn 是否有对应组件**，有则直接使用
- shadcn 没有的组件才自己实现，自定义组件同样**严格遵循本规范的 token**
- 通过 `className` + `cn()` 工具（`clsx + tailwind-merge`）覆盖 shadcn 默认样式，**不修改 `web/src/components/ui/` 下的组件源码**（除非是 token 对接层升级，需评审）
- 业务组件统一放在 `web/src/components/` 或 `web/src/features/<feature>/components/`

### 7.2 定制方式

shadcn 组件样式通过 `className` 覆盖，结合本规范 token：
- 颜色 → §1 颜色系统（`bg-primary` / `text-foreground` / `border-border` / …）
- 间距 → §5 间距系统（`p-4` / `gap-3` / `mt-2` / …）
- 圆角 → §3 圆角系统（`radius-square` / `rounded-xs` / `radius-tab-item` / `rounded-md` / `rounded-xl` / `rounded-full`）
- 文字 → §2 文字系统（`display` / `heading-1..4` / `body` / `label` / `caption` / `nav` / `overline` / `code` / `micro`）
- 阴影 → §4 阴影系统（仅浮层组件 + `var(--shadow)`）

### 7.3 业务专属组件

以下是 Spark Web 业务专属组件，不在 shadcn/ui 内，必须按 Figma 设计稿落地：

| 组件 | 说明 | 关键 token |
|---|---|---|
| `Sidebar` | 220 宽固定侧边栏 + logo + 多级 nav + 折叠态 | `bg-sidebar` / `text-sidebar-foreground` / `border-sidebar-border` |
| `TopBar` | 44 高固定顶栏 + 返回 + 操作按钮组 + 升级会员 | `bg-background` / `border-border` |
| `ChatBoxIndexInterface` | 首页 chat 输入框（带 prompt / upload / focus 渐变描边） | `bg-card` / `rounded-xl` / `var(--shadow)` |
| `UpgradeMembershipButton` | 升级会员按钮（橙金渐变 + 皇冠 icon） | 专用 `card/version update` 渐变 style |

> 这些组件的具体视觉变体（state / size / variant）以 Figma 为准，落地后在 `web/src/components/` 中沉淀对应实现并写好 props。

———————————————————————————————————————————————————————————————————————————————————————————

## 8. 图标库

本项目使用 **Lucide Icons**（shadcn 默认图标库，与 Figma、移动端一致）。图标文档：https://lucide.dev/icons

### 8.1 使用方式

```tsx
import { Search, Settings, ChevronDown } from 'lucide-react';

<Search className="w-5 h-5" />
<Settings className="w-4 h-4 text-muted-foreground" />
```

### 8.2 尺寸规则

- 默认尺寸 → `w-5 h-5`（20px）
- 紧凑辅助信息场景（metadata / status / 卡片辅助信息 / tag 内）→ `w-4 h-4`（16px）

### 8.3 颜色规则

- 默认继承父元素文字颜色（`currentColor`），无需单独设置
- 禁用态 → `text-muted-foreground`
- 危险操作 → `text-destructive`
- 主题色强调 → `text-primary`

### 8.4 图标可执行检查规则（供 AI 与 Hook 严格执行）

#### A. 图标库规则
- 本项目图标只能使用 `lucide-react`
- 禁止混用其他图标库
- 禁止使用 `@heroicons`
- 禁止使用 `react-icons`
- 禁止使用 `phosphor-react` / `@phosphor-icons/*`
- 禁止使用 `tabler-icons-react` / `@tabler/icons-react`
- 禁止使用 `@iconify/*`
- 禁止使用 `<img>` 标签引入 svg 作为图标

#### B. 尺寸规则
- Lucide 图标默认尺寸使用 `w-5 h-5`
- Lucide 图标在紧凑场景可使用 `w-4 h-4`
- 不允许使用 `w-6 h-6`（除非是顶栏 logo / 空态图，需评审）
- 不允许仅写 `w-5` 不写 `h-5`（或反之）
- 不允许仅写 `w-4` 不写 `h-4`（或反之）
- 不允许通过父容器尺寸间接控制图标大小来绕过本规范
- 不允许 `w-[<num>]` / `h-[<num>]` 任意值

#### C. 颜色规则
- 图标默认继承父元素文字颜色
- 禁用态图标只能使用 `text-muted-foreground`
- 危险态图标只能使用 `text-destructive`
- 强调态图标只能使用 `text-primary`
- 禁止为图标硬编码颜色
- 禁止为图标写十六进制颜色、rgb、rgba
- 禁止 `<svg fill="#...">` / `<svg stroke="#...">` 写死颜色

#### D. 暗色模式要求
- 单色线性图标的颜色必须通过 `text-*` token 控制（`currentColor` 自动跟随）
- 多色品牌图标（logo / illustration）允许保留原始 SVG 颜色，但必须经过设计确认且不承担 light / dark 语义切换
- 任何需要随主题切换的图标，禁止把 light 色固化在组件逻辑或 SVG 内

#### E. Hook 检查约定
以下写法可被 Hook 直接判定为违规：
- 非 `lucide-react` 的图标 import（除项目认可的 logo / brand asset）
- `<img src="*.svg">` / `<img src="data:image/svg...">`
- Lucide 图标 className 不成对包含 `w-5 h-5` 或 `w-4 h-4`
- Lucide 图标 className 含 `w-6` / `h-6`（除非评审通过）
- Lucide 图标 className 含 `w-[...]` / `h-[...]` 任意值
- 图标直接使用硬编码颜色（hex / rgb / rgba）

———————————————————————————————————————————————————————————————————————————————————————————

## 9. AI 协同约定

### 9.1 AI 生成代码时的强制规则

1. **永远从 token 出发**：每写一个数值、每写一个颜色，先查表，找到匹配的 CSS 变量或 Tailwind 语义类；找不到匹配 token 时，先停下询问，**不要自创数值**或使用任意值语法
2. **CSS 变量优先**：所有颜色、圆角、阴影、布局常量统一通过 `var(--xxx)` 调用；Tailwind 语义类（`bg-primary` 等）等价合规但本质就是 `var(--primary)`，二选一即可
3. **暗色模式自动支持**：颜色 token 已含双模，生成代码不需要写两套颜色，只需调用语义 token；除非组件本身需要主题敏感渐变（如 hero 区背景），此时仍要通过 token 切换不能写 `if (isDark)`
4. **禁止内联样式与硬编码**：所有 spacing、radius、color、fontSize、shadow 必须走 CSS 变量 / Tailwind 语义类；禁止 `style={{ color: '#xxx' }}` / `bg-[#...]` / `p-[18px]` / `rounded-[14px]` / `box-shadow: 0 ...`
5. **禁止 Tailwind 调色板**：禁止 `bg-blue-500` / `text-gray-900` / `border-zinc-200` 等跳过语义层的写法；颜色必须用 `bg-primary` / `text-foreground` / `border-border` 这类语义 token
6. **变体优先 props 化**：组件变体（如 Button 的 variant/size）应作为 props，由 token 映射决定最终样式（基于 cva / shadcn 模式），而非每次重写
7. **shadcn/ui 优先**：基础组件优先使用 shadcn/ui 已封装的版本（`@/components/ui/*`），业务定制再 wrap 一层
8. **使用 cn() 合并 className**：所有动态 className 通过 `cn()` 工具（`clsx + tailwind-merge`）合并
9. **图标先注册再使用**：业务文件不直接 `import { ... } from 'lucide-react'`；统一通过 `@/components/icon/spark-icons` re-export 后调用
10. **整体框架使用 §6 Sidebar + TopBar + Main 布局结构**

### 9.2 AI 应主动停下询问的情况

- 设计稿出现 token 表外的数值（padding 18 / gap 13、字号 17、圆角 14）
- 设计稿出现新颜色（不在 §1.3 的语义色内，如新增 success / warning / info 语义）
- 设计稿出现彩色 badge / tag（在 §1.4 的 7 色多色 token 还没补充前）
- 设计稿要求新组件，但 §7 没有匹配的 spec
- 出现「特殊状态」（如渐变描边、玻璃态、自定义阴影、营销 hero display）需要新增 token
- 出现 web 端尚未明确支持的响应式断点

### 9.3 文档自检 Checklist

提交代码前，AI 应自检以下 8 条：

- [ ] 所有颜色都使用 `var(--xxx)` 或 `bg-/text-/border-` 语义类，没有硬编码 hex / RGBA？
- [ ] 没有 Tailwind 调色板（`bg-blue-500` / `text-gray-900`）跳过语义层？
- [ ] 所有间距都在白名单内（`1` ~ `10` 或布局常量 `var(--sidebar-width)` 等）？
- [ ] 所有圆角都使用 `rounded-{xs,sm,md,lg,xl,full}` 语义类？
- [ ] 所有字号 / 字重都来自语义类（`display` / `heading-x` / `body` / `label` / `caption` / `nav` 等），没有裸 `text-2xl` / `text-[15px]`？
- [ ] 所有阴影只在 §4.1.3.A 白名单组件上出现，且只用 `var(--shadow)`？
- [ ] 没有任意值（`bg-[#...]` / `p-[18px]` / `rounded-[14px]` / `shadow-[...]`）？
- [ ] 暗色模式可正常切换（无硬编码颜色 / 无 `dark:bg-[#...]` 任意值阻断）？

再额外自检以下 5 条：

- [ ] 所有图标都来自 `lucide-react`（业务文件经过 `spark-icons` re-export）？
- [ ] 没有 `<img src="*.svg">` 加载图标？
- [ ] 图标 className 成对包含 `w-5 h-5` 或 `w-4 h-4`，没有 `w-6` / `w-[...]`？
- [ ] Light / Dark 两套模式下图标颜色都通过 `text-*` token 控制？
- [ ] 整体框架使用 §6.2 Sidebar + TopBar + Main 布局结构？

### 9.4 Token 全局结构（参考实现 — `web/src/styles/globals.css`）

```css
@layer base {
  :root {
    /* === Color: Mode 集合（语义层） === */
    --primary: 241 100% 69%;              /* #615FFF */
    --primary-foreground: 0 0% 100%;

    --background: 0 0% 100%;
    --foreground: 230 10% 12%;            /* #1B1C21 */

    --card: 0 0% 100%;
    --card-foreground: 0 0% 9%;           /* #171717 */

    --popover: 0 0% 100%;
    --popover-foreground: 0 0% 9%;        /* #171717 */

    --secondary: 240 5% 96%;              /* #F4F4F5 */
    --secondary-foreground: 240 6% 34%;   /* #52525C */

    --muted: 215 33% 96%;                 /* #F0F4F9 */
    --muted-foreground: 240 2% 52%;       /* #828287 */

    --accent: 240 5% 96%;                 /* #F4F4F5 */
    --accent-foreground: 240 6% 34%;      /* #52525C */

    --destructive: 345 100% 46%;          /* #EC003F */
    --destructive-foreground: 0 0% 100%;

    --border: 240 6% 90%;                 /* #E4E4E7 */
    --input: 240 6% 90%;                  /* #E4E4E7 */
    --ring: 241 100% 69%;                 /* #615FFF */

    /* Sidebar */
    --sidebar: 240 5% 96% / 0.6;          /* rgba(244, 244, 245, 0.60) */
    --sidebar-foreground: 230 10% 12%;    /* #1B1C21 */
    --sidebar-primary: 0 0% 100%;
    --sidebar-primary-foreground: 0 0% 9%; /* #171717 */
    --sidebar-accent: 240 5% 96%;          /* #F4F4F5 */
    --sidebar-accent-foreground: 240 6% 34%; /* #52525C */
    --sidebar-border: 240 6% 90%;          /* #E4E4E7 */
    --sidebar-ring: 241 100% 69%;          /* #615FFF */

    /* Charts (具体值由设计在 Figma Theme 集合中给出) */
    --chart-1: ...; --chart-2: ...; --chart-3: ...; --chart-4: ...; --chart-5: ...;

    /* === Shadow === */
    --shadow: 0 1.5px 5px rgba(63, 63, 70, 0.06), 0 1px 1px rgba(63, 63, 70, 0.06);

    /* === Radius === */
    --radius-square: 4px;
    --rounded-xs: 15.2px;
    --radius-tab-item: 17.2px;
    --rounded-md: 19.2px;
    --rounded-xl: 27.2px;
    --rounded-full: 9999px;

    /* === Typography === */
    --text-xxs: 10px;
    --text-xs: 12px;
    --text-xs-2: 13px;
    --text-sm: 14px;
    --text-md: 16px;
    --text-lg: 18px;
    --text-xl: 20px;
    --text-2xl: 24px;

    --font-sans: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei",
                 "Segoe UI", Roboto, sans-serif;
    --font-mono: "SFMono-Regular", Menlo, Consolas, "Liberation Mono", monospace;

    /* === Spacing === */
    --spacing-1: 4px;
    --spacing-2: 8px;
    --spacing-3: 12px;
    --spacing-4: 16px;
    --spacing-5: 20px;
    --spacing-6: 24px;
    --spacing-7: 28px;
    --spacing-8: 32px;
    --spacing-9: 36px;
    --spacing-10: 40px;

    /* === Layout === */
    --sidebar-width: 220px;
    --sidebar-collapsed-width: 64px;
    --top-bar-height: 44px;
    --content-padding-h: 75px;
    --content-padding-top: 32px;
  }

  .dark {
    --primary: 250 100% 69%;              /* #7B61FF */
    --primary-foreground: 0 0% 100%;

    --background: 0 0% 5%;                /* #0D0D0D */
    --foreground: 0 0% 85%;               /* #D9D9D9 */

    --card: 0 0% 11%;                     /* #1D1D1D */
    --card-foreground: 0 0% 85%;

    --popover: 0 0% 13%;                  /* #222222 */
    --popover-foreground: 0 0% 85%;

    --secondary: 0 0% 15%;                /* #262626 */
    --secondary-foreground: 0 0% 85%;

    --muted: 0 0% 11%;                    /* #1B1B1B */
    --muted-foreground: 222 8% 65%;       /* #A0A4B0 */

    --accent: 0 0% 15%;
    --accent-foreground: 0 0% 85%;

    --destructive: 4 75% 53%;             /* #E1372E */
    --destructive-foreground: 0 0% 100%;

    --border: 0 0% 18%;                   /* #2D2D2D */
    --input: 0 0% 18%;
    --ring: 250 100% 69%;

    --sidebar: 0 0% 9%;                   /* #171717 */
    --sidebar-foreground: 0 0% 85%;
    --sidebar-primary: 0 0% 15%;
    --sidebar-primary-foreground: 0 0% 100%;
    --sidebar-accent: 0 0% 12%;
    --sidebar-accent-foreground: 0 0% 85%;
    --sidebar-border: 0 0% 18%;
    --sidebar-ring: 250 100% 69%;

    --shadow: 0 1.5px 5px rgba(0, 0, 0, 0.16), 0 1px 1px rgba(0, 0, 0, 0.12);
  }
}
```

```ts
// tailwind.config.ts — 让 Tailwind 语义类直连 CSS 变量
import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: { DEFAULT: 'hsl(var(--primary))', foreground: 'hsl(var(--primary-foreground))' },
        secondary: { DEFAULT: 'hsl(var(--secondary))', foreground: 'hsl(var(--secondary-foreground))' },
        destructive: { DEFAULT: 'hsl(var(--destructive))', foreground: 'hsl(var(--destructive-foreground))' },
        muted: { DEFAULT: 'hsl(var(--muted))', foreground: 'hsl(var(--muted-foreground))' },
        accent: { DEFAULT: 'hsl(var(--accent))', foreground: 'hsl(var(--accent-foreground))' },
        popover: { DEFAULT: 'hsl(var(--popover))', foreground: 'hsl(var(--popover-foreground))' },
        card: { DEFAULT: 'hsl(var(--card))', foreground: 'hsl(var(--card-foreground))' },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        sidebar: {
          DEFAULT: 'hsl(var(--sidebar))',
          foreground: 'hsl(var(--sidebar-foreground))',
          primary: 'hsl(var(--sidebar-primary))',
          'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
          accent: 'hsl(var(--sidebar-accent))',
          'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
          border: 'hsl(var(--sidebar-border))',
          ring: 'hsl(var(--sidebar-ring))',
        },
        chart: {
          1: 'hsl(var(--chart-1))', 2: 'hsl(var(--chart-2))', 3: 'hsl(var(--chart-3))',
          4: 'hsl(var(--chart-4))', 5: 'hsl(var(--chart-5))',
        },
      },
      borderRadius: {
        square: 'var(--radius-square)',
        xs: 'var(--rounded-xs)',
        tab: 'var(--radius-tab-item)',
        md: 'var(--rounded-md)',
        xl: 'var(--rounded-xl)',
        full: 'var(--rounded-full)',
      },
      boxShadow: {
        DEFAULT: 'var(--shadow)',
      },
      fontSize: {
        xxs: ['var(--text-xxs)', '12px'],
        xs:  ['var(--text-xs)', '16px'],
        'xs-2': ['var(--text-xs-2)', '18px'],
        sm:  ['var(--text-sm)', '20px'],
        md:  ['var(--text-md)', '24px'],
        lg:  ['var(--text-lg)', '28px'],
        xl:  ['var(--text-xl)', '28px'],
        '2xl': ['var(--text-2xl)', '32px'],
      },
      fontFamily: {
        sans: 'var(--font-sans)',
        mono: 'var(--font-mono)',
      },
      spacing: {
        1: 'var(--spacing-1)',  2: 'var(--spacing-2)',  3: 'var(--spacing-3)',
        4: 'var(--spacing-4)',  5: 'var(--spacing-5)',  6: 'var(--spacing-6)',
        7: 'var(--spacing-7)',  8: 'var(--spacing-8)',  9: 'var(--spacing-9)',
        10: 'var(--spacing-10)',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
} satisfies Config;
```

```css
/* web/src/styles/typography.css — 语义化字号类 */
@layer components {
  .display      { font-size: var(--text-2xl); line-height: 32px; font-weight: 600; }
  .heading-1    { font-size: var(--text-2xl); line-height: 32px; font-weight: 600; }
  .heading-2    { font-size: var(--text-xl);  line-height: 28px; font-weight: 600; }
  .heading-3    { font-size: var(--text-lg);  line-height: 28px; font-weight: 600; }
  .heading-4    { font-size: var(--text-md);  line-height: 24px; font-weight: 600; }
  .body-lg      { font-size: var(--text-md);  line-height: 24px; font-weight: 400; }
  .body         { font-size: var(--text-sm);  line-height: 20px; font-weight: 400; }
  .label        { font-size: var(--text-sm);  line-height: 20px; font-weight: 600; }
  .caption      { font-size: var(--text-xs);  line-height: 16px; font-weight: 400; }
  .overline     { font-size: var(--text-xs);  line-height: 16px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }
  .code         { font-size: var(--text-sm);  line-height: 20px; font-weight: 400; font-family: var(--font-mono); }
  .nav          { font-size: var(--text-sm);  line-height: 20px; font-weight: 600; }
  .micro        { font-size: var(--text-xxs); line-height: 12px; font-weight: 400; }
}
```

> ⚠️ 上面给出的 HSL 值是基于 Figma 视觉观察 + shadcn/ui 默认值的推荐落地。**实际接入项目时，必须以 Figma 文件 Mode 集合 + Theme 集合的最终 hex 为准**（接入时通过 Figma 选中节点后调用 `get_variable_defs` 提取最终值并覆盖此处推荐值）。

———————————————————————————————————————————————————————————————————————————————————————————

**文档结束。**
适用于 AI 直接生成 Web 端 UI 代码 / 解读 Figma 设计稿 / 校验现有 React + Tailwind + shadcn/ui 实现。
