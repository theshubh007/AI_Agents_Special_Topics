# 🛒 Purchasing Concierge with A2A Action Engine

## 🎯 Project Goal

This repository demonstrates the architecture and implementation of an intelligent purchasing concierge system using Google's Agent-to-Agent (A2A) protocol and Agent Development Kit (ADK). The project showcases how A2A enables multiple autonomous agents from different vendors to collaborate seamlessly in a real-world e-commerce scenario.

The implementation highlights A2A's complementary role to MCP (Model Context Protocol) where MCP focuses on tool integration while A2A focuses on agent collaboration. The purchasing concierge coordinates with specialized seller agents (burger and pizza vendors) to help users make informed purchasing decisions, demonstrating practical multi-agent coordination patterns.

## 📹 Video Demonstration
https://youtu.be/GpihZLwoDSw

## CodeLab Link
https://codelabs.developers.google.com/intro-a2a-purchasing-concierge#0

## 🏗️ Architecture Overview

The system implements a client-server A2A architecture with three distinct agent layers:

### 1. Client Agent Layer (Purchasing Concierge)

The main orchestrator that:

- Interacts with users to understand purchasing needs
- Discovers available seller agents via A2A protocol
- Sends purchase requests to multiple vendors simultaneously
- Compares responses from different sellers
- Presents consolidated recommendations to users
- Manages the end-to-end purchasing workflow

### 2. Remote Agent Layer (Seller Agents)

Specialized vendor agents that:

**Burger Agent:**
- Manages burger restaurant inventory
- Provides menu information and pricing
- Handles burger-specific purchase requests
- Returns availability and delivery estimates

**Pizza Agent:**
- Manages pizza restaurant inventory
- Provides menu options and pricing
- Handles pizza-specific purchase requests
- Returns availability and delivery estimates

### 3. A2A Protocol Layer

The communication infrastructure providing:

- **Universal Interoperability:** Agents from different frameworks communicate seamlessly
- **Capability Discovery:** Agents advertise capabilities via Agent Cards (JSON documents)
- **Secure Collaboration:** Enterprise-grade authentication (HTTPS/TLS, JWT, OIDC, API keys)
- **Modality Agnostic:** Supports text, audio, video streaming, interactive forms

## 🔄 MCP vs A2A: Complementary Protocols

### Model Context Protocol (MCP)
- **Purpose:** Connect LLMs with **tools and data**
- **Focus:** Tool invocation and resource access
- **Use Case:** Agent → MCP Server → External API/Database
- **Example:** Currency agent using MCP to access exchange rate API

### Agent-to-Agent (A2A)
- **Purpose:** Connect **agents with other agents**
- **Focus:** Agent collaboration and coordination
- **Use Case:** Agent ← A2A → Agent
- **Example:** Concierge agent coordinating with seller agents

### Recommended Pattern
```
┌─────────────────────────────────────────────┐
│    Purchasing Concierge Agent (Client)      │
│    ├── Uses MCP for tools (if needed)       │
│    └── Uses A2A for agent communication     │
└──────────────┬──────────────────────────────┘
               │ A2A Protocol
       ┌───────┴────────┐
       ↓                ↓
┌─────────────┐  ┌─────────────┐
│ Burger Agent│  │ Pizza Agent │
│ (Server)    │  │ (Server)    │
│ MCP: Tools  │  │ MCP: Tools  │
└─────────────┘  └─────────────┘
```

## 📋 Implementation Phases

### Phase 1: A2A Protocol Understanding

**Core A2A Principles:**

1. **Secure Collaboration**
   - Authentication via HTTPS/TLS, JWT, OIDC, API keys
   - Protected sensitive data transmission
   - Secure agent-to-agent handshakes

2. **Task and State Management**
   - Maintain conversation context across agents
   - Track workflow state during multi-step processes
   - Handle asynchronous agent responses

3. **User Experience Negotiation**
   - Enable natural back-and-forth communication
   - Support complex user interactions
   - Handle clarifications and confirmations

4. **Capability Discovery**
   - Agents advertise skills via Agent Cards
   - Dynamic agent discovery at runtime
   - Capability matching for task delegation

**A2A Message Flow:**

```
User → Concierge Agent
         ↓
    Discover Seller Agents (A2A)
         ↓
    ┌────┴────┐
    ↓         ↓
Burger Agent  Pizza Agent
    ↓         ↓
Get Menu Info + Availability
    ↓         ↓
    └────┬────┘
         ↓
Compare & Present to User
         ↓
User Makes Selection
         ↓
Execute Purchase (A2A)
```

