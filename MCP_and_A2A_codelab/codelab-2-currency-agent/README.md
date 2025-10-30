# 💱 Currency Conversion Agent with ADK, MCP, and A2A

## 🎯 Project Goal

This repository demonstrates the architecture and implementation of a production-grade currency conversion agent using Google's Agent Development Kit (ADK), Model Context Protocol (MCP), and Agent-to-Agent (A2A) protocol. The agent provides real-time currency conversion capabilities while leveraging MCP servers to expose external tools and A2A protocol for seamless agent communication.

The implementation showcases how MCP acts as a crucial bridge between the LLM-powered agent and external currency exchange rate APIs, providing secure, standardized tool execution. The agent can communicate with other financial agents via A2A protocol, enabling complex multi-agent financial workflows.

## 📹 Video Demonstration
*[Link to video walkthrough will be added here]*

## CodeLab Link
https://codelabs.developers.google.com/codelabs/currency-agent#0

## 🏗️ Architecture Overview

The system operates across three integrated layers with clear separation of concerns:

### 1. Agent Layer (ADK)

The application hosting the Gemini model that:

- Acts as the reasoning engine for currency queries
- Interprets natural language requests
- Decides when to invoke currency conversion tools
- Generates user-friendly responses based on conversion results
- Maintains conversation context via MCP

### 2. MCP Server Layer (Tool Provider)

A crucial intermediary service that:

- Exposes currency conversion as standardized tools
- Provides secure access to the Frankfurter API
- Defines tool schemas for the LLM to understand
- Translates natural language requests into API calls
- Handles rate limiting and error responses
- Shields the agent from raw API complexity

**Key MCP Features:**
```python
# MCP Server exposes tools
get_exchange_rate(from_currency, to_currency)
# Returns current exchange rate between currencies

# MCP provides standardized interface
- Tool discovery
- Parameter validation
- Error handling
- Response formatting
```

### 3. External API Layer (Frankfurter)

The data source providing:

- Real-time currency exchange rates
- Historical exchange rate data
- Support for 30+ currencies
- Free, open-source currency API
- No authentication required

## 📋 Implementation Phases

### Phase 1: MCP Server Development

**Create Local MCP Server:**

The MCP server uses FastMCP Python package to create a lightweight server that exposes currency conversion tools:

```python
# mcp-server/server.py
import logging
import os
from mcp import FastMCP
import httpx

# Setup logging
logging.basicConfig(level=logging.INFO)

# Create MCP server
mcp = FastMCP()

# Frankfurter API endpoint
FRANKFURTER_API = "https://api.frankfurter.app/latest"

@mcp.tool()
async def get_exchange_rate(from_currency: str, to_currency: str) -> dict:
    """
    Get the current exchange rate between two currencies.
    
    Args:
        from_currency: Source currency code (e.g., USD)
        to_currency: Target currency code (e.g., EUR)
    
    Returns:
        Exchange rate and conversion details
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            FRANKFURTER_API,
            params={"from": from_currency, "to": to_currency}
        )
        data = response.json()
        
        return {
            "from": from_currency,
            "to": to_currency,
            "rate": data["rates"][to_currency],
            "date": data["date"]
        }
```

**MCP Server Configuration:**

```toml
# mcp-server/pyproject.toml
[project]
name = "currency-mcp-server"
version = "0.1.0"
dependencies = [
    "fastmcp>=0.1.0",
    "httpx>=0.24.0"
]

[tool.fastmcp]
name = "currency-converter"
description = "MCP server for currency conversion"
```

### Phase 2: Deploy MCP Server to Cloud Run

**Containerization:**

```dockerfile
# mcp-server/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
EXPOSE 8080

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Deploy to Cloud Run:**

```bash
# Build and deploy
gcloud run deploy currency-mcp-server \
  --source=./mcp-server \
  --region=us-central1 \
  --allow-unauthenticated \
  --platform=managed

# Get the service URL
gcloud run services describe currency-mcp-server \
  --region=us-central1 \
  --format='value(status.url)'
```

### Phase 3: Currency Agent Development

**Agent Implementation:**

```python
# currency_agent/agent.py
from google.adk.agents import Agent
from google.adk.mcp import MCPClient

# Initialize MCP client
mcp_client = MCPClient("https://your-mcp-server-url.run.app")

# Load tools from MCP server
currency_tools = mcp_client.load_tools()

