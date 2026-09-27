---
name: anime-wallpaper-prompt-design
description: >
  动漫角色立绘壁纸 Prompt 设计技能。当用户要为桌面、手机或锁屏设计动漫风格角色壁纸/立绘，
  或需要为 NovelAI、SDXL/ComfyUI、FLUX、GPT Image、Midjourney Niji 等模型撰写、优化、
  调试角色插画 Prompt 时使用。不维护单一万能 Prompt，而是把任务拆成用途、分辨率、取景、
  构图位置、姿态、服装、美术语言、光线色盘、背景景深、镜头、约束、模型参数等独立可调变量，
  再针对目标模型编译成自然语言 Prompt、Danbooru 风格标签、或 Midjourney 参数。涵盖壁纸
  安全区（桌面图标区/手机锁屏时钟区）、full body 不被裁脚裁头的写法、多角色属性串色的
  规避、CFG/steps/guidance/seed 等参数的模型专属含义、常见失败模式与修正、以及原创角色
  与版权/许可的注意事项。参考 references/ 目录获取分辨率表、模型参数对照表、Prompt 模板、
  14 个可直接复用的完整案例，以及失败模式修正清单。
---

# 动漫角色立绘壁纸 Prompt 设计

把"立绘壁纸"当作一个有独立变量的工程任务，而不是往 Prompt 里堆形容词。核心认知：立绘构图（人物居中完整展示）和壁纸构图（要给图标、时钟、通知区留白）不是一回事；不同模型（NovelAI / SDXL+ComfyUI / FLUX / GPT Image / Midjourney Niji）暴露的参数完全不同，不能把一套参数机械复制到所有模型上。

## 何时使用本技能

用户想要生成/优化动漫角色壁纸、立绘、角色卡插画的 Prompt，或者想知道某个模型（NovelAI、SDXL、FLUX、GPT Image、Midjourney）该怎么调参数、怎么避免裁脚/串色/画风冲突等问题。

## 核心工作流

```
定义最终用途(桌面/手机/锁屏) → 锁定比例与安全区 → 定义角色身份与核心服装
  → 低成本构图探索(先低 steps/低成本档位, 多个 seed)
  → 构图是否正确？否 → 只改取景/姿势/位置，重新探索
  → 是 → 记录 Prompt+Seed+参数，一次只改一个视觉变量
  → 角色一致性是否足够？否 → 用角色参考/LoRA/Precise Reference
  → 是 → 检查脸/眼/手/脚 → 局部 inpaint/edit → upscale
  → 裁切至最终壁纸尺寸 → 抗锯齿/轻度锐化/色彩 QA
  → 检查 logo/水印/IP/授权 → 最终导出
```

**调参顺序（先构图，后细节，永远不要反过来）**：比例 → 人物数量 → 人物位置 → 全身/半身取景 → 姿势 → 脸和服装身份 → 光线/色盘 → 背景 → 细节 → 局部修复 → Upscale。

**Prompt A/B 测试原则**：固定 seed，一次只改一个变量（如光线），跑几组对比，确认方向后再用 8–16 个随机 seed 验证是否普适。不要同时改 sampler + CFG + 背景 + 服装 + 光线 + seed 后凭感觉判断哪个更好。

## 先问清楚这几件事（决定后续所有变量）

1. **最终用途**：桌面 / 手机主屏 / 手机锁屏，决定比例与安全区方向。
2. **目标模型**：NovelAI / SDXL+ComfyUI / FLUX / GPT Image / Midjourney Niji —— 决定输出是自然语言段落、Danbooru 标签、还是带 `--ar --seed --stylize --no` 的 Midjourney 格式，也决定是否存在 sampler/CFG/steps 这些参数。
3. **取景范围**：不要只写 `portrait` 或 `full body`，要写清人体边界（见 `references/output-specs-and-composition.md`）。
4. **人物位置与负空间**：壁纸必须给图标区/时钟区留白，不是居中放大就好。
5. **人物数量**：单人还是多人 —— 多人任务要用"整体场景 Prompt + 每人独立 Character Prompt"结构，避免属性串色（头发/眼睛/服装颜色互相泄漏）。

## 通用抽象规格（先填这个，再编译成具体模型的 Prompt）

用一份结构化规格描述角色壁纸，字段包括：`task`(用途/分辨率/比例)、`subject`(身份/发色/瞳色/表情)、`framing`(取景/位置/人体边界/负空间)、`pose`(动作/视线/手部)、`wardrobe`(服装/材质/配饰)、`visual`(美术风格/线稿/渲染/细节度)、`lighting`(主光/轮廓光/色盘/情绪)、`background`(类型/描述/景深)、`camera`(机位/镜头感/景深)、`constraints`(必须保留的身份特征/禁止出现的内容)。完整 YAML 示例见 `references/prompt-templates.md`。

