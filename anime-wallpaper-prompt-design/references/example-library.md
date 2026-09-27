# 案例库（A–N，均为起始配置，非跨 checkpoint 通用保证）

| 案例 | 输出目标 | 核心效果 | 推荐模型 | 比例 |
|---|---|---|---|---|
| A | 手机全身立绘 | 标准高质量日系赛璐璐 | NovelAI V5 | 9:16 |
| B | 桌面半写实肖像 | Cyberpunk 电影感 | FLUX.2 | 16:9 |
| C | 手机全身 | 水彩和服、柔和留白 | GPT Image 2.5 | 9:16 |
| D | 手机 Q 版 | Chibi 萌系锁屏 | Midjourney Niji | 9:16 |
| E | 手机膝上肖像 | 哥特月光、暗色 | NovelAI V5 | 9:16 |
| F | 4K 桌面 | 奇幻骑士环境场景 | SDXL Anime | 16:9 |
| G | 桌面近景 | 咖啡馆暖色 Bokeh | FLUX.2 | 16:9 |
| H | 手机动态全身 | Streetwear 低机位 | GPT Image 2.5 | 9:16 |
| I | 超宽桌面 | 机甲驾驶员、赛璐璐 | SDXL Anime | ≈21:9 |
| J | 手机双人 | 互补角色海报 | NovelAI V5 | 9:16 |
| K | 桌面四人群像 | RPG Party | NovelAI V5 | 16:9 |
| L | 桌面肖像 | Anime × 3D render | FLUX.2 | 16:9 |
| M | 桌面全身 | 极简抽象品牌感 | GPT Image 2.5 | 16:9 |
| N | 手机暗黑全身 | 墨线、黑白红点色 | SDXL Anime | 9:16 |

---

### A — 日系赛璐璐全身手机立绘

**Prompt**
```
1girl, adult,
long silver hair, flowing hair, violet eyes,
calm expression, slight smile,

full body, head to toe, feet visible,
standing, slight contrapposto,
looking at viewer,
one hand holding a slim magical staff,

navy fantasy dress,
silver embroidery, layered skirt,
moon pendant, black ankle boots,

clean anime illustration,
clean thin lineart,
crisp cel shading,
subtle soft gradients,
high detail,

cool moonlight,
soft silver rim light,
navy blue, violet, silver color palette,

night sky, distant ruined observatory,
subtle stars, atmospheric depth,
simple background near upper area,
negative space above head for phone clock,

best quality, masterpiece, high complexity
```
**Negative/UC**
```
lowres, blurry, bad anatomy, bad hands,
extra fingers, fused fingers, extra limbs,
cropped, cropped feet, feet out of frame,
multiple views, duplicate character,
text, logo, watermark, signature
```
**设置**：NovelAI V5；DPM++ 2M；Steps 24–28；Guidance 5–6；seed 首轮随机、选中构图后锁定。建议先出 1024×1536 一类纵向画布，再扩展/裁成 1440×2560 或 1440×3200。
**要点**：feet visible + 顶部 negative space 同时解决"脚被切"与"锁屏时钟压脸"。

---

### B — 半写实 Cyberpunk 桌面人物肖像

**Prompt**
```
An original adult anime-inspired cyberpunk woman,
waist-up portrait positioned on the right third of a widescreen desktop wallpaper.
Short asymmetrical black hair with subtle cyan highlights,
amber eyes, composed and observant expression.

She wears a matte black technical jacket with brushed-metal fasteners,
translucent polymer panels and a small geometric earring.

Semi-realistic anime illustration:
realistic material response and facial lighting,
but clearly stylized anime facial proportions,
clean controlled linework and refined digital painting.

Night rain in a futuristic city,
cyan and warm amber practical lights,
soft neon reflections on wet surfaces,
subtle volumetric haze,
shallow depth of field with restrained bokeh.

Eye-level camera, natural perspective.
Keep approximately 35 percent clean negative space on the left for desktop icons.
No text, no logo, no watermark.
Do not crop the top of the hair.
```
**排除项（并入自然语言约束）**
```
Avoid distorted hands, duplicated accessories, excessive neon,
plastic-looking skin, illegible signage, logos and watermarks.
```
**设置**：FLUX.2 [dev]；28 inference steps 起步、guidance 4；固定 seed 做局部 A/B。最终 3840×2160；显存不足先低分辨率同比例生成再 upscale。
**要点**：人物/取景/位置最先写，材质/灯光/背景放后（FLUX 官方建议重要信息优先出现）。

---

### C — 水彩和服锁屏全身壁纸

