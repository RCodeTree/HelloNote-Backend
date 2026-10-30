# Hello!Note 前端主题与视觉设计规范



设计方向确定

Light / Dark 双主题



项目整体采用 Retro Glassmorphism（复古玻璃拟态） 设计风格，并支持完整的 Light（浅色）和 Dark（深色）主题切换。

这份规范不仅定义颜色，还会覆盖字体、玻璃材质、组件样式、页面布局、主题切换机制、不同页面的适配规则以及响应式设计，作为后续前端开发和 AI 编程工具生成 UI 的统一依据。

# 一、整体设计定位

## 1.1 设计风格

Hello!Note — Retro Glassmorphism

中文定位：复古黑白美学 + 现代玻璃质感。

整体设计由三个部分构成：

| 设计元素 | 核心作用   | 具体表现                |
| ---- | ------ | ------------------- |
| 黑白基调 | 建立视觉秩序 | 黑色、白色、灰色            |
| 复古风格 | 建立品牌气质 | 暖白纸张、衬线字体、古铜金、低饱和色彩 |
| 玻璃质感 | 增加视觉层次 | 半透明、背景模糊、细边框、柔和阴影   |

整体需要呈现出一种安静、简洁、有质感的笔记应用风格。

不希望采用常见的高饱和度科技风，也不希望页面出现大量鲜艳的渐变色。

## 1.2 核心设计原则

1. 黑色和白色是整个项目的基础色。
2. Light 和 Dark 两种主题必须保持统一的视觉语言。
3. 复古风格通过字体、材质、颜色和细节体现，而不是堆砌装饰。
4. 玻璃效果用于增加层次，不能影响正文阅读。
5. 所有页面和组件必须适配当前主题，不能只切换页面背景。
6. 同一组件在两种主题下应保持结构、布局和交互一致。
7. 优先保证笔记阅读、编辑、搜索等核心功能的体验。

# 二、主题配色系统

整个项目采用两套配色方案：

- Light：暖白纸张风格。
- Dark：复古墨黑风格。

两套主题使用相同的颜色语义，例如 `--bg-primary`、`--text-primary`、`--border-default`。

这样组件只需要使用语义化变量，不需要在每个组件中单独判断当前主题。

## 2.1 Light Theme（浅色主题）

