# 🔥 Colab 1: Full Fine-tuning with SmolLM2 135M

## 🎯 Project Goal

This notebook demonstrates full parameter fine-tuning using Unsloth.ai with the SmolLM2 135M model. Unlike parameter-efficient methods like LoRA, full fine-tuning updates all model parameters, providing maximum adaptation capability at the cost of higher memory and compute requirements.

The implementation showcases how to properly configure Unsloth for full fine-tuning, prepare datasets with chat templates, and train a small but capable language model for instruction-following tasks.

## 📹 Video Demonstration
https://www.youtube.com/

## 🏗️ Architecture Overview

### Model Selection: SmolLM2 135M

**Why SmolLM2 135M?**
- Smallest model in the SmolLM2 family (135 million parameters)
- Fast training and inference on consumer hardware
- Suitable for learning fine-tuning fundamentals
- Good baseline for comparing with LoRA in Colab 2

**Model Specifications:**
- Parameters: 135M
- Context Length: 2048 tokens
- Architecture: Transformer-based
- Quantization: 4-bit support for memory efficiency

### Full Fine-tuning vs LoRA

**Full Fine-tuning:**
- Updates ALL 135M parameters
- Requires more memory (stores gradients for all params)
- Potentially better performance with sufficient data
- Longer training time
- Larger checkpoint files

**When to Use Full Fine-tuning:**
- Large, high-quality datasets available
- Significant domain shift from base model
- Maximum performance is critical
- Sufficient compute resources available

---

## 📋 Implementation Steps

### Step 1: Environment Setup
- Install Unsloth with colab dependencies
- Import FastLanguageModel, torch, datasets, trl, transformers
- Verify GPU availability

### Step 2: Load Model with Full Fine-tuning Configuration
- Load SmolLM2-135M-Instruct model
- Configure max sequence length (2048 tokens)
- Enable 4-bit quantization for memory efficiency
- Set r=0 for full fine-tuning (not LoRA)
- Call model.to_full_finetune() to enable full parameter updates

### Step 3: Dataset Preparation
- Load instruction-following dataset (e.g., Alpaca cleaned)
- Define chat template format (Instruction/Input/Response)
- Create formatting function to structure prompts
- Apply formatting to entire dataset
- Add EOS tokens appropriately

### Step 4: Training Configuration
- Set batch size (2) and gradient accumulation (4)
- Configure learning rate (2e-4 for full fine-tuning)
- Enable mixed precision (fp16 or bf16)
- Use memory-efficient optimizer (adamw_8bit)
- Set warmup steps and max training steps
- Initialize SFTTrainer with configuration

### Step 5: Training Execution
- Start training process
- Monitor loss curve during training
- Track training time and samples per second
- Observe memory usage
- Wait for training completion

### Step 6: Inference Testing
- Switch model to inference mode
- Test with coding tasks (e.g., factorial function)
- Test with question answering
- Test with text summarization
- Compare outputs with base model

### Step 7: Save Model
- Save fine-tuned model locally
- Save tokenizer configuration
- Optionally push to Hugging Face Hub
- Document model performance

---

## 🎓 Key Concepts Explained

### Full Fine-tuning Mechanics

**Parameter Updates:**
- Total Parameters: 135,000,000
- Trainable Parameters: 135,000,000 (100%)
- Frozen Parameters: 0 (0%)

**Memory Requirements:**
- Model weights: ~540 MB (4-bit quantized)
- Gradients: ~540 MB
- Optimizer states: ~1.08 GB
- Activations: ~500 MB (with gradient checkpointing)
- Total: ~2.7 GB VRAM

### Chat Template Formats

**Alpaca Format:**
- Instruction: Task description
- Input: Optional context
- Response: Model output

**ChatML Format:**
- System message with role tags
- User message with role tags
- Assistant response with role tags

**Llama 3 Format:**
- Begin of text marker
- Header IDs for each role
- End of turn tokens

### Gradient Checkpointing

Unsloth's gradient checkpointing reduces memory by:
- Not storing all intermediate activations
- Recomputing activations during backward pass
- Trading compute for memory
- Enabling larger batch sizes

---

## 🚀 Usage Examples

### Example 1: Coding Task
- Instruction: Write a Python function to calculate factorial
- Expected: Recursive or iterative factorial implementation
- Demonstrates code generation capability

### Example 2: Question Answering
- Instruction: What is the capital of France?
- Expected: The capital of France is Paris
- Demonstrates factual knowledge retention

