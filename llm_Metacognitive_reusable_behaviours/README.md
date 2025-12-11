# Metacognitive-Reuse-LLM-Behaviors

## Overview

This repository provides a structured overview of Metacognitive Reuse in Large Language Models (LLMs), a groundbreaking approach that converts recurring reasoning patterns into concise, reusable "behaviors." Based on the 2025 research paper, this framework addresses the inefficiency of LLMs repeatedly deriving the same intermediate steps across problems, leading to inflated token usage and latency.

By enabling LLMs to remember **how to reason** rather than just **what to conclude**, this approach achieves up to 46% reduction in reasoning tokens while maintaining or improving accuracy on challenging mathematical benchmarks.

## The Problem with Repetitive Reasoning

Current LLMs face a structural inefficiency when solving multi-step problems:
- **Token Inflation**: Models re-derive common sub-procedures (e.g., geometric series formulas, unit conversions) from scratch for each problem
- **Increased Latency**: Verbose derivations slow down inference time
- **Context Window Saturation**: Repetitive reasoning leaves less capacity for exploration and novel problem-solving

## What Are Behaviors?

A **behavior** is a reusable skill—a concise piece of procedural knowledge distilled from an LLM's chain of thought. Each behavior consists of:
- **Name**: A canonical identifier (e.g., `behavior_systematic_counting`)
- **Instruction**: A short, actionable description of how to apply the skill

**Example**:
```
behavior_inclusion_exclusion → Use P(A∪B) = P(A)+P(B)−P(A∩B) to avoid double-counting overlapping events
```

Unlike traditional memory systems that store declarative facts (what is true), behaviors capture **procedural knowledge** (how to think).

## The Metacognitive Framework

The framework employs three LLM roles:

### 1. Metacognitive Strategist (LLM A)
Extracts behaviors from its own reasoning traces through a three-step process:
1. **Solution Generation**: Solves a problem with full chain-of-thought reasoning
2. **Reflection**: Critiques the solution for correctness, missing strategies, and reusable patterns
3. **Behavior Extraction**: Converts insights into named, actionable behaviors stored in a "behavior handbook"

### 2. Teacher (LLM B)
Generates training data using behavior-conditioned inference for supervised fine-tuning

### 3. Student (LLM C)
Benefits from behaviors through in-context learning or parameter internalization via fine-tuning

## Three Ways to Use Behaviors

### Behavior-Conditioned Inference (BCI)
Relevant behaviors are retrieved from the handbook and provided in-context during reasoning.

**Results**:
- Up to **46% reduction** in reasoning tokens
- Maintains or improves baseline accuracy on MATH and AIME benchmarks
- More cost-efficient inference (fewer output tokens, pre-computed input representations)

### Behavior-Guided Self-Improvement
The model improves its own reasoning by learning from behaviors extracted from its past attempts.

**Results**:
- Up to **10% higher accuracy** compared to naive critique-and-revise baseline
- Better test-time scaling with increasing token budgets
- Enables models to accumulate procedural knowledge over time

### Behavior-Conditioned Supervised Fine-Tuning (BC-SFT)
Models are fine-tuned on reasoning traces generated via behavior-conditioned inference, internalizing behaviors into parameters.

**Results**:
- **Superior performance** compared to vanilla SFT across all token budgets
- More effective at converting non-reasoning models into reasoning models
- Produces both more accurate and more concise outputs

## Key Experimental Results

### MATH Dataset
- **Models Tested**: DeepSeek-R1-Distill-Llama-70B, Qwen3-32B
- **Behavior Handbook**: 785 behaviors curated from 1,000 training questions
- **Outcome**: Similar or improved accuracy with significantly fewer tokens

### AIME Datasets (2024-2025)
- **Behavior Handbook**: 1,457 behaviors from AIME-22/23 (60 questions)
- **Retrieval Method**: Embedding-based retrieval using FAISS index
- **Outcome**: Competitive performance with enhanced token efficiency

### SFT Experiments
- **Models**: Qwen2.5-14B, Qwen2.5-32B-Instruct, Qwen3-14B, Llama-3.1-8B
- **Training Data**: S1 dataset with behavior-conditioned responses
- **Outcome**: BC-SFT models consistently outperform both original and vanilla SFT models

## Example Behaviors by Domain

| Domain | Behavior | Instruction |
|--------|----------|-------------|
| **Algebra** | `behavior_recognize_algebraic_patterns` | Look for common patterns such as perfect squares, cubes, or factorable forms |
| **Geometry** | `behavior_use_shoelace_formula` | Use the shoelace formula to find polygon area from coordinates |
| **Probability** | `behavior_complementary_probability` | Use the complement when it's simpler than calculating direct probability |
| **Number Theory** | `behavior_check_prime_factors` | Confirm prime factorization is complete and correct for each number |
| **Precalculus** | `behavior_convert_to_polar_form` | Use polar form for complex operations like exponentiation |

## Efficiency Considerations

The approach offers significant cost advantages:
- **Reduced Output Tokens**: Fewer tokens generated means lower inference costs
- **Pre-computed Inputs**: Behavior representations can be cached and reused
- **No Autoregressive Input**: Input processing is faster than generation
- **API Cost Savings**: Most APIs charge less for input tokens than output tokens

## Future Directions

Key areas for advancement:
- **Dynamic Retrieval**: Enable models to query the behavior handbook on-the-fly during reasoning
- **Cross-Domain Scaling**: Build large-scale behavior libraries spanning multiple domains
- **Tool Integration**: Train models to treat the behavior handbook as a retrievable tool
- **Continual Learning**: Enable models to continuously expand their procedural memory

## Limitations

- Behaviors are currently retrieved at the beginning and remain fixed during reasoning
- Framework demonstrated primarily on mathematical reasoning tasks
- Requires further exploration for programming, theorem proving, and open-ended dialogue
- Scalability to massive cross-domain behavior libraries needs investigation

## Conclusion

Metacognitive Reuse represents a fundamental shift in how LLMs approach reasoning. By converting slow, verbose derivations into fast, reusable behaviors, this framework enables models to:
- **Remember procedural knowledge** across problems
- **Reason more efficiently** with fewer tokens
- **Self-improve** by learning from past attempts
- **Scale better** through parameter internalization

This work points toward a future where LLMs don't just solve problems—they learn and remember **how to think**.

## Project Deliverables

- **Medium Article**: [Link](https://medium.com/@ShubhamKothiya/teaching-ai-to-remember-how-to-think-81649008d22a)
- **Slide Deck**: [Link](https://gamma.app/docs/Teaching-AI-to-Remember-How-to-Think-e5nnmihwz4fstq1)
- **YouTube Video**: [Link](https://www.youtube.com/)

## References

Based on the research paper:
**"Metacognitive Reuse: Turning Recurring LLM Reasoning Into Concise Behaviors"**
- Authors: Aniket Didolkar, Nicolas Ballas, Sanjeev Arora, Anirudh Goyal
- Affiliation: Meta, Mila-Quebec AI Institute, Princeton University
- arXiv: 2509.13237v1 [cs.LG] 16 Sep 2025
