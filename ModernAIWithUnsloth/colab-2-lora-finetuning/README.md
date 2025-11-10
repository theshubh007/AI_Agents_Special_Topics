# 🎯 Colab 2: LoRA Parameter-Efficient Fine-tuning

## 🎯 Project Goal

This notebook demonstrates LoRA (Low-Rank Adaptation) parameter-efficient fine-tuning using the same SmolLM2 135M model and dataset from Colab 1. The goal is to compare LoRA's efficiency with full fine-tuning in terms of memory usage, training speed, and model quality.

LoRA enables fine-tuning large language models by training only small adapter matrices while keeping the base model frozen, dramatically reducing memory requirements and training time.

## 📹 Video Demonstration
https://www.youtube.com/

## 🏗️ Architecture Overview

### LoRA Fundamentals

**What is LoRA?**
- Low-Rank Adaptation of Large Language Models
- Adds trainable rank decomposition matrices to model layers
- Freezes original pre-trained weights
- Only trains small adapter matrices
- Reduces trainable parameters by 90-99%

**How LoRA Works:**
- Original weight matrix: W (frozen)
- LoRA adds: ΔW = BA (trainable)
- Final output: Wx + BAx
- B and A are low-rank matrices (rank r << model dimension)

### LoRA vs Full Fine-tuning Comparison

| Aspect | Full Fine-tuning | LoRA |
|--------|------------------|------|
| Trainable Params | 135M (100%) | ~1-5M (1-5%) |
| Memory Usage | ~2.7 GB | ~1.2 GB |
| Training Speed | Baseline | 2-3x faster |
| Checkpoint Size | ~540 MB | ~10-50 MB |
| Quality | Potentially higher | Comparable |

---

## 📋 Implementation Steps

### Step 1: Environment Setup
- Install Unsloth with same dependencies as Colab 1
- Import required libraries
- Verify GPU availability

### Step 2: Load Model with LoRA Configuration
- Load same SmolLM2-135M-Instruct model
- Configure LoRA parameters:
  - r = 16 (LoRA rank)
  - lora_alpha = 16 (scaling factor)
  - target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]
  - lora_dropout = 0
- Do NOT call to_full_finetune() (keep LoRA adapters)

### Step 3: Dataset Preparation
- Use SAME dataset as Colab 1 (Alpaca cleaned)
- Use SAME chat template formatting
- Ensure identical data preprocessing
- This enables fair comparison

### Step 4: Training Configuration
- Use similar hyperparameters as Colab 1
- Same learning rate (2e-4)
- Same batch size and gradient accumulation
- Same number of training steps
- Monitor memory usage difference

### Step 5: Training Execution
- Start LoRA training
- Compare training speed with Colab 1
- Monitor loss curve
- Track memory consumption
- Note faster iteration time

### Step 6: Inference Testing
- Test with SAME examples as Colab 1
- Compare output quality
- Measure inference speed
- Evaluate performance differences

### Step 7: Save and Compare
- Save LoRA adapters (much smaller files)
- Compare checkpoint sizes
- Document performance metrics
- Create comparison table

---

## 🎓 Key Concepts Explained

### LoRA Parameters

**Rank (r):**
- Controls adapter matrix dimensions
- Higher rank = more capacity, more parameters
- Typical values: 8, 16, 32, 64
- r=16 is good balance for most tasks

**Alpha (lora_alpha):**
- Scaling factor for LoRA updates
- Usually set equal to rank
- Controls magnitude of adapter contribution
- Higher alpha = stronger adaptation

**Target Modules:**
- Which layers get LoRA adapters
- Common: attention projection layers (q, k, v, o)
- Can also target MLP layers
- More modules = more parameters

**Dropout:**
- Regularization for LoRA layers
- Usually set to 0 for small models
- Can use 0.05-0.1 for larger models

### Memory Efficiency

**Why LoRA Uses Less Memory:**
- Base model weights frozen (no gradients)
- Only adapter gradients computed
- Smaller optimizer states
- Reduced activation memory

**Memory Breakdown:**
- Model weights: ~540 MB (same as full)
- Gradients: ~50 MB (only adapters)
- Optimizer states: ~100 MB (only adapters)
- Activations: ~500 MB (with checkpointing)
- Total: ~1.2 GB VRAM (vs 2.7 GB full)

### Training Speed

**Why LoRA is Faster:**
- Fewer parameters to update
- Smaller gradient computations
- Faster backward pass
- Less optimizer overhead
- Typically 2-3x faster per step

---

## 🚀 Usage Examples

### Example 1: Coding Task
- Same prompt as Colab 1
- Compare output quality
- Evaluate code correctness
- Note any differences

### Example 2: Question Answering
- Same factual questions
- Compare accuracy
- Check response formatting
- Assess knowledge retention

### Example 3: Text Summarization
- Same long text inputs
- Compare summary quality
- Evaluate coherence
- Check key point coverage

---

## 📊 Training Metrics & Comparison

### Expected LoRA Performance

| Metric | Full Fine-tuning | LoRA |
|--------|------------------|------|
| Training Time | 10-15 min | 5-8 min |
| Final Loss | 0.5-1.0 | 0.5-1.0 |
| Memory Usage | ~2.7 GB | ~1.2 GB |
| Tokens/Second | 1000-1500 | 2000-3000 |
| Checkpoint Size | ~540 MB | ~20 MB |
| Trainable Params | 135M | ~2M |