### Example 3: Text Summarization
- Instruction: Summarize the following text
- Input: Long text about AI
- Expected: Concise summary of key points
- Demonstrates comprehension and synthesis

---

## 📊 Training Metrics

### Expected Performance

| Metric | Value |
|--------|-------|
| Training Time | 10-15 minutes (60 steps) |
| Final Loss | 0.5-1.0 |
| Memory Usage | ~2.7 GB VRAM |
| Tokens/Second | 1000-1500 |
| Checkpoint Size | ~540 MB |

### Loss Curve Analysis
- Initial loss: ~2.5
- Rapid decrease in first 20 steps
- Gradual convergence after step 30
- Final loss: ~0.5-0.6
- Monitor for overfitting signs

---

## 💡 Best Practices

### Dataset Quality
- Use clean, well-formatted data
- Remove duplicates and low-quality examples
- Balance different task types
- Aim for 1000+ high-quality examples

### Hyperparameter Tuning
- Start with learning rate 2e-4
- Adjust batch size based on memory
- Use gradient accumulation for larger effective batch size
- Monitor loss curve for overfitting

### Memory Optimization
- Enable 4-bit quantization
- Use gradient checkpointing
- Reduce batch size if OOM
- Clear cache between runs

### Evaluation
- Test on diverse prompts
- Compare with base model
- Check for catastrophic forgetting
- Validate on held-out test set

---

## 🐛 Troubleshooting

### Issue: Out of Memory (OOM)
**Solutions:**
- Reduce batch size to 1
- Increase gradient accumulation to 8
- Reduce sequence length to 1024
- Enable aggressive gradient checkpointing

### Issue: Slow Training
**Solutions:**
- Enable mixed precision training
- Optimize data loading with more workers
- Use faster optimizer (adamw_8bit)
- Reduce logging frequency

### Issue: Poor Model Quality
**Solutions:**
- Increase training steps
- Improve dataset quality
- Adjust learning rate
- Add more diverse examples
- Verify chat template formatting

---

## 🔗 Resources

### Documentation
- Unsloth Full Fine-tuning Guide: https://docs.unsloth.ai/get-started/fine-tuning-llms-guide
- SmolLM2 Model Card: https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct
- Alpaca Dataset: https://huggingface.co/datasets/yahma/alpaca-cleaned

### Related Notebooks
- Unsloth Examples: https://github.com/unslothai/notebooks
- Kaggle Notebooks: https://www.kaggle.com/code/kingabzpro/fine-tuning-llms-using-unsloth

---

## ✅ Completion Checklist

- [ ] Environment setup complete
- [ ] SmolLM2 135M model loaded
- [ ] Full fine-tuning configured (r=0, to_full_finetune())
- [ ] Dataset prepared with proper chat template
- [ ] Training completed successfully
- [ ] Loss curve shows convergence
- [ ] Inference tested with multiple examples
- [ ] Model saved locally
- [ ] Video walkthrough recorded covering:
  - [ ] Code explanation
  - [ ] Dataset format
  - [ ] Training process
  - [ ] Output examples
  - [ ] Key learnings
- [ ] Colab notebook uploaded and runnable

---

## 📝 Video Walkthrough Requirements

Your video should cover:

1. **Introduction (2 min)**
   - Explain full fine-tuning concept
   - Why SmolLM2 135M was chosen
   - Comparison with LoRA (preview Colab 2)

2. **Code Walkthrough (5 min)**
   - Model loading and configuration
   - Full fine-tuning setup (r=0, to_full_finetune())
   - Dataset preparation and chat template
   - Training arguments explanation

3. **Training Process (3 min)**
   - Show training execution
   - Explain loss curve
   - Discuss memory usage
   - Training time analysis

4. **Results & Inference (3 min)**
   - Demonstrate model outputs
   - Compare with base model
   - Show different task types
   - Discuss quality

5. **Key Learnings (2 min)**
   - Full fine-tuning vs LoRA tradeoffs
   - When to use full fine-tuning
   - Memory and compute considerations
   - Next steps for Colab 2

**Total Duration:** 15 minutes

---

## 🎯 Learning Outcomes

After completing this colab, you should understand:

1. How to configure Unsloth for full parameter fine-tuning
2. The difference between full fine-tuning and LoRA
3. How to prepare datasets with chat templates
4. Memory and compute requirements for full fine-tuning
5. When full fine-tuning is preferred over LoRA
6. How to evaluate and test fine-tuned models

---

**Last Updated:** November 2025
**Colab:** 1 of 5
**Next:** Colab 2 - LoRA Fine-tuning (same model, compare results)

