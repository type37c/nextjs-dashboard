# Primary-literature checks

2026-11-06. Claim-focused checks of eight primary papers using Firecrawl paper passages and publisher pages. This is not an exhaustive novelty review. Abstracts alone were not used for the substantive claims below. Bibliographic years distinguish arXiv versions from the two verified journal articles.

## ALIF2018

[Long short-term memory and learning-to-learn in networks of spiking neurons](https://arxiv.org/abs/1803.09574) (2018).

- Checked: Section 2, equations 1–2; Section 3.
- Used claim: Adaptive thresholds depend on prior firing and decay; synaptic weights are optimized with BPTT.
- Coverage: retrieved in-body passages; not a complete paper read.

Short locating excerpt:

> We assume that the firing threshold Bj​(t)B\_{j}(t) of neuron jj increases by some fixed amount β/τa,j\\beta/\\tau\_{a,j} for each spike of this neuron jj, and then decays exponentially back to a baseline value …

## EPROP2020

[A solution to the learning dilemma for recurrent networks of spiking neurons](https://www.nature.com/articles/s41467-020-17236-y) (2020).

- Checked: Introduction; Results: Mathematical basis for e-prop, equations 1–2.
- Used claim: E-prop combines locally computed eligibility traces with learning signals for recurrent-network learning.
- Coverage: publisher article after paper-index full-text passages unavailable.

Short locating excerpt:

> A re-analysis of the mathematical basis of gradient descent learning in recurrent neural networks tells us how local eligibility traces and top–down learning signals should be optimally combined—without requiring …

## DAMB2012

[Information Processing Capacity of Dynamical Systems](https://www.nature.com/articles/srep00514) (2012).

- Checked: Results: capacity definition and Proposition 3; subsequent capacity bounds.
- Used claim: Capacity is assessed through linear reconstruction of functions of input history; assumptions constrain the interpretation and bounds.
- Coverage: publisher article after paper-index full-text passages unavailable.

Short locating excerpt:

> The capacity is based on simple linear estimators ![](https://media.springernature.com/lw124/springer-static/image/art%3A10.1038%2Fsrep00514/MediaObjects/41598_2012_Article_BFsrep00514_IEq9_HTML.jpg). For this reason …

## GRU2014

[Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) (2014).

- Checked: Section 2.3, equations 5–8.
- Used claim: Reset and update gates control prior-state use and interpolation with candidate activation.
- Coverage: retrieved in-body passages; not a complete paper read.

Short locating excerpt:

> On the other hand, the update gate controls how much information from the
previous hidden state will carry over to the current hidden state. This acts
similarly to the memory cell in the LSTM network and helps the RNN …

## MAMBA2023

[Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) (2023).

- Checked: Section 3.2; Section 3.5 interpretations of selective parameters.
- Used claim: Input-dependent state-space parameters implement selective propagation or forgetting.
- Coverage: retrieved in-body passages; not a complete paper read.

Short locating excerpt:

> One method of incorporating a selection mechanism into models is by letting their parameters that affect interactions along the sequence (e.g. the recurrent dynamics of an RNN or the convolution kernel of a CNN) be …

## EWC2016

[Overcoming catastrophic forgetting in neural networks](https://arxiv.org/abs/1612.00796) (2016).

- Checked: Section 2: Elastic weight consolidation.
- Used claim: A parameter-importance-weighted penalty constrains change during learning of another task.
- Coverage: retrieved in-body passages; not a complete paper read.

Short locating excerpt:

> This algorithm slows down learning on certain weights based on how important they are to
previously seen tasks. We show how EWC can be used in supervised learning and reinforcement
learning problems to train several …

## NTM2014

[Neural Turing Machines](https://arxiv.org/abs/1410.5401) (2014).

- Checked: Sections 3.1–3.3: reading, writing, addressing.
- Used claim: A controller accesses external memory with selective read and erase/add write operations.
- Coverage: retrieved in-body passages; not a complete paper read.

Short locating excerpt:

> A Neural Turing Machine (NTM) architecture contains two basic components: a neural
network *controller* and a memory bank. Figure 1 presents a high-level diagram of the NTM
architecture. Like most neural networks, the …

## RAG2020

[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) (2020).

- Checked: Introduction; Sections 2.2–2.4.
- Used claim: A parametric generator conditions on documents accessed from a non-parametric index.
- Coverage: retrieved in-body passages; not a complete paper read.

Short locating excerpt:

> We build RAG models where the parametric memory is a pre-trained seq2seq transformer, and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We combine these …

## Scope of the check

The paper index did not supply full-text passages for the e-prop journal paper or Dambre et al.; their publisher article bodies were retrieved instead. The early arXiv:1901.09049 preprint has a different title and author list and is not silently substituted for the 2020 journal paper. No general priority claim, systematic review, formal observability/control-theory comparison, or survey of distributed-memory methods is asserted.
