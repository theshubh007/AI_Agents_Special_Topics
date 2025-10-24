# 🎓 Academic Research Assistant with ADK

## 🎯 Project Overview

This project demonstrates building a sophisticated multi-agent AI system using Google's Agent Development Kit (ADK) to accelerate academic literature reviews. The implementation showcases advanced agent orchestration patterns including sequential workflows, loop agents for iterative refinement, and specialized sub-agents working in concert to deliver personalized research insights.

The system analyzes a researcher's academic profile, searches for relevant recent publications, and generates detailed comparative analyses showing how new papers relate to the researcher's work—all through natural conversation.


## 📹 Video Demonstration
https://youtu.be/Cp3Fl-m5IFA


## ✨ Key Features

### 🔍 Intelligent Research Profile Analysis

- **Profile Extraction** from Google Scholar, ORCID, and other academic platforms
- **Research Identity Recognition** with key concepts and methodologies
- **Semantic Understanding** of your academic specialization
- **Automatic Keyword Generation** for optimized search queries

### 📚 Advanced Academic Search

- **Multi-Database Search** across Google Scholar, arXiv, PubMed, and more
- **Intelligent Query Construction** based on your research profile
- **Recent Publications Filter** for cutting-edge research
- **Adaptive Search Refinement** based on initial results
- **Robust Search Implementation** with automatic SerpAPI fallback for reliability

### 🧠 Research Synthesis & Analysis

- **Thematic Connection** identification between papers and your work
- **Methodological Innovation** spotting for research advancement
- **Supporting & Contradictory Evidence** analysis for comprehensive understanding
- **Quality-Assured Reports** with multi-step critique and refinement

### 📊 Insightful Reporting

- **Annotated Bibliography** with personalized relevance notes
- **Connection Categorization** across themes, methods, and evidence
- **Research Gap Identification** for potential new directions
- **Actionable Insights** tailored to your academic profile

## 🏗️ Architecture Overview

The system implements a hierarchical multi-agent architecture with three distinct workflow layers:

### 1. Root Orchestrator Agent
The main coordinator that manages the overall workflow:
- Collects user inputs (research topic and profile URL)
- Executes a deterministic state machine
- Delegates tasks to specialized sub-agents
- Handles error scenarios and user guidance

### 2. Specialized Sub-Agents

**Profiler Agent:**
- Extracts keywords from researcher's academic profile
- Analyzes research identity and specialization
- Identifies key concepts and methodologies
- Uses web scraping tools to parse profile pages

**Searcher Agent:**
- Finds relevant academic papers based on topic and keywords
- Implements robust two-tier search strategy:
  - Primary: Scrapy-based Google Scholar scraper
  - Fallback: SerpAPI integration for reliability
- Filters for recent publications (last 5 years)
- Handles rate limiting and blocking gracefully

**Comparison Root Agent (Sequential):**
- Orchestrates analysis generation and refinement
- Implements a loop agent for iterative improvement
- Contains two sub-agents:
  - **Analysis Generator**: Creates detailed paper comparisons
  - **Analysis Critic**: Reviews and refines the analysis
- **Formatter Agent**: Prepares final report for presentation

### 3. Agent Interaction Flow

```
Root Orchestrator
   │
   ├─► State 1: PROFILING
   │   └─► Profiler Agent → Extract keywords from profile
   │
   ├─► State 2: SEARCHING  
   │   └─► Searcher Agent → Find relevant papers
   │
   └─► State 3: COMPARISON
       └─► Comparison Root Agent (Sequential)
           ├─► Loop Agent (max 5 iterations)
           │   ├─► Analysis Generator → Create comparison
           │   └─► Analysis Critic → Review & refine
           └─► Formatter Agent → Present final report
```

## 📋 Implementation Phases

### Phase 1: Environment Setup

**Prerequisites:**
- Python 3.9 or newer
- Google ADK (`pip install google-adk`)
- Chrome browser (for Selenium web scraping)
- Public academic profile (Google Scholar, ORCID, etc.)

