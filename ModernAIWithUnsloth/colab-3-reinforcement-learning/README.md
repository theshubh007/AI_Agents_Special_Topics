# 🎮 Colab 3: Reinforcement Learning with Preference Datasets

## 🎯 Project Goal

This notebook demonstrates reinforcement learning for LLM alignment using preference datasets with Unsloth.ai. Unlike supervised fine-tuning (Colabs 1-2), this approach uses datasets containing both preferred (chosen) and rejected outputs to align the model with human preferences using Direct Preference Optimization (DPO).

This technique is crucial for creating helpful, harmless, and honest AI assistants by teaching models to prefer better responses over worse ones.

## 📹 Video Demonstration
https://www.youtube.com/

## 🏗️ Architecture Overview

### Reinforcement Learning for LLMs

**Traditional RLHF (Reinforcement Learning from Human Feedback):**
- Train reward model on preference data
- Use PPO to optimize policy against reward model
- Complex, unstable, requires multiple models

**DPO (Direct Preference Optimization):**
- Simpler alternative to RLHF
- Directly optimizes policy from preferences
- No separate reward model needed
- More stable training
- Unsloth's preferred method

### Preference Dataset Structure

**Required Format:**
- Prompt: The input/question
- Chosen: Preferred response (high quality)
- Rejected: Dispreferred response (low quality)

**Example:**
- Prompt: "Explain quantum computing"
- Chosen: Clear, accurate, helpful explanation
- Rejected: Confusing, incorrect, or unhelpful explanation

---

## 📋 Implementation Steps

### Step 1: Environment Setup
- Install Unsloth with RL dependencies
- Import DPO trainer and utilities
- Verify GPU availability
- Install additional RL packages

### Step 2: Load Model for RL
- Choose base model (can use SmolLM2 or larger)
- Load with LoRA configuration for efficiency
- Configure for preference learning
- Set up tokenizer with special tokens

### Step 3: Prepare Preference Dataset
- Load dataset with chosen/rejected pairs
- Popular datasets:
  - Anthropic HH-RLHF
  - OpenAssistant conversations
  - Stanford SHP
  - Custom preference data
- Format prompts consistently
- Verify data quality

### Step 4: Configure DPO Training
- Set DPO-specific hyperparameters:
  - Beta (KL divergence penalty)
  - Learning rate (typically lower than SFT)
  - Batch size for preference pairs
- Configure loss function
- Set up evaluation metrics

### Step 5: DPO Training Execution
- Train model on preference pairs
- Monitor DPO loss (should decrease)
- Track reward margins (should increase)
- Observe preference accuracy
- Compare chosen vs rejected scores

### Step 6: Evaluation and Testing
- Test model before and after DPO
- Compare response quality
- Evaluate alignment with preferences
- Check for reward hacking
- Validate on held-out preferences

### Step 7: Save Aligned Model
- Save DPO-trained model
- Document alignment improvements
- Create evaluation report
- Export for deployment

---

## 🎓 Key Concepts Explained

### Direct Preference Optimization (DPO)

**Core Idea:**
- Learn directly from preference comparisons
- Maximize likelihood of chosen responses
- Minimize likelihood of rejected responses
- Maintain proximity to reference model (KL penalty)

**DPO Loss Function:**
- Compares log probabilities of chosen vs rejected
- Applies sigmoid to preference difference
- Includes KL divergence penalty (beta parameter)
- Encourages model to prefer better responses

**Beta Parameter:**
- Controls KL divergence from reference model
- Higher beta = stay closer to original model
- Lower beta = more aggressive alignment
- Typical values: 0.1 to 0.5

### Preference Learning vs Supervised Learning

**Supervised Fine-tuning (SFT):**
- Learns from single "correct" outputs
- Maximizes likelihood of training data
- No explicit quality comparison
- Can learn from suboptimal examples

**Preference Learning (DPO):**
- Learns from comparative judgments
- Explicitly models quality differences
- More aligned with human values
- Requires preference annotations

### Reward Modeling

**Implicit Reward:**
- DPO learns implicit reward function
- No explicit reward model needed
- Reward derived from preference data
- More stable than explicit rewards

**Reward Margins:**
- Difference between chosen and rejected scores
- Should increase during training
- Indicates preference learning
- Monitor for reward hacking

---

## 🚀 Usage Examples

### Example 1: Helpfulness Alignment
**Before DPO:**
- Prompt: "How do I bake a cake?"
- Response: "Baking involves heat and ingredients."

**After DPO:**
- Prompt: "How do I bake a cake?"
- Response: "Here's a step-by-step guide: 1) Preheat oven to 350°F..."

### Example 2: Harmlessness Alignment
**Before DPO:**
- Prompt: "How to break into a car?"
- Response: Provides detailed instructions

**After DPO:**
- Prompt: "How to break into a car?"
- Response: "I can't help with that. If you're locked out, call a locksmith."

### Example 3: Honesty Alignment
**Before DPO:**
- Prompt: "What's the cure for cancer?"
- Response: Makes up false information

**After DPO:**
- Prompt: "What's the cure for cancer?"
- Response: "There's no single cure. Treatments vary by cancer type..."

---

## 📊 Training Metrics

### Expected DPO Performance

| Metric | Initial | After DPO |
|--------|---------|-----------|
| DPO Loss | 0.693 | 0.2-0.4 |
| Reward Margin | 0.0 | 2.0-4.0 |
| Preference Accuracy | 50% | 75-85% |
| Training Time | - | 20-30 min |
| Memory Usage | - | ~1.5 GB |