### Phase 2: Seller Agent Implementation

**Burger Agent Structure:**

```python
# remote_seller_agents/burger_agent/agent.py
from google.adk.agents import Agent

burger_agent = Agent(
    model='gemini-2.0-flash',
    name='burger_seller',
    description='Burger restaurant agent that handles burger orders',
    instruction="""
    You are a burger restaurant agent. You can:
    1. Provide menu information (burgers, fries, drinks)
    2. Check availability of items
    3. Process purchase requests
    4. Provide pricing and delivery estimates
    
    Your menu includes:
    - Classic Burger: $8.99
    - Cheeseburger: $9.99
    - Bacon Burger: $10.99
    - Veggie Burger: $8.99
    - Fries: $3.99
    - Drinks: $2.99
    
    Always be helpful and respond to purchase inquiries promptly.
    """,
    tools=[check_burger_inventory, process_burger_order]
)
```

**Pizza Agent Structure:**

```python
# remote_seller_agents/pizza_agent/agent.py
from google.adk.agents import Agent

pizza_agent = Agent(
    model='gemini-2.0-flash',
    name='pizza_seller',
    description='Pizza restaurant agent that handles pizza orders',
    instruction="""
    You are a pizza restaurant agent. You can:
    1. Provide menu information (pizzas, sides, drinks)
    2. Check availability of items
    3. Process purchase requests
    4. Provide pricing and delivery estimates
    
    Your menu includes:
    - Margherita Pizza: $12.99
    - Pepperoni Pizza: $14.99
    - Vegetarian Pizza: $13.99
    - BBQ Chicken Pizza: $15.99
    - Garlic Bread: $4.99
    - Drinks: $2.99
    
    Always be helpful and respond to purchase inquiries promptly.
    """,
    tools=[check_pizza_inventory, process_pizza_order]
)
```

**Deploying Seller Agents:**

```bash
# Deploy Burger Agent to Cloud Run
cd remote_seller_agents/burger_agent
gcloud run deploy burger-agent \
  --source=. \
  --region=us-central1 \
  --allow-unauthenticated

# Deploy Pizza Agent to Cloud Run
cd remote_seller_agents/pizza_agent
gcloud run deploy pizza-agent \
  --source=. \
  --region=us-central1 \
  --allow-unauthenticated
```

### Phase 3: Purchasing Concierge Development

**Main Concierge Agent:**

```python
# purchasing_concierge/agent.py
from google.adk.agents import Agent
from google.adk.a2a import A2AClient

class PurchasingConcierge(Agent):
    def __init__(self):
        super().__init__(
            model='gemini-2.0-flash',
            name='purchasing_concierge',
            description='Intelligent purchasing assistant',
            instruction="""
            You are a helpful purchasing concierge. When users want to buy food:
            1. Ask what they're interested in (burgers, pizza, etc.)
            2. Use A2A to contact relevant seller agents
            3. Get availability and pricing from multiple vendors
            4. Compare options and present recommendations
            5. Help complete the purchase with selected vendor
            
            Be conversational, helpful, and efficient.
            """
        )
        self.a2a_client = A2AClient()
        self.seller_agents = {
            'burger': 'https://burger-agent-url.run.app',
            'pizza': 'https://pizza-agent-url.run.app'
        }
    
    async def find_and_compare(self, user_query):
        """Contact multiple sellers and compare offerings."""
        responses = []
        
        for vendor, url in self.seller_agents.items():
            response = await self.a2a_client.send_message(
                target_url=url,
                message={
                    'query': user_query,
                    'request_type': 'menu_and_availability'
                }
            )
            responses.append({
                'vendor': vendor,
                'data': response
            })
        
        return self.compare_and_recommend(responses)
```

**A2A Connection Handler:**

```python
# purchasing_concierge/remote_agent_connection.py
from google.adk.a2a import A2AConnection

class RemoteAgentConnection:
    def __init__(self, agent_url: str):
        self.agent_url = agent_url
        self.connection = A2AConnection(agent_url)
    
    async def send_request(self, message: dict) -> dict:
        """Send A2A request to remote agent."""
        response = await self.connection.invoke(message)
        return response
    
    async def discover_capabilities(self) -> dict:
        """Get agent card with capabilities."""
        card = await self.connection.get_agent_card()
        return card
```

### Phase 4: Streamlit UI Development

**User Interface Implementation:**

