# Modern AI with Unsloth.ai

**Course:** FA25: CMPE-297 Sec 49 - Special Topics

---

## 📋 Assignment Overview

This repository contains implementations of various modern AI tasks using Unsloth.ai for efficient LLM fine-tuning. The assignment involves five different colab notebooks demonstrating full fine-tuning, LoRA, reinforcement learning, GRPO reasoning, and continued pretraining techniques, each with detailed video walkthroughs.

**Assignment Goals:**
- Master full fine-tuning with small models (SmolLM2 135M)
- Implement LoRA parameter-efficient fine-tuning
- Practice reinforcement learning with preference datasets
- Train reasoning models using GRPO
- Perform continued pretraining for new language learning
- Export models to Ollama for local inference

---

## 📂 Project Structure

Each colab is organized in its own subdirectory with complete implementation, documentation, and execution artifacts.

```
ModernAIWithUnsloth/
├── colab-1-full-finetuning/
│   └── README.md (Full fine-tuning with SmolLM2 135M)
├── colab-2-lora-finetuning/
│   └── README.md (LoRA parameter-efficient fine-tuning)
├── colab-3-reinforcement-learning/
│   └── README.md (RL with preference datasets)
├── colab-4-grpo-reasoning/
│   └── README.md (GRPO reasoning model training)
└── colab-5-continued-pretraining/
    └── README.md (Continued pretraining for new languages)
```

---

## 🎯 Learning Objectives

### 1. Full Fine-tuning (Colab 1)
- Understand full parameter fine-tuning vs parameter-efficient methods
- Work with small models (SmolLM2 135M parameters)
- Learn chat model templates and formatting
- Master dataset preparation for instruction tuning

### 2. LoRA Fine-tuning (Colab 2)
- Implement Low-Rank Adaptation (LoRA) technique
- Compare efficiency vs full fine-tuning
- Understand rank and alpha hyperparameters
- Optimize memory usage with parameter-efficient methods

### 3. Reinforcement Learning (Colab 3)
- Work with preference datasets (chosen vs rejected outputs)
- Implement DPO (Direct Preference Optimization)
- Understand reward modeling concepts
- Align models with human preferences

### 4. GRPO Reasoning (Colab 4)
- Train reasoning models using GRPO (Group Relative Policy Optimization)
- Generate reasoning traces
- Implement chain-of-thought capabilities
- Build models similar to OpenAI's o1

### 5. Continued Pretraining (Colab 5)
- Extend model knowledge to new languages
- Perform domain adaptation
- Work with custom checkpoints
- Fine-tune for specialized use cases (mental health chatbot)

---

## 🔗 Key Resources

### Official Documentation
- **Unsloth GitHub:** https://github.com/unslothai/notebooks/
- **Kaggle Notebooks:** https://github.com/unslothai/notebooks/#-kaggle-notebooks
- **Fine-tuning Guide:** https://docs.unsloth.ai/get-started/fine-tuning-llms-guide
- **RL Guide:** https://docs.unsloth.ai/get-started/reinforcement-learning-rl-guide
- **GRPO Tutorial:** https://docs.unsloth.ai/get-started/reinforcement-learning-rl-guide/tutorial-train-your-own-reasoning-model-with-grpo
- **Continued Pretraining:** https://docs.unsloth.ai/basics/continued-pretraining
- **Ollama Export:** https://docs.unsloth.ai/tutorials/how-to-finetune-llama-3-and-export-to-ollama

### Helpful Articles
- **LoRA with Ollama:** https://sarinsuriyakoon.medium.com/unsloth-lora-with-ollama-lightweight-solution-to-full-cycle-llm-development-edadb6d9e0f0
- **Mental Health Chatbot:** https://medium.com/@mauryaanoop3/fine-tuning-microsoft-phi3-with-unsloth-for-mental-health-chatbot-development-ddea4e0c46e7
- **R1 Reasoning Blog:** https://unsloth.ai/blog/r1-reasoning

### Supported Models
- Llama 3.1 (8B)
- Mistral NeMo (12B)
- Gemma 2 (9B)
- Phi-3.5 (mini)
- Llama 3 (8B)
- Mistral v0.3 (7B)
- Phi-3 (medium)
- Qwen2 (7B)
- Gemma 2 (2B)
- SmolLM2 (135M, 360M, 1.7B)
- TinyLlama

---

## 🚀 Quick Start

### Prerequisites
```bash
# Install Unsloth
pip install unsloth

# For Kaggle/Colab
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
```

### Basic Usage Pattern
```python
from unsloth import FastLanguageModel

# Load model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/SmolLM2-135M",
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)

# Configure for training
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,  # LoRA rank
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
)
```

---

## 📊 Comparison: Full Fine-tuning vs LoRA

| Aspect | Full Fine-tuning | LoRA |
|--------|------------------|------|
| **Parameters Updated** | All model parameters | Only LoRA adapters (~1-5% of params) |
| **Memory Usage** | High (requires full model gradients) | Low (only adapter gradients) |
| **Training Speed** | Slower | 2-3x faster |
| **Storage** | Full model checkpoint | Small adapter files (~10-100MB) |
| **Quality** | Potentially higher for large datasets | Comparable for most tasks |
| **Use Case** | Large datasets, domain shift | Quick adaptation, limited resources |

