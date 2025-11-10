# 🌍 Colab 5: Continued Pretraining for New Languages

## 🎯 Project Goal

This notebook demonstrates continued pretraining using Unsloth.ai to teach an LLM a new language or domain-specific knowledge. Unlike fine-tuning (Colabs 1-2) which adapts behavior, continued pretraining extends the model's fundamental knowledge base by training on raw text data.

Additionally, this colab covers fine-tuning from custom checkpoints, specialized use cases (mental health chatbot), and exporting models to Ollama for local inference.

## 📹 Video Demonstration
https://www.youtube.com/

## 🏗️ Architecture Overview

### Continued Pretraining vs Fine-tuning

**Fine-tuning (Colabs 1-2):**
- Adapts existing knowledge
- Uses instruction-response pairs
- Teaches task-specific behavior
- Relatively small datasets (1K-100K examples)
- Short training (minutes to hours)

**Continued Pretraining:**
- Extends knowledge base
- Uses raw text data
- Teaches new language/domain
- Large datasets (millions of tokens)
- Longer training (hours to days)

### Use Cases for Continued Pretraining

**New Language Learning:**
- Teach model a low-resource language
- Extend multilingual capabilities
- Improve language-specific performance

**Domain Adaptation:**
- Medical knowledge
- Legal terminology
- Scientific literature
- Technical documentation
- Industry-specific jargon

**Knowledge Updates:**
- Recent events
- New terminology
- Updated facts
- Current trends

---

## 📋 Implementation Steps

### Step 1: Environment Setup
- Install Unsloth with pretraining dependencies
- Import required libraries
- Verify GPU availability
- Set up data processing tools

### Step 2: Load Base Model
- Choose appropriate base model
- Consider model size vs training time
- Load with efficient configuration
- Prepare for continued pretraining

### Step 3: Prepare Pretraining Data
- Collect raw text in target language/domain
- Clean and preprocess text
- Tokenize data
- Create training chunks
- Aim for millions of tokens

### Step 4: Configure Pretraining
- Set longer context windows
- Use causal language modeling objective
- Configure learning rate schedule
- Set appropriate batch sizes
- Plan for longer training duration

### Step 5: Execute Continued Pretraining
- Train on raw text data
- Monitor perplexity metrics
- Track loss convergence
- Validate on held-out data
- Save checkpoints regularly

### Step 6: Fine-tune from Custom Checkpoint
- Load pretrained checkpoint
- Apply task-specific fine-tuning
- Use instruction data for target use case
- Example: Mental health chatbot
- Combine domain knowledge with task behavior

### Step 7: Export to Ollama
- Convert model to GGUF format
- Quantize for efficiency
- Create Ollama modelfile
- Test local inference
- Deploy for production use

---

## 🎓 Key Concepts Explained

### Continued Pretraining Mechanics

**Training Objective:**
- Causal language modeling (predict next token)
- Same objective as original pretraining
- No instruction formatting needed
- Raw text input

**Data Requirements:**
- Large volume (millions of tokens)
- High quality, clean text
- Representative of target domain
- Diverse examples

**Training Duration:**
- Much longer than fine-tuning
- Hours to days depending on data size
- Multiple epochs over data
- Regular checkpoint saving

### Language Learning Process

**Phase 1: Vocabulary Expansion**
- Model learns new tokens
- Character patterns recognized
- Word boundaries identified

**Phase 2: Grammar Acquisition**
- Syntactic patterns learned
- Language structure internalized
- Grammar rules implicit

**Phase 3: Semantic Understanding**
- Meaning associations formed
- Context comprehension
- Cultural knowledge embedded

### Custom Checkpoint Fine-tuning

**Why Use Custom Checkpoints:**
- Build on domain-specific knowledge
- Combine pretraining + fine-tuning
- Better performance on specialized tasks
- Efficient knowledge transfer

**Mental Health Chatbot Example:**
- Pretrain on mental health literature
- Fine-tune on counseling conversations
- Combine domain knowledge with empathy
- Specialized, helpful responses

---

## 🚀 Usage Examples

### Example 1: New Language Learning