**Prompt**
```
制作一张原创成年女性动漫角色的竖屏锁屏壁纸。

人物必须从头到脚完整可见，两只鞋都在画面内。
她位于画面下方约三分之二处，头顶留出大面积干净空间供手机时钟显示。

角色穿现代化的浅灰蓝和服，衣料上只有少量原创的银杏叶纹样，
长黑发被微风轻轻吹起，神情平静，略带怀念。

视觉风格是精致的日系水彩插画：
柔和透明颜料叠色、纸张颗粒、细而克制的铅笔线稿，不要厚重油画效果。

清晨逆光，乳白、淡青、暖金的低饱和色盘。
背景是被晨雾弱化的河岸和远山，环境细节逐渐淡出，不与人物争夺注意力。

不要任何文字、logo、水印、签名。不要切掉头发、手或脚。
```
**设置**：GPT Image 2.5；quality=high 或最终稿 xhigh；建议先 1024×1536 试稿，再用支持范围内的自定义尺寸输出/编辑，最终导出 1440×2560 或 1440×3200。无独立 Negative 输入，排除条件直接写入主指令。Sampler/Steps/CFG/Seed 不填（不暴露）。
**要点**：GPT Image 更适合"用途 + 构图 + framing + 保留/排除项"的自然语言写法，而非扩散模型式 tag soup。

---

### D — Q 版 Chibi 手机壁纸

**Prompt**
```
cute original chibi witch character,
full body, tiny body and oversized expressive head,
short lavender hair, large golden eyes,
oversized navy wizard hat,
small star-shaped satchel,
cheerful pose, one foot lifted,
clean anime cel shading,
rounded shapes, crisp lineart,
pastel lavender and cream palette,
floating tiny stars,
minimal soft gradient background,
large clean space above the character,
mobile lock-screen wallpaper
--ar 9:16 --niji --no text, logo, watermark
```
**排除（通过 --no）**：`text, watermark, logo, extra characters, photorealism`
**设置**：Midjourney Niji；`--ar 9:16`；stylize 建议先中性范围测试；选到构图后固定 seed。Sampler/Steps/CFG 由服务端管理，无用户可设参数。
**要点**：Chibi 不需要大量皮肤材质/镜头/纹理描述，关键词越集中造型越干净。

---

### E — 哥特月下膝上肖像

**Prompt**
```
1girl, adult,
long black hair, straight hair,
pale violet eyes,
serious expression,

knees-up, three-quarter view,
looking sideways,
one hand touching a black rose choker,

gothic dress,
black lace, dark velvet,
silver jewelry,
long sleeves,

anime illustration,
fine detailed lineart,
dramatic cel shading,
subtle painterly rendering,

moonlight,
strong cool rim light,
deep navy, black, silver,
small crimson accents,

gothic cathedral terrace,
full moon behind thin clouds,
mist, atmospheric perspective,
soft distant bokeh,

masterpiece, best quality, high complexity
```
**Negative**
```
lowres, bad anatomy, bad hands,
extra fingers, duplicate,
overexposed moon,
washed-out blacks,
text, signature, watermark
```
**设置**：NovelAI V5；Euler Ancestral 或 DPM++ 2M；24–28 steps；Guidance 5–5.5；9:16。
**要点**：略微降低 guidance 可让阴影与材质更柔软；较低 guidance 往往更偏柔和/绘画感。

---

### F — 奇幻骑士 4K 桌面完整场景

**Prompt**
```
original adult female knight,
full body visible, both boots fully inside frame,
standing on the right third of a panoramic battlefield,
looking toward the distant horizon,

weathered white-and-navy plate armor,
blue fabric cape moving in the wind,
long sword held downward in one hand,

premium anime fantasy key visual,
clean lineart,
refined cel shading combined with digital painting,
detailed metal surfaces,
controlled texture,
cinematic but clearly illustrated,

late golden-hour sunlight,
warm rim light against cool storm clouds,
dramatic cloud layers,
distant ruined castle,
grass bending in the wind,
foreground stones for depth,
strong atmospheric perspective,

large uncluttered sky and landscape on the left for desktop icons,
wide establishing composition,
no text, no logo, no watermark
```
**Negative**
```
cropped feet, cropped sword,
extra sword, fused fingers,
deformed armor, asymmetrical shoulder armor,
duplicate character, multiple views,
busy left side, text, logo, watermark
```
**设置**：SDXL Anime checkpoint + ComfyUI；工程起点 DPM++ 2M / Karras；30–34 steps；CFG 6–7；seed 随机探索后锁定。先按 16:9 生成，再 2×/4× 放大至 3840×2160。

---

### G — 暖色咖啡馆角色近景

