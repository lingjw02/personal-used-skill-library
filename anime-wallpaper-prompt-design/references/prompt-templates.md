# Prompt 模板

## 结构化角色壁纸规格（先填这个，再"编译"成具体模型 Prompt）

```yaml
task:
  use: "{desktop wallpaper | mobile lockscreen | character sheet}"
  final_resolution: "{3840x2160}"
  aspect_ratio: "{16:9}"

subject:
  count: "{1}"
  identity: "{original female mage}"
  age_presentation: "{adult}"
  hair: "{long silver hair}"
  eyes: "{violet}"
  expression: "{calm, slightly melancholic}"

framing:
  shot: "{full body}"
  position: "{right third}"
  body_constraints: "{head-to-toe visible, both feet inside frame}"
  negative_space: "{left 35 percent}"

pose:
  action: "{standing naturally, slight contrapposto}"
  gaze: "{looking toward viewer}"
  hands: "{one hand holding a staff, other relaxed}"

wardrobe:
  clothing: "{layered dark fantasy robe}"
  materials: "{velvet, silver embroidery}"
  accessories: "{moon pendant, staff}"

visual:
  style: "{high-end anime illustration}"
  linework: "{clean fine lineart}"
  rendering: "{cel shading + soft digital painting}"
  detail: "{high}"
  texture: "{subtle fabric texture}"

lighting:
  key: "{cool moonlight}"
  rim: "{soft silver rim light}"
  palette: "{navy, violet, silver}"
  mood: "{quiet, mysterious}"

background:
  type: "{environment}"
  description: "{ruined moonlit observatory}"
  depth: "{atmospheric perspective, subtle bokeh}"

camera:
  angle: "{slightly low angle}"
  lens_cue: "{50mm-like perspective}"
  depth_of_field: "{moderate}"

constraints:
  preserve: "{face identity, outfit motifs}"
  exclude: "{text, watermark, logo}"
```

编译方向：
```
Skill specification
  ├── GPT Image / FLUX      → 自然语言分段 Prompt
  ├── NovelAI                → Danbooru-like tags + Character Prompts + UC
  ├── SDXL / ComfyUI         → Positive / Negative + sampler/CFG/seed
  └── Midjourney             → Natural-language prompt + --ar --seed --stylize --no
```

## 自然语言型模板（GPT Image / FLUX，也可作 Midjourney 主体文本）

```
用途：
为 {desktop/mobile} 制作一张 {aspect_ratio} 的动漫角色壁纸。

主体：
{character_count} 名 {character_description}。
{hair}, {eyes}, {facial_features}, {expression}。

构图：
{shot_type}，{body_visibility}。
人物位于画面的 {left/right/center}，
在 {opposite_area} 保留约 {negative_space}% 简洁负空间。
{camera_angle}，{camera_distance}。
{pose}，{gaze_direction}。

服装与配件：
{clothing}，材质为 {materials}，配有 {accessories}。

视觉语言：
{anime/semi-realistic/chibi/cel-shaded}，
{linework}，
{digital painting/watercolor/3D render}，
{detail_level}。
避免视觉语言互相冲突。

光线与颜色：
{lighting_setup}，主色为 {palette}，整体情绪 {mood}。

背景：
{abstract/environment/bokeh/minimal}，{background_description}，
{depth_of_field}，主体与背景有明确层次分离。

硬性约束：
{feet/hands/face constraints}。
不要文字、logo、水印。
{wallpaper safe-zone requirement}。
```

## Anime 标签型模板（NovelAI 等标签导向模型）

```
1girl,
adult,
{hair color}, {hair style},
{eye color},
{expression},

full body, standing,
feet visible,
{pose},
looking at viewer,

{outfit tags},
{accessory tags},

{camera angle},
{background tags},
{lighting tags},
{palette tags},

anime,
{cel shading / watercolor / detailed digital painting},
{lineart tags},
{texture tags},

best quality,
masterpiece,
{medium/high/ultra complexity}
```

