---
paths:
  - "web/**/*.tsx"
  - "web/**/*.ts"
  - "web/**/*.jsx"
  - "web/**/*.js"
  - "web/**/*.css"
  - "web/**/*.scss"
  - "web/**/*.sass"
  - "web/**/*.less"
  - "web/**/*.html"
  - "web/**/*.vue"
---
# Spark Web Design Spec 强制规则

> 凡是修改 `web/` 下任何 React / Tailwind / shadcn UI / styles / icon 代码，必须严格遵守本规则。
> 本规则与 `design/spark-web-design-spec.md`（仓库内规范文件）配套，spec 是唯一事实来源。
> Web 端**不复用** mobile 规则；mobile 用 `colors.brand` / `spacing.s4` 这套 camelCase token，web 用 shadcn `var(--primary)` / `gap-4` 这套 CSS 变量 + Tailwind 语义类。两者命名约定刻意不一致，禁止互串。

## 0. 写代码前必须先读 spec（Hard Requirement）

**触发条件**：本次任务涉及任意以下文件路径：

- `web/**/*.tsx`
- `web/**/*.ts`
- `web/**/*.jsx`
- `web/**/*.js`
- `web/**/*.css` / `*.scss` / `*.sass` / `*.less`
- `web/**/*.html`
- `web/**/*.vue`
- 任意 `web/` 下的页面 / 组件 / 布局代码

**强制动作**：在动手写 / 改任何一行代码 **之前**，按以下顺序执行：

1. 用 Read 工具完整读取 `design/spark-web-design-spec.md`（不允许只读片段或跳读）。
2. 在该 spec 中定位本次任务相关章节（§1 颜色 / §2 文字 / §3 圆角 / §4 阴影 / §5 间距 / §6 布局 / §7 组件 / §8 图标）。
3. 在回复中向用户简要复述将引用的 token（例：`var(--primary)`、`bg-card`、`rounded-md`、`heading-2`），让用户能即时纠偏。
4. 同步阅读 token 实现：`web/src/styles/globals.css`（CSS 变量定义层）与 `web/tailwind.config.ts`（Tailwind 语义类映射层），确认 spec 中的 token 在代码中对应的实际命名。
5. 如果 `web/src/styles/globals.css` 或 `web/tailwind.config.ts` 不存在（项目刚起步），先停下询问用户是否要先按 spec §9.4 落地这两份文件，再开始写业务代码。

**禁止跳过**：即便对 spec 内容看似熟悉、即便是「微小修改」，仍必须先读。spec 在持续演进，缓存的记忆不可信。

## 1. Token 调用白名单

UI 代码中所有视觉数值，**只允许**通过以下两种入口取得：

### 1.1 CSS 变量（首选）

```css
background: var(--primary);
color: var(--foreground);
border: 1px solid var(--border);
box-shadow: var(--shadow);
border-radius: var(--rounded-md);
padding: var(--spacing-4);
font-size: var(--text-sm);
width: var(--sidebar-width);
height: var(--top-bar-height);
```

### 1.2 Tailwind 语义类（同语义、等价合规）

```tsx
<div className="bg-primary text-primary-foreground border border-border rounded-md p-4 shadow" />
<aside className="bg-sidebar text-sidebar-foreground border-r border-sidebar-border" />
<button className="bg-secondary text-secondary-foreground hover:bg-accent" />
```

> Tailwind 语义类的本质就是 `var(--primary)`（在 `tailwind.config.ts` 中通过 `'hsl(var(--primary))'` 挂接），两种写法二选一即可。

### 1.3 文字使用语义类（不允许裸 `text-*` 字号）

文字必须用语义类而不是裸字号：

```css
/* ✅ 推荐：语义类 */
.title { /* 由 web/src/styles/typography.css 中的 .heading-1 提供 */ }
```

```tsx
<h1 className="display">页面主标题</h1>
<h2 className="heading-2">卡片标题</h2>
<p className="body">正文</p>
<label className="label">字段名</label>
<span className="caption">辅助说明</span>
<nav className="nav">导航</nav>
```

**绝对禁止**（`web_design_spec_guard.py` PostToolUse hook 会扫描并拦截）：

- 硬编码 hex / RGBA / HSL：`#1F69FF`、`rgb(...)`、`rgba(...)`、`hsl(...)`、`hsla(...)` 写在业务 UI 代码里
  （仅 `web/src/styles/globals.css` 等 token 定义层允许）