**Prompt**
```
An original adult anime woman sitting beside a café window,
head-and-shoulders to chest-up portrait,
placed slightly left of center.

Chestnut bob haircut, warm brown eyes,
relaxed subtle smile,
cream knitted cardigan over a dark green blouse,
small understated gold earrings.

Sophisticated anime illustration with semi-realistic lighting,
soft clean linework,
natural skin shading,
visible knit texture without photorealistic pores.

Late-afternoon sunlight through the window,
warm amber edge light,
soft shadow on the opposite cheek.
Background café lights become large restrained circular bokeh,
with only vague silhouettes of shelves and plants.

Shallow depth of field,
intimate 50mm-like portrait perspective,
quiet cozy atmosphere.
Keep the right side relatively uncluttered for desktop widgets.
No text or branding.
```
**排除项**
```
Avoid excessive skin smoothing, malformed earrings,
duplicate cups, distorted hands, harsh HDR,
oversaturated orange tones, text and logos.
```
**设置**：FLUX.2 [dev]；28 steps；guidance 4；16:9。
**要点**：把 bokeh 定义为"背景灯的视觉形态"而不是只写 beautiful bokeh，模型更容易理解其空间来源。

---

### H — Streetwear 动态低角度手机全身

**Prompt**
```
制作一张 9:16 原创成年动漫角色街头时装壁纸。

一个短银灰发的女性角色从城市天桥上向镜头方向走来。
使用轻微低机位，但不要夸张广角变形。
从头顶到鞋底必须全部出现在画面内，双手、双脚完整可见。

她穿宽松黑色 bomber jacket、白色短款内搭、高腰 cargo pants 和原创设计运动鞋，
搭配耳机与简单银饰。

风格：高级商业动漫插画，锐利干净线稿、现代 cel shading，
少量柔和数字绘画渐变，清晰但不过度复杂。

傍晚蓝调时刻，背景有暖色城市灯光，
冷蓝环境光 + 暖橙轮廓光形成互补色，地面略有雨后反射。

人物位于下方和中央偏右，顶部留下足够锁屏时钟空间。
不要品牌标识、文字、广告牌可读文字或水印。
```
**设置**：GPT Image 2.5；quality=high/xhigh；可直接生成支持范围内的纵向自定义尺寸（注意高于约 2560×1440 的尺寸可能仍属 experimental，需 QA）。Sampler/Steps/CFG 不适用。
**要点**："低机位"后立即加"不要夸张广角变形"，避免模型把 dynamic low angle 理解成超广角大鞋小头。

---

### I — 超宽屏机甲驾驶员壁纸

**Prompt**
```
1girl, adult mecha pilot,
full body,
standing beside a giant humanoid mecha,
pilot occupies the right third,
mecha silhouette occupies the distant center-right,

short dark blue hair,
orange eyes,
white and graphite pilot suit,
small orange technical accents,
helmet held under one arm,

retro-futuristic anime,
precise mechanical lineart,
strong cel shading,
1980s-inspired mecha visual language
without copying any existing franchise,
modern high-detail rendering,

aircraft hangar at sunrise,
huge hangar doors,
long perspective lines,
volumetric sun rays,
cool industrial interior versus warm exterior,

very wide cinematic composition,
large uncluttered negative space on the left,
no readable text,
no logos,
no franchise insignia
```
**Negative**
```
cropped character, cropped feet,
deformed mecha, extra mechanical limbs,
tiny unreadable typography,
existing franchise logo,
watermark, signature
```
**设置**：SDXL Anime/mecha 兼容 checkpoint；DPM++ 2M Karras；30–36 steps；CFG 6；先按 3440:1440 等比例较低原生画布生成再 upscale。
**要点**：超宽屏最容易犯"为了填满画面复制人物/机甲"的错误，明确主体数量和空间位置很关键。

---

### J — 双角色手机海报

NovelAI V5 的多人任务特别适合用 Base Prompt + 独立 Character Prompt，用以减少角色属性串色。

**Base Prompt**
```
2girls, full body, side-by-side, standing on a rooftop,
sunset city, wind, cinematic composition,
anime illustration, clean lineart, cel shading,
orange and blue complementary palette,
best quality, high complexity
```
**Character A**: `girl, left side, long black hair, blue eyes, calm expression, navy long coat, black boots, holding closed umbrella`
**Character B**: `girl, right side, short white hair, amber eyes, energetic smile, orange cropped jacket, dark cargo pants, headphones around neck`
**Negative/UC**
```
merged bodies, fused arms, same face,
hair color leakage, clothing color leakage,
extra person, cropped feet, text, watermark
```
**设置**：NovelAI V5；DPM++ 2M；26–28 steps；Guidance 5–6；9:16。
**要点**：关键不是提高 `2girls` 权重，而是不要把两人的头发/眼睛/衣服全部写进同一段 Prompt。

---

### K — 四人 RPG Party 桌面群像