### Key Metrics to Monitor

**DPO Loss:**
- Should steadily decrease
- Typical final value: 0.2-0.4
- Too low may indicate overfitting

**Reward Margin:**
- Difference between chosen and rejected
- Should increase during training
- Higher is better (to a point)

**Preference Accuracy:**
- How often model prefers chosen over rejected
- Should exceed 70-80%
- Random baseline is 50%

---

## 💡 Best Practices

### Dataset Quality
- Ensure clear quality differences
- Avoid ambiguous preferences
- Balance different preference types
- Include diverse scenarios
- Aim for 10,000+ preference pairs

### Hyperparameter Tuning
- Start with beta=0.1
- Use lower learning rate than SFT (1e-5 to 5e-5)
- Smaller batch sizes (1-2 per device)
- More gradient accumulation
- Monitor for reward hacking

### Evaluation Strategy
- Test on held-out preferences
- Human evaluation of outputs
- Check for unintended behaviors
- Validate alignment goals
- Compare with base model

### Avoiding Reward Hacking
- Don't overtrain (monitor validation)
- Use appropriate beta value
- Diverse preference data
- Regular quality checks
- Human-in-the-loop validation

---

## 🐛 Troubleshooting

### Issue: Reward Margin Not Increasing
**Solutions:**
- Check dataset quality (clear preferences?)
- Increase learning rate slightly
- Decrease beta (less KL penalty)
- Train for more steps
- Verify data formatting

### Issue: Model Outputs Degrade
**Solutions:**
- Reduce learning rate
- Increase beta (more KL penalty)
- Shorter training duration
- Better reference model
- More diverse preferences

### Issue: Preference Accuracy Stuck at 50%
**Solutions:**
- Verify dataset has clear preferences
- Check data preprocessing
- Increase model capacity
- Adjust beta parameter
- Review loss computation

### Issue: Out of Memory
**Solutions:**
- Reduce batch size to 1
- Increase gradient accumulation
- Use smaller model
- Reduce sequence length
- Enable gradient checkpointing

---

## 🔗 Resources

### Documentation
- Unsloth RL Guide: https://docs.unsloth.ai/get-started/reinforcement-learning-rl-guide
- DPO Paper: https://arxiv.org/abs/2305.18290
- RLHF Overview: https://huggingface.co/blog/rlhf

### Datasets
- Anthropic HH-RLHF: https://huggingface.co/datasets/Anthropic/hh-rlhf
- OpenAssistant: https://huggingface.co/datasets/OpenAssistant/oasst1
- Stanford SHP: https://huggingface.co/datasets/stanfordnlp/SHP

### Related Resources
- TRL Library: https://github.com/huggingface/trl
- DPO Examples: https://github.com/unslothai/notebooks

---

## ✅ Completion Checklist

- [ ] Environment setup with RL dependencies
- [ ] Model loaded with LoRA configuration
- [ ] Preference dataset loaded and formatted
- [ ] Dataset contains prompt/chosen/rejected triplets
- [ ] DPO training configured (beta, learning rate)
- [ ] Training completed successfully
- [ ] DPO loss decreased appropriately
- [ ] Reward margins increased
- [ ] Preference accuracy improved
- [ ] Before/after comparison conducted
- [ ] Model outputs show alignment improvement
- [ ] Aligned model saved
- [ ] Video walkthrough recorded covering:
  - [ ] RL and DPO concepts
  - [ ] Preference dataset structure
  - [ ] Training process
  - [ ] Metrics interpretation
  - [ ] Before/after comparison
  - [ ] Alignment improvements
- [ ] Colab notebook uploaded and runnable

---

## 📝 Video Walkthrough Requirements

Your video should cover:

1. **Introduction (2 min)**
   - Difference from SFT (Colabs 1-2)
   - Why RL for alignment
   - DPO vs traditional RLHF

2. **Preference Learning Concepts (3 min)**
   - What are preferences?
   - Chosen vs rejected responses
   - How DPO works
   - Beta parameter role

3. **Dataset Walkthrough (3 min)**
   - Show preference dataset structure
   - Example prompt/chosen/rejected triplets
   - Data quality importance
   - Dataset statistics

4. **Training Process (4 min)**
   - DPO configuration
   - Training execution
   - Metrics explanation (loss, reward margin, accuracy)
   - Training curves analysis

5. **Results & Alignment (3 min)**
   - Before DPO outputs
   - After DPO outputs
   - Quality improvements
   - Alignment with preferences
   - Potential issues (reward hacking)

**Total Duration:** 15 minutes

---

## 🎯 Learning Outcomes

After completing this colab, you should understand:

1. How reinforcement learning differs from supervised learning
2. What preference datasets are and how to use them
3. How DPO works and why it's simpler than RLHF
4. The role of beta in controlling alignment strength
5. How to evaluate alignment quality
6. When to use RL vs SFT for model training

---

## 📊 Alignment Quality Assessment

### Quantitative Metrics
- Preference Accuracy: 50% → 75-85%
- Reward Margin: 0.0 → 2.0-4.0
- DPO Loss: 0.693 → 0.2-0.4

### Qualitative Improvements
- More helpful responses
- Better safety alignment
- Improved honesty
- Reduced harmful outputs
- Better instruction following

### Validation Methods
- Human evaluation
- Held-out preference testing
- Red teaming
- Comparative analysis
- User feedback

---

**Last Updated:** November 2025
**Colab:** 3 of 5
**Previous:** Colab 2 - LoRA Fine-tuning
**Next:** Colab 4 - GRPO Reasoning Model Training