# Create currency agent
currency_agent = Agent(
    model='gemini-2.0-flash',
    name='currency_agent',
    description='Agent for currency conversion using real-time exchange rates',
    instruction="""
    You are a helpful currency conversion assistant. When users ask about 
    currency conversions or exchange rates, use the available tools to:
    1. Get current exchange rates from the MCP server
    2. Perform accurate conversions
    3. Provide clear explanations with the conversion details
    4. Always specify the date of the exchange rate
    
    Be conversational and helpful in your responses.
    """,
    tools=currency_tools  # MCP tools loaded from server
)
```

**Agent Execution:**

```python
# Run the agent locally
from google.adk.runner import AgentRunner

runner = AgentRunner(currency_agent)
runner.run()

# Example interactions:
# User: "Convert 100 USD to EUR"
# Agent uses get_exchange_rate tool → Returns conversion
```

### Phase 4: A2A Protocol Integration

**Agent Card Definition:**

```json
{
  "name": "currency_agent",
  "description": "Real-time currency conversion agent with 30+ currencies",
  "version": "1.0.0",
  "capabilities": [
    "currency_conversion",
    "exchange_rate_lookup",
    "multi_currency_support"
  ],
  "supported_currencies": [
    "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "BRL"
  ],
  "authentication": {
    "type": "none",
    "required": false
  },
  "endpoint": "https://your-agent-url.run.app",
  "protocol": "a2a",
  "tools": [
    {
      "name": "get_exchange_rate",
      "description": "Get current exchange rate between two currencies",
      "parameters": {
        "from_currency": "string",
        "to_currency": "string"
      }
    }
  ]
}
```

**A2A Communication Example:**

```python
# Another agent requesting currency conversion via A2A
from google.adk.a2a import A2AClient

a2a_client = A2AClient()

# Discover currency agent
agent_card = await a2a_client.discover_agent("currency_agent")

# Send request to currency agent
response = await a2a_client.send_message(
    target_agent="currency_agent",
    message={
        "type": "tool_request",
        "tool": "get_exchange_rate",
        "parameters": {
            "from_currency": "USD",
            "to_currency": "EUR"
        }
    }
)

print(f"Exchange rate: {response['rate']}")
```

## 🚀 Usage Examples

The currency agent handles various conversion scenarios:

**Simple Conversion:**

```
User: "Convert 100 USD to EUR"
→ Agent invokes get_exchange_rate(USD, EUR)
→ MCP Server calls Frankfurter API
→ Returns: "100 USD equals 92.15 EUR at the exchange rate of 0.9215 (as of 2024-01-15)"
```

**Multiple Currency Inquiry:**

```
User: "What's the exchange rate from GBP to JPY and CAD?"
→ Agent makes two tool calls via MCP
→ get_exchange_rate(GBP, JPY) → 184.52
→ get_exchange_rate(GBP, CAD) → 1.68
→ Returns formatted response with both rates
```

**Historical Context:**

```
User: "I need to convert 500 EUR to USD"
→ Agent uses MCP tool: get_exchange_rate(EUR, USD)
→ Conversion: 500 EUR = 542.50 USD (rate: 1.085)
→ Agent provides context: "Based on today's rate..."
```

**A2A Multi-Agent Scenario:**

```
Financial Advisor Agent: "Check if 1000 USD is enough to buy item priced at 850 EUR"
→ Sends A2A request to Currency Agent
→ Currency Agent: get_exchange_rate(USD, EUR) → 0.92
→ Calculation: 1000 * 0.92 = 920 EUR
→ Response: "Yes, 1000 USD (920 EUR) is sufficient for 850 EUR purchase"
```

## 🔄 Interaction Flow

1. **User Query** → Natural language currency conversion request
2. **LLM Analysis** → Agent interprets intent and identifies currency pair
3. **Tool Selection** → Agent chooses get_exchange_rate tool
4. **MCP Invocation** → Tool call sent to MCP server
5. **API Execution** → MCP server queries Frankfurter API
6. **Data Return** → Exchange rate data flows back through layers
7. **Response Generation** → LLM creates natural language response
8. **User Response** → Formatted conversion result delivered

## 🔑 Key Concepts

### Model Context Protocol (MCP) Benefits

**Standardized Tool Interface:**
- Consistent tool definition across different agents
- Easy tool discovery and documentation
- Parameter validation at the protocol level

**Secure API Access:**
- MCP server acts as security boundary
- API keys and secrets stored server-side
- Rate limiting and quota management
- Prevents direct API exposure to LLM

**Tool Reusability:**
- Multiple agents can use same MCP server
- Tools defined once, used everywhere
- Centralized maintenance and updates

**Context Management:**
- MCP can maintain conversation state
- Share context between agents
- Persist tool call history

### Complementary Roles: MCP vs A2A

**MCP (Model Context Protocol):**
- Focus: Connecting LLMs with **tools and data**
- Purpose: Tool invocation and resource access
- Scope: Single agent to multiple tools
- Example: Agent → MCP Server → Currency API

**A2A (Agent-to-Agent):**
- Focus: Connecting **agents with agents**
- Purpose: Agent collaboration and coordination
- Scope: Multi-agent communication
- Example: Financial Agent ← A2A → Currency Agent

**Recommended Pattern:**
- Use MCP for tools/APIs
- Use A2A for agent collaboration
- Agents expose MCP tools to other agents via A2A

### Currency Agent Architecture

**Three-Layer Design:**
```
┌─────────────────────────────────────┐
│   Currency Agent (ADK + Gemini)     │  ← Reasoning & NL interface
├─────────────────────────────────────┤
│   MCP Server (Tool Provider)        │  ← Tool definition & API access
├─────────────────────────────────────┤
│   Frankfurter API (Data Source)     │  ← Exchange rate data
└─────────────────────────────────────┘
```

## 🔗 Learning Resources

- **Original Codelab:** https://codelabs.developers.google.com/codelabs/currency-agent#0
- **MCP Documentation:** https://modelcontextprotocol.io/
- **ADK Documentation:** https://developers.google.com/adk
- **A2A Protocol:** https://developers.google.com/adk/a2a
- **Frankfurter API:** https://www.frankfurter.app/docs/
- **FastMCP Guide:** https://github.com/jlowin/fastmcp

## 🧹 Cleanup

Always clean up Google Cloud resources to manage costs:

```bash
# Delete Cloud Run service
gcloud run services delete currency-mcp-server \
  --region=us-central1

