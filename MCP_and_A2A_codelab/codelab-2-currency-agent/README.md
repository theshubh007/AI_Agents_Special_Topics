# Codelab 2: Currency Agent with ADK, MCP, and A2A

**Codelab Link:** [Getting Started with ADK, MCP, and A2A](https://codelabs.developers.google.com/codelabs/currency-agent#0)

---

## 📋 Overview

This codelab demonstrates building a currency conversion agent that integrates Google's Agent Development Kit (ADK), Model Context Protocol (MCP), and Agent-to-Agent (A2A) protocol. The agent provides real-time currency conversion capabilities while leveraging MCP for context management and A2A for agent communication.

**Learning Objectives:**
- Implement currency conversion functionality
- Integrate Model Context Protocol (MCP)
- Use ADK for agent development
- Enable A2A protocol for agent communication
- Handle real-time data from external APIs

---

## 🎯 What You'll Build

A fully functional currency conversion agent that:
- Converts between multiple currencies
- Provides real-time exchange rates
- Uses MCP to maintain conversation context
- Communicates with other agents via A2A
- Handles multiple currency pairs simultaneously

---

## 🛠️ Prerequisites

Before starting this codelab, ensure you have:
- Python 3.10 or higher installed
- Google ADK installed
- API key for currency exchange rate service
- Basic understanding of REST APIs
- Familiarity with async programming in Python

---

## 📚 Key Concepts

### Model Context Protocol (MCP)
A protocol for managing context between models and applications, enabling:
- Context persistence across conversations
- Efficient context retrieval
- Context sharing between agents
- Memory management

### Currency Conversion Agent
An AI agent that:
- Fetches real-time exchange rates
- Performs currency calculations
- Maintains conversion history
- Provides currency information

### Integration Architecture
```
User Input → Currency Agent → MCP (Context) → External API → Response
                ↓                                    ↓
            A2A Protocol ← → Other Agents        Exchange Rates
```

---

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install google-adk
pip install requests
pip install aiohttp
pip install mcp-client
```

### 2. Configure API Keys
Create a `.env` file:
```bash
CURRENCY_API_KEY=your_api_key_here
GOOGLE_API_KEY=your_google_api_key
```

### 3. Initialize Project
```bash
adk init currency-agent
cd currency-agent
```

---

## 📁 Project Structure

```
codelab-2-currency-agent/
├── README.md                      # This file
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
├── currency_agent/
│   ├── __init__.py
│   ├── agent.py                  # Main agent implementation
│   ├── currency_service.py       # Currency API integration
│   ├── mcp_handler.py            # MCP context management
│   └── a2a_client.py             # A2A protocol client
├── config/
│   ├── agent_config.yaml         # Agent configuration
│   └── mcp_config.yaml           # MCP configuration
├── tools/
│   ├── __init__.py
│   └── currency_tools.py         # Currency conversion tools
└── tests/
    ├── test_agent.py
    ├── test_currency_service.py
    └── test_mcp_integration.py
```

---

## 💻 Implementation

### Currency Agent Core

```python
# Example agent implementation
from google_adk import Agent
from mcp_client import MCPClient

class CurrencyAgent(Agent):
    def __init__(self):
        super().__init__(name="currency_agent")
        self.mcp_client = MCPClient()
        self.supported_currencies = ["USD", "EUR", "GBP", "JPY", "CAD"]
    
    async def convert_currency(self, amount, from_currency, to_currency):
        # Fetch exchange rate
        rate = await self.get_exchange_rate(from_currency, to_currency)
        
        # Perform conversion
        result = amount * rate
        
        # Store in MCP context
        await self.mcp_client.store_context({
            "conversion": {
                "from": from_currency,
                "to": to_currency,
                "rate": rate,
                "result": result
            }
        })
        
        return result
```

### MCP Integration

**Context Management:**
- Store conversion history
- Retrieve previous conversions
- Share context with other agents
- Maintain user preferences

**Context Structure:**
```json
{
  "user_id": "user123",
  "conversation_id": "conv456",
  "conversions": [
    {
      "timestamp": "2024-01-01T12:00:00Z",
      "from": "USD",
      "to": "EUR",
      "amount": 100,
      "rate": 0.85,
      "result": 85
    }
  ],
  "preferences": {
    "default_currency": "USD",
    "precision": 2
  }
}
```

### A2A Protocol Implementation

**Agent Communication:**
```python
# Request assistance from another agent
response = await a2a_client.send_message(
    target_agent="financial_advisor_agent",
    message={
        "type": "currency_conversion_complete",
        "data": {
            "conversion_result": result,
            "request_advice": True
        }
    }
)
```

---

## 🔧 Configuration

### Agent Configuration (agent_config.yaml)
```yaml
agent:
  name: currency_agent
  description: "Real-time currency conversion agent"
  capabilities:
    - currency_conversion
    - exchange_rate_lookup
    - historical_data
  
  supported_currencies:
    - USD
    - EUR
    - GBP
    - JPY
    - CAD
    - AUD
    - CHF
    - CNY

mcp:
  enabled: true
  context_retention: 24h
  max_context_size: 1MB

a2a:
  enabled: true
  discovery: true
  timeout: 30s
```

### API Configuration
```python
CURRENCY_API = {
    "base_url": "https://api.exchangerate-api.com/v4/latest/",
    "fallback_url": "https://api.fixer.io/latest",
    "timeout": 10,
    "cache_duration": 3600  # 1 hour
}
```

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/test_agent.py -v
pytest tests/test_currency_service.py -v
pytest tests/test_mcp_integration.py -v
```

### Integration Tests
```bash
# Test currency conversion
python -m currency_agent.test_conversion --from USD --to EUR --amount 100

# Test MCP context
python -m currency_agent.test_mcp_context

# Test A2A communication
python -m currency_agent.test_a2a_messages
```

### Manual Testing
```bash
# Start the agent
adk run currency_agent

# Test queries:
# "Convert 100 USD to EUR"
# "What's the exchange rate for GBP to JPY?"
# "Convert 50 euros to dollars"
```

---

## 🚢 Running the Agent

### Local Development
```bash
# Set environment variables
export CURRENCY_API_KEY=your_key_here

# Run the agent
adk run currency_agent --local

# Access the agent
curl -X POST http://localhost:8080/convert \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "from": "USD", "to": "EUR"}'
```

### Production Deployment
```bash
# Deploy to Agent Engine
adk deploy currency_agent --environment production

# Verify deployment
adk status currency_agent
```

---

## 📊 Results

### Supported Operations

1. **Currency Conversion**
   - Input: Amount, source currency, target currency
   - Output: Converted amount with exchange rate

2. **Exchange Rate Lookup**
   - Input: Currency pair (e.g., USD/EUR)
   - Output: Current exchange rate

3. **Historical Data**
   - Input: Currency pair and date range
   - Output: Historical exchange rates

4. **Multi-Currency Conversion**
   - Input: Amount and list of target currencies
   - Output: Conversion to all specified currencies

### Example Interactions

**User:** "Convert 100 USD to EUR"
**Agent:** "100 USD equals 85.50 EUR at the current exchange rate of 0.855"

**User:** "What about to GBP and JPY?"
**Agent:** "Based on your previous conversion:
- 100 USD = 78.20 GBP (rate: 0.782)
- 100 USD = 11,050 JPY (rate: 110.50)"

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** API rate limit exceeded
- **Solution:** Implement caching and rate limiting in `currency_service.py`

**Issue:** MCP context not persisting
- **Solution:** Check MCP client configuration and connection

**Issue:** Stale exchange rates
- **Solution:** Adjust cache duration in configuration

**Issue:** A2A timeout errors
- **Solution:** Increase timeout value or check network connectivity

---

## 🔒 Security Considerations

- Store API keys securely using environment variables
- Implement rate limiting to prevent abuse
- Validate all input currencies against supported list
- Sanitize user inputs before processing
- Use HTTPS for all API communications
- Implement proper error handling and logging

---

## 📖 Additional Resources

- [ADK Documentation](https://developers.google.com/adk)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Currency Exchange API Documentation](https://exchangerate-api.com/docs)
- [A2A Protocol Guide](https://developers.google.com/adk/a2a)
- [Financial Data Best Practices](https://developers.google.com/adk/financial)

---

## 🎥 Video Walkthrough

See the main repository for video demonstration of:
- Agent setup and configuration
- Currency conversion functionality
- MCP context management
- A2A protocol integration
- Real-time exchange rate updates
- Error handling and edge cases

---

## ✅ Completion Checklist

- [ ] Currency agent implemented
- [ ] MCP integration complete
- [ ] A2A protocol configured
- [ ] API integration working
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Video walkthrough recorded
- [ ] Deployment successful

---

## 📝 Notes

*Add your implementation notes, API observations, and learnings here.*

### Performance Metrics
- Average response time:
- API call latency:
- Cache hit rate:
- Conversion accuracy:

### Lessons Learned
- MCP context management strategies
- A2A communication patterns
- API error handling approaches
- Caching optimization techniques
