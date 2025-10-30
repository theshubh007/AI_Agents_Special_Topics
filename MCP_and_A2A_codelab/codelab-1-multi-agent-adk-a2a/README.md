# 🤖 Multi-Agent System with ADK, Deploy in Agent Engine and A2A Protocol

## 🎯 Project Goal

This repository demonstrates the architecture and implementation of a production-grade multi-agent system using Google's Agent Development Kit (ADK). The project showcases how to build a collaborative image generation and scoring system where specialized agents work together through hierarchical delegation and the Agent-to-Agent (A2A) protocol to accomplish complex tasks.

The implementation highlights the power of multi-agent architectures where a main orchestrator agent coordinates multiple sub-agents, each specialized in specific tasks (prompt refinement, image generation, and quality scoring), all communicating through the A2A protocol for seamless agent-to-agent interactions.

## 📹 Video Demonstration
*[Link to video walkthrough will be added here]*

## CodeLab Link
https://codelabs.developers.google.com/codelabs/create-multi-agents-adk-a2a#0

## 🏗️ Architecture Overview

The system operates through a hierarchical three-layer agent architecture:

### 1. Main Orchestrator Layer (image_scoring Agent)

The central coordination hub that:

- Receives user requests for image generation and scoring
- Analyzes the overall task requirements
- Delegates work to specialized sub-agents
- Aggregates results from sub-agents
- Maintains workflow state and orchestration logic

### 2. Sub-Agent Layer (Specialized Agents)

Three specialized agents working under the orchestrator:

**Prompt Agent:**
- Refines and optimizes user prompts
- Ensures prompts follow best practices for image generation
- Adds descriptive details for better image quality
- Validates prompt structure

**Image Generation Agent (Imagen):**
- Generates images using Google's Imagen API
- Accepts refined prompts from Prompt Agent
- Produces high-quality images based on specifications
- Handles multiple image variations

**Scoring Agent:**
- Evaluates generated images against policy criteria
- Performs quality assessment
- Checks adherence to content policies
- Provides detailed scoring feedback

### 3. A2A Communication Layer

The Agent-to-Agent protocol enables:

- **Universal Interoperability:** Agents built with different frameworks can communicate seamlessly
- **Capability Discovery:** Agents can advertise their capabilities using "Agent Cards" (JSON documents)
- **Secure Collaboration:** Enterprise-grade authentication using HTTPS/TLS, JWT, OIDC, and API keys
- **Modality Agnostic:** Supports text, audio, video streaming, and interactive forms

## 📋 Implementation Phases

### Phase 1: Infrastructure Setup

**Environment Configuration:**

- Install Python 3.10+ and required dependencies
- Set up Google Cloud Project with billing enabled
- Configure Google ADK and required APIs
- Install necessary Python packages (google-adk, Pillow, etc.)

**Project Initialization:**

```bash
# Install ADK
pip install google-adk

# Create new project
adk init multiagenthandson
cd multiagenthandson
```

### Phase 2: Agent Development

**Main Orchestrator Implementation:**

```python
# image_scoring/agent.py
from google.adk.agents import Agent

root_agent = Agent(
    model='gemini-2.0-flash',
    name='image_scoring',
    description='Main agent that orchestrates image generation and scoring',
    instruction="""
    You are the main orchestrator agent. When a user requests an image:
    1. Delegate to prompt_agent to refine the prompt
    2. Pass refined prompt to imagen_agent for generation
    3. Send generated images to scoring_agent for evaluation
    4. Return the final scored results to the user
    """,
    sub_agents=[prompt_agent, imagen_agent, scoring_agent]
)
```

**Prompt Agent Implementation:**

```python
# sub_agents/prompt/prompt_agent.py
prompt_agent = Agent(
    model='gemini-2.0-flash',
    name='prompt_agent',
    description='Refines and optimizes prompts for image generation',
    instruction="""
    Analyze the user's prompt and enhance it by:
    - Adding descriptive details
    - Ensuring clarity and specificity
    - Following image generation best practices
    - Maintaining the user's original intent
    """
)
```

**Image Generation Agent Implementation:**

```python
# sub_agents/image/imagen_agent.py
from imagen_tools import generate_image

imagen_agent = Agent(
    model='gemini-2.0-flash',
    name='imagen_agent',
    description='Generates images using Imagen API',
    instruction='Generate high-quality images based on the refined prompt',
    tools=[generate_image]
)
```

**Scoring Agent Implementation:**

```python
# sub_agents/scoring/scoring_agent.py
from scoring_tools import score_images

scoring_agent = Agent(
    model='gemini-2.0-flash',
    name='scoring_agent',
    description='Evaluates image quality and policy compliance',
    instruction="""
    Evaluate each generated image against policy criteria:
    - Quality assessment (composition, clarity, relevance)
    - Content policy compliance
    - Adherence to user requirements
    Provide detailed scoring feedback
    """,
    tools=[get_images_tool, set_score_tool]
)
```