再根据目标模型"编译"成对应格式：
- **GPT Image / FLUX** → 分段自然语言 Prompt
- **NovelAI** → Danbooru 风格标签 + Base Prompt + 独立 Character Prompt + Undesired Content(UC)
- **SDXL / ComfyUI** → Positive / Negative + sampler/scheduler/CFG/steps/seed
- **Midjourney** → 自然语言主体 + `--ar --seed --stylize --no`

不要给不支持这些参数的服务（GPT Image、Midjourney）编造 sampler/CFG/steps；这些模型端参数不对用户暴露。

## 关键写法要点（最容易出错的地方）

- **全身不被裁脚**：写 `full body visible from head to toe, both feet fully inside frame`，并且**不要**同时出现 `close-up`、`portrait` 这类会与全身冲突的取景词。
- **壁纸负空间**：桌面写 `character positioned on the right/left third, generous clean negative space on the opposite side for desktop icons`；锁屏写 `generous clean space above the character's head for lock-screen clock, face placed below the upper UI area`。
- **多人不串色**：场景/整体一个 Base Prompt，每个角色单独一段 Character Prompt（NovelAI 原生支持），不要把所有人的发色、瞳色、服装颜色混写在同一段里。
- **颜色不失控**：不要同时叠 `neon/vibrant/glowing/HDR/colorful/strong contrast`，改为明确"主色 + 辅色 + 点缀色分别出现在哪里"。
- **"8K/4K/UHD"不是分辨率设置**：这些词只是细节程度的暗示，真正的输出尺寸由 width/height 参数或后期 upscale 决定。
- **CFG/Guidance/Steps 不是越高越好**：过高的 guidance 容易过饱和/僵硬，过多 steps 收益递减甚至变差；先解决 Prompt 本身的冲突，而不是暴力拉参数。
- **画师名字不是必要成分**：与其写"in the style of [在世插画师]"，用可观察的视觉属性描述（线条粗细、上色方式、色盘、轮廓光）更可控也更原创，见 `references/legal-and-qa.md`。

## 参考文件（按需加载，不要一次性全读）

- `references/output-specs-and-composition.md` — 壁纸分辨率/比例表、取景类型对照表（不要只写 portrait）、桌面/锁屏安全区示意、完整"视觉变量矩阵"（美术风格/渲染媒介/线稿/光线/色盘/机位/镜头/姿势/服装/配件/背景/景深/细节等级/纹理）。
- `references/model-comparison-and-params.md` — 各模型强项与适合任务对照表、参数含义表（steps/CFG/sampler/scheduler/seed/resolution/negative）、各模型推荐参数起点（NovelAI guidance 5–6、FLUX.2 dev 28 steps guidance 4、SDXL CFG 6–8 等，均标注为工程起点而非官方最优值）、seed 的正确用法、放大/修脸/抗锯齿的生产顺序。
- `references/prompt-templates.md` — 结构化 YAML 规格模板、自然语言模板（GPT Image/FLUX/Midjourney 通用）、Danbooru 标签模板（NovelAI）、通用 Negative Prompt 模板（含全身图、多人图专项补充）、可直接复用的"Prompt Builder 上层 Skill 指令"文本。
- `references/example-library.md` — 14 个完整可复用案例（A–N），覆盖手机全身日系赛璐璐、桌面半写实 cyberpunk、水彩和服锁屏、chibi、哥特肖像、4K 奇幻骑士场景、咖啡馆近景、streetwear 动态全身、超宽机甲、双人/四人群像、3D 渲染风、极简抽象、黑白墨线红点色，每个案例含 Prompt、Negative、推荐模型与参数设置、设计理由。
- `references/failure-modes.md` — 常见失败模式与修正（裁脚裁头、壁纸不好用、CFG/Steps 迷思、群像撞脸、Negative Prompt 堆砌、色彩炸掉、半写实变真人、水彩变油画、修脸换脸、参考图强度过高）。
- `references/legal-and-qa.md` — 原创角色与版权/许可注意事项（知名角色/在世画师风格/真人参考/AI 生成版权归属的现状与限制）、模型许可证核对、最终验收 QA 清单表。

## 输出时的原则

按用户实际需求调整深度——只要一条 Prompt 就给一条完整可用的 Prompt（含 Negative 与推荐参数）；要构建体系就给 YAML 规格 + 多模型编译结果。每次只建议修改 1–2 个主要变量；给出最终 Prompt 前自检：是否会裁脚/裁头、人数是否明确、角色属性是否可能串色、背景是否过度复杂、是否与 UI 安全区冲突、是否有文字/logo/水印风险。
