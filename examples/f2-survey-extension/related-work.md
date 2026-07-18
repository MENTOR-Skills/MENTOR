## Related Work

> **演示说明：** 本文件基于 `examples/sample-topic/references.json` 三篇文献，**低于** Related Work 建议门槛（≥5 篇 + 正式贡献说明），仅展示结构与 positioning 写法。  
> **假设本文贡献（用户输入）：** 提出一种在相同 FLOPs 预算下训练稀疏自注意力变体的方法，面向长序列理解任务，在少微调数据下保持竞争力。

### 序列建模骨干

自注意力序列模型以 Transformer 为代表，用多头注意力与位置编码替代循环结构，在翻译等任务上验证了并行训练与建模能力 [1]。该骨干成为后续预训练与规模化工作的共同起点。其局限包括标准注意力的二次复杂度与位置编码设计选择；本文在**保持 Transformer 式堆叠**的前提下，通过稀疏模式降低有效复杂度，而非回到 RNN。

### 预训练范式：双向与自回归

BERT 将双向上下文引入 Transformer 编码器预训练，在理解类任务上表现突出 [2]。与之对照，GPT-3 路线通过放大自回归语言模型，在少样本设定下展示任务适应 [3]。理解任务常受益于双向或编码器式目标，而生成与通用接口更常沿自回归扩展。（推断）稀疏注意力与两种范式均可结合，但训练目标与推理成本权衡不同。（推断结束）本文聚焦**理解向长序列**，预训练阶段采用双向/掩码式目标，与 GPT-3 式纯自回归设定区分开。

### Positioning

库内三篇工作覆盖「通用骨干—双向预训练—规模化少样本」三条线，但均未系统讨论**固定 FLOPs 下的稀疏注意力训练**。本文在该缺口上给出可复现的训练配方，并在长序列理解基准上与全注意力基线对比（具体数字须来自用户实验，本 Related Work 不编造）。与 BERT [2] 的差异在于结构级稀疏而非仅堆叠深度；与 GPT-3 [3] 的差异在于问题设定与训练目标；与原始 Transformer [1] 的差异在于复杂度—精度折中与长序列适用性。

### 参考文献

[1] Vaswani et al., 2017. Attention Is All You Need. NeurIPS. https://arxiv.org/abs/1706.03762  
[2] Devlin et al., 2019. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. NAACL. https://arxiv.org/abs/1810.04805  
[3] Brown et al., 2020. Language Models are Few-Shot Learners. NeurIPS. https://arxiv.org/abs/2005.14165
