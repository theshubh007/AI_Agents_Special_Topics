# Deep Research Lead Generation Agent

An intelligent multi-agent system built with Google's Generative AI that discovers patterns in successful companies and generates qualified leads based on data-driven insights.

## Features

- 🎯 **Intent Extraction**: Automatically parses user requests into structured criteria
- 🔬 **Pattern Discovery**: Analyzes successful companies to identify common success patterns
- ✅ **Parallel Validation**: Validates multiple companies simultaneously for efficiency
- 🚀 **Lead Generation**: Finds potential leads matching discovered patterns
- 📊 **Comprehensive Reports**: Generates detailed analysis with prioritized leads
- 💬 **Interactive Workflow**: Guides users through each step with confirmations


## 📹 Video Demonstration
[Walkthrough YouTube Video](https://youtu.be/XyXIlwc8AXU)

## Architecture

The system uses a hierarchical multi-agent architecture:

```
Root Agent (InteractiveLeadGenerator)
├── Intent Extractor Agent
├── Pattern Discovery Workflow
│   ├── Company Finder
│   ├── Company Formatter
│   ├── Research Orchestrator (parallel validation)
│   ├── Synthesizer Orchestrator
│   └── Pattern Synthesizer
└── Lead Generation Workflow
    ├── Lead Finder
    ├── Lead Formatter
    ├── Lead Research Orchestrator (parallel analysis)
    ├── Report Orchestrator
    └── Report Compiler
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Google API key:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Configuration

Environment variables in `.env`:

- `GOOGLE_API_KEY`: Your Google Generative AI API key (required)
- `GEN_ADVANCED_MODEL`: Model for complex reasoning (default: gemini-2.0-flash-exp)
- `GEN_FAST_MODEL`: Model for fast processing (default: gemini-2.0-flash-exp)

## Usage

Run the interactive agent:

```bash
python main.py
```

Example conversation:

```
You: Find SaaS companies in Germany

Agent: I understand you're looking for leads in:
- Industry: SaaS
- Country: Germany
- Goal: Find successful SaaS companies for lead generation

Is this correct? (yes/no)

You: yes

Agent: ✅ Pattern Discovery Complete!

I analyzed 12 companies and found these success patterns:
1. Cloud-native architecture with API-first approach
   - Confidence: 0.85
   - Found in 10 companies
...

Would you like to proceed with lead generation based on these patterns?

You: yes

Agent: 🎉 Lead Generation Complete!

Found 25 high-quality leads matching your criteria...
```

## Project Structure

```
.
├── agent.py                    # Root agent implementation
├── main.py                     # Entry point
├── config.py                   # Configuration management
├── models.py                   # Data models (Pydantic)
├── error_handling.py           # Error handling utilities
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── callbacks/
│   └── state_manager.py       # Session state management
├── tools/
│   └── user_interaction.py    # User interaction tools
└── sub_agents/
    ├── intent_extractor/      # Intent extraction agent
    ├── shared/
    │   └── validator/         # Reusable validation agent
    ├── pattern_discovery/     # Pattern discovery workflow
    │   ├── company_finder/
    │   ├── company_formatter/
    │   ├── research_orchestrator/
    │   ├── synthesizer_orchestrator/
    │   └── pattern_synthesizer/
    └── lead_generation/       # Lead generation workflow
        ├── lead_finder/
        ├── lead_formatter/
        ├── lead_research_orchestrator/
        ├── signal_analyzer/
        ├── report_orchestrator/
        └── report_compiler/
```

## Data Models

Key data structures:

- `IntentExtractionResult`: Parsed user intent
- `CompanyData`: Standardized company information
- `ValidationResult`: Company validation assessment
- `SuccessPattern`: Identified success pattern
- `PatternReport`: Complete pattern analysis
- `LeadData`: Potential lead information
- `SignalAnalysis`: Lead quality signals
- `LeadAnalysisResult`: Complete lead assessment
- `LeadReport`: Final lead generation report
- `SessionState`: Conversation state management

## Workflow

1. **Intent Extraction**: User provides industry and country
2. **Pattern Discovery**: System analyzes successful companies
3. **User Review**: User confirms or modifies patterns
4. **Lead Generation**: System finds matching leads
5. **Report Delivery**: User receives prioritized leads

## Performance

- Parallel execution for validation and analysis
- Efficient resource utilization
- Scalable to large datasets
- Typical execution time: 5-15 minutes for complete workflow

## Error Handling

- Automatic retry with exponential backoff
- Graceful degradation for partial results
- Session state persistence
- Comprehensive error messages

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