**Installation:**
```bash
# Navigate to project directory
cd academic-research-assistant

# Install dependencies
pip install -r requirements.txt
```

**Configuration (.env file):**
```bash
# Required
GOOGLE_API_KEY=your_gemini_api_key_here
MODEL=gemini-2.0-flash

# Optional
DISABLE_WEB_DRIVER=0  # 0=enabled, 1=disabled
SERPAPI_KEY=your_serpapi_key_here  # Fallback search
```

### Phase 2: Agent Architecture Implementation

**Root Orchestrator:**
```python
academic_research_assistant = Agent(
    model=constants.MODEL,
    name="academic_research_assistant",
    description="An AI assistant to accelerate academic literature reviews.",
    instruction=prompts.ROOT_PROMPT,
    sub_agents=[
        comparison_root_agent,
        profiler_agent,
        searcher_agent,  
    ],
)
```

**Key Design Patterns:**
- **State Machine**: Deterministic workflow (GREET → PROFILE → SEARCH → COMPARE)
- **Sequential Agent**: For ordered execution of analysis steps
- **Loop Agent**: For iterative refinement (max 5 iterations)
- **Tool Integration**: Web scraping, API calls, and data processing

### Phase 3: Running the Agent

**Start the agent:**
```bash
adk run academic_research_assistant

# Or use web interface
adk web
```

**Interaction flow:**
1. Agent greets and explains the process
2. User provides research topic and profile URL
3. Agent executes three-stage workflow
4. Agent presents personalized research report

## 💬 Example Interactions

### 🎯 Machine Learning Researcher

```text
You: "I'm researching reinforcement learning for robotics. Here's my profile: 
      https://scholar.google.com/citations?user=..."

Agent: "Analyzing your profile... I've identified keywords: reinforcement learning, 
        robotics, policy gradient methods, multi-agent systems.
        
        Searching for relevant papers... Found 5 recent publications."

[Agent provides annotated bibliography with detailed relevance notes]

Paper 1: "Sample-Efficient Reinforcement Learning for Robot Manipulation Tasks"
Relevance Note: This paper presents a methodological innovation by combining 
contrastive learning with policy gradient methods - directly building on your
work with TRPO algorithms. Their approach achieves 75% faster convergence and
could address the sample efficiency challenges mentioned in your 2022 paper.
```

### 🧬 Biomedical Scientist

```text
You: "I'm interested in CRISPR gene editing techniques. Here's my ORCID: 
      https://orcid.org/..."

Agent: "Based on your profile, I see you focus on CRISPR-Cas9 off-target effects 
        and delivery mechanisms. Searching for relevant papers..."

[Agent provides detailed analysis of new methodologies and contradictory findings]

Paper 3: "Novel delivery vectors for CRISPR-Cas9 with reduced immunogenicity"
Relevance Note: This presents supporting evidence for your hypothesis on 
lipid nanoparticle delivery systems, confirming your findings on reduced
immune response while extending the work to new tissue types not covered
in your research.
```

## ⚙️ Advanced Configuration

### 🔍 Search Engine Customization

Edit `.env` file to customize search behavior:

```bash
# Enable/disable web driver for interactive searches
DISABLE_WEB_DRIVER=0  # 0=enabled, 1=disabled

# Change model for different capabilities
MODEL=gemini-2.0-pro  # For more sophisticated analysis

# SerpAPI Configuration (optional fallback mechanism)
SERPAPI_KEY=your_serpapi_key_here  # Only used when primary search fails
```

### 📊 Analysis Customization

You can modify the prompts in `academic_research_assistant/sub_agents/comparison_root_agent/prompt.py` to customize analysis focus:

```python
# Customize analysis categories
- **Thematic Overlap**: "This paper addresses the same theme of 'X' seen in your work on 'Y'."
- **Methodological Innovation**: "This is relevant because it uses a novel 'Z' methodology that could be applied to your research."
- **Supporting Evidence**: "Its findings on 'A' provide strong support for your previous conclusions about 'B'."
- **Contradictory Evidence**: "This paper's results challenge your work on 'C' by showing 'D', suggesting a new direction for investigation."
```

## 📁 Project Structure

```
academic-research-assistant/
├── academic_research_assistant/
│   ├── agent.py                    # Root orchestrator agent
│   ├── prompts.py                  # Root agent instructions
│   │
│   ├── sub_agents/
│   │   ├── profiler_agent/         # Profile analysis
│   │   │   ├── agent.py
│   │   │   └── prompt.py
│   │   │
│   │   ├── searcher_agent/         # Paper search
│   │   │   ├── agent.py
│   │   │   └── prompt.py
│   │   │
│   │   └── comparison_root_agent/  # Analysis orchestration
│   │       ├── agent.py            # Sequential + Loop agents
│   │       └── sub_agents/
│   │           ├── analysis_generator_agent/
│   │           ├── analysis_critic_agent/
│   │           └── analysis_formatter_agent/
│   │
│   ├── tools/                      # Utility functions
│   │   ├── scholar_scraper.py      # Scrapy + SerpAPI search
│   │   ├── serpapi_tools.py        # SerpAPI integration
│   │   └── url_scraper.py          # Profile scraping
│   │
│   └── shared_libraries/
│       └── constants.py            # Configuration constants
│
├── .env.example                    # Environment template
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation
```

## 🔑 Key Concepts

### Multi-Agent Orchestration
- **Root agent** coordinates workflow through state machine
- **Sub-agents** handle specialized tasks independently
- **Sequential agent** ensures ordered execution
- **Loop agent** enables iterative refinement

### Robust Search Implementation
- **Two-tier strategy**: Primary Scrapy scraper + SerpAPI fallback
- **Rate limiting handling**: Random delays and user agent rotation
- **Error resilience**: Automatic fallback when primary method fails
- **Thread-safe design**: Avoids event loop conflicts

### Analysis Quality Assurance
- **Generator-Critic pattern**: Iterative improvement loop
- **Multi-step refinement**: Up to 5 iterations for quality
- **Structured output**: Formatted reports with clear categorization
- **Personalized insights**: Tailored to researcher's profile

### Tool Integration Patterns
- **Web scraping**: Selenium + BeautifulSoup for profile extraction
- **API integration**: SerpAPI for reliable academic search
- **Artifact management**: Screenshot and data persistence
- **Error handling**: Graceful degradation and user feedback

## 🚀 Usage Examples

### Machine Learning Researcher
```
User: "I'm researching reinforcement learning for robotics. 
       Here's my profile: https://scholar.google.com/citations?user=..."

Agent: "Analyzing your profile... I've identified keywords: reinforcement 
        learning, robotics, policy gradient methods, multi-agent systems.
        
        Searching for relevant papers... Found 5 recent publications.
        
        Generating your comparison report now..."

[Agent provides annotated bibliography with detailed relevance analysis]
```

### Biomedical Scientist
```
User: "I'm interested in CRISPR gene editing techniques. 
       Here's my ORCID: https://orcid.org/..."

Agent: "Based on your profile, I see you focus on CRISPR-Cas9 off-target 
        effects and delivery mechanisms. Searching for relevant papers..."

[Agent provides analysis categorized by themes, methods, and evidence]
```

## 💡 Key Takeaways

1. **Hierarchical agent architecture** - Root orchestrator with specialized sub-agents
2. **Sequential and loop agents** - Advanced workflow patterns for complex tasks
3. **Robust search strategy** - Primary + fallback methods ensure reliability
4. **Iterative refinement** - Generator-critic loop improves output quality
5. **Personalized analysis** - Profile-based keyword extraction and relevance scoring
6. **Production-ready patterns** - Error handling, rate limiting, and graceful degradation