- Tailwind 任意值：`bg-[#1F69FF]`、`text-[#xxx]`、`p-[18px]`、`rounded-[14px]`、`shadow-[...]`、`text-[15px]`、`w-[16px]`
- Tailwind 调色板（跳过语义层）：`bg-blue-500`、`text-gray-900`、`border-zinc-200`、`bg-slate-50` 等任何 `bg-/text-/border-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(50..950)`
- 裸 Tailwind 字号 token：`text-2xl`、`text-xl`、`text-lg`、`text-md`、`text-sm`、`text-xs`、`text-xxs`、`text-base`（必须用 `display` / `heading-x` / `body` / `label` / `caption` / `overline` / `code` / `nav` / `micro` 等语义类）
- 裸 Tailwind 字重：`font-bold`（700）、`font-extrabold`（800）、`font-black`（900）、`font-medium`（500）（Spark Web 只允许 `400` / `600`，且通过语义类隐式应用）
- 间距白名单外的 Tailwind 类：`p-0.5`、`p-1.5`、`p-2.5`、`p-3.5`、`p-11`、`p-12`、`p-14`、`p-16`、`p-20`、`p-24`、`p-32` 等（合法 spacing 仅 `1` ~ `10`，对应 4 ~ 40 px）
- Tailwind 圆角越界：`rounded-2xl`、`rounded-3xl`（合法仅 `rounded-{xs,sm,md,lg,xl,full}`）
- Tailwind 阴影越界：`shadow-sm`、`shadow-md`、`shadow-lg`、`shadow-xl`、`shadow-2xl`（Spark Web 只有单一 `var(--shadow)`；写 `shadow` 或 `style={{ boxShadow: 'var(--shadow)' }}` 才合规）
- 内联硬编码：`style={{ color: '#xxx', padding: 24, fontSize: 14, borderRadius: 12, boxShadow: '0 4px 16px ...' }}`
- CSS 内硬编码：`padding: 24px`、`margin: 14px`、`font-size: 14px`、`border-radius: 12px`、`box-shadow: 0 ...`（在 `globals.css` token 定义层之外）
- 双模手写分支：`if (theme === 'dark')`、`useDarkMode()` 后切换硬编码颜色，`dark:bg-[#xxx]`（颜色应由 token 自带双模解决）
- Tailwind 透明度任意值：`bg-[rgba(...)]`、`/<非白名单数>`（合法 `/` 后值仅 `5` `10` `15` `75` `85` `90` `95`）

设计稿出现 spec 外的数值或新颜色 → **停止编码并向用户提问**，请求扩 token 或更新 spec，不允许自创。

## 2. 图标使用规则

- 所有 UI 图标 **必须** 通过 `lucide-react` 引用。
- 推荐统一封装到 `web/src/components/icon/spark-icons.ts(x)` 再 re-export，业务代码引用 `@/components/icon/spark-icons` 而非直接 `from 'lucide-react'`。
- **禁止** 在 feature / components 代码中混入其他图标库：
  - `@heroicons/react`
  - `react-icons`
  - `phosphor-react` / `@phosphor-icons/react`
  - `tabler-icons-react` / `@tabler/icons-react`
  - `@iconify/react` / `@iconify-icons/react`
- **禁止** 用 `<img src="*.svg">` / `<img src="data:image/svg...">` 加载图标。
- 图标尺寸只能用 `w-5 h-5`（默认 20px）或 `w-4 h-4`（紧凑 16px）；`w-6 h-6` / `w-[16px]` / 仅 `w-5` 不写 `h-5` 都禁止。
- 图标颜色默认通过 `text-*` 语义类继承（`currentColor`），禁用态用 `text-muted-foreground`、危险态用 `text-destructive`、强调态用 `text-primary`。
- 禁止 `<svg fill="#xxx">` / `<svg stroke="#xxx">` 写死颜色。
- 按需新增：实现具体组件前先扫一遍 `spark-icons.ts(x)` 是否已 re-export 目标图标，缺失才新增；不要批量预导出 lucide。

## 3. 组件实现约束