### Quality Comparison
- LoRA typically achieves 95-99% of full fine-tuning quality
- Differences most noticeable on complex reasoning tasks
- For most practical applications, LoRA is sufficient
- Significant efficiency gains justify minor quality tradeoff

---

## 💡 Best Practices

### LoRA Hyperparameter Selection

**For Small Models (< 1B params):**
- r = 8-16
- alpha = r
- Target attention layers only

**For Medium Models (1-7B params):**
- r = 16-32
- alpha = r or 2*r
- Target attention + some MLP layers

**For Large Models (7B+ params):**
- r = 32-64
- alpha = r or 2*r
- Target all attention and MLP layers

### When to Use LoRA
- Limited GPU memory available
- Quick experimentation needed
- Multiple task-specific adapters
- Frequent model updates
- Good enough quality acceptable

### When to Use Full Fine-tuning
- Maximum quality required
- Significant domain shift
- Abundant compute resources
- Single-task specialization

---

## 🐛 Troubleshooting

### Issue: LoRA Not Training
**Solutions:**
- Verify r > 0 (not 0 like full fine-tuning)
- Check target_modules are correct
- Ensure NOT calling to_full_finetune()
- Verify adapters are trainable

### Issue: Poor Quality vs Full Fine-tuning
**Solutions:**
- Increase LoRA rank (r)
- Increase alpha
- Add more target modules
- Train for more steps
- Adjust learning rate

### Issue: Still Running Out of Memory
**Solutions:**
- Reduce batch size further
- Decrease sequence length
- Lower LoRA rank
- Enable more aggressive checkpointing

---

## 🔗 Resources

### Documentation
- LoRA Paper: https://arxiv.org/abs/2106.09685
- Unsloth LoRA Guide: https://docs.unsloth.ai/get-started/fine-tuning-llms-guide
- LoRA with Ollama: https://sarinsuriyakoon.medium.com/unsloth-lora-with-ollama-lightweight-solution-to-full-cycle-llm-development-edadb6d9e0f0

### Related Resources
- PEFT Library: https://github.com/huggingface/peft
- LoRA Examples: https://github.com/unslothai/notebooks

---

## ✅ Completion Checklist

- [ ] Environment setup complete
- [ ] SmolLM2 135M model loaded with LoRA config
- [ ] LoRA parameters configured (r=16, alpha=16)
- [ ] SAME dataset as Colab 1 used
- [ ] Training completed successfully
- [ ] Memory usage compared with Colab 1
- [ ] Training speed compared with Colab 1
- [ ] Inference tested with same examples
- [ ] Output quality compared
- [ ] LoRA adapters saved
- [ ] Comparison table created
- [ ] Video walkthrough recorded covering:
  - [ ] LoRA concept explanation
  - [ ] Configuration differences from Colab 1
  - [ ] Training process and metrics
  - [ ] Performance comparison
  - [ ] When to use LoRA vs full fine-tuning
- [ ] Colab notebook uploaded and runnable

---

## 📝 Video Walkthrough Requirements

Your video should cover:

1. **Introduction (2 min)**
   - Recap Colab 1 (full fine-tuning)
   - Introduce LoRA concept
   - Preview efficiency gains

2. **LoRA Explanation (3 min)**
   - How LoRA works (low-rank matrices)
   - Parameter efficiency benefits
   - Memory and speed advantages
   - When to use LoRA

3. **Configuration Walkthrough (3 min)**
   - LoRA parameters (r, alpha, target_modules)
   - Differences from Colab 1 setup
   - Same dataset usage for fair comparison
   - Training configuration

4. **Training & Comparison (4 min)**
   - Show training execution
   - Compare memory usage (2.7 GB → 1.2 GB)
   - Compare training speed (2-3x faster)
   - Compare loss curves
   - Show checkpoint size difference

5. **Results & Analysis (3 min)**
   - Test same examples as Colab 1
   - Compare output quality
   - Discuss quality vs efficiency tradeoff
   - Recommendations for when to use each method

**Total Duration:** 15 minutes

---

## 🎯 Learning Outcomes

After completing this colab, you should understand:

1. How LoRA achieves parameter-efficient fine-tuning
2. The role of rank, alpha, and target modules
3. Memory and speed advantages of LoRA
4. Quality comparison with full fine-tuning
5. When to choose LoRA vs full fine-tuning
6. How to configure and train LoRA adapters

---

## 📊 Detailed Comparison Summary

### Quantitative Metrics
- Memory Reduction: 56% (2.7 GB → 1.2 GB)
- Speed Improvement: 2-3x faster
- Parameter Reduction: 98.5% (135M → 2M trainable)
- Storage Reduction: 96% (540 MB → 20 MB)

### Qualitative Assessment
- Output Quality: 95-99% of full fine-tuning
- Task Performance: Comparable for most tasks
- Generalization: Similar to full fine-tuning
- Stability: More stable training

### Recommendation
For most practical applications with limited resources, LoRA provides the best balance of efficiency and quality. Use full fine-tuning only when maximum quality is critical and resources are abundant.

---

**Last Updated:** November 2025
**Colab:** 2 of 5
**Previous:** Colab 1 - Full Fine-tuning
**Next:** Colab 3 - Reinforcement Learning with Preferences
