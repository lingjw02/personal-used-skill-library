# 常见失败模式与修正策略

## "明明写了 full body，为什么还是切脚？"

典型失败 Prompt：
```
beautiful anime girl, full body, detailed face, beautiful eyes,
cinematic portrait, close-up details
```
问题：`full body` 与 `portrait`/`close-up details` 直接冲突。

改为：
```
full-body character,
entire body visible from head to toe,
both feet completely inside the frame,
camera far enough to include the whole figure,
comfortable margin above the head and below the shoes
```
并删除 `close-up`。

## 人物脸很好，但壁纸完全不好用

原因通常不是模型质量，而是 Prompt 没有描述 UI 空间。加入：
```
character on the right third,
clean low-detail negative space on the left,
no major focal elements in the empty area
```
或（锁屏）：
```
face below the top quarter of the mobile composition,
large calm background area above the head
```

## CFG 越高越好吗？—— 不是

较高 guidance 虽能增强 Prompt 遵循，但过高可能产生负面效果（色彩/视觉 artifact，僵硬感）。更合理的顺序：
```
检查 Prompt 冲突 → 提升重要内容优先级 → 删除无效标签 → 小幅提高 CFG → 比较
```
而不是"CFG 6 不听话 → 直接跳到 CFG 16"。

## Steps 越多越高清吗？—— 不是

Steps 控制去噪迭代过程，不是输出像素数量。过多 steps 可能收益很小甚至产生反效果；`steps=80` 也不会把 1024×1536 自动变成 4K。分辨率必须靠真实的 width/height 参数或后期 upscale 实现。

## Prompt 写 "8K UHD" 能产生 8K 吗？—— 不能

不要把它当成技术分辨率设置。`4K/8K/UHD` 更接近"高细节视觉暗示"，真正的输出尺寸需通过 size 参数、模型输出规格或 upscale 流程控制。

## 所有人都长同一张脸（群像通病）

不要：
```
2girls, black hair, blue eyes, white hair, red eyes, black dress, white jacket...
```
应该：
```
Scene: 2girls, rooftop, sunset...
Character A: black hair, blue eyes, black dress...
Character B: white hair, red eyes, white jacket...
```
用 Base Prompt + 独立 Character Prompt 的结构（NovelAI 原生支持），而不是把所有人的属性混写在一个 Prompt 空间里。

## Negative Prompt 变成几百个词

把 Negative 当作"故障日志"来维护：
```
出现脚被切 → 加 cropped feet / feet out of frame
出现文字 → 加 text / caption / watermark
出现重复人 → 加 duplicate character / multiple views
```
而不是在每张图上都预加载几百个互不相关的 negative tags。

## 色彩"炸掉"

同时打开 `neon, vibrant, glowing, high saturation, cinematic, HDR, RGB lighting, colorful, strong contrast` 很容易失控。改为明确指定主色/辅色/点缀色各自出现在哪里：
```
dominant palette: deep navy and muted cyan
accent color: warm amber, limited to lights and eye highlights
moderate saturation
```

## 半写实变成真人

`semi-realistic anime` 单独使用很模糊，需把边界讲清：
```
stylized anime facial proportions,
clean illustrated linework,
realistic material lighting,
painted skin shading,
not a photograph
```
如果真的想偏真人一些：
```
semi-realistic anime-inspired portrait,
natural facial anatomy and lighting,
subtle stylization rather than exaggerated anime proportions
```

## 水彩结果却像油画

不要只写 `watercolor`，写具体可观察属性：
```
transparent watercolor washes,
soft pigment blooms,
visible cold-press paper grain,
light pencil contour,
unpainted paper highlights,
no thick impasto
```

## 五官修复导致角色换脸

局部编辑时使用低强度，并在每轮重复声明约束（连续编辑仍可能产生漂移）：
```
Preserve exactly:
- face shape - eye color - hairstyle - eyebrow shape - expression - camera angle
Change only:
- malformed fingers
```

## 参考图强度越高越好？—— 也不是

参考强度越高越容易模仿参考中的颜色/姿态/角度，但过高时也可能让表情、角度、姿态过度绑定于参考图。更适合长期角色工作流的配置：
```
Identity reference = 较强
Pose reference     = 按需求
Style reference    = 中等
Prompt             = 明确新服装/动作
```
而不是把所有 reference slider 拉满。