**Before Continued Pretraining:**
- Prompt (in target language): "Translate: Hello"
- Response: Gibberish or English

**After Continued Pretraining:**
- Prompt (in target language): "Translate: Hello"
- Response: Correct translation in target language

### Example 2: Domain Adaptation (Medical)

**Before Domain Pretraining:**
- Prompt: "Explain myocardial infarction"
- Response: Generic, possibly incorrect

**After Medical Pretraining:**
- Prompt: "Explain myocardial infarction"
- Response: Accurate medical explanation with proper terminology

### Example 3: Mental Health Chatbot

**Base Model:**
- User: "I'm feeling anxious"
- Response: Generic advice

**After Custom Checkpoint + Fine-tuning:**
- User: "I'm feeling anxious"
- Response: Empathetic, informed, helpful guidance with mental health awareness

---

## 📊 Training Metrics

### Expected Pretraining Performance

| Metric | Initial | After Pretraining |
|--------|---------|-------------------|
| Perplexity | High (100+) | Lower (20-40) |
| Loss | High (4-5) | Lower (2-3) |
| Training Time | - | 2-8 hours |
| Data Size | - | 10M-100M tokens |
| Memory Usage | - | 3-6 GB |

### Evaluation Metrics

**Perplexity:**
- Measures prediction confidence
- Lower is better
- Should decrease during training
- Target: 20-40 for good performance

**Loss:**
- Cross-entropy loss
- Should steadily decrease
- Monitor for overfitting
- Validate on held-out data

**Language Proficiency:**
- Grammar correctness
- Vocabulary usage
- Fluency
- Cultural appropriateness

---

## 💡 Best Practices

### Data Collection
- High-quality sources
- Native speaker text (for languages)
- Authoritative sources (for domains)
- Diverse examples
- Clean, preprocessed data

### Training Configuration
- Start with lower learning rate (1e-5)
- Longer warmup period
- Larger batch sizes
- Multiple epochs
- Regular checkpointing

### Evaluation Strategy
- Held-out validation set
- Perplexity tracking
- Qualitative assessment
- Native speaker review (for languages)
- Domain expert review (for specialization)

### Combining with Fine-tuning
- Pretrain first (knowledge)
- Fine-tune second (behavior)
- Use appropriate data for each phase
- Monitor for catastrophic forgetting
- Balance general and specific capabilities

---

## 🔧 Ollama Export Process

### Step 1: Model Conversion
- Convert to GGUF format
- Choose quantization level (Q4, Q5, Q8)
- Balance size vs quality
- Test converted model

### Step 2: Create Modelfile
- Define model parameters
- Set system prompt
- Configure temperature
- Specify stop tokens

### Step 3: Import to Ollama
- Use ollama create command
- Test with ollama run
- Verify outputs
- Deploy locally

### Step 4: Local Inference
- Run without internet
- Fast inference on CPU/GPU
- Privacy-preserving
- Production-ready

---

## 🐛 Troubleshooting

### Issue: High Perplexity Not Decreasing
**Solutions:**
- Check data quality
- Increase training duration
- Adjust learning rate
- Verify tokenization
- Ensure sufficient data volume

### Issue: Model Forgets Original Capabilities
**Solutions:**
- Mix original and new data
- Use lower learning rate
- Shorter training duration
- Regular validation on original tasks
- Catastrophic forgetting mitigation

### Issue: Poor Language Quality
**Solutions:**
- More training data
- Better data quality
- Longer training
- Native speaker data
- Grammar-focused examples

### Issue: Ollama Export Fails
**Solutions:**
- Check model format compatibility
- Verify quantization settings
- Update Ollama version
- Test with smaller model first
- Review conversion logs

---

## 🔗 Resources

### Documentation
- Unsloth Continued Pretraining: https://docs.unsloth.ai/basics/continued-pretraining
- Ollama Export Guide: https://docs.unsloth.ai/tutorials/how-to-finetune-llama-3-and-export-to-ollama
- Mental Health Chatbot: https://medium.com/@mauryaanoop3/fine-tuning-microsoft-phi3-with-unsloth-for-mental-health-chatbot-development-ddea4e0c46e7