# Delete container images (optional)
gcloud artifacts docker images delete \
  us-central1-docker.pkg.dev/PROJECT_ID/currency-mcp-server

# Delete Agent Engine deployment (if deployed)
adk delete currency_agent
```

## 💡 Key Takeaways

1. **MCP as Tool Bridge** - MCP servers provide standardized, secure access to external APIs
2. **Three-layer architecture** - Clear separation between agent, tools, and data sources
3. **FastMCP simplicity** - Creating MCP servers is straightforward with FastMCP
4. **Cloud Run deployment** - Serverless MCP server hosting for scalability
5. **A2A for collaboration** - Currency agent can serve other financial agents
6. **Real-world integration** - Demonstrates practical API integration patterns
7. **Production patterns** - Security, error handling, and rate limiting considerations

## 🎓 Advanced Topics

### Adding Historical Rate Support

```python
@mcp.tool()
async def get_historical_rate(
    from_currency: str,
    to_currency: str,
    date: str  # Format: YYYY-MM-DD
) -> dict:
    """Get historical exchange rate for a specific date."""
    url = f"https://api.frankfurter.app/{date}"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={"from": from_currency, "to": to_currency}
        )
        return response.json()
```

### Multi-Currency Conversion

```python
@mcp.tool()
async def convert_to_multiple(
    amount: float,
    from_currency: str,
    to_currencies: list[str]
) -> dict:
    """Convert amount to multiple target currencies."""
    results = {}
    async with httpx.AsyncClient() as client:
        for to_curr in to_currencies:
            rate_data = await get_exchange_rate(from_currency, to_curr)
            results[to_curr] = amount * rate_data["rate"]
    return results
```

### Caching for Performance

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache rates for 1 hour
_rate_cache = {}
_cache_duration = timedelta(hours=1)

async def get_cached_exchange_rate(from_curr: str, to_curr: str):
    cache_key = f"{from_curr}_{to_curr}"
    now = datetime.now()
    
    if cache_key in _rate_cache:
        cached_time, cached_rate = _rate_cache[cache_key]
        if now - cached_time < _cache_duration:
            return cached_rate
    
    # Fetch fresh rate
    rate = await get_exchange_rate(from_curr, to_curr)
    _rate_cache[cache_key] = (now, rate)
    return rate
```

## 📊 Supported Currencies

The Frankfurter API supports 30+ currencies:

**Major Currencies:**
- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- CHF (Swiss Franc)
- CAD (Canadian Dollar)
- AUD (Australian Dollar)

**Asian Currencies:**
- CNY (Chinese Yuan)
- INR (Indian Rupee)
- KRW (South Korean Won)
- SGD (Singapore Dollar)
- THB (Thai Baht)