角色数量、人物/作品相关标签建议优先出现；标签顺序和模型版本会影响权重，不需要把几百个标签无序堆在一起。

## 通用 Negative Prompt 模板（按需局部选用，不建议全部无脑复制）

```
lowres, blurry, out of focus,
bad anatomy, bad hands,
extra fingers, missing fingers, fused fingers,
extra limbs, duplicated limbs,
deformed face, malformed eyes,
asymmetrical eyes, cross-eyed,
cropped feet, feet out of frame,
cut off legs, cropped head,
duplicate character, multiple views,
text, caption, speech bubble,
logo, watermark, signature,
jpeg artifacts, chromatic aberration
```

全身图重点加入：`cropped, close-up, feet out of frame, cut off legs`
多人图重点加入：`merged bodies, fused arms, duplicate faces, same face, overlapping limbs, attribute leakage`

把 Negative Prompt 当作"故障日志"来维护——出现什么问题就针对性加什么词，而不是预先加载几百个互不相关的词。

## 多人角色的 Base + Character 结构（避免串色）

```
Base Prompt:
2girls, full body, side-by-side, standing on a rooftop, sunset city, wind,
cinematic composition, anime illustration, clean lineart, cel shading,
orange and blue complementary palette, best quality, high complexity

Character A:
girl, left side, long black hair, blue eyes, calm expression,
navy long coat, black boots, holding closed umbrella

Character B:
girl, right side, short white hair, amber eyes, energetic smile,
orange cropped jacket, dark cargo pants, headphones around neck

Negative / UC:
merged bodies, fused arms, same face, hair color leakage,
clothing color leakage, extra person, cropped feet, text, watermark
```

## 可直接复用的 Prompt Builder 上层 Skill 指令

把下面这段当作让其他 LLM 帮忙生成壁纸 Prompt 时的系统级指令：

```
你是 Anime Character Wallpaper Prompt Designer。

任务：根据输入的角色设定与目标设备，生成适配指定图像模型的专业提示词。

优先级：
1. 构图正确  2. 角色身份一致  3. 人体完整性
4. 壁纸 UI 安全区  5. 光色统一  6. 风格统一  7. 微细节

必须先确定：最终用途 / 横屏竖屏 / 最终比例 / 人物数量 /
close-up|portrait|waist-up|knees-up|full-body|full-scene / 人物画面位置 / 需要保留的负空间

对 full-body：明确写出 head-to-toe visible, both feet fully inside frame,
camera far enough to include entire body。

对手机锁屏：在人物头顶保留干净负空间，不要把眼睛放在时钟区域。
对桌面：根据用户指定的图标区域，在对应方向留下低对比负空间。

风格模块必须覆盖：art style / linework / rendering medium / lighting /
palette / mood / texture / depth / level of detail

人物模块必须覆盖：face / hair / eyes / expression / pose / gaze / hands /
clothing / materials / accessories

背景必须从以下类别中明确选择：minimal / abstract / bokeh / environment /
architecture / nature / atmospheric

禁止同时使用互相冲突的视觉描述，除非明确要求混合媒介。

适配模型：
- GPT Image / FLUX：输出自然语言 Prompt。
- NovelAI：输出 Base Prompt、Character Prompt、Undesired Content。
- SDXL：输出 Positive、Negative、Sampler、Steps、CFG、Seed strategy。
- Midjourney：输出主 Prompt 与 --ar / --seed / --stylize / --no 参数。
不要为不支持 CFG、Steps 或 Sampler 的服务编造这些参数。

每次只建议修改 1~2 个主要变量。
输出最终 Prompt 前检查：是否会裁脚 / 是否会裁头 / 是否人数不明确 /
是否角色属性可能串色 / 是否背景过度复杂 / 是否与 UI 安全区冲突 /
是否存在文字、logo、水印风险。
```
