# 模型对照与参数指南

## 模型强项与适合任务

| 模型/工作流 | 强项 | 适合的壁纸任务 | 参数控制方式 |
|---|---|---|---|
| NovelAI Diffusion V5 | 二次元标签理解、角色特征、多人分离 | 日系立绘、角色卡、双人/多人动漫壁纸 | sampler、steps、guidance、seed、UC(Undesired Content) |
| SDXL 动漫 checkpoint + ComfyUI | 自定义程度最高、LoRA/ControlNet/局部修复生态 | 需要固定角色、固定姿势、批量生产 | sampler、scheduler、steps、CFG、seed |
| FLUX.2 | 自然语言、手脸细节、材质、复杂场景、参考图 | 半写实动漫、电影感壁纸、服装设计 | dev 本地可调 steps/guidance；API 依版本而定 |
| GPT Image 2.5 | 指令遵循、编辑、引用角色/服装/背景、复杂约束 | 原创人物、连续改稿、桌面/手机成套壁纸 | quality、size、reference/edit；不暴露 CFG/sampler |
| Midjourney Niji | 快速获得强烈二次元视觉风格和构图 | 概念探索、海报型/视觉冲击型壁纸 | `--ar`、`--seed`、`--stylize`、`--no` 等 |

不要把 SDXL 的"30 steps / CFG 7"机械复制给所有模型——GPT Image、Midjourney 不向用户暴露传统 sampler/CFG/steps，写这些参数进 Prompt 不会真正控制底层采样。

## 参数含义（不是越高越好）

| 参数 | 推荐理解 | 实用起点 |
|---|---|---|
| Steps | 去噪迭代次数 | 先低成本探索，构图确定后提高 |
| CFG / Guidance | Prompt 约束强度 | 太低可能跑题，太高可能僵硬/过饱和 |
| Sampler | 去噪算法 | 与模型相关，不存在跨模型绝对冠军 |
| Scheduler | 噪声时间表 | 和 sampler 共同影响生成轨迹 |
| Seed | 初始随机状态 | 调 Prompt 时锁 seed；探索时随机 |
| Resolution | 实际生成尺寸 | 不要用 Prompt 中的"4K"字样替代真实参数 |
| Negative | 排除内容 | 针对实际出现的问题加，而不是无限堆砌 |

## 各模型推荐起点（工程起点，不是厂商保证的最优值）

- **NovelAI**：DPM++ 2M 或 Euler Ancestral 较稳定；guidance 约 5–6（V3 以上）；steps 24–28。过高 guidance 可能产生反效果，steps 加太多收益也可能很小甚至适得其反；官方 Decrisper 机制用于缓解高 guidance 下的色彩/视觉 artifact。
- **SDXL + ComfyUI**：CFG 官方文档给出的通用参考区间约 6–8，具体动漫 checkpoint 经常需要重新验证；steps 30 左右起步；KSampler 把 steps、CFG、sampler、scheduler、positive/negative conditioning 分别作为独立控制量。
- **FLUX.2 [dev]**：官方模型卡当前示例用 `num_inference_steps=50, guidance_scale=4`，同时注明 28 steps 是很好的折中；重要主体/动作信息应优先出现在 Prompt 前部。
- **GPT Image 2.5**：只有 quality（low→max）、size、format、reference/edit 等；无 sampler/steps/CFG 可填，不要编造。
- **Midjourney Niji**：`--ar` 控制比例、`--seed` 复现、`--stylize` 控制风格化强度、`--no` 排除内容；Niji 是官方定位为 anime/Eastern aesthetics 的模型选项，服务端管理采样，无用户可设置的传统参数。

## Seed 的正确用法

```
探索阶段：Prompt A + random seeds × 8~16
   ↓ 选构图
锁定 seed = X
   ↓ 每次只改一个变量（发型 → 光线 → 衣服 → 背景）
构图定稿
   ↓ 重新随机 seed 做最终候选
```

固定 seed 适合做 Prompt 的 A/B 测试，但它不是"角色 ID"——只有所有相关设置一致才可能复现接近相同的结果，且部分 sampler 本身并非完全确定性（deterministic）。

## 放大、修脸与抗锯齿的生产顺序

```
构图生成 → 选图 → 局部修脸/手 → 放大 → 最终裁切 → 轻度锐化/抗锯齿 → 导出
```

不要一开始就追求最大分辨率。放大（如 4× Upscale）与"会重新创造细节"的 Enhance 类操作应区分对待。`anti-aliased edges` 这类词有时会改变整体视觉风格，却不能保证解决像素级锯齿——更可靠的是把抗锯齿当成后期步骤：

```
生成/修复 → 2×或4×放大 → 检查眼睛/睫毛/发丝/线稿halo → 必要时轻度降噪
   → 缩放到最终壁纸尺寸 → 高质量 resampling
```

脸和眼睛不应靠无限堆叠 `beautiful eyes, perfect eyes, detailed eyes` 来改善，更可控的写法：

```
clear irises, consistent catchlights, symmetrical eye placement,
clean eyelashes, natural eyelid shape
```

如果脸本身已经正确，优先局部 inpaint，而不是重新生成整幅图。