**Other Major Economies:**
- BRL (Brazilian Real)
- MXN (Mexican Peso)
- RUB (Russian Ruble)
- ZAR (South African Rand)

## 🐛 Troubleshooting

### Common Issues

**Issue:** MCP server not starting
- **Solution:** Check port 8080 is not in use, verify dependencies installed

**Issue:** Tool not discovered by agent
- **Solution:** Verify MCP server URL is correct, check server is running

**Issue:** API rate limit exceeded
- **Solution:** Implement caching, add rate limiting in MCP server

**Issue:** Currency not found
- **Solution:** Verify currency code is valid (use ISO 4217 codes)

**Issue:** A2A connection timeout
- **Solution:** Check network connectivity, increase timeout settings

## 🔐 Security Considerations

- MCP server acts as security perimeter
- No API keys needed for Frankfurter (free service)
- If using paid APIs, store keys in Secret Manager
- Implement rate limiting in MCP server
- Validate all currency codes before API calls
- Use HTTPS for all communications
- Sanitize user inputs
- Log all transactions for audit

## 📝 Project Structure

```
codelab-2-currency-agent/
├── currency-agent/
│   ├── currency_agent/
│   │   ├── __init__.py
│   │   ├── agent.py              # Main agent implementation
│   │   └── test_client.py        # Test client for agent
│   ├── mcp-server/
│   │   ├── server.py             # MCP server implementation
│   │   ├── test_server.py        # MCP server tests
│   │   ├── Dockerfile            # Container definition
│   │   ├── pyproject.toml        # Python project config
│   │   └── uv.lock               # Dependency lock file
│   ├── images/
│   │   ├── architecture.png      # Architecture diagram
│   │   ├── adk-favicon.ico       # ADK icon
│   │   └── mcp-favicon.ico       # MCP icon
│   ├── pyproject.toml            # Agent project config
│   ├── uv.lock                   # Agent dependencies
│   ├── .env.example              # Environment template
│   └── README.md                 # Project documentation
└── README.md                     # This file
```

## ✅ Completion Checklist

- [ ] MCP server implemented and tested locally
- [ ] Currency conversion tool working
- [ ] MCP server deployed to Cloud Run
- [ ] Currency agent created with ADK
- [ ] Agent connected to MCP server
- [ ] Local agent testing completed
- [ ] A2A protocol configured
- [ ] Agent Card created
- [ ] Multi-agent communication tested
- [ ] Documentation complete
- [ ] Video walkthrough recorded

## 🚧 Testing

### Test MCP Server Locally

```bash
# Start MCP server
cd mcp-server
python server.py

# Test with curl
curl -X POST http://localhost:8080/tools/get_exchange_rate \
  -H "Content-Type: application/json" \
  -d '{"from_currency": "USD", "to_currency": "EUR"}'
```

### Test Currency Agent

```bash
# Run agent locally
cd currency-agent
adk run

# Example queries:
# "Convert 100 USD to EUR"
# "What's the exchange rate from GBP to JPY?"
# "I need to convert 50 euros to dollars"
```

### Test A2A Communication

```python
# test_a2a.py
from currency_agent.test_client import test_a2a_connection

# Test agent discovery
agent_card = await test_a2a_connection("currency_agent")
print(f"Agent capabilities: {agent_card['capabilities']}")

# Test tool invocation via A2A
result = await invoke_via_a2a(
    agent="currency_agent",
    tool="get_exchange_rate",
    params={"from_currency": "USD", "to_currency": "EUR"}
)
print(f"Exchange rate: {result['rate']}")
```

## 📈 Performance Metrics

Expected performance characteristics:

- **MCP Server Response:** < 200ms
- **API Call Latency:** 100-300ms
- **Agent Processing:** < 1 second
- **End-to-End Query:** 1-2 seconds
- **Cache Hit Rate:** 60-70% (with caching)
- **Concurrent Users:** 100+ (Cloud Run)

## 🔄 Future Enhancements

- [ ] Add historical rate lookup
- [ ] Implement rate trend analysis
- [ ] Add currency conversion alerts
- [ ] Support cryptocurrency conversions
- [ ] Add batch conversion support
- [ ] Implement rate comparison across providers
- [ ] Add GraphQL API support
- [ ] Create mobile app interface

---

**Last Updated:** October 2025
**Codelab Author:** Jack Wotherspoon, Google
**Assignment:** CMPE-297 Special Topics - MCP and A2A Codelab