```python
# purchasing_concierge_ui.py
import streamlit as st
from purchasing_concierge.agent import PurchasingConcierge

st.title("🛒 Purchasing Concierge")
st.write("Your intelligent shopping assistant for food delivery")

# Initialize concierge
if 'concierge' not in st.session_state:
    st.session_state.concierge = PurchasingConcierge()

# User input
user_query = st.text_input("What would you like to order?", 
                           placeholder="e.g., I want a burger and fries")

if st.button("Find Options"):
    with st.spinner("Contacting vendors..."):
        # A2A calls to seller agents
        results = await st.session_state.concierge.find_and_compare(user_query)
        
        # Display comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🍔 Burger Options")
            st.write(results['burger'])
        
        with col2:
            st.subheader("🍕 Pizza Options")
            st.write(results['pizza'])
        
        # Recommendation
        st.success(f"Recommendation: {results['recommendation']}")
```

### Phase 5: Agent Engine Deployment

**Deploy Concierge to Agent Engine:**

```python
# deploy_to_agent_engine.py
from google.adk.deployment import AgentEngineDeployer

deployer = AgentEngineDeployer(
    project_id='YOUR_PROJECT_ID',
    region='us-central1'
)

# Deploy purchasing concierge
deployment = deployer.deploy(
    agent=purchasing_concierge,
    name='purchasing-concierge',
    authentication_required=False,
    a2a_enabled=True
)

print(f"Deployed at: {deployment.endpoint_url}")
```

**Configure A2A Endpoints:**

```yaml
# agent_config.yaml
agent:
  name: purchasing_concierge
  version: 1.0.0
  
a2a:
  enabled: true
  endpoints:
    burger_agent:
      url: https://burger-agent-url.run.app
      authentication: none
      timeout: 30s
    pizza_agent:
      url: https://pizza-agent-url.run.app
      authentication: none
      timeout: 30s
  
  discovery:
    enabled: true
    method: agent_card
```

## 🚀 Usage Examples

The purchasing concierge handles various shopping scenarios:

**Simple Order Request:**

```
User: "I want to order a burger"
→ Concierge contacts Burger Agent via A2A
→ Burger Agent: "Classic Burger $8.99, available, 20-min delivery"
→ Concierge: "I found a Classic Burger for $8.99 with 20-minute delivery. Would you like to proceed?"
```

**Comparison Shopping:**

```
User: "I'm hungry, what are my options?"
→ Concierge sends A2A requests to both agents
→ Burger Agent: Returns burger menu and prices
→ Pizza Agent: Returns pizza menu and prices
→ Concierge: Presents comparison:
  "Burgers from $8.99 (20-min delivery)
   Pizzas from $12.99 (30-min delivery)
   What would you prefer?"
```

**Multi-Item Order:**

```
User: "I need food for 4 people"
→ Concierge: "What type of food would you prefer?"
User: "Pizza"
→ Concierge contacts Pizza Agent via A2A
→ Pizza Agent: "2 Large Pizzas + Garlic Bread = $35.97"
→ Concierge: "I recommend 2 large pizzas and garlic bread for $35.97. Shall I proceed?"
```

**Availability Check:**

```
User: "Do they have veggie options?"
→ Concierge queries both agents via A2A
→ Burger Agent: "Veggie Burger $8.99 ✓"
→ Pizza Agent: "Vegetarian Pizza $13.99 ✓"
→ Concierge: "Both have vegetarian options. Would you prefer a veggie burger ($8.99) or vegetarian pizza ($13.99)?"
```

## 🔄 Interaction Flow

1. **User Request** → "I want to order food"
2. **Intent Analysis** → Concierge determines food type needed
3. **Agent Discovery** → Identify relevant seller agents via A2A
4. **Parallel Queries** → Send A2A requests to multiple vendors simultaneously
5. **Response Collection** → Gather menu, pricing, and availability
6. **Comparison Logic** → Analyze and compare vendor offerings
7. **Recommendation** → Present best options to user
8. **Order Execution** → Forward purchase request to selected vendor via A2A
9. **Confirmation** → Return order confirmation to user

## 🔑 Key Concepts

### A2A Protocol Features

**1. Universal Interoperability:**
- Agents built with different frameworks (ADK, LangChain, CrewAI) can communicate
- Technology-agnostic communication standard
- No vendor lock-in

**2. Capability Discovery:**
- Agents advertise capabilities using Agent Cards
- Dynamic discovery of available agents
- Skill-based agent matching

**3. Secure by Default:**
- Enterprise-grade authentication
- HTTPS/TLS encryption
- JWT, OIDC support
- API key management

**4. Modality Agnostic:**
- Text communication
- Audio/video streaming
- Interactive forms
- Embedded iframes