### Datasets
- Wikipedia dumps (multilingual)
- Common Crawl (web text)
- Domain-specific corpora
- Medical literature (PubMed)
- Legal documents

### Tools
- Ollama: https://ollama.ai/
- GGUF Conversion: https://github.com/ggerganov/llama.cpp
- Tokenizers: https://github.com/huggingface/tokenizers

---

## ✅ Completion Checklist

- [ ] Environment setup complete
- [ ] Base model loaded
- [ ] Pretraining data collected and preprocessed
- [ ] Data contains millions of tokens
- [ ] Continued pretraining configured
- [ ] Training completed (hours duration)
- [ ] Perplexity decreased significantly
- [ ] New language/domain knowledge validated
- [ ] Custom checkpoint saved
- [ ] Fine-tuning from checkpoint performed
- [ ] Mental health chatbot (or similar) created
- [ ] Model exported to GGUF format
- [ ] Ollama modelfile created
- [ ] Local inference tested
- [ ] Video walkthrough recorded covering:
  - [ ] Continued pretraining concept
  - [ ] Data preparation
  - [ ] Training process
  - [ ] Language/domain learning demonstration
  - [ ] Custom checkpoint fine-tuning
  - [ ] Ollama export and inference
- [ ] Colab notebook uploaded and runnable

---

## 📝 Video Walkthrough Requirements

Your video should cover:

1. **Introduction (2 min)**
   - Continued pretraining vs fine-tuning
   - Use cases (new languages, domains)
   - Overview of complete pipeline

2. **Data Preparation (3 min)**
   - Target language/domain selection
   - Data collection process
   - Preprocessing steps
   - Data statistics

3. **Continued Pretraining (4 min)**
   - Configuration differences from fine-tuning
   - Training execution
   - Perplexity tracking
   - Loss curves
   - Training duration

4. **Custom Checkpoint Fine-tuning (3 min)**
   - Loading pretrained checkpoint
   - Task-specific fine-tuning
   - Mental health chatbot example
   - Combining knowledge + behavior

5. **Ollama Export & Inference (3 min)**
   - Model conversion to GGUF
   - Ollama setup
   - Local inference demonstration
   - Performance comparison

**Total Duration:** 15 minutes

---

## 🎯 Learning Outcomes

After completing this colab, you should understand:

1. Difference between continued pretraining and fine-tuning
2. How to teach models new languages or domains
3. Data requirements for continued pretraining
4. How to fine-tune from custom checkpoints
5. How to export models to Ollama for local use
6. Complete pipeline from pretraining to deployment

---

## 📊 Complete Pipeline Summary

### Phase 1: Continued Pretraining
- Input: Raw text in target language/domain
- Process: Causal language modeling
- Output: Model with extended knowledge
- Duration: Hours to days

### Phase 2: Task-Specific Fine-tuning
- Input: Instruction-response pairs
- Process: Supervised fine-tuning
- Output: Task-capable model
- Duration: Minutes to hours

### Phase 3: Export & Deployment
- Input: Fine-tuned model
- Process: GGUF conversion, quantization
- Output: Ollama-compatible model
- Duration: Minutes

### End Result
- Specialized model with domain knowledge
- Task-specific capabilities
- Local inference ready
- Production deployable

---

## 🌟 Advanced Topics

### Multilingual Continued Pretraining
- Train on multiple languages simultaneously
- Cross-lingual transfer learning
- Language-specific adapters
- Balanced multilingual data

### Domain Mixing
- Combine multiple domains
- Prevent catastrophic forgetting
- Curriculum learning strategies
- Progressive domain addition

### Efficient Pretraining
- LoRA for continued pretraining
- Gradient checkpointing
- Mixed precision training
- Distributed training

### Production Deployment
- Model serving with Ollama
- API integration
- Monitoring and logging
- Continuous improvement

---

**Last Updated:** November 2025
**Colab:** 5 of 5
**Previous:** Colab 4 - GRPO Reasoning
**Status:** Final Colab - Complete Pipeline

