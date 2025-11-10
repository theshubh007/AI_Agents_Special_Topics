# 🤖 Building E2E Google ADK Agent Applications

**Course:** FA25: CMPE-297 Sec 49 - Special Topics

---

## 📋 Assignment Overview

This repository contains five production-quality agent applications built end-to-end using Google's Agent Development Kit (ADK). Each agent demonstrates different capabilities, tools, and integration patterns, showcasing the versatility and power of ADK for building intelligent, autonomous systems.

**Assignment Goals:**
- Build 5 complete ADK agent applications
- Demonstrate deep research capabilities
- Integrate advanced tools (Gemini CLI)
- Implement MCP-based tools
- Create production-quality code review systems
- Deploy e-commerce agents with database integration
- Provide comprehensive code walkthroughs

## 📹 Video Demonstration
[Walkthrough YouTube Video](https://www.youtube.com/)

---

## 📂 Project Structure

```
E2E_Google_ADK_Agent/
├── agent-1-deep-research-lead-generation/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── research_agent.py
│   │   └── tools/
│   ├── README.md
│   └── requirements.txt
├── agent-2-gemini-cli-tool/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── gemini_cli_agent.py
│   │   └── tools/
│   ├── README.md
│   └── requirements.txt
├── agent-3-mcp-bug-assistant/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── bug_assistant.py
│   │   └── tools/
│   ├── README.md
│   └── requirements.txt
├── agent-4-code-review-assistant/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── code_reviewer.py
│   │   └── tools/
│   ├── README.md
│   └── requirements.txt
├── agent-5-ecommerce-sports-agent/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── sports_agent.py
│   │   └── tools/
│   ├── database/
│   ├── README.md
│   └── requirements.txt
└── README.md (this file)
```

---

## 🎯 Agent Overview

### Agent 1: Deep Research Agent for Lead Generation

**Purpose:** Autonomous research agent that discovers, analyzes, and qualifies potential leads

**Key Features:**
- Web scraping and data extraction
- Company information gathering
- Contact discovery
- Lead scoring and qualification
- Automated research reports

**Technologies:**
- Google ADK
- Gemini 2.0
- Web search tools
- Data extraction APIs
- Lead scoring algorithms

**Resources:**
- Blog: https://cloud.google.com/blog/products/ai-machine-learning/build-a-deep-research-agent-with-google-adk
- Code: https://github.com/MagnIeeT/leadGenerationAgentADK

---

### Agent 2: Advanced Tool Agent with Gemini CLI

**Purpose:** Agent that uses Gemini CLI as a tool within ADK pipeline for advanced AI capabilities

**Key Features:**
- Gemini CLI integration
- Pipeline orchestration
- Cloud Run deployment
- Multi-step reasoning
- Tool chaining

**Technologies:**
- Google ADK
- Gemini CLI
- Cloud Run
- FastAPI
- Docker

**Resources:**
- Article: https://medium.com/@derrickchwong/combine-adk-gemini-cli-and-cloud-run-c5dea5118853
- Code: https://github.com/derrickchwong/gemini-cli-on-adk

---

### Agent 3: MCP Tools-Based Bug Assistant

**Purpose:** Software bug assistance agent using Model Context Protocol tools

**Key Features:**
- Bug analysis and diagnosis
- Code context understanding
- Solution recommendations
- MCP tool integration
- Issue tracking

**Technologies:**
- Google ADK
- Model Context Protocol (MCP)
- GitHub integration
- Code analysis tools
- Issue tracking APIs

**Resources:**
- Blog: https://cloud.google.com/blog/topics/developers-practitioners/tools-make-an-agent-from-zero-to-assistant-with-adk
- Code: https://github.com/google/adk-samples/tree/main/python/agents/software-bug-assistant

---

### Agent 4: Production Quality Code Review Assistant

**Purpose:** Automated code review agent for pull requests and code quality analysis

**Key Features:**
- Automated code review
- Best practices enforcement
- Security vulnerability detection
- Performance optimization suggestions
- Documentation quality checks

**Technologies:**
- Google ADK
- Gemini 2.0
- GitHub API
- Static analysis tools
- Code quality metrics

**Resources:**
- Codelab: https://codelabs.developers.google.com/adk-code-reviewer-assistant/instructions
- Code: https://github.com/ayoisio/adk-code-review-assistant

---

### Agent 5: Production Quality E-Commerce Sports Agent

**Purpose:** E-commerce agent for sports equipment with database integration

**Key Features:**
- Product search and recommendations
- Inventory management
- Order processing
- AlloyDB integration
- MCP tools for database operations

**Technologies:**
- Google ADK
- AlloyDB (PostgreSQL)
- MCP for database tools
- E-commerce APIs
- Cloud deployment

**Resources:**
- Codelab: https://codelabs.developers.google.com/codelabs/sports-agent-adk-mcp-alloydb
- Code: https://github.com/mtoscano84/sports-agent-adk-mcp-alloydb

---

## 🏗️ Common Architecture Patterns

### ADK Agent Structure

**Core Components:**
1. Agent Definition (model, instructions, tools)
2. Tool Implementation (custom functions)
3. State Management (conversation context)
4. Deployment Configuration (Cloud Run, Agent Engine)

**Best Practices:**
- Clear tool definitions with type hints
- Comprehensive error handling
- Logging and monitoring
- Proper authentication
- Scalable deployment

### Tool Integration Patterns

**Pattern 1: Direct API Tools**
- Call external APIs directly
- Handle authentication
- Parse responses
- Return structured data

**Pattern 2: MCP Tools**
- Use Model Context Protocol
- Standardized tool interface
- Reusable across agents
- Better context management

**Pattern 3: CLI Tools**
- Wrap command-line tools
- Execute system commands
- Parse output
- Handle errors

---

## 📋 Implementation Checklist

### Agent 1: Deep Research Lead Generation
- [ ] Environment setup complete
- [ ] Research agent implemented
- [ ] Web scraping tools configured
- [ ] Lead scoring algorithm implemented
- [ ] Data extraction working
- [ ] Report generation functional
- [ ] Testing completed
- [ ] Documentation written
- [ ] Video walkthrough recorded

### Agent 2: Gemini CLI Tool
- [ ] Gemini CLI installed and configured
- [ ] ADK agent with CLI tool created
- [ ] Pipeline orchestration working
- [ ] Cloud Run deployment successful
- [ ] Tool chaining functional
- [ ] Error handling implemented
- [ ] Testing completed
- [ ] Documentation written
- [ ] Video walkthrough recorded

### Agent 3: MCP Bug Assistant
- [ ] MCP tools configured
- [ ] Bug assistant agent implemented
- [ ] GitHub integration working
- [ ] Code analysis functional
- [ ] Issue tracking connected
- [ ] Solution recommendations working
- [ ] Testing completed
- [ ] Documentation written
- [ ] Video walkthrough recorded

### Agent 4: Code Review Assistant
- [ ] Code review agent implemented
- [ ] GitHub API integration working
- [ ] Static analysis tools configured
- [ ] Security checks functional
- [ ] Performance analysis working
- [ ] Documentation checks implemented
- [ ] PR automation working
- [ ] Testing completed
- [ ] Documentation written
- [ ] Video walkthrough recorded

### Agent 5: E-Commerce Sports Agent
- [ ] AlloyDB database setup
- [ ] MCP database tools configured
- [ ] Sports agent implemented
- [ ] Product search working
- [ ] Inventory management functional
- [ ] Order processing implemented
- [ ] Database integration complete
- [ ] Testing completed
- [ ] Documentation written
- [ ] Video walkthrough recorded

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Cloud account
- ADK installed
- Docker (for deployment)
- Git

### General Setup

```bash
# Install ADK
pip install google-adk

# Clone repository
git clone <repository-url>
cd E2E_Google_ADK_Agent

# Navigate to specific agent
cd agent-1-deep-research-lead-generation

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run agent locally
adk run
```

### Testing Agents

Each agent directory contains specific testing instructions in its README.

---

## 💡 Key Concepts

### Agent Development Kit (ADK)

**What is ADK?**
- Framework for building AI agents
- Integrates with Gemini models
- Supports custom tools
- Enables agent orchestration
- Production deployment ready

**Core Features:**
- Tool integration
- State management
- Multi-agent coordination
- Cloud deployment
- Monitoring and logging

### Model Context Protocol (MCP)

**Purpose:**
- Standardize tool interfaces
- Enable tool reusability
- Improve context management
- Facilitate agent collaboration

**Benefits:**
- Consistent tool definitions
- Better error handling
- Easier testing
- Cross-agent compatibility

### Production Deployment

**Deployment Options:**
1. Cloud Run (serverless)
2. Agent Engine (managed)
3. Kubernetes (self-managed)
4. Local development

**Best Practices:**
- Environment variable management
- Secret handling
- Logging and monitoring
- Error tracking
- Performance optimization

---

## 🎓 Learning Outcomes

After completing all 5 agents, you will understand:

1. **Deep Research Capabilities**
   - Web scraping and data extraction
   - Information synthesis
   - Lead qualification
   - Automated research workflows

2. **Advanced Tool Integration**
   - CLI tool wrapping
   - Pipeline orchestration
   - Tool chaining
   - Cloud deployment

3. **MCP Tool Development**
   - Protocol implementation
   - Tool standardization
   - Context management
   - Reusable components

4. **Production Code Quality**
   - Automated code review
   - Best practices enforcement
   - Security analysis
   - Quality metrics

5. **E-Commerce Applications**
   - Database integration
   - Product management
   - Order processing
   - Scalable architecture

---

## 📊 Comparison Matrix

| Agent | Complexity | Tools | Database | Deployment | Use Case |
|-------|-----------|-------|----------|------------|----------|
| Lead Generation | High | Web APIs | Optional | Cloud Run | B2B Sales |
| Gemini CLI | Medium | CLI Tools | No | Cloud Run | AI Pipeline |
| Bug Assistant | Medium | MCP Tools | Optional | Agent Engine | DevOps |
| Code Review | High | GitHub API | No | Cloud Run | CI/CD |
| E-Commerce | High | MCP + DB | AlloyDB | Cloud Run | Retail |

---

## 🐛 Common Issues & Solutions

### Issue: ADK Installation Fails
**Solutions:**
- Update pip: `pip install --upgrade pip`
- Use virtual environment
- Check Python version (3.10+)
- Install build tools

### Issue: Authentication Errors
**Solutions:**
- Verify Google Cloud credentials
- Check API keys in .env
- Enable required APIs
- Review IAM permissions

### Issue: Tool Execution Fails
**Solutions:**
- Validate tool definitions
- Check parameter types
- Review error logs
- Test tools independently

### Issue: Deployment Issues
**Solutions:**
- Verify Docker configuration
- Check Cloud Run settings
- Review environment variables
- Test locally first

---

## 📹 Video Walkthrough Requirements

Each agent requires a detailed video covering:

### Video Structure (Per Agent)

1. **Introduction (2 min)**
   - Agent purpose and capabilities
   - Architecture overview
   - Key features

2. **Code Walkthrough (8 min)**
   - Agent implementation
   - Tool definitions
   - Integration points
   - Configuration

3. **Execution Demo (5 min)**
   - Live agent interaction
   - Tool usage examples
   - Error handling
   - Results analysis

4. **Deployment (3 min)**
   - Deployment process
   - Configuration
   - Testing in production
   - Monitoring

5. **Key Learnings (2 min)**
   - Challenges faced
   - Solutions implemented
   - Best practices
   - Future improvements

**Total per Agent:** 20 minutes
**Total for All 5 Agents:** 100 minutes

---

## 🎯 Grading Criteria

**Total Points: 500 (100 points per agent)**

### Per Agent Breakdown:
- **Implementation (40 points)** - Complete, working agent
- **Tool Integration (20 points)** - Proper tool usage
- **Code Quality (15 points)** - Clean, documented code
- **Deployment (10 points)** - Successfully deployed
- **Documentation (10 points)** - Clear README and comments
- **Video Walkthrough (5 points)** - Comprehensive explanation

### Overall Assessment:
- All 5 agents must be functional
- Each agent must have video walkthrough
- Code must be well-documented
- Deployment must be demonstrated
- GitHub repository must be organized

---

## 🔗 Additional Resources

### Official Documentation
- ADK Documentation: https://developers.google.com/adk
- Gemini API: https://ai.google.dev/docs
- Cloud Run: https://cloud.google.com/run/docs
- AlloyDB: https://cloud.google.com/alloydb/docs

### Community Resources
- ADK Samples: https://github.com/google/adk-samples
- ADK Discord: [Community Link]
- Stack Overflow: Tag `google-adk`

### Related Codelabs
- ADK Getting Started: https://codelabs.developers.google.com/adk-getting-started
- Multi-Agent Systems: https://codelabs.developers.google.com/multi-agent-adk
- MCP Integration: https://codelabs.developers.google.com/mcp-adk

---

## 🔐 Security Best Practices

- Store API keys in Secret Manager
- Use environment variables
- Implement authentication
- Validate all inputs
- Enable HTTPS
- Regular security audits
- Monitor for anomalies
- Implement rate limiting

---

## 🌟 Advanced Topics

### Multi-Agent Orchestration
- Coordinate multiple agents
- Share context between agents
- Implement agent hierarchies
- Handle agent communication

### Performance Optimization
- Caching strategies
- Parallel tool execution
- Response streaming
- Resource management

### Monitoring & Observability
- Logging best practices
- Metrics collection
- Error tracking
- Performance monitoring

---

## ✅ Final Submission Checklist

- [ ] All 5 agents implemented and working
- [ ] Each agent has dedicated README
- [ ] All code is documented
- [ ] Environment setup instructions provided
- [ ] Deployment configurations included
- [ ] 5 video walkthroughs recorded (one per agent)
- [ ] Videos uploaded to YouTube
- [ ] Video links added to READMEs
- [ ] GitHub repository organized
- [ ] All dependencies listed
- [ ] Testing instructions provided
- [ ] Main README complete

---

**Last Updated:** November 2025
**Course:** CMPE-297 Special Topics
**Assignment:** Building E2E Google ADK Agent Applications
**Due Date:** November 9, 2025
**Total Points:** 500