[The Atelier Process | How Custom Storybooks Are Created at Atelier Agolée  – Atelier Agolée](https://images.openai.com/static-rsc-4/2vQUJPXyJOhQKaZxXy3Jr6E1EYy47el5ExyC1OHcSLAvC2ZvUoi6ofU91hp_x_U240o-h9KO3ohF80EXj5itHqFfIGY-45oVUDVEZKAF3uIu63Yo_bkCb_Unjku7ABKzYn9aKppV-AHOQXHNPyaWv_JlzTF2Te9qVwCXuVXHze0?purpose=inline)

[atelieragolee.com](https://atelieragolee.com/pages/storybook-creation-process?utm_source=chatgpt.com)

默认推荐主题

浅色主题以暖白、象牙白、墨黑为基础，强调纸张质感和复古气息。

| 颜色名称             | HEX       | 使用场景     |
| ---------------- | --------- | -------- |
| Ink Black        | `#171715` | 主要文字、按钮  |
| Pure Black       | `#000000` | 强调文字     |
| Warm White       | `#F7F5F0` | 页面背景     |
| Ivory            | `#EFECE4` | 卡片、内容区域  |
| Pure White       | `#FFFFFF` | 输入框、玻璃高光 |
| Light Gray       | `#E5E2DA` | 边框、分割线   |
| Medium Gray      | `#92918B` | 次要文字     |
| Dark Gray        | `#41413D` | 辅助文字     |
| Antique Brass    | `#9A8052` | 选中状态、强调  |
| Vintage Burgundy | `#754747` | 特殊标签、提醒  |
| Olive Gray       | `#77735D` | 分类、辅助标记  |

浅色主题的主要视觉效果：

- 页面使用暖白背景，而不是刺眼的纯白。
- 内容区域使用象牙白或白色。
- 文字以墨黑为主。
- 边框使用低对比度灰色。
- 选中状态使用古铜金。
- 玻璃组件使用半透明白色。

## 2.2 Dark Theme（深色主题）

[Dark Academia Decor for Sale: Curated by AURA](https://images.openai.com/static-rsc-4/gVGWOJCCAWmrhoSlNw_6bGcgcqfHNsC68GEbhfovx-VYFUjHO4YX8RQoC-2jIN1ikPFTKEmp5NNq3gHEUKdF3_GLi3WPEwP10EfB_pfIdJEk4aJkM4_EedNyaFl3qAhELYGe2sGdzpMhJI6-ZiYkONp0-r5c6Ih0toQEbGO48xI?purpose=inline)

[auramodernhome.com](https://auramodernhome.com/blogs/the-modern/dark-academia-decor-for-sale?srsltid=AfmBOorvstnLRm5pTOp2LsAgkZfHHS_-OIuPYVCS6YEgsEDG7jG9Kqw9\&utm_source=chatgpt.com)

深色主题

深色主题采用复古墨黑风格，不是简单地将浅色主题的白色替换为黑色。

需要保留复古材质感，同时避免纯黑背景造成视觉压迫。

| 颜色名称             | HEX       | 使用场景     |
| ---------------- | --------- | -------- |
| Deep Black       | `#111110` | 页面主背景    |
| Ink Dark         | `#191917` | 侧边栏、深色面板 |
| Charcoal         | `#242421` | 卡片、内容区域  |
| Soft Charcoal    | `#2D2D29` | 悬浮区域     |
| Dark Gray        | `#41413D` | 辅助背景     |
| Warm White       | `#F1EEE6` | 主要文字     |
| Ivory White      | `#DCD8CE` | 次级文字     |
| Medium Gray      | `#96948B` | 辅助文字     |
| Dark Border      | `#383833` | 边框、分割线   |
| Antique Brass    | `#B49A6B` | 选中状态、强调  |
| Vintage Burgundy | `#A16B6B` | 特殊标签、提醒  |
| Olive Gray       | `#969078` | 分类、辅助标记  |

深色主题的主要视觉效果：

- 页面使用深墨黑背景。
- 卡片使用炭灰色。
- 主要文字使用暖白色。
- 次要文字使用柔和灰色。
- 玻璃组件使用半透明深色。
- 古铜金适当提高亮度，保证可见性。

## 2.3 颜色语义对照

实际开发时，不建议在 Vue 组件中直接写 HEX 颜色。

应该使用统一的 CSS Variables：

| 语义变量               | Light     | Dark      |
| ------------------ | --------- | --------- |
| `--bg-primary`     | `#F7F5F0` | `#111110` |
| `--bg-secondary`   | `#EFECE4` | `#191917` |
| `--bg-card`        | `#FFFFFF` | `#242421` |
| `--bg-elevated`    | `#FFFFFF` | `#2D2D29` |
| `--text-primary`   | `#171715` | `#F1EEE6` |
| `--text-secondary` | `#41413D` | `#DCD8CE` |
| `--text-muted`     | `#92918B` | `#96948B` |
| `--border-default` | `#E5E2DA` | `#383833` |
| `--accent-primary` | `#9A8052` | `#B49A6B` |
| `--accent-danger`  | `#754747` | `#A16B6B` |
| `--accent-olive`   | `#77735D` | `#969078` |

重要： 后续所有页面都必须通过语义变量使用颜色。禁止在业务组件中大量硬编码颜色，否则主题切换时很容易出现遗漏。

# 三、玻璃材质设计

玻璃拟态是 Hello!Note 的重要视觉特征，但需要控制使用范围。

## 3.1 Light Glass（浅色玻璃）

[Minimal light glassmorphism panel with soft neutral spheres on cream background](https://images.openai.com/static-rsc-4/NVY7FT0A1-5JrVvifgoFLO6w95pMCINmZgFtwY9W2sUf_tMU7fCrphajePjmdqqTHdW5laf5wdSpF6moybUBWJQKktRRBOe8d9kW4_42CEpddDZZwX8P2F1DaDALjAITNHbgC87ZqDtVwFFTj3tc-9O1bdoTQAGSv6q1b34QEpLS1YDeEef8EkPBY8vGBBZw?purpose=inline)

建议样式：

```
.glass-light {
  background: rgba(255, 255, 255, 0.62);

  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);

  border: 1px solid rgba(255, 255, 255, 0.72);

  box-shadow:
    0 8px 32px rgba(23, 23, 21, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
}
```

## 3.2 Dark Glass（深色玻璃）

[Horizontal abstract background with a dark, rectangular glass banner on a black gradient background.](https://images.openai.com/static-rsc-4/fpfOzlLLyKFCqoIQd9ChcWDlJESb7r1r58L7CbKedfmCTxMei7vScq-AsOMz3lO9rgcoLZPYQBsIKmScPHDgIol2IKQmG-p30uv1ssSUzWMZALw4-7WHWtywaKE8DkV9Awdy5qLpPDEefAt0oEBQ4S26_Ty7lmNay6Unm5efbXTh52RIt4pts-4ZOL6LSi55?purpose=inline)

建议样式：

```
.glass-dark {
  background: rgba(25, 25, 23, 0.78);

  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);

  border: 1px solid rgba(255, 255, 255, 0.10);

  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.20),
    inset 0 1px 0 rgba(255, 255, 255, 0.06);
}
```

## 3.3 玻璃组件使用范围

| 组件       | 是否使用玻璃 | 说明        |
| -------- | ------ | --------- |
| 顶部导航栏    | 是      | 半透明悬浮效果   |
| 侧边栏      | 可使用    | 轻微透明效果    |
| 搜索框      | 是      | 背景模糊、细边框  |
| 下拉菜单     | 是      | 浮层效果      |
| Modal 弹窗 | 是      | 背景模糊      |
| 悬浮工具栏    | 是      | 突出层次感     |
| 普通卡片     | 适量     | 避免所有卡片都透明 |
| 笔记编辑器    | 不建议    | 优先保证阅读体验  |
| 长文本阅读区域  | 不建议    | 使用稳定的背景色  |

设计重点： 玻璃效果应当让界面更有质感，而不是让页面变得模糊、复杂。

# 四、字体与排版规范

复古风格可以通过衬线字体体现，但不能让整个网站都使用衬线字体。

## 4.1 字体方案

| 使用位置  | 推荐字体           | 说明      |
| ----- | -------------- | ------- |
| 页面标题  | Georgia        | 复古衬线风格  |
| 笔记标题  | Georgia        | 增加编辑感   |
| 中文标题  | Noto Serif SC  | 中文衬线字体  |
| 正文    | Inter          | 清晰易读    |
| 中文正文  | Noto Sans SC   | 中文无衬线字体 |
| 时间、编号 | JetBrains Mono | 等宽字体    |

CSS：

```
:root {
  --font-display:
    "Georgia",
    "Noto Serif SC",
    serif;

  --font-body:
    "Inter",
    "Noto Sans SC",
    sans-serif;

  --font-mono:
    "JetBrains Mono",
    monospace;
}
```

## 4.2 字号规范

| 内容    | 字号      |
| ----- | ------- |
| 页面主标题 | 32–40px |
| 页面副标题 | 20–24px |
| 卡片标题  | 17–20px |
| 笔记正文  | 14–16px |
| 辅助信息  | 12–13px |
| 时间、编号 | 11–12px |

## 4.3 排版原则

- 标题可以使用衬线字体。
- 正文优先使用无衬线字体。
- 正文行高建议为 `1.6–1.8`。
- 不要使用过多粗体。
- 不要为了复古效果降低文字可读性。
- 笔记正文应有足够的宽度和留白。

# 五、基础组件设计规范

所有组件必须同时适配 Light 和 Dark 两种主题。

## 5.1 Button 按钮

Light

Create Note

Cancel

Dark

Create Note

Cancel

按钮分为：

- Primary：主要操作，Light 使用黑底白字，Dark 使用暖白底深色字。
- Secondary：次要操作，使用透明或卡片背景。
- Ghost：纯文字或图标按钮。
- Danger：删除等危险操作，使用低饱和红色。

## 5.2 Card 卡片

My Notes

Updated just now

A quiet place for ideas and thoughts.

My Notes

Updated just now

A quiet place for ideas and thoughts.

卡片规范：

- 圆角建议 `12–16px`。
- 使用低对比度边框。
- 阴影不宜过重。
- Hover 时轻微上移 `2px`。
- 内容区域保持清晰，不要过度透明。

## 5.3 Input 输入框

- Light：暖白背景、浅灰边框、墨黑文字。
- Dark：炭灰背景、深灰边框、暖白文字。
- Focus：古铜金描边。
- Placeholder：使用次要文字颜色。
- Disabled：降低透明度，并明确表现不可操作状态。

## 5.4 Tag 标签

- 普通标签：灰色背景。
- 选中标签：古铜金强调。
- 特殊标签：少量使用酒红色或橄榄灰。
- Dark 模式下适当提高标签文字亮度。

## 5.5 Modal / Dropdown / Tooltip

这些浮层组件应统一采用：

- 半透明背景。
- 适当的 `backdrop-filter`。
- 细边框。
- 柔和阴影。
- 与当前主题匹配的文字和背景。
- 明确的关闭、悬停、选中状态。

# 六、Light / Dark 主题切换系统

核心功能

主题切换不是简单地替换页面背景，而是整个应用的主题状态切换。

需要保证：

- 所有页面同步切换。
- 所有组件同步切换。
- 所有浮层同步切换。
- 输入框、滚动条、编辑器等原生元素正确适配。
- 用户刷新页面后仍保留选择。
- 第一次访问时可以根据系统主题自动选择。

## 6.1 主题切换模式

建议支持三种模式：

| 模式     | 说明       |
| ------ | -------- |
| Light  | 始终使用浅色主题 |
| Dark   | 始终使用深色主题 |
| System | 跟随操作系统主题 |

默认使用 `System`，用户主动选择后保存自己的偏好。

注意区分：

- `themeMode`：用户选择的模式，值为 `light`、`dark`、`system`。
- `resolvedTheme`：最终实际使用的主题，值为 `light` 或 `dark`。

例如：

用户选择 `system`，操作系统是深色模式，那么：

```
themeMode = system
resolvedTheme = dark
```

## 6.2 主题切换按钮设计

建议在顶部导航栏右侧放置主题切换入口。

Light Theme

Appearance

Warm paper and soft shadows

Dark Theme

Appearance

Deep ink and subtle reflections

建议点击后弹出三个选项：

- &#x20;Light
- &#x20;Dark
- &#x20;System

也可以在设置页面提供完整的主题设置。

## 6.3 主题切换实现方式

前端使用 Vue 3 + TypeScript + Pinia。

建议结构：

```
src/
├── app/
│   └── providers/
├── stores/
│   └── theme.store.ts
├── composables/
│   └── useTheme.ts
└── assets/
    └── styles/
        ├── index.css
        ├── variables.css
        └── themes.css
```

主题状态由 Pinia 管理，CSS Variables 负责控制实际颜色。

建议在 `theme.store.ts` 中管理：

```
type ThemeMode = "light" | "dark" | "system";

interface ThemeState {
  mode: ThemeMode;
  resolvedTheme: "light" | "dark";
}
```

主题切换时，统一设置根元素：

```
<html data-theme="light">
```

或：

```
<html data-theme="dark">
```

CSS 根据 `data-theme` 自动应用不同颜色。

### 主题持久化

建议使用 `localStorage` 保存：

```
hellonote-theme = system
```

刷新页面后读取用户设置。

首次访问时：

1. 先读取 LocalStorage。
2. 如果没有保存记录，使用系统主题。
3. 监听系统主题变化。
4. 当用户明确选择 Light 或 Dark 后，不再自动跟随系统。
5. 用户切换回 System 后，重新跟随系统。

为了避免页面刷新时短暂闪烁，应在应用首次渲染之前读取主题并设置 `data-theme`，而不是等 Vue 页面加载完成后才切换。

另外，设置：

```
color-scheme: light;
```

或：

```
color-scheme: dark;
```

让浏览器原生控件、表单控件等尽可能匹配当前主题。

# 七、页面级主题适配规范

这一部分非常重要。

不能只做到按钮和卡片切换颜色，还必须确保整个页面结构在两种主题下都保持协调。

## 7.1 整体布局

建议使用以下结构：

Hello!Note

Navigation

Notes

Tags

Favorites

My Notes

Your personal knowledge space.

A new note

Start writing your thoughts...

Hello!Note

Navigation

Notes

Tags

Favorites

My Notes

Your personal knowledge space.

A new note

Start writing your thoughts...

整体布局在两种主题下保持一致，变化集中在背景、文字、边框、阴影和材质。

整体页面划分为：

1. 顶部导航栏。
2. 左侧侧边栏。
3. 主内容区域。
4. 可选右侧辅助区域。
5. 弹窗、下拉菜单等浮层。

## 7.2 登录与注册页面

Light：

- 暖白背景。
- 白色登录卡片。
- 墨黑主按钮。
- 古铜金聚焦边框。

Dark：

- 深墨黑背景。
- 炭灰登录卡片。
- 暖白主按钮。
- 柔和古铜金强调。

登录页面可以适当使用玻璃卡片，但表单内容必须清晰。

## 7.3 笔记列表页面

Light：

- 暖白页面背景。
- 白色笔记卡片。
- 墨黑标题。
- 灰色时间和摘要。

Dark：

- 深色页面背景。
- 炭灰笔记卡片。
- 暖白标题。
- 柔和灰色摘要。

列表卡片的选中、Hover、收藏状态必须在两种主题下有明确表现。

## 7.4 笔记详情与编辑页面

这两个页面是 Hello!Note 最重要的页面之一。

需要特别注意：

- 正文背景必须稳定。
- 正文文字和背景之间必须有足够对比度。
- 编辑器工具栏可以采用玻璃效果。
- 编辑区域不建议采用透明玻璃。
- 代码块、引用块、表格、链接、图片等内容都需要适配主题。
- Markdown 编辑器和预览区域都必须适配主题。

特别是 Dark 模式，不要直接使用纯黑背景搭配灰色正文，容易造成阅读疲劳。

## 7.5 搜索页面

- 搜索框需要适配两种主题。
- 搜索结果关键词使用古铜金或适合当前主题的强调色。
- 搜索结果卡片保持统一。
- 搜索历史、空状态、加载状态也需要切换主题。

## 7.6 AI 页面

后续增加 AI 功能时：

- AI 对话气泡需要区分用户和 AI。
- AI 工具栏可以使用玻璃质感。
- 代码块、Markdown 内容和引用内容需要适配主题。
- 加载动画使用低饱和度颜色。
- 不要默认采用紫色、蓝色霓虹渐变等常见 AI 产品风格。

# 八、响应式布局规范

主题适配不仅包括颜色，也包括不同屏幕下的页面布局。

| 设备           | 页面适配要求           |
| ------------ | ---------------- |
| Desktop      | 完整侧边栏、顶部导航、主内容区域 |
| Tablet       | 侧边栏收窄，主内容区域自适应   |
| Mobile       | 侧边栏改为抽屉或底部导航     |
| Small Mobile | 减少装饰，保证阅读和编辑     |

建议断点：

| 设备            | 宽度             |
| ------------- | -------------- |
| Mobile        | `< 640px`      |
| Tablet        | `640px–1023px` |
| Desktop       | `≥ 1024px`     |
| Large Desktop | `≥ 1440px`     |

具体要求：

1. 页面不能出现横向溢出。
2. 笔记正文需要根据屏幕宽度调整。
3. 导航栏按钮在手机端需要适当缩小。
4. 侧边栏在手机端不能一直占据内容空间。
5. 弹窗在移动端应尽量使用适合屏幕的宽度。
6. 主题切换入口在移动端也必须可访问。

# 九、设计细节与交互规范

## 9.1 圆角

| 类型     | 建议值  |
| ------ | ---- |
| 小按钮    | 8px  |
| 普通按钮   | 10px |
| 输入框    | 10px |
| 卡片     | 14px |
| 大卡片    | 18px |
| 弹窗     | 18px |
| 圆形图标按钮 | 50%  |

## 9.2 阴影

Light：

```
--shadow-card:
  0 4px 16px rgba(23, 23, 21, 0.05);

--shadow-floating:
  0 12px 32px rgba(23, 23, 21, 0.10);
```

Dark：

```
--shadow-card:
  0 4px 16px rgba(0, 0, 0, 0.16);

--shadow-floating:
  0 12px 32px rgba(0, 0, 0, 0.30);
```

## 9.3 动画

建议使用：

- Hover：150–200ms。
- 页面切换：200–300ms。
- 弹窗：200ms。
- 主题切换：200–250ms。

主题切换时可以对背景、文字、边框和阴影进行轻微过渡。

```
* {
  transition:
    background-color 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}
```

但不建议对所有元素无差别添加全局过渡，尤其是大型编辑器、图片、复杂动画和滚动区域。应当将过渡限制在需要切换主题的界面元素上。

同时尊重系统的 `prefers-reduced-motion` 设置。

# 十、CSS Variables 实施规范

建议将主题变量集中管理，避免后期维护困难。

推荐文件结构：

```
src/
└── assets/
    └── styles/
        ├── index.css
        ├── variables.css
        ├── themes.css
        ├── glass.css
        ├── typography.css
        └── utilities.css
```

## 10.1 variables.css

定义通用尺寸、字体、圆角、动画等不随主题变化的变量：

```
:root {
  /* Typography */
  --font-display: "Georgia", "Noto Serif SC", serif;
  --font-body: "Inter", "Noto Sans SC", sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Radius */
  --radius-sm: 8px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 18px;
  --radius-full: 9999px;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;

  /* Animation */
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
}
```

## 10.2 themes.css

```
/* Light Theme */
:root,
:root[data-theme="light"] {
  color-scheme: light;

  --bg-primary: #F7F5F0;
  --bg-secondary: #EFECE4;
  --bg-card: #FFFFFF;
  --bg-elevated: #FFFFFF;

  --text-primary: #171715;
  --text-secondary: #41413D;
  --text-muted: #92918B;

  --border-default: #E5E2DA;

  --accent-primary: #9A8052;
  --accent-danger: #754747;
  --accent-olive: #77735D;

  --glass-bg: rgba(255, 255, 255, 0.62);
  --glass-border: rgba(255, 255, 255, 0.72);

  --shadow-card:
    0 4px 16px rgba(23, 23, 21, 0.05);

  --shadow-floating:
    0 12px 32px rgba(23, 23, 21, 0.10);
}

/* Dark Theme */
:root[data-theme="dark"] {
  color-scheme: dark;

  --bg-primary: #111110;
  --bg-secondary: #191917;
  --bg-card: #242421;
  --bg-elevated: #2D2D29;

  --text-primary: #F1EEE6;
  --text-secondary: #DCD8CE;
  --text-muted: #96948B;

  --border-default: #383833;

  --accent-primary: #B49A6B;
  --accent-danger: #A16B6B;
  --accent-olive: #969078;

  --glass-bg: rgba(25, 25, 23, 0.78);
  --glass-border: rgba(255, 255, 255, 0.10);

  --shadow-card:
    0 4px 16px rgba(0, 0, 0, 0.16);

  --shadow-floating:
    0 12px 32px rgba(0, 0, 0, 0.30);
}
```

## 10.3 glass.css

```
.glass-panel {
  background: var(--glass-bg);

  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);

  border: 1px solid var(--glass-border);

  box-shadow: var(--shadow-card);
}
```

## 10.4 index.css

```
@import "./variables.css";
@import "./themes.css";
@import "./glass.css";
@import "./typography.css";
@import "./utilities.css";

body {
  margin: 0;

  font-family: var(--font-body);

  background: var(--bg-primary);
  color: var(--text-primary);
}
```

# 十一、Tailwind CSS 3 配置规范

项目使用 Tailwind CSS 3。

建议将主题颜色映射到 CSS Variables，而不是在 Tailwind 配置中重复维护 Light 和 Dark 两套颜色。

`tailwind.config.js`：

```
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["selector", '[data-theme="dark"]'],

  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],

  theme: {
    extend: {
      colors: {
        page: "var(--bg-primary)",
        surface: "var(--bg-secondary)",
        card: "var(--bg-card)",
        elevated: "var(--bg-elevated)",

        text: {
          primary: "var(--text-primary)",
          secondary: "var(--text-secondary)",
          muted: "var(--text-muted)",
        },

        border: {
          DEFAULT: "var(--border-default)",
        },

        accent: {
          DEFAULT: "var(--accent-primary)",
          danger: "var(--accent-danger)",
          olive: "var(--accent-olive)",
        },
      },

      borderRadius: {
        retro: "14px",
        panel: "18px",
      },

      backdropBlur: {
        glass: "18px",
      },

      boxShadow: {
        retro: "var(--shadow-card)",
        floating: "var(--shadow-floating)",
      },
    },
  },

  plugins: [],
};
```

使用示例：

```
<div class="bg-page text-text-primary">
  <div class="bg-card border border-border rounded-retro shadow-retro">
    Hello!Note
  </div>
</div>
```

由于颜色来自 CSS Variables，切换 `data-theme` 后页面会自动更新。

# 十二、前端开发实施顺序

建议不要一开始就开发所有业务页面，而是先把主题系统和基础组件建立起来。

| 阶段 | 开发内容          | 目标                        |
| -- | ------------- | ------------------------- |
| 1  | CSS Variables | 建立统一配色体系                  |
| 2  | Light / Dark  | 完成主题状态管理和持久化              |
| 3  | 基础组件          | Button、Input、Card、Tag     |
| 4  | 玻璃组件          | GlassPanel、Modal、Dropdown |
| 5  | 全局布局          | Header、Sidebar、Main       |
| 6  | 登录注册          | 完成认证页面                    |
| 7  | 笔记列表          | 完成核心列表页面                  |
| 8  | 笔记编辑          | 完成核心编辑页面                  |
| 9  | 搜索与分类         | 完成辅助业务页面                  |
| 10 | 细节优化          | 响应式、动效、无障碍和视觉统一           |

建议先开发一个主题展示页面，集中展示：

- Light / Dark 两种主题。
- 所有基础颜色。
- 所有按钮状态。
- 卡片。
- 输入框。
- 标签。
- 弹窗。
- 玻璃组件。
- 主题切换入口。

这样后续开发新页面时，可以直接复用已有组件，不必反复调整视觉风格。

# 十三、项目主题开发约束（AI Rules 建议）

以下内容建议作为前端项目的设计约束，后续可以整理成适合当前 AI 编程工具的项目级 Rules。

Hello!Note Frontend Design Rules

1. 整体采用 Retro Glassmorphism 设计风格。
2. 黑色、白色、灰色是基础颜色。
3. 支持 Light、Dark、System 三种主题模式。
4. 所有页面、组件、弹窗和原生控件必须适配主题。
5. 禁止在业务组件中随意硬编码主题颜色。
6. 所有主题颜色必须优先使用 CSS Variables。
7. 玻璃效果只用于合适的浮层和界面组件。
8. 笔记正文和编辑器必须保证阅读清晰度。
9. Light 和 Dark 两种主题必须保持一致的布局与交互。
10. 用户主题选择必须持久化。
11. 首次访问默认跟随系统主题。
12. 主题切换不能造成页面闪烁。
13. 所有新组件开发时必须检查 Light 和 Dark 两种主题。
14. 所有页面必须适配桌面、平板和移动端。
15. 不使用高饱和度霓虹色和大面积科技风渐变。
16. 优先考虑可读性、可访问性和实际使用体验。

## 主题验收清单

开发完成后，可以逐项检查：

主题系统验收

0/14 已完成

首次访问时能正确识别系统主题

可以手动切换 Light 和 Dark

可以切换回 System 模式

刷新页面后保留主题选择

主题切换时没有明显闪屏

顶部导航和侧边栏适配两种主题

按钮、输入框、卡片和标签适配两种主题

Modal、Dropdown、Tooltip 适配两种主题

笔记编辑器和 Markdown 预览适配两种主题

搜索、空状态、加载状态适配两种主题

原生表单控件和滚动条适配两种主题

桌面、平板和移动端布局正常

文字和背景有足够对比度

减少动态效果设置能够正常生效

重置检查

# 十四、最终设计总结

Hello!Note 的视觉设计可以归纳为：

# HELLO!NOTE

A QUIET SPACE FOR YOUR THOUGHTS.

Light

Warm Paper

Soft and calm.

Dark

Deep Ink

Quiet and focused.

Retro · Minimal · Glass · Dual Theme

| 设计维度 | 最终方向                  |
| ---- | --------------------- |
| 整体风格 | Retro Glassmorphism   |
| 基础颜色 | 黑、白、灰                 |
| 浅色主题 | 暖白、象牙白、墨黑             |
| 深色主题 | 墨黑、炭灰、暖白              |
| 强调颜色 | 古铜金、酒红、橄榄灰            |
| 材质   | 半透明玻璃、柔和阴影            |
| 字体   | 衬线标题 + 无衬线正文          |
| 主题模式 | Light / Dark / System |
| 主题保存 | LocalStorage          |
| 页面适配 | 桌面、平板、移动端             |
| 核心要求 | 统一、清晰、易读、易维护          |

我的建议： Hello!Note 不要做成一个单纯追求视觉效果的玻璃拟态网站，而应该做成一个具有复古气质、现代交互体验，并且真正适合长期记录和阅读的笔记应用。