---

## 🎓 Key Concepts

### LoRA (Low-Rank Adaptation)
- Adds trainable rank decomposition matrices to model layers
- Freezes original model weights
- Dramatically reduces trainable parameters
- Enables efficient fine-tuning on consumer hardware

### GRPO (Group Relative Policy Optimization)
- Advanced RL technique for reasoning models
- Generates multiple reasoning traces
- Selects best traces using group-relative rewards
- Enables chain-of-thought capabilities

### DPO (Direct Preference Optimization)
- Simpler alternative to RLHF
- Directly optimizes policy from preference data
- No separate reward model needed
- More stable training

### Chat Templates
- Standardized formats for instruction-following
- Different templates for different model families
- Includes system prompts, user messages, assistant responses
- Critical for proper model behavior

---

## 💡 Best Practices

### Dataset Preparation
- Use high-quality, diverse training data
- Format data according to model's chat template
- Include system prompts for context
- Balance dataset across different task types

### Hyperparameter Tuning
- Start with recommended defaults
- Adjust learning rate based on model size
- Use gradient accumulation for larger effective batch sizes
- Monitor loss curves for overfitting

### Model Selection
- Start with smallest model that works (SmolLM2 135M)
- Scale up only if needed
- Consider task complexity vs model capacity
- Balance performance with inference speed

### Evaluation
- Test on held-out validation set
- Use task-specific metrics
- Perform qualitative analysis
- Compare with baseline models

---

## 🔧 Common Issues & Solutions

### Out of Memory (OOM)
- Reduce batch size
- Enable gradient checkpointing
- Use 4-bit quantization
- Reduce max sequence length

### Slow Training
- Enable gradient accumulation
- Use mixed precision training
- Optimize data loading
- Use faster tokenizers

### Poor Model Performance
- Check data quality and formatting
- Verify chat template is correct
- Increase training steps
- Adjust learning rate

### Export Issues
- Ensure model is properly saved
- Check Ollama compatibility
- Verify quantization settings
- Test exported model before deployment

---

## 📹 Video Requirements

Each colab must include a YouTube video demonstrating:
1. **Code Walkthrough** - Explain each section of the notebook
2. **Dataset Explanation** - Show input format and data structure
3. **Training Process** - Display training logs and metrics
4. **Output Examples** - Demonstrate model inference
5. **Key Learnings** - Highlight important concepts

---

## ✅ Completion Checklist

### Colab 1: Full Fine-tuning
- [ ] SmolLM2 135M model loaded
- [ ] Full fine-tuning configured (full_finetuning=True)
- [ ] Dataset prepared with chat template
- [ ] Training completed successfully
- [ ] Model inference tested
- [ ] Video walkthrough recorded
- [ ] Colab notebook uploaded

### Colab 2: LoRA Fine-tuning
- [ ] Same model and dataset as Colab 1
- [ ] LoRA parameters configured
- [ ] Training completed with LoRA
- [ ] Performance compared with full fine-tuning
- [ ] Memory usage analyzed
- [ ] Video walkthrough recorded
- [ ] Colab notebook uploaded

### Colab 3: Reinforcement Learning
- [ ] Preference dataset loaded (chosen/rejected pairs)
- [ ] DPO training configured
- [ ] Model aligned with preferences
- [ ] Before/after comparison shown
- [ ] Video walkthrough recorded
- [ ] Colab notebook uploaded

### Colab 4: GRPO Reasoning
- [ ] Problem dataset prepared
- [ ] GRPO training implemented
- [ ] Reasoning traces generated
- [ ] Chain-of-thought demonstrated
- [ ] Video walkthrough recorded
- [ ] Colab notebook uploaded

### Colab 5: Continued Pretraining
- [ ] New language dataset prepared
- [ ] Continued pretraining configured
- [ ] Model learns new language/domain
- [ ] Custom checkpoint used (optional)
- [ ] Ollama export demonstrated
- [ ] Video walkthrough recorded
- [ ] Colab notebook uploaded

---

## 🎯 Grading Criteria

Each colab will be evaluated on:
- **Code Quality** (20%) - Clean, well-documented code
- **Execution** (20%) - Notebook runs successfully
- **Understanding** (30%) - Video demonstrates clear understanding
- **Results** (20%) - Model produces expected outputs
- **Documentation** (10%) - README and comments are thorough

---

## 📝 Submission Guidelines

1. Complete all 5 colab notebooks
2. Record detailed video walkthrough for each
3. Upload videos to YouTube
4. Include video links in respective README files
5. Ensure all notebooks run successfully
6. Document any issues or modifications
7. Submit repository link with all artifacts

---

## 🔗 Additional Resources

### Community & Support
- Unsloth Discord: https://discord.gg/unsloth
- GitHub Issues: https://github.com/unslothai/unsloth/issues
- Kaggle Community: https://www.kaggle.com/discussions

### Advanced Topics
- Multi-GPU training
- Custom model architectures
- Advanced LoRA configurations
- Production deployment strategies
- Model quantization techniques

---

**Last Updated:** November 2025
**Course:** CMPE-297 Special Topics
**Instructor:** [Instructor Name]
**Assignment:** Modern AI with Unsloth.ai

