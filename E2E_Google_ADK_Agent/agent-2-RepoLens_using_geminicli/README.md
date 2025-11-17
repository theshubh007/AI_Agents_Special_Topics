# 🛠️ Agent 2: Advanced Tool Agent with Gemini CLI

## 🎯 Project Goal

This agent demonstrates advanced tool integration by using Gemini CLI as a tool within an ADK pipeline. It showcases how to combine ADK's orchestration capabilities with Gemini CLI's powerful AI features for complex multi-step reasoning tasks.

## 📹 Video Demonstration
[Walkthrough YouTube Video](https://youtu.be/c0Ec0y3wieE)

## 🏗️ Architecture Overview

### Agent Capabilities
- Gemini CLI integration
- Pipeline orchestration
- Multi-step reasoning
- Tool chaining
- Cloud deployment

### Key Components
1. **ADK Agent** - Main orchestrator
2. **Gemini CLI Tool** - AI capabilities wrapper
3. **Pipeline Manager** - Workflow coordination
4. **Cloud Run Service** - Deployment platform

---

## 📋 Implementation Steps

### Step 1: Gemini CLI Setup
- Install Gemini CLI
- Configure authentication
- Test CLI functionality
- Verify API access

### Step 2: Tool Wrapper Development
- Create CLI tool wrapper
- Handle input/output formatting
- Implement error handling
- Add logging

### Step 3: Agent Development
- Create ADK agent
- Integrate CLI tool
- Define pipeline steps
- Configure orchestration

### Step 4: Cloud Run Deployment
- Create Dockerfile
- Configure Cloud Run
- Set environment variables
- Deploy service

### Step 5: Testing
- Test CLI tool wrapper
- Test agent pipeline
- Validate Cloud Run deployment
- Performance testing

---

## 🚀 Usage Examples

### Example 1: Multi-Step Analysis
**Input:** "Analyze this document and summarize key points"

**Agent Actions:**
1. Receives document
2. Calls Gemini CLI for analysis
3. Processes results
4. Generates summary
5. Returns formatted output

**Output:** Structured summary with key insights

### Example 2: Complex Reasoning
**Input:** "Compare these two approaches and recommend best option"

**Agent Actions:**
1. Parses input
2. Uses CLI for comparison
3. Evaluates criteria
4. Generates recommendation
5. Provides justification

**Output:** Detailed recommendation with reasoning

---

## 🔑 Key Features

### CLI Integration
- Seamless CLI tool wrapping
- Input/output handling
- Error management
- Performance optimization

### Pipeline Orchestration
- Multi-step workflows
- Tool chaining
- State management
- Result aggregation

### Cloud Deployment
- Serverless architecture
- Auto-scaling
- High availability
- Cost optimization

---

## 💡 Best Practices

- Proper CLI error handling
- Efficient input formatting
- Result caching
- Timeout management
- Resource optimization
- Monitoring and logging

---

## 🔗 Resources

- Article: https://medium.com/@derrickchwong/combine-adk-gemini-cli-and-cloud-run-c5dea5118853
- Code: https://github.com/derrickchwong/gemini-cli-on-adk
- Gemini CLI: https://github.com/google/generative-ai-cli

---

## ✅ Completion Checklist

- [ ] Gemini CLI installed
- [ ] CLI tool wrapper created
- [ ] ADK agent implemented
- [ ] Pipeline orchestration working
- [ ] Cloud Run deployment successful
- [ ] Testing completed
- [ ] Monitoring configured
- [ ] Video walkthrough recorded

---

**Agent:** 2 of 5
**Complexity:** Medium
**Points:** 100
