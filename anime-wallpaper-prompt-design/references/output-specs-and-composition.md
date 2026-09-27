# 输出规格、取景与视觉变量矩阵

## 壁纸输出规格

下面的分辨率应视为最终交付画布，不代表模型必须原生按该尺寸生成（很多情况下应先按同比例较低分辨率生成，再 upscale/裁切）。

| 用途 | 常用最终尺寸 | 比例 | 最适合的构图 |
|---|---|---|---|
| FHD 桌面 | 1920×1080 | 16:9 | 半身、全身偏侧、完整场景 |
| QHD 桌面 | 2560×1440 | 16:9 | 高细节立绘、场景型 |
| UHD/4K 桌面 | 3840×2160 | 16:9 | 高细节场景、群像 |
| 超宽屏 | 3440×1440 | ≈2.39:1 | 角色放左右三分之一，大片负空间 |
| 经典竖屏 | 1080×1920 | 9:16 | 全身、膝上、人物海报 |
| 高分辨率竖屏 | 1440×2560 | 9:16 | 细节型角色立绘 |
| 长屏手机 | 1080×2400 | 9:20 | 上方留时钟区，全身 |
| 高分辨率长屏 | 1440×3200 | 9:20 | 手机主屏/锁屏成套 |

**比例 ≠ 像素尺寸**：例如 Midjourney 的 `--ar 16:9` 只指定比例，不等于指定 3840×2160；比例与最终输出像素是两件独立的事。

**GPT Image 尺寸约束（截至撰写时）**：宽高需为 16 的倍数、比例介于 1:3 至 3:1、单边不超过 3840、总像素不超过约 8,294,400。3840×2160 满足约束；1920×1080 中的 1080 不是 16 的倍数，API 工作流更适合先生成 1920×1088 再裁成 1920×1080。官方推荐标准尺寸包括 1024×1024、1536×1024、1024×1536。高于约 2560×1440 的尺寸目前仍可能标注为 experimental，最终高分辨率交付前应做人工 QA。

## 取景类型（不要只写 portrait / full body）

| 类型 | 推荐描述 | 主要风险 |
|---|---|---|
| 面部特写 | extreme close-up, face filling most of frame | 发型、配饰被切掉 |
| 头像/肩像 | head and shoulders portrait | 容易过于证件照 |
| 胸像 | bust portrait, upper body visible | 双手容易出现在边缘 |
| 腰上 | waist-up portrait | 手部错误 |
| Cowboy shot | thigh-up / cowboy shot | 与全身混淆 |
| 膝上 | knees-up composition | 鞋子自然消失 |
| 全身 | full body visible from head to toe, both feet fully inside frame | 脚被裁切 |
| 全场景 | character occupies about one-third of frame, environment clearly visible | 人物脸部细节下降 |

明确身体边界（"feet included"这类具体描述）比泛泛写 "full body" 更可靠，尤其不要让 `full body` 与 `close-up`/`portrait` 同时出现在一个 Prompt 里——这是最常见的裁脚/裁头原因。

## 壁纸安全区（设计经验，作为工作流默认值，不是硬性标准）

**桌面 16:9**：人物放右侧三分之一，左侧 25–35% 留白给图标；避免背景元素、光源粒子侵入留白区。写法示例：

```
full-body character positioned on the right third of the frame,
generous clean negative space on the left for desktop icons,
unobstructed background, feet fully visible
```

**手机锁屏 9:16**：顶部预留时钟/状态栏空间，人脸尽量不要顶到最上方；底部预留快捷方式区。写法示例：

```
generous clean space above the character's head for lock-screen clock,
face placed below the upper UI area
```

## 视觉变量矩阵

一张立绘至少应能独立控制以下变量；关键不是"全部打开"，而是选择互相支持、不冲突的组合（例如"粗黑赛璐璐线条"与"柔焦水彩超写实毛孔"就是互相冲突的视觉语言）：

| 变量 | 可选值示例 | 对结果最直接的影响 |
|---|---|---|
| 美术风格 | anime / semi-realistic / chibi / cel-shaded | 人体比例、材质、线条 |
| 渲染媒介 | digital painting / watercolor / gouache / 3D render | 纹理、边缘、光影 |
| 线稿 | clean thin lineart / thick graphic outline / sketchy ink | 二次元感 |
| 光线 | soft daylight / rim light / neon / moonlight / volumetric | 戏剧性 |
| 色盘 | pastel / monochrome / complementary / muted / neon | 情绪和辨识度 |
| 情绪 | serene / melancholic / heroic / mysterious / playful | 表情、动作、光线 |
| 机位 | eye-level / low-angle / high-angle / Dutch angle | 人物气场 |
| 镜头 | close-up / medium / full-body / wide establishing shot | 信息密度 |
| 姿势 | contrapposto / walking / combat / seated / floating | 动态性 |
| 服装 | school uniform / streetwear / armor / kimono / techwear | 世界观 |
| 配件 | sword / headphones / ribbons / jewelry / halo | 角色识别 |
| 背景 | abstract / environment / gradient / bokeh / architecture | 壁纸复杂度 |
| 景深 | deep focus / shallow DOF / foreground blur | 层次感 |
| 细节等级 | clean/simple / detailed / ultra-detailed | 视觉噪声 |
| 表面纹理 | paper grain / silk / brushed metal / rain droplets | 材质可信度 |