### Phase 3: A2A Protocol Integration

**Agent Card Definition:**

```json
{
  "name": "image_scoring",
  "description": "Multi-agent image generation and scoring system",
  "capabilities": [
    "image_generation",
    "prompt_refinement",
    "quality_scoring"
  ],
  "authentication": {
    "type": "bearer_token",
    "required": true
  },
  "endpoint": "https://your-agent-url.com/invoke"
}
```

**A2A Message Structure:**

```python
{
    "sender": "image_scoring",
    "receiver": "remote_agent",
    "message_type": "task_request",
    "payload": {
        "action": "generate_and_score",
        "prompt": "refined_prompt_here",
        "parameters": {
            "num_images": 3,
            "quality_threshold": 0.8
        }
    },
    "correlation_id": "unique_request_id"
}
```

### Phase 4: Deployment to Agent Engine

**Local Testing:**

```bash
# Test locally
adk run image_scoring

# Test with sample query
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A serene mountain landscape at sunset"}'
```

**Agent Engine Deployment:**

```bash
# Deploy to Agent Engine
adk deploy agent-engine \
  --project YOUR_PROJECT_ID \
  --region us-central1 \
  --agent image_scoring

# Verify deployment
gcloud agent-engine agents list --project YOUR_PROJECT_ID
```

**A2A Server Configuration:**

```python
# a2a_agent.py
from google.adk.a2a import A2AServer

a2a_server = A2AServer(
    agent=root_agent,
    port=8080,
    authentication_required=True
)

# Start A2A server
a2a_server.start()
```

## 🚀 Usage Examples

The multi-agent system handles various image generation scenarios:

**Basic Image Generation:**

```
User: "Create an image of a sunset over the ocean"
→ Orchestrator receives request
→ Prompt Agent refines: "A breathtaking sunset over a calm ocean with vibrant orange and pink hues reflecting on the water"
→ Imagen Agent generates 3 variations
→ Scoring Agent evaluates each image
→ Returns highest-scored image with feedback
```

**Quality-Focused Generation:**

```
User: "Generate a professional product photo of a watch"
→ Prompt Agent adds: "High-quality professional product photography of a luxury watch, studio lighting, clean background, sharp focus"
→ Images generated with enhanced prompt
→ Scoring Agent checks: composition, lighting, clarity, professionalism
→ Returns image meeting quality criteria
```

**Policy Compliance Check:**

```
User: "Create an image for marketing campaign"
→ System generates images
→ Scoring Agent verifies: brand guidelines, content policy, image appropriateness
→ Returns compliant images with detailed scoring report
```

## 🔄 Interaction Flow

1. **User Query** → Natural language request for image generation
2. **Orchestrator Analysis** → Main agent parses intent and creates workflow
3. **Prompt Refinement** → Prompt Agent enhances the user's request
4. **Image Generation** → Imagen Agent creates multiple image variations
5. **Quality Scoring** → Scoring Agent evaluates images against criteria
6. **Result Aggregation** → Orchestrator compiles results and feedback
7. **User Response** → Delivers final images with scoring details

## 🔑 Key Concepts

### Multi-Agent Orchestration

- **Hierarchical Delegation:** Main agent delegates to specialized sub-agents
- **Task Decomposition:** Complex tasks broken into manageable sub-tasks
- **Result Aggregation:** Sub-agent outputs combined into cohesive results
- **State Management:** Workflow state maintained across agent interactions

### A2A Protocol Benefits

**Universal Interoperability:**
- Agents from different frameworks/vendors can collaborate
- Technology-agnostic communication standard
- Multi-agent ecosystem enablement

**Capability Discovery:**
- Agents advertise capabilities via Agent Cards
- Dynamic discovery of available agents and actions
- Skill-based agent selection

**Secure by Default:**
- Enterprise-grade authentication (HTTPS/TLS, JWT, OIDC)
- API key management
- Protected sensitive data

**Modality Agnostic:**
- Text, audio, video streaming support
- Interactive forms and embedded iframes
- Flexible information exchange

### ADK Agent Features

- **Tool Integration:** Agents can use external tools and APIs
- **Sub-Agent Support:** Hierarchical agent structures
- **Gemini Model Integration:** Powered by Google's Gemini models
- **Flexible Deployment:** Local testing and cloud deployment

## 🔗 Learning Resources

- **Original Codelab:** https://codelabs.developers.google.com/codelabs/create-multi-agents-adk-a2a#0
- **ADK Documentation:** https://developers.google.com/adk
- **A2A Protocol Specification:** https://developers.google.com/adk/a2a
- **Agent Engine Guide:** https://cloud.google.com/agent-engine
- **Multi-Agent Patterns:** https://developers.google.com/adk/multi-agent-patterns

## 🧹 Cleanup

