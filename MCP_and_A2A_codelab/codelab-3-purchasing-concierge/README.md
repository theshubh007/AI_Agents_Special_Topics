# Codelab 3: Purchasing Concierge with A2A Action Engine

**Codelab Link:** [Getting Started with A2A Action Engine](https://codelabs.developers.google.com/intro-a2a-purchasing-concierge#0)

---

## 📋 Overview

This codelab introduces the A2A Action Engine through building an intelligent purchasing concierge agent. The agent assists users with making purchasing decisions, comparing products, finding deals, and coordinating the buying process across multiple services using the Agent-to-Agent (A2A) protocol.

**Learning Objectives:**
- Understand A2A Action Engine architecture
- Build a purchasing concierge agent
- Implement action coordination between agents
- Manage complex multi-step purchasing workflows
- Integrate with e-commerce APIs and services

---

## 🎯 What You'll Build

An intelligent purchasing concierge that:
- Helps users find and compare products
- Provides personalized recommendations
- Coordinates actions across multiple services
- Manages the entire purchasing workflow
- Tracks orders and provides updates
- Uses A2A to communicate with specialized agents (inventory, payment, shipping)

---

## 🛠️ Prerequisites

Before starting this codelab, ensure you have:
- Python 3.10 or higher installed
- Google ADK installed
- Google Cloud Project with billing enabled
- Basic understanding of e-commerce workflows
- Familiarity with REST APIs and webhooks

---

## 📚 Key Concepts

### A2A Action Engine
A powerful framework for orchestrating actions across multiple agents:
- **Action Discovery:** Find available actions from other agents
- **Action Coordination:** Sequence and coordinate complex workflows
- **Action Execution:** Execute actions across distributed agents
- **State Management:** Maintain workflow state across actions

### Purchasing Concierge Architecture
```
User Request → Concierge Agent → A2A Action Engine
                                        ↓
                        ┌───────────────┼───────────────┐
                        ↓               ↓               ↓
                Product Search    Price Compare    Inventory Check
                        ↓               ↓               ↓
                        └───────────────┼───────────────┘
                                        ↓
                            Payment Processing Agent
                                        ↓
                            Shipping Coordination Agent
                                        ↓
                            Order Tracking Agent
```

### Agent Roles

1. **Concierge Agent (Main)**
   - User interaction
   - Workflow orchestration
   - Decision making

2. **Product Search Agent**
   - Product discovery
   - Feature matching
   - Catalog search

3. **Price Comparison Agent**
   - Price aggregation
   - Deal finding
   - Price alerts

4. **Inventory Agent**
   - Stock verification
   - Availability checking
   - Reservation management

5. **Payment Agent**
   - Payment processing
   - Transaction security
   - Receipt generation

6. **Shipping Agent**
   - Shipping coordination
   - Tracking management
   - Delivery estimation

---

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install google-adk
pip install google-cloud-agent-engine
pip install a2a-action-engine
pip install fastapi uvicorn
```

### 2. Configure Environment
Create a `.env` file:
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
A2A_ACTION_ENGINE_API_KEY=your-api-key
PAYMENT_GATEWAY_KEY=your-payment-key
SHIPPING_API_KEY=your-shipping-key
```

### 3. Initialize Project
```bash
adk init purchasing-concierge
cd purchasing-concierge
```

### 4. Set Up Action Engine
```bash
gcloud config set project YOUR_PROJECT_ID
gcloud services enable actionengine.googleapis.com
```

---

## 📁 Project Structure

```
codelab-3-purchasing-concierge/
├── README.md                          # This file
├── .env.example                       # Environment variables template
├── requirements.txt                   # Python dependencies
├── purchasing_concierge/
│   ├── __init__.py
│   ├── main_agent.py                 # Main concierge agent
│   ├── action_coordinator.py         # Action Engine coordinator
│   └── workflow_manager.py           # Workflow state management
├── specialized_agents/
│   ├── __init__.py
│   ├── product_search_agent.py      # Product search functionality
│   ├── price_comparison_agent.py    # Price comparison
│   ├── inventory_agent.py           # Inventory management
│   ├── payment_agent.py             # Payment processing
│   └── shipping_agent.py            # Shipping coordination
├── actions/
│   ├── __init__.py
│   ├── search_actions.py            # Search-related actions
│   ├── purchase_actions.py          # Purchase workflow actions
│   └── tracking_actions.py          # Order tracking actions
├── config/
│   ├── action_engine_config.yaml    # Action Engine configuration
│   ├── agent_definitions.yaml       # Agent specifications
│   └── workflow_templates.yaml      # Workflow definitions
├── api/
│   ├── __init__.py
│   ├── ecommerce_client.py         # E-commerce API client
│   └── payment_client.py           # Payment gateway client
└── tests/
    ├── test_concierge.py
    ├── test_workflow.py
    └── test_actions.py
```

---

## 💻 Implementation

### Main Concierge Agent

```python
from google_adk import Agent
from a2a_action_engine import ActionEngine

class PurchasingConcierge(Agent):
    def __init__(self):
        super().__init__(name="purchasing_concierge")
        self.action_engine = ActionEngine()
        
    async def process_purchase_request(self, user_request):
        # Parse user intent
        intent = await self.parse_intent(user_request)
        
        # Create workflow
        workflow = await self.create_workflow(intent)
        
        # Execute workflow using A2A Action Engine
        result = await self.action_engine.execute_workflow(workflow)
        
        return result
    
    async def create_workflow(self, intent):
        return {
            "workflow_id": self.generate_id(),
            "steps": [
                {"action": "search_products", "agent": "product_search_agent"},
                {"action": "compare_prices", "agent": "price_comparison_agent"},
                {"action": "check_inventory", "agent": "inventory_agent"},
                {"action": "process_payment", "agent": "payment_agent"},
                {"action": "coordinate_shipping", "agent": "shipping_agent"}
            ],
            "state": {}
        }
```

### Action Engine Configuration

```yaml
# action_engine_config.yaml
action_engine:
  name: purchasing_action_engine
  version: 1.0.0
  
  agents:
    - name: product_search_agent
      actions:
        - search_by_category
        - search_by_features
        - get_product_details
    
    - name: price_comparison_agent
      actions:
        - compare_across_vendors
        - find_best_deal
        - check_price_history
    
    - name: inventory_agent
      actions:
        - check_availability
        - reserve_item
        - get_stock_levels
    
    - name: payment_agent
      actions:
        - process_payment
        - validate_payment_method
        - issue_refund
    
    - name: shipping_agent
      actions:
        - calculate_shipping
        - coordinate_delivery
        - track_shipment

  workflows:
    - name: standard_purchase
      description: "Standard product purchase workflow"
      steps:
        - search
        - compare
        - check_inventory
        - payment
        - shipping
```

### Action Definitions

```python
# Example action implementation
from a2a_action_engine import Action

class SearchProductsAction(Action):
    async def execute(self, params):
        query = params.get("query")
        category = params.get("category")
        
        # Search products
        products = await self.search_service.search(
            query=query,
            category=category
        )
        
        # Return results via A2A
        return {
            "status": "success",
            "products": products,
            "count": len(products)
        }

class ComparepricesAction(Action):
    async def execute(self, params):
        product_ids = params.get("product_ids")
        
        # Compare prices across vendors
        comparisons = await self.price_service.compare(product_ids)
        
        return {
            "status": "success",
            "comparisons": comparisons,
            "best_deal": self.find_best_deal(comparisons)
        }
```

### Workflow Execution

```python
# Example workflow execution
async def execute_purchase_workflow(user_request):
    concierge = PurchasingConcierge()
    
    # Step 1: Search for products
    search_result = await concierge.action_engine.execute_action(
        agent="product_search_agent",
        action="search_by_category",
        params={"category": user_request.category}
    )
    
    # Step 2: Compare prices
    comparison_result = await concierge.action_engine.execute_action(
        agent="price_comparison_agent",
        action="compare_across_vendors",
        params={"products": search_result.products}
    )
    
    # Step 3: Check inventory
    inventory_result = await concierge.action_engine.execute_action(
        agent="inventory_agent",
        action="check_availability",
        params={"product_id": comparison_result.best_deal.id}
    )
    
    # Continue workflow...
    return final_result
```

---

## 🔧 Configuration

### Agent Definitions
```yaml
# agent_definitions.yaml
agents:
  concierge:
    name: purchasing_concierge
    role: orchestrator
    capabilities:
      - workflow_management
      - user_interaction
      - decision_making
    
  product_search:
    name: product_search_agent
    role: specialist
    capabilities:
      - product_discovery
      - catalog_search
      - feature_matching
  
  price_comparison:
    name: price_comparison_agent
    role: specialist
    capabilities:
      - price_aggregation
      - deal_finding
      - price_tracking
```

### Workflow Templates
```yaml
# workflow_templates.yaml
workflows:
  electronics_purchase:
    name: "Electronics Purchase Workflow"
    steps:
      - id: search
        agent: product_search_agent
        action: search_by_category
        params:
          category: electronics
      
      - id: compare
        agent: price_comparison_agent
        action: compare_across_vendors
        depends_on: [search]
      
      - id: check_warranty
        agent: warranty_agent
        action: verify_warranty
        depends_on: [compare]
      
      - id: finalize
        agent: payment_agent
        action: process_payment
        depends_on: [check_warranty]
```

---

## 🧪 Testing

### Unit Tests
```bash
# Test individual agents
pytest tests/test_concierge.py -v
pytest tests/test_specialized_agents.py -v

# Test actions
pytest tests/test_actions.py -v
```

### Workflow Tests
```bash
# Test complete workflows
python -m purchasing_concierge.test_workflow --workflow standard_purchase

# Test action coordination
python -m purchasing_concierge.test_action_coordination
```

### Integration Tests
```bash
# End-to-end purchase simulation
python -m purchasing_concierge.integration_test \
  --product "laptop" \
  --budget 1000 \
  --shipping-preference "express"
```

---

## 🚢 Deployment

### Deploy to Action Engine
```bash
# Deploy all agents
adk deploy purchasing-concierge --all-agents

# Deploy specific agent
adk deploy purchasing-concierge --agent product_search_agent

# Verify deployment
gcloud action-engine agents list
```

### Configure Webhooks
```bash
# Set up webhooks for order updates
curl -X POST https://actionengine.googleapis.com/v1/webhooks \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -d '{
    "url": "https://your-domain.com/webhooks/order-updates",
    "events": ["order.created", "order.shipped", "order.delivered"]
  }'
```

---

## 📊 Results

### Sample Interactions

**User:** "I need a laptop for programming under $1000"

**Concierge:** 
```
Searching for programming laptops under $1000...
Found 15 options. Comparing prices across vendors...
Best deal found: Dell XPS 13 at $899 from Vendor A
Checking inventory... In stock, 5 units available
Would you like to proceed with purchase?
```

**User:** "Yes, proceed"

**Concierge:**
```
Processing payment... Payment successful
Coordinating shipping... Estimated delivery: 3-5 business days
Order #12345 created successfully
You can track your order at: [tracking link]
```

### Metrics

- **Workflow Completion Rate:** 95%
- **Average Response Time:** 2.3 seconds
- **User Satisfaction:** 4.7/5
- **Successful Transactions:** 98%

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Action execution timeout
- **Solution:** Increase timeout in action_engine_config.yaml or optimize action logic

**Issue:** Workflow state inconsistency
- **Solution:** Implement proper state management with rollback capabilities

**Issue:** Agent communication failure
- **Solution:** Check A2A network configuration and agent availability

**Issue:** Payment processing errors
- **Solution:** Verify payment gateway credentials and test in sandbox mode

---

## 🔒 Security Best Practices

- Encrypt payment information at rest and in transit
- Implement proper authentication for all agents
- Use secure webhooks with signature verification
- Implement rate limiting to prevent abuse
- Log all transactions for audit purposes
- Implement PCI compliance for payment processing
- Use HTTPS for all communications

---

## 📖 Additional Resources

- [A2A Action Engine Documentation](https://cloud.google.com/action-engine)
- [ADK Workflow Guide](https://developers.google.com/adk/workflows)
- [E-commerce Integration Best Practices](https://developers.google.com/adk/ecommerce)
- [Payment Processing Security](https://developers.google.com/adk/payments)
- [Multi-Agent Coordination Patterns](https://developers.google.com/adk/patterns)

---

## 🎥 Video Walkthrough

See the main repository for video demonstration of:
- Concierge agent setup
- Product search and comparison
- Workflow execution
- Payment processing
- Order tracking
- Error handling scenarios
- Multi-agent coordination

---

## ✅ Completion Checklist

- [ ] All specialized agents implemented
- [ ] Action Engine configured
- [ ] Workflows defined and tested
- [ ] API integrations complete
- [ ] Payment processing working
- [ ] Shipping coordination functional
- [ ] End-to-end testing passed
- [ ] Security measures implemented
- [ ] Documentation complete
- [ ] Video walkthrough recorded

---

## 📝 Notes

*Add your implementation notes, observations, and learnings here.*

### Architecture Decisions
- Why specific workflow patterns were chosen
- Agent responsibility boundaries
- Error handling strategies
- State management approach

### Performance Optimizations
- Action caching strategies
- Parallel execution opportunities
- Database query optimizations
- API call batching

### Lessons Learned
- A2A Action Engine best practices
- Workflow coordination patterns
- Error recovery strategies
- Testing methodologies

---

## 🔄 Future Enhancements

- [ ] Add machine learning for recommendation improvement
- [ ] Implement dynamic pricing alerts
- [ ] Add voice interface support
- [ ] Integrate with more vendors
- [ ] Add social shopping features
- [ ] Implement wish list management
- [ ] Add subscription service support