**Base**
```
2girls, 2boys,
four-person fantasy adventuring party,
full body group,
walking toward viewer,
forest ruins at dawn,
anime RPG key visual,
clean detailed lineart,
refined cel shading,
soft atmospheric perspective,
balanced group composition,
best quality
```
**角色 Prompts**
```
Character A: girl, leftmost, red hair, green eyes, light leather armor, bow and quiver
Character B: boy, center-left, black hair, blue eyes, silver knight armor, sword at hip
Character C: girl, center-right, silver hair, violet eyes, dark mage robe, staff
Character D: boy, rightmost, blonde hair, brown eyes, green travel cloak, small satchel
```
**Negative**
```
merged characters, duplicate face, identical outfits,
weapon leakage, hair color leakage,
extra people, missing person, fused hands, text, logo
```
**设置**：NovelAI V5；DPM++ 2M；28 steps；Guidance 5–5.5；16:9。
**要点**：群像最重要的是"角色身份隔离"，其次才是细节量——四人每人十几个核心 tag，通常优于把 150 个外观标签混在一起。

---

### L — Anime × 高级 3D Render

**Prompt**
```
An original adult anime heroine rendered as a premium stylized 3D cinematic character,
waist-up portrait on the right side of a widescreen wallpaper.

Long white hair with individually grouped stylized strands,
clear sapphire eyes,
natural anime facial proportions,
calm confident expression.

Dark navy ceremonial jacket with satin trim,
brushed silver clasps and translucent crystal ornament.

High-end stylized 3D rendering,
not photorealistic,
smooth but believable materials,
subtle subsurface skin response,
clean modeled eyelashes,
precise hair highlights,
cinematic global illumination.

Large soft key light from camera-left,
cool rim light from behind,
deep blue-to-black abstract gradient background,
subtle particles,
very shallow background depth,
clean negative space on the left.

No text, no logo, no plastic toy appearance,
no excessive skin pores.
```
**排除项**
```
Avoid waxy skin, plastic doll appearance,
uncanny photorealism, excessive pores,
misaligned eyes, duplicate accessories.
```
**设置**：FLUX.2 [dev]；28–36 steps；guidance 4；16:9。
**要点**："3D render"容易滑向"玩偶/塑料手办"，需同时定义 stylized cinematic character + 具体材质响应，并明确排除 plastic doll look。

---

### M — 极简抽象高级桌面立绘

**Prompt**
```
创建一张极简主义 16:9 桌面动漫壁纸。

原创成年女性角色，完整全身，从头顶到鞋底全部可见，
站在画面右侧三分之一位置。

她有齐肩深蓝短发、灰蓝眼睛，穿剪裁非常简洁的白色长外套、
深灰高领上衣和黑色长裤。没有复杂装饰。

采用现代高级动漫编辑插画风格：极干净的细线条，大块明确的色面，
非常克制的 cel shading，极少纹理。

背景只使用暖灰到浅米色的柔和抽象渐变，加少量极细几何弧线。
左边至少三分之一保持安静、干净、低对比度，用于桌面图标。

使用柔和侧光，人物与背景保持清楚的轮廓分离。
不要景物堆叠，不要文字，不要 logo，不要水印。
```
**设置**：GPT Image 2.5；quality=high；3840×2160 作为最终输出目标（需满足尺寸约束）。
**要点**：极简图的失败通常是"模型主动添加太多装饰"，Prompt 应强调限制信息密度，而不是追加更多细节词。

---

### N — 黑白墨线 + 红色点色暗黑壁纸

**Prompt**
```
original adult female swordswoman,
full body, head to toe,
standing still in strong wind,
long black hair flowing horizontally,
black ceremonial coat,
slender katana held downward,

dark fantasy anime illustration,
expressive black ink linework,
sharp brush strokes,
high-contrast black and off-white,
very limited crimson accent only on ribbon and eyes,
rough paper texture,
controlled cross-hatching,
minimal grayscale cel shading,

slightly low camera angle,
large pale moon behind thin clouds,
black tree branches framing the sides,
mist at ground level,
vertical composition,
clean space above character,

dramatic, solemn, restrained,
no colorful background,
no text, no logos
```
**Negative**
```
rainbow colors, neon lighting,
photorealism, glossy 3D,
cropped feet, extra sword,
bad hands, duplicate character,
text, logo, watermark
```
**设置**：SDXL Anime checkpoint；Euler A 与 DPM++ 2M 各跑一批比较（实验策略，不是宣称某 sampler 必然产生"墨线风"）；Steps 28–34；CFG 5.5–6.5；9:16。
**要点**：`limited crimson accent only on...` 比 `black white red palette` 更强，因为它定义了红色允许出现的具体位置，降低整个背景被染红的概率。