Always clean up Google Cloud resources to manage costs:

```bash
# Delete Agent Engine deployment
gcloud agent-engine agents delete image_scoring \
  --project YOUR_PROJECT_ID \
  --region us-central1

# Disable APIs if no longer needed
gcloud services disable agentengine.googleapis.com

# Delete project resources
gcloud projects delete YOUR_PROJECT_ID  # Use with caution
```

## 💡 Key Takeaways

1. **Multi-Agent Architecture** - Hierarchical agent structures enable complex task orchestration
2. **Specialized Agents** - Each sub-agent focuses on specific capabilities (prompting, generation, scoring)
3. **A2A Protocol** - Enables seamless communication between agents regardless of implementation
4. **Agent Engine Deployment** - Cloud-based agent hosting with scalability and reliability
5. **Production Patterns** - Demonstrates real-world multi-agent collaboration patterns
6. **Modular Design** - Clear separation of concerns between agents improves maintainability

## 🎓 Advanced Topics

### Custom Tool Development

```python
from google.adk.tools import Tool

@Tool(
    name='fetch_policy',
    description='Fetches content policy for image evaluation'
)
def fetch_policy_tool(policy_type: str) -> dict:
    # Load policy document
    with open('policy.json') as f:
        policy = json.load(f)
    return policy
```

### State Management

```python
# Maintain workflow state across agent calls
workflow_state = {
    'original_prompt': user_prompt,
    'refined_prompt': None,
    'generated_images': [],
    'scores': [],
    'status': 'in_progress'
}
```

### Error Handling

```python
try:
    images = await imagen_agent.generate(refined_prompt)
except GenerationError as e:
    # Fallback or retry logic
    logging.error(f"Image generation failed: {e}")
    return error_response(e)
```

## 📊 Performance Metrics

Expected performance characteristics:

- **Agent Response Time:** < 2 seconds for orchestration
- **Image Generation:** 5-10 seconds per image
- **Scoring Evaluation:** < 1 second per image
- **End-to-End Workflow:** 15-30 seconds
- **A2A Message Latency:** < 100ms

## 🔐 Security Considerations

- Store API keys securely using Secret Manager
- Implement proper authentication for A2A endpoints
- Validate all inputs before processing
- Use HTTPS for all agent communications
- Implement rate limiting to prevent abuse
- Log all agent interactions for audit trails

## 📝 Project Structure

```
codelab-1-multi-agent-adk-a2a/
├── multiagenthandson/
│   ├── image_scoring/
│   │   ├── __init__.py
│   │   ├── agent.py                 # Main orchestrator agent
│   │   ├── checker_agent.py         # Termination condition checker
│   │   ├── config.py                # Configuration settings
│   │   ├── policy.json              # Content policy document
│   │   ├── prompt.py                # Agent prompts
│   │   ├── sub_agents/
│   │   │   ├── prompt/
│   │   │   │   ├── prompt_agent.py  # Prompt refinement agent
│   │   │   │   └── prompt.py        # Prompt agent instructions
│   │   │   ├── image/
│   │   │   │   ├── imagen_agent.py  # Image generation agent
│   │   │   │   └── tools/
│   │   │   │       └── image_generation_tool.py
│   │   │   └── scoring/
│   │   │       ├── scoring_agent.py  # Image scoring agent
│   │   │       └── tools/
│   │   │           ├── get_images_tool.py
│   │   │           └── set_score_tool.py
│   │   └── tools/
│   │       └── loop_condition_tool.py
│   ├── image_scoring_adk_a2a_server/  # A2A server implementation
│   │   ├── a2a_agent.py
│   │   └── remote_a2a/
│   └── testclient/
│       └── remote_test.py            # Test client for A2A
├── requirements.txt
├── pyproject.toml
└── README.md
```

## ✅ Completion Checklist

- [ ] ADK and Python environment setup complete
- [ ] Main orchestrator agent implemented
- [ ] All three sub-agents (prompt, imagen, scoring) implemented
- [ ] Agent tools developed and integrated
- [ ] Local testing completed successfully
- [ ] A2A protocol configured and tested
- [ ] Deployed to Agent Engine (if required)
- [ ] Remote A2A testing completed
- [ ] Documentation updated
- [ ] Video walkthrough recorded

## 🚧 Troubleshooting

**Issue:** Sub-agents not responding
- **Solution:** Verify sub-agent registration in main agent's `sub_agents` list

**Issue:** Image generation fails
- **Solution:** Check Imagen API credentials and quota limits

**Issue:** A2A connection timeout
- **Solution:** Verify network connectivity and firewall rules

**Issue:** Policy scoring errors
- **Solution:** Ensure policy.json is properly formatted and accessible

---

**Last Updated:** October 2025
**Codelab Author:** Haren Bhandari, Google
**Assignment:** CMPE-297 Special Topics - MCP and A2A Codelab