- 写新组件前，先查 [shadcn/ui](https://ui.shadcn.com/docs/components) 是否已有对应组件；有则直接复用 `web/src/components/ui/<component>.tsx`。
- 业务定制只通过 `className` + `cn()` 工具（`clsx + tailwind-merge`）覆盖，**不修改** `web/src/components/ui/` 下源码（除非是 token 对接层升级，需评审）。
- 业务专属组件（Sidebar / TopBar / ChatBoxIndexInterface / UpgradeMembershipButton）放在 `web/src/components/` 或 `web/src/features/<feature>/components/`，按 spec §7.3 落地，所有视觉数值来自 §1 token。
- 组件变体（`variant` / `size` / `state`）必须基于 `cva`（class-variance-authority）+ props 表达，由 token 映射决定样式，不要在调用方层层重写 `className`。
- 所有 token 取值放在组件顶部统一从 CSS 变量 / Tailwind 语义类解出，便于审查。
- 整体页面框架必须遵循 spec §6.2 的 Sidebar (`var(--sidebar-width)`) + TopBar (`var(--top-bar-height)`) + Main 三段结构，不允许自创布局。

## 4. 提交前自检 Checklist

修改完成后，务必逐条核对（对应 spec §9.3）：

视觉 token 类（8 条）：

- [ ] 所有颜色都用了 `var(--xxx)` 或 `bg-/text-/border-` 语义类，没有硬编码 hex / RGBA / HSL？
- [ ] 没有 Tailwind 调色板（`bg-blue-500` / `text-gray-900` / `border-zinc-200`）？
- [ ] 所有间距都在白名单内（`1` ~ `10` 或布局常量 `var(--sidebar-width)` / `var(--top-bar-height)` / `var(--content-padding-h)`）？
- [ ] 所有圆角都使用 `rounded-{xs,sm,md,lg,xl,full}` 语义类（或 `var(--rounded-xx)`）？没有 `rounded-2xl` / `rounded-[14px]`？
- [ ] 所有字号 / 字重都来自语义类（`display` / `heading-1..4` / `body-lg` / `body` / `label` / `caption` / `overline` / `code` / `nav` / `micro`），没有裸 `text-2xl` / `text-[15px]` / `font-bold`？
- [ ] 所有阴影只在 spec §4.1.3.A 白名单组件上出现，且只用 `var(--shadow)` / `shadow`，没有 `shadow-sm/md/lg` / `shadow-[...]`？
- [ ] 没有任意值（`bg-[#...]` / `p-[18px]` / `rounded-[14px]` / `shadow-[...]` / `text-[15px]` / `w-[16px]`）？
- [ ] 暗色模式可正常切换（无硬编码颜色 / 无 `dark:bg-[#xxx]` 任意值阻断 / 无 `if (theme === 'dark')` 分支）？

图标 + 布局类（5 条）：

- [ ] 所有图标都来自 `lucide-react`（业务文件经过 `spark-icons` re-export）？
- [ ] 没有 `<img src="*.svg">` 加载图标？
- [ ] 图标 className 成对包含 `w-5 h-5` 或 `w-4 h-4`，没有 `w-6` / `w-[...]` / 单边尺寸？
- [ ] Light / Dark 两套模式下图标颜色都通过 `text-*` token 控制？
- [ ] 整体框架使用 spec §6.2 Sidebar + TopBar + Main 布局结构？

未通过任意一项 → 返回修改，不要交付。

## 5. 配套机制（自动校验，不可绕过）

以下机制会在编辑后自动执行，输出违例必须先修复再继续：

- `scripts/hooks/web_design_spec_guard.py`：扫描 `web/` UI 代码中的硬编码、Tailwind 任意值、Tailwind 调色板、非 lucide 图标库引入。
- `.claude/hooks/ai_runtime_guard.sh` → `scripts/hooks/ai_runtime_guard.py`：注入 spec 约束、PostToolUse / Stop 阶段做自查（**同时**跑 mobile 与 web 两个 guard）。
- `.githooks/pre-commit` → `scripts/hooks/pre-commit.sh`：提交前最后一道闸（mobile + web 两个 guard 都跑 `--staged`）。
- 新 clone 后必须执行 `bash scripts/install-hooks.sh` 启用 git hook。

如果任何一道闸报错，**优先修代码** 而不是修 hook；只有规则本身确有问题、且与用户对齐后，才能调整 spec / hook。

## 6. 越界行为（Block 级）

以下任何一种情况都属于规则违反，发现立即停手并向用户报告：

- 在 UI 代码里直接写硬编码颜色 / 数值 / 字号
- 用 Tailwind 调色板（`bg-blue-500` 等）替代语义 token
- 用任意值语法（`bg-[#...]` / `p-[18px]` / `rounded-[14px]` / `shadow-[...]`）绕过 token
- 在 feature / components 里使用 `@heroicons` / `react-icons` / `phosphor` / `tabler-icons` / `@iconify` 等非 lucide 图标库
- 用 `<img src="*.svg">` 加载图标
- 用 `if (theme === 'dark')` 之类条件分支替代 token 双模
- 引入 spec 之外的新组件或新视觉规则却没先和用户对齐
- 跳过 §0「写代码前先读 spec」直接动手
- 把 mobile 的 `colors.*` / `spacing.s4` / `radius.md` 等 token 写进 `web/`（命名约定不互通）

## 参考

- 规范源文件：`design/spark-web-design-spec.md`
- Token CSS 变量定义：`web/src/styles/globals.css`（项目落地后存在）
- Tailwind 语义类映射：`web/tailwind.config.ts`
- 语义化字号类：`web/src/styles/typography.css`
- 图标统一入口：`web/src/components/icon/spark-icons.ts(x)`
- 自动校验脚本：`scripts/hooks/web_design_spec_guard.py`
- AI runtime hook：`scripts/hooks/ai_runtime_guard.py`
- 顶层项目说明：`CLAUDE.md` / `AGENTS.md`（亦记录了同一约束）
