# Codelab 1: Multi-Agent System with ADK and A2A Protocol

**Codelab Link:** [Create Multi-Agent System with ADK, Deploy in Agent Engine and Get Started with A2A Protocol](https://codelabs.developers.google.com/codelabs/create-multi-agents-adk-a2a#0)

---

## 📋 Overview

This codelab demonstrates how to create a multi-agent system using Google's Agent Development Kit (ADK), deploy it in Agent Engine, and implement the Agent-to-Agent (A2A) protocol for seamless communication between agents.

**Learning Objectives:**
- Build a multi-agent system architecture
- Deploy agents using Agent Engine
- Implement A2A protocol for agent communication
- Coordinate multiple agents to accomplish complex tasks

---

## 🎯 What You'll Build

A multi-agent system where multiple specialized agents work together using the A2A protocol to:
- Communicate and coordinate tasks
- Share information and context
- Delegate work between agents
- Provide a unified solution to complex problems

---

## 🛠️ Prerequisites

Before starting this codelab, ensure you have:
- Google Cloud Project with billing enabled
- Python 3.10 or higher installed
- Google ADK installed
- Basic understanding of agent concepts
- Familiarity with Python programming

---

## 📚 Key Concepts

### Agent Development Kit (ADK)
Google's framework for building, testing, and deploying AI agents with tools and capabilities.

### Agent Engine
Google Cloud's platform for deploying and managing AI agents at scale.

### Agent-to-Agent (A2A) Protocol
A communication protocol enabling agents to:
- Discover other agents
- Exchange messages and data
- Coordinate tasks
- Share context and state

---

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install google-adk
pip install google-cloud-agent-engine
```

### 2. Configure Google Cloud
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 3. Initialize ADK Project
```bash
adk init multi-agent-system
cd multi-agent-system
```

---

## 📁 Project Structure

```
codelab-1-multi-agent-adk-a2a/
├── README.md                    # This file
├── agent_config.yaml            # Agent configuration
├── requirements.txt             # Python dependencies
├── agents/
│   ├── __init__.py
│   ├── coordinator_agent.py    # Main coordination agent
│   ├── task_agent.py           # Task-specific agent
│   └── data_agent.py           # Data processing agent
├── config/
│   └── deployment.yaml         # Agent Engine deployment config
└── tests/
    └── test_agents.py          # Agent tests
```

---

## 💻 Implementation

### Agent Architecture

**Coordinator Agent:**
- Receives user requests
- Analyzes task requirements
- Delegates to specialized agents
- Aggregates results

**Task Agent:**
- Executes specific tasks
- Reports progress via A2A
- Returns results to coordinator

**Data Agent:**
- Handles data retrieval and processing
- Provides data to other agents
- Maintains data consistency

### A2A Protocol Implementation

```python
# Example A2A message structure
{
    "sender": "coordinator_agent",
    "receiver": "task_agent",
    "action": "execute_task",
    "payload": {
        "task_type": "data_analysis",
        "parameters": {...}
    },
    "correlation_id": "unique_id"
}
```

---

## 🔧 Configuration

### Agent Configuration (agent_config.yaml)
```yaml
agents:
  - name: coordinator_agent
    type: coordinator
    capabilities:
      - task_delegation
      - result_aggregation
    
  - name: task_agent
    type: worker
    capabilities:
      - task_execution
      - progress_reporting
    
  - name: data_agent
    type: worker
    capabilities:
      - data_retrieval
      - data_processing
```

### Deployment Configuration (deployment.yaml)
```yaml
deployment:
  platform: agent_engine
  region: us-central1
  scaling:
    min_instances: 1
    max_instances: 10
```

---

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/test_agents.py
```

### Test A2A Communication
```bash
python -m agents.test_a2a_communication
```

### Integration Testing
```bash
adk test --integration
```

---

## 🚢 Deployment

### Deploy to Agent Engine
```bash
adk deploy --config config/deployment.yaml
```

### Verify Deployment
```bash
gcloud agent-engine agents list
```

### Test Deployed Agents
```bash
curl -X POST https://agent-engine.googleapis.com/v1/agents/YOUR_AGENT_ID/invoke \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -d '{"query": "test query"}'
```

---

## 📊 Results

### Expected Outputs
- Successfully deployed multi-agent system
- Functional A2A communication between agents
- Coordinated task execution
- Aggregated results from multiple agents

### Performance Metrics
- Agent response time
- A2A message latency
- Task completion rate
- Resource utilization

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Agents not communicating
- **Solution:** Verify A2A protocol configuration and network connectivity

**Issue:** Deployment fails
- **Solution:** Check GCP permissions and project billing

**Issue:** Import errors
- **Solution:** Ensure all dependencies are installed: `pip install -r requirements.txt`

---

## 📖 Additional Resources

- [ADK Documentation](https://developers.google.com/adk)
- [Agent Engine Guide](https://cloud.google.com/agent-engine)
- [A2A Protocol Specification](https://developers.google.com/adk/a2a)
- [Multi-Agent Systems Best Practices](https://developers.google.com/adk/best-practices)

---

## 🎥 Video Walkthrough

See the main repository for video demonstration of:
- Setup and configuration
- Agent implementation
- A2A protocol in action
- Deployment to Agent Engine
- Testing and validation

---

## ✅ Completion Checklist

- [ ] ADK and Agent Engine setup complete
- [ ] Multi-agent system implemented
- [ ] A2A protocol configured
- [ ] Agents deployed to Agent Engine
- [ ] Testing completed successfully
- [ ] Documentation updated
- [ ] Video walkthrough recorded

---

## 📝 Notes

*Add your implementation notes, observations, and learnings here.*