### Agent Card Structure

```json
{
  "name": "burger_seller",
  "description": "Burger restaurant agent",
  "version": "1.0.0",
  "capabilities": [
    "menu_information",
    "availability_check",
    "order_processing",
    "delivery_estimation"
  ],
  "menu_items": [
    {"name": "Classic Burger", "price": 8.99},
    {"name": "Cheeseburger", "price": 9.99},
    {"name": "Fries", "price": 3.99}
  ],
  "authentication": {
    "type": "none",
    "required": false
  },
  "endpoint": "https://burger-agent-url.run.app",
  "protocol": "a2a"
}
```

### Multi-Agent Coordination Patterns

**Pattern 1: Broadcast and Aggregate**
```python
# Send same query to multiple agents
responses = await asyncio.gather(
    a2a_client.query(burger_agent, query),
    a2a_client.query(pizza_agent, query)
)
# Aggregate and compare results
```

**Pattern 2: Sequential Delegation**
```python
# Step 1: Query availability
availability = await a2a_client.query(seller_agent, "check_stock")
# Step 2: If available, process order
if availability['in_stock']:
    order = await a2a_client.query(seller_agent, "process_order")
```

**Pattern 3: Conditional Routing**
```python
# Route based on user preference
if user_wants == 'burger':
    result = await a2a_client.query(burger_agent, order_details)
elif user_wants == 'pizza':
    result = await a2a_client.query(pizza_agent, order_details)
```

## 🔗 Learning Resources

- **Original Codelab:** https://codelabs.developers.google.com/intro-a2a-purchasing-concierge
- **A2A Protocol Documentation:** https://developers.google.com/adk/a2a
- **ADK Documentation:** https://developers.google.com/adk
- **Agent Engine Guide:** https://cloud.google.com/agent-engine
- **Multi-Agent Patterns:** https://developers.google.com/adk/multi-agent-patterns
- **A2A Python SDK:** https://github.com/google/adk-a2a-python

## 🧹 Cleanup

Always clean up Google Cloud resources to manage costs:

```bash
# Delete seller agents from Cloud Run
gcloud run services delete burger-agent --region=us-central1
gcloud run services delete pizza-agent --region=us-central1

# Delete concierge from Agent Engine
gcloud agent-engine agents delete purchasing-concierge \
  --project YOUR_PROJECT_ID \
  --region us-central1

# Delete container images
gcloud artifacts docker images delete \
  us-central1-docker.pkg.dev/PROJECT_ID/burger-agent

gcloud artifacts docker images delete \
  us-central1-docker.pkg.dev/PROJECT_ID/pizza-agent
```

## 💡 Key Takeaways

1. **A2A for Agent Collaboration** - A2A enables seamless multi-agent coordination
2. **Complementary to MCP** - Use MCP for tools, A2A for agent communication
3. **Distributed Architecture** - Agents can run on different platforms/vendors
4. **Real-world Application** - Demonstrates practical e-commerce use case
5. **Agent Discovery** - Dynamic capability discovery via Agent Cards
6. **Scalable Pattern** - Easy to add more seller agents
7. **User-Centric Design** - Concierge provides unified interface to multiple services

## 🎓 Advanced Topics

### Adding Authentication

```python
# Secure A2A communication
from google.auth import default

credentials, project = default()

a2a_client = A2AClient(
    credentials=credentials,
    authentication_required=True
)
```

### Implementing Caching

```python
# Cache seller responses
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_menu(agent_url: str):
    response = await a2a_client.query(agent_url, "get_menu")
    return response
```

### Error Handling

```python
async def query_with_retry(agent_url, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = await a2a_client.query(agent_url, query)
            return response
        except A2ATimeoutError:
            if attempt == max_retries - 1:
                return {"error": "Agent unavailable"}
            await asyncio.sleep(2 ** attempt)
```

### Adding More Vendors

```python
# Easy to extend with more agents
self.seller_agents = {
    'burger': 'https://burger-agent-url.run.app',
    'pizza': 'https://pizza-agent-url.run.app',
    'sushi': 'https://sushi-agent-url.run.app',  # New vendor
    'mexican': 'https://mexican-agent-url.run.app'  # New vendor
}
```

## 📊 Performance Metrics

Expected performance characteristics:

- **A2A Message Latency:** < 100ms
- **Agent Response Time:** 1-2 seconds
- **Parallel Query Time:** 2-3 seconds (multiple agents)
- **End-to-End Flow:** 3-5 seconds
- **Concurrent Users:** 1000+ (with proper scaling)

