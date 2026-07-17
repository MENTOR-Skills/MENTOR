# Attention / Transformer：文献全景说明（样例）

> 本文件为联调样例，依据 `examples/sample-topic/references.json` 三篇短名单撰写，**非**全域综述。

## 1. 主题与范围

围绕序列建模中的注意力机制与预训练范式，时间跨度约 2017–2020，文献类型含会议论文与 arXiv 预印本来源条目。深度档：标准（样例）。

## 2. 主线 / 问题线程

1. **架构主线**：用自注意力替代 RNN/CNN 作为序列转导骨干（代表：Transformer）。
2. **预训练主线**：双向掩码预训练提升语言理解（代表：BERT）。
3. **规模与少样本主线**：放大自回归模型以获得上下文学习能力（代表：GPT-3 一文）。

## 3. 代表工作与方法族

Transformer 提出多头自注意力与位置编码，为后续编码/解码与预训练变体提供骨架。BERT 在此骨干上强调双向上下文。GPT-3 则沿自回归路线放大参数与数据，展示少样本泛化。（推断）大规模自回归路线与双向预训练路线形成互补而非简单替代。

## 4. 关系说明

- BERT → Transformer：方法继承（**事实**，BERT 明确建立在 Transformer 编码结构之上，见库内 `relations.basis: fact`）。
- Transformer → GPT-3：方法继承（**推断**，同属注意力骨干演进叙事，非本样例逐页核对的引用边）。

## 5. 可见缺口

据当前短名单，可能遗漏：高效注意力、多模态扩展、对齐与安全相关工作。以上空白**不是**对全领域的断言。

## 6. 参考文献

1. Vaswani et al., 2017. Attention Is All You Need. NeurIPS. https://arxiv.org/abs/1706.03762
2. Devlin et al., 2019. BERT… NAACL. https://arxiv.org/abs/1810.04805
3. Brown et al., 2020. Language Models are Few-Shot Learners. NeurIPS. https://arxiv.org/abs/2005.14165
