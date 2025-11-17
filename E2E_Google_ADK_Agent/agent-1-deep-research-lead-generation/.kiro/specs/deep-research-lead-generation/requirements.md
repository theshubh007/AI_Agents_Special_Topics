# Requirements Document

## Introduction

This document defines the requirements for building a deep research agent for lead generation using Google's Agent Development Kit (ADK). The system will emulate the analytical process of a market research team by discovering patterns in successful companies and generating qualified leads based on dynamic understanding of success criteria. The agent architecture uses a hierarchical structure of cooperative agents with parallel processing capabilities.

## Glossary

- **Root Agent**: The primary orchestrator agent (InteractiveLeadGenerator) that manages workflow, delegates to specialized sub-agents, and interacts with users
- **Pattern Discovery Workflow**: The process of analyzing historical company data to identify success patterns
- **Lead Generation Workflow**: The process of finding potential leads based on discovered success patterns
- **Research Squad**: Collection of agents responsible for analyzing historical data and finding success signals
- **Hunter Squad**: Collection of agents responsible for finding future leads based on success patterns
- **SequentialAgent**: An ADK agent type that executes sub-agents in a defined sequence
- **AgentTool**: An ADK abstraction that wraps a SequentialAgent into a callable function
- **Session State**: Persistent data structure maintaining context across multiple agent turns
- **Validation Pipeline**: A process that scrutinizes companies against strict criteria
- **Parallel Execution**: Running multiple agent pipelines simultaneously for efficiency

## Requirements

### Requirement 1

**User Story:** As a business development professional, I want to provide my target industry and country so that the agent can understand my lead generation needs

#### Acceptance Criteria

1. WHEN a user provides an initial request, THE Root Agent SHALL delegate intent extraction to the Intent Extractor Agent
2. THE Intent Extractor Agent SHALL parse user input into structured data containing industry, country, and user intent
3. THE Intent Extractor Agent SHALL use the gemini-2.5-flash model for fast processing
4. THE Intent Extractor Agent SHALL output data conforming to the IntentExtractionResult schema
5. WHEN intent extraction completes, THE Root Agent SHALL confirm understanding with the user before proceeding

### Requirement 2

**User Story:** As a market researcher, I want the system to discover patterns in successful companies so that I can understand what makes companies succeed in my target market

#### Acceptance Criteria

1. WHEN user intent is confirmed, THE Root Agent SHALL invoke the Pattern Discovery Workflow via AgentTool
2. THE Pattern Discovery Agent SHALL execute sub-agents in the following sequence: CompanyFinderAgent, CompanyFormatterAgent, ResearchOrchestratorAgent, SynthesizerOrchestratorAgent, PatternSynthesizerAgent
3. THE CompanyFinderAgent SHALL execute searches to find companies based on user-specified industry and country
4. THE CompanyFormatterAgent SHALL transform raw company data into standardized structure
5. THE PatternSynthesizerAgent SHALL identify common threads and synthesize them into an evidence-based report with source citations

### Requirement 3

**User Story:** As a system architect, I want the research process to validate multiple companies in parallel so that the system operates efficiently at scale

#### Acceptance Criteria

1. THE ResearchOrchestratorAgent SHALL create a validation pipeline for each discovered company
2. THE ResearchOrchestratorAgent SHALL execute all validation pipelines in parallel
3. WHEN a company enters validation, THE ValidatorAgent SHALL scrutinize the company against strict criteria
4. THE SynthesizerOrchestratorAgent SHALL gather validated data from all parallel pipelines
5. THE SynthesizerOrchestratorAgent SHALL consolidate data into a unified dataset for pattern analysis

### Requirement 4

**User Story:** As a user, I want to review and confirm discovered patterns before lead generation begins so that I can ensure the search criteria align with my goals

#### Acceptance Criteria

1. WHEN pattern discovery completes, THE Root Agent SHALL present findings to the user
2. THE Root Agent SHALL use the get_user_choice tool to obtain user confirmation
3. IF the user requests modifications, THEN THE Root Agent SHALL re-execute pattern discovery with updated parameters
4. THE Root Agent SHALL NOT proceed to lead generation until receiving explicit user approval
5. THE Session State SHALL maintain pattern discovery results across interaction turns

