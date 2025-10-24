# 🤖 Building AI Agents with ADK: Empowering with Tools

## 🎯 Project Overview

This project demonstrates the power of Google's Agent Development Kit (ADK) by building a multi-tool personal assistant agent. The implementation showcases how to transform a basic LLM into an intelligent agent capable of executing real-world tasks through three distinct tool integration patterns:

- **Custom Functions** - Direct Python function integration
- **Agent Tools** - Nested agent delegation for specialized tasks
- **Third-Party Tools** - LangChain tool integration for extended capabilities

The result is a grounded, actionable AI system that goes beyond text generation to perform concrete operations like currency conversion, web searches, and knowledge retrieval.

## 📹 Video Demonstration
https://youtu.be/FT24n1NLqdE

## CodeLab Link
https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-empowering-with-tools#0


## ✨ Core Architecture

### Root Agent
The main orchestrator (`root_agent`) coordinates between multiple specialized tools:

```python
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    tools=[FunctionTool, AgentTool, LangchainTool]
)
```

### Tool Integration Patterns

#### 1. FunctionTool - Custom Python Functions
**Implementation:** `get_fx_rate(base: str, target: str)`
- Fetches real-time currency exchange rates via REST API
- Demonstrates direct function-to-tool conversion
- Shows how to define clear docstrings for LLM understanding

#### 2. AgentTool - Nested Agent Delegation
**Implementation:** `google_search_agent`
- Specialized agent focused on real-time information retrieval
- Uses Google Search for current events, weather, business hours
- Demonstrates agent composition and task delegation

#### 3. LangchainTool - Third-Party Integration
**Implementation:** `langchain_wikipedia_tool`
- Integrates LangChain's Wikipedia query capabilities
- Configured for historical and cultural information
- Shows interoperability with existing tool ecosystems

## 🛠️ Key Concepts

### Tool Definition Schema
Each tool requires:
- **Clear description** - Helps the LLM understand when to use it
- **Type annotations** - Defines expected parameters
- **Docstrings** - Provides context for intelligent selection

### Three-Part Interaction Flow
1. **LLM Analysis** - Agent determines which tool to invoke
2. **Function Execution** - Tool performs the actual operation
3. **Result Integration** - Output is fed back to LLM for response generation

### Agent Specialization
The `google_search_agent` demonstrates:
- Focused instruction sets for specific domains
- Tool scoping (only has access to google_search)
- Clear delegation boundaries

## 📁 Project Structure

```
ai-agents-adk/
└── personal_assistant/
    ├── __init__.py              # Package initialization
    ├── agent.py                 # Root agent configuration
    ├── custom_functions.py      # FunctionTool implementation
    ├── custom_agents.py         # AgentTool implementation
    └── third_party_tools.py     # LangchainTool integration
```

## 🚀 Capabilities

The personal assistant can handle:
- **Currency Conversion** - "What's the exchange rate from SGD to JPY?"
- **Real-Time Search** - "What's the weather in Seattle?" or "When does the museum close?"
- **Knowledge Queries** - "Tell me about the Eiffel Tower's history"



## 💡 Key Takeaways

1. **Tool diversity matters** - Different integration patterns serve different use cases
2. **Agent composition** - Nested agents enable modular, specialized functionality
3. **Clear descriptions** - Well-documented tools improve selection accuracy
4. **Ecosystem integration** - ADK works seamlessly with existing tools (LangChain)
5. **Grounded responses** - External tools transform speculation into actionable results
