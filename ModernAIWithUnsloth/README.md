# LLM Training with Unsloth

Practical notebooks exploring efficient training methods for compact language models using Unsloth.ai framework.

[Watch Video Tutorial](https://youtu.be/m1ONP5oDvvE)

## Notebooks

### 1. Full Fine-Tuning
Complete weight updates on SmolLM2-135M using instruction datasets. Demonstrates traditional fine-tuning approach with full parameter optimization.

[Open in Colab](https://colab.research.google.com/drive/1bkLd9W9wEWNAbKG7uszjmQOOyvoRaPnF?usp=sharing)

### 2. LoRA Adaptation  
Parameter-efficient training using Low-Rank Adaptation. Achieves comparable results with 2-3x faster training and 50% less memory.

[Open in Colab](https://colab.research.google.com/drive/1auiyjpT35Fza2mSL0YMhE4YjQ-JxnlG0?usp=sharing)

### 3. DPO Alignment
Direct Preference Optimization using chosen/rejected response pairs. Aligns model behavior with human preferences without separate reward models.

[Open in Colab](https://colab.research.google.com/drive/1l4bTpeCpbGFIczpYWxE_SgPq7tHVp9Ik?usp=sharing)

### 4. GRPO Reasoning
Group Relative Policy Optimization for reasoning tasks. Generates multiple solution traces and learns from self-generated rewards.

[Open in Colab](https://colab.research.google.com/drive/1ONhgYirGpIZqhFyfont7_YXP43hf_UoC?usp=sharing)

### 5. Continued Pretraining
Domain and language adaptation through continued pretraining on raw text. Demonstrates Hindi language learning while preserving existing capabilities.

[Open in Colab](https://colab.research.google.com/drive/1KCmr3Ap3OhJXDn8Q51Wiyl_MR32-sZb4?usp=sharing)

## Models

Primary: SmolLM2-135M (ultra-lightweight for experimentation)  
Also compatible: Gemma-3-1B, Llama 3/3.1, Phi-3, TinyLlama, Qwen2, Mistral

## Quick Comparison

| Method | Memory | Speed | Use Case |
|--------|--------|-------|----------|
| Full Fine-tuning | High | Baseline | Domain-specific adaptation |
| LoRA | Low | 2-3x faster | Quick adaptation, limited resources |
| DPO | Medium | Moderate | Preference alignment |
| GRPO | Medium | Slower | Reasoning capabilities |

## Key Techniques

**LoRA**: Trains only 1-5% of parameters via rank decomposition matrices. Adapter files are 10-100MB vs full model checkpoints.

**DPO**: Simpler than traditional RLHF. Directly optimizes policy from preference data with more stable training.

**GRPO**: Generates multiple reasoning traces per problem, ranks them using group-relative rewards. Enables chain-of-thought problem solving.

## Setup Tips

- Use 4-bit quantization with LoRA for limited GPU memory
- Enable `packing=True` and gradient checkpointing for efficiency  
- Apply proper chat templates for consistent formatting
- Start with models under 1B parameters for rapid iteration
- Monitor validation loss to prevent overfitting

## Resources

- [Unsloth GitHub](https://github.com/unslothai/notebooks/)
- [Fine-tuning Guide](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide)
- [RL Guide](https://docs.unsloth.ai/get-started/reinforcement-learning-rl-guide)
- [GRPO Tutorial](https://docs.unsloth.ai/get-started/reinforcement-learning-rl-guide/tutorial-train-your-own-reasoning-model-with-grpo)