### Requirement 5

**User Story:** As a sales professional, I want the system to find potential leads matching discovered success patterns so that I can focus on high-quality prospects

#### Acceptance Criteria

1. WHEN patterns are confirmed, THE Root Agent SHALL invoke the Lead Generation Workflow via AgentTool
2. THE Lead Generation Agent SHALL execute sub-agents in the following sequence: LeadFinderAgent, LeadFormatterAgent, LeadResearchOrchestratorAgent, ReportOrchestratorAgent, ReportCompilerAgent
3. THE LeadFinderAgent SHALL use synthesized patterns as search queries to find similar companies
4. THE LeadFormatterAgent SHALL standardize raw lead data for parallel processing
5. THE ReportCompilerAgent SHALL generate a comprehensive report of qualified leads

### Requirement 6

**User Story:** As a data analyst, I want each potential lead to be validated and analyzed in parallel so that I receive comprehensive insights efficiently

#### Acceptance Criteria

1. THE LeadResearchOrchestratorAgent SHALL create an analysis pipeline for each potential lead
2. THE LeadResearchOrchestratorAgent SHALL execute all analysis pipelines in parallel
3. FOR each lead, THE LeadResearchOrchestratorAgent SHALL run both ValidatorAgent and LeadSignalAnalyzerAgent simultaneously
4. THE ValidatorAgent SHALL verify lead quality against established criteria
5. THE LeadSignalAnalyzerAgent SHALL identify specific success signals in each lead

### Requirement 7

**User Story:** As a system administrator, I want the root agent to manage workflow state across multiple interactions so that the system maintains context throughout the process

#### Acceptance Criteria

1. THE Root Agent SHALL register a before_agent_callback that executes before each agent turn
2. THE before_agent_callback SHALL initialize or update session state
3. THE Root Agent SHALL register an after_tool_callback that executes after any tool completes
4. THE after_tool_callback SHALL process tool output and update the stage variable in session state
5. THE Session State SHALL persist across all agent turns within a single session

### Requirement 8

**User Story:** As a developer, I want the root agent to use AgentTool abstractions for workflow delegation so that complex multi-step processes can be invoked as single function calls

#### Acceptance Criteria

1. THE Pattern Discovery Agent SHALL be wrapped in an AgentTool
2. THE Lead Generation Agent SHALL be wrapped in an AgentTool
3. THE Root Agent SHALL include both AgentTools in its tools list
4. WHEN the Root Agent invokes an AgentTool, THE entire SequentialAgent workflow SHALL execute
5. THE AgentTool SHALL return consolidated results to the Root Agent upon completion

### Requirement 9

**User Story:** As a user, I want the root agent to maintain an interactive and proactive approach so that I feel guided through the lead generation process

#### Acceptance Criteria

1. THE Root Agent SHALL use the gemini-2.5-pro model for advanced reasoning
2. THE Root Agent SHALL follow the instruction: "assist user in finding leads by discovering patterns, confirm findings, execute lead generation"
3. THE Root Agent SHALL proactively communicate progress at each workflow stage
4. THE Root Agent SHALL request user input at decision points using the get_user_choice tool
5. THE Root Agent SHALL maintain a conversational tone throughout all interactions

### Requirement 10

**User Story:** As a system operator, I want the agent architecture to support environment-based model configuration so that I can optimize performance and cost

#### Acceptance Criteria

1. THE Root Agent SHALL use the model specified in GEN_ADVANCED_MODEL environment variable with fallback to "gemini-2.5-pro"
2. THE Intent Extractor Agent SHALL use the model specified in GEN_FAST_MODEL environment variable with fallback to "gemini-2.5-flash"
3. WHERE model configuration is not specified in environment variables, THE System SHALL use default model values
4. THE System SHALL support switching models without code changes
5. THE System SHALL validate that specified models are available before agent initialization