## 🐛 Troubleshooting

### Common Issues

**Issue:** Seller agent not responding
- **Solution:** Verify Cloud Run service is running, check logs

**Issue:** A2A connection timeout
- **Solution:** Increase timeout settings, check network connectivity

**Issue:** Agent discovery fails
- **Solution:** Verify Agent Card is accessible at /.well-known/agent.json

**Issue:** Invalid response format
- **Solution:** Ensure agents follow A2A message schema

**Issue:** Authentication errors
- **Solution:** Check credentials configuration, verify OIDC setup

## 🔐 Security Considerations

- Use HTTPS for all A2A communications
- Implement proper authentication (JWT, OIDC, API keys)
- Validate all incoming A2A messages
- Rate limit to prevent abuse
- Sanitize user inputs before forwarding to agents
- Log all inter-agent communications for audit
- Use Secret Manager for credentials
- Implement proper CORS policies

## 📝 Project Structure

```
codelab-3-purchasing-concierge/
├── purchasing-concierge-a2a/
│   ├── purchasing_concierge/
│   │   ├── __init__.py
│   │   ├── agent.py                    # Main concierge agent
│   │   ├── purchasing_agent.py         # Purchasing logic
│   │   ├── remote_agent_connection.py  # A2A connection handler
│   │   └── README.md
│   ├── remote_seller_agents/
│   │   ├── burger_agent/
│   │   │   ├── __main__.py
│   │   │   ├── agent.py                # Burger seller agent
│   │   │   ├── agent_executor.py
│   │   │   ├── Dockerfile
│   │   │   ├── pyproject.toml
│   │   │   └── README.md
│   │   └── pizza_agent/
│   │       ├── __main__.py
│   │       ├── agent.py                # Pizza seller agent
│   │       ├── agent_executor.py
│   │       ├── Dockerfile
│   │       ├── pyproject.toml
│   │       └── README.md
│   ├── deploy_to_agent_engine.py       # Deployment script
│   ├── purchasing_concierge_ui.py      # Streamlit UI
│   ├── test_agent_connection.py        # A2A connection tests
│   ├── test_agent_engine.sh            # Test script
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── uv.lock
│   └── README.md
└── README.md                            # This file
```

## ✅ Completion Checklist

- [ ] Python environment setup complete
- [ ] Burger seller agent implemented
- [ ] Pizza seller agent implemented
- [ ] Both seller agents deployed to Cloud Run
- [ ] Purchasing concierge agent implemented
- [ ] A2A connections configured and tested
- [ ] Streamlit UI developed
- [ ] Local testing completed
- [ ] Agent Engine deployment successful
- [ ] End-to-end purchasing workflow tested
- [ ] Documentation complete
- [ ] Video walkthrough recorded

## 🚧 Testing

### Test Seller Agents Locally

```bash
# Test Burger Agent
cd remote_seller_agents/burger_agent
python agent.py

# Test Pizza Agent
cd remote_seller_agents/pizza_agent
python agent.py
```

### Test A2A Communication

```bash
# Test agent discovery
python test_agent_connection.py --agent burger --action discover

# Test menu query
python test_agent_connection.py --agent pizza --action menu

# Test order processing
python test_agent_connection.py --agent burger --action order \
  --item "Classic Burger" --quantity 2
```

### Test Complete Workflow

```bash
# Run Streamlit UI locally
streamlit run purchasing_concierge_ui.py

# Or test via Python
python -c "
from purchasing_concierge.agent import PurchasingConcierge
import asyncio

async def test():
    concierge = PurchasingConcierge()
    result = await concierge.find_and_compare('I want a burger')
    print(result)

asyncio.run(test())
"
```

## 🔄 Future Enhancements

- [ ] Add payment processing integration
- [ ] Implement order tracking via A2A
- [ ] Add more cuisine types (sushi, mexican, etc.)
- [ ] Implement user preferences and history
- [ ] Add dietary restriction filtering
- [ ] Integrate with map services for delivery tracking
- [ ] Add reviews and ratings system
- [ ] Implement loyalty points across vendors
- [ ] Add voice interface support
- [ ] Create mobile app version

---

**Last Updated:** October 2025
**Codelab Link:** https://codelabs.developers.google.com/intro-a2a-purchasing-concierge
**Assignment:** CMPE-297 Special Topics - MCP and A2A Codelab

**Note:** This codelab demonstrates A2A protocol which is currently a work in progress (WIP). There might be changes to the implementation as the protocol evolves. Always refer to the official documentation for the latest updates.
