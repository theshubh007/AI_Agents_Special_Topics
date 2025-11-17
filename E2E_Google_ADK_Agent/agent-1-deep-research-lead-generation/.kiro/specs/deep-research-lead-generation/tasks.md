# Implementation Plan

- [x] 1. Set up project structure and core data models





  - Create directory structure: agent.py, sub_agents/, tools/, callbacks/, models/
  - Define all data model classes: IntentExtractionResult, CompanyData, ValidationResult, SuccessPattern, PatternReport, LeadData, SignalAnalysis, LeadAnalysisResult, LeadReport, SessionState
  - Implement schema validation for structured outputs
  - _Requirements: 1.2, 1.4, 2.4, 3.4, 5.4, 6.4, 7.4, 10.3_

- [x] 2. Implement Intent Extractor Agent


  - Create sub_agents/intent_extractor/agent.py with LlmAgent configuration
  - Write INTENT_EXTRACTOR_PROMPT instruction
  - Configure gemini-2.5-flash model with environment variable support
  - Set output_schema to IntentExtractionResult
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 10.2_

- [x] 3. Implement Pattern Discovery Workflow - Company Discovery Phase




  - [x] 3.1 Create Company Finder Agent

    - Implement sub_agents/pattern_discovery/company_finder/agent.py
    - Write search logic for companies based on industry and country
    - Integrate web search and company database tools
    - _Requirements: 2.3_
  
  - [x] 3.2 Create Company Formatter Agent



    - Implement sub_agents/pattern_discovery/company_formatter/agent.py
    - Write data normalization and standardization logic
    - Transform raw data into CompanyData objects
    - Implement deduplication logic
    - _Requirements: 2.4_


- [x] 4. Implement Pattern Discovery Workflow - Validation Phase

  - [x] 4.1 Create Validator Agent (reusable)



    - Implement sub_agents/shared/validator/agent.py
    - Define validation criteria and scoring algorithm
    - Implement validation logic returning ValidationResult
    - Add rejection reason tracking
    - _Requirements: 3.3_
  

  - [x] 4.2 Create Research Orchestrator Agent


    - Implement sub_agents/pattern_discovery/research_orchestrator/agent.py
    - Implement parallel execution pattern using asyncio.gather
    - Create validation pipeline for each company
    - Handle concurrent validator agent invocations
    - _Requirements: 3.1, 3.2_
  
  - [x] 4.3 Create Synthesizer Orchestrator Agent



    - Implement sub_agents/pattern_discovery/synthesizer_orchestrator/agent.py
    - Gather and consolidate validated data from parallel pipelines
    - Filter invalid results and aggregate valid data
    - _Requirements: 3.4, 3.5_


- [x] 5. Implement Pattern Discovery Workflow - Synthesis Phase

  - Create Pattern Synthesizer Agent in sub_agents/pattern_discovery/pattern_synthesizer/agent.py
  - Implement pattern detection algorithm across companies
  - Calculate confidence scores and frequency metrics
  - Track evidence and source citations
  - Generate PatternReport with SuccessPattern objects
  - _Requirements: 2.5_





- [x] 6. Create Pattern Discovery SequentialAgent


  - Implement sub_agents/pattern_discovery/agent.py




  - Configure SequentialAgent with all 5 sub-agents in order
  - Set agent name and description
  - _Requirements: 2.1, 2.2_

- [x] 7. Implement Lead Generation Workflow - Lead Discovery Phase

  - [ ] 7.1 Create Lead Finder Agent
    - Implement sub_agents/lead_generation/lead_finder/agent.py
    - Use PatternReport to construct search queries
    - Find companies matching success patterns




    - _Requirements: 5.3_
  
  - [ ] 7.2 Create Lead Formatter Agent
    - Implement sub_agents/lead_generation/lead_formatter/agent.py
    - Standardize raw lead data into LeadData objects
    - Calculate initial match scores
    - Track matching patterns and discovery sources

    - _Requirements: 5.4_


- [ ] 8. Implement Lead Generation Workflow - Analysis Phase
  - [x] 8.1 Create Lead Signal Analyzer Agent



    - Implement sub_agents/lead_generation/signal_analyzer/agent.py
    - Detect success signals in leads

    - Calculate signal strength scores
    - Identify growth indicators and risk factors
    - Generate SignalAnalysis objects
    - _Requirements: 6.5_

  




  - [ ] 8.2 Create Lead Research Orchestrator Agent
    - Implement sub_agents/lead_generation/lead_research_orchestrator/agent.py
    - Implement parallel execution for all leads
    - Run Validator and Signal Analyzer simultaneously per lead
    - Combine results into LeadAnalysisResult objects
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  




  - [x] 8.3 Create Report Orchestrator Agent

    - Implement sub_agents/lead_generation/report_orchestrator/agent.py
    - Consolidate all LeadAnalysisResult objects
    - Rank and filter leads by priority



    - Group leads by categories
    - _Requirements: 5.4_


- [x] 9. Implement Lead Generation Workflow - Report Phase

  - Create Report Compiler Agent in sub_agents/lead_generation/report_compiler/agent.py


  - Generate executive summary
  - Categorize leads into high/medium priority
  - Create pattern match analysis
  - Generate recommendations

  - Produce final LeadReport
  - _Requirements: 5.5_



- [ ] 10. Create Lead Generation SequentialAgent
  - Implement sub_agents/lead_generation/agent.py
  - Configure SequentialAgent with all 5 sub-agents in order
  - Set agent name and description

  - _Requirements: 5.1, 5.2_

- [ ] 11. Implement State Management System
  - [x] 11.1 Create session state management

    - Implement callbacks/state_manager.py
    - Define SessionState class with all required fields
    - Implement load_or_create_session function
    - Implement save_session function
    - _Requirements: 7.4, 7.5_
  

  - [-] 11.2 Implement before_agent_run callback

    - Create callbacks/before_agent_run.py
    - Initialize or restore session state
    - Set state in agent context
    - _Requirements: 7.1, 7.2_
  

  - [x] 11.3 Implement after_tool_run callback

    - Create callbacks/after_tool_run.py
    - Process tool output
    - Update stage variable based on completed tool
    - Save updated session state
    - _Requirements: 7.3, 7.4_

- [x] 12. Create AgentTool abstractions


  - Implement tools/agent_tools.py
  - Wrap pattern_discovery_agent in AgentTool
  - Wrap lead_generation_agent in AgentTool
  - Export agent_tools list
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 13. Implement user interaction tool



  - Create tools/user_interaction.py
  - Implement get_user_choice function
  - Handle user confirmation and feedback
  - Support modification requests
  - _Requirements: 4.2, 9.4_

- [-] 14. Implement Root Agent


  - [x] 14.1 Create root agent configuration



    - Implement agent.py with Agent configuration
    - Set name to "InteractiveLeadGenerator"
    - Configure gemini-2.5-pro model with environment variable
    - Write ROOT_AGENT_INSTRUCTION
    - Add tools: get_user_choice and agent_tools
    - Register callbacks: before_agent_run and after_tool_run
    - _Requirements: 9.1, 9.2, 10.1_
  



  - [ ] 14.2 Implement root agent workflow logic
    - Delegate intent extraction to Intent Extractor Agent
    - Confirm intent with user before proceeding
    - Invoke Pattern Discovery Workflow via AgentTool
    - Present pattern findings and request user approval
    - Handle modification requests by re-executing pattern discovery
    - Invoke Lead Generation Workflow only after approval
    - Communicate progress proactively at each stage
    - _Requirements: 1.1, 1.5, 2.1, 4.1, 4.3, 4.4, 5.1, 9.3, 9.5_

- [x] 15. Implement error handling


  - Create error_handling.py with AgentError class
  - Implement handle_agent_error function with recovery strategies
  - Add retry logic with exponential backoff for data retrieval
  - Implement timeout management for all agents
  - Add graceful degradation for partial results
  - _Requirements: All requirements (error handling support)_


- [-] 16. Create environment configuration

  - Create .env.example file with GEN_ADVANCED_MODEL and GEN_FAST_MODEL
  - Implement config.py to load environment variables
  - Add model validation logic
  - Set default fallback values
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 17. Create main entry point



  - Implement main.py or run.py
  - Initialize root agent
  - Set up session management
  - Handle user input loop
  - Display results and reports
  - _Requirements: All requirements (system integration)_

- [ ]* 18. Write unit tests
  - [ ]* 18.1 Test Intent Extractor Agent
    - Test valid input parsing
    - Test missing field handling
    - Test ambiguous input resolution
    - _Requirements: 1.2, 1.4_
  
  - [ ]* 18.2 Test Company Formatter Agent
    - Test data normalization
    - Test deduplication logic
    - Test schema validation
    - _Requirements: 2.4_
  
  - [ ]* 18.3 Test Validator Agent
    - Test validation criteria application
    - Test scoring algorithm
    - Test edge cases
    - _Requirements: 3.3_
  
  - [ ]* 18.4 Test Pattern Synthesizer Agent
    - Test pattern detection accuracy
    - Test confidence scoring
    - Test source citation
    - _Requirements: 2.5_
  
  - [ ]* 18.5 Test Signal Analyzer Agent
    - Test signal detection
    - Test risk assessment
    - Test scoring consistency
    - _Requirements: 6.5_

- [ ]* 19. Write integration tests
  - [ ]* 19.1 Test Pattern Discovery Workflow
    - Test end-to-end execution
    - Test parallel orchestration
    - Test state transitions
    - _Requirements: 2.1, 2.2, 3.1, 3.2_
  
  - [ ]* 19.2 Test Lead Generation Workflow
    - Test pattern-based search
    - Test dual-agent parallel execution
    - Test report generation
    - _Requirements: 5.1, 5.2, 6.1, 6.2, 6.3_
  
  - [ ]* 19.3 Test Root Agent Coordination
    - Test tool invocation
    - Test callback execution
    - Test user interaction flow
    - _Requirements: 7.1, 7.2, 7.3, 8.3, 8.4, 9.4_

- [ ]* 20. Write end-to-end tests
  - [ ]* 20.1 Test happy path
    - Test complete journey: Intent → Pattern Discovery → Review → Lead Generation
    - Verify final state and reports
    - _Requirements: All requirements_
  
  - [ ]* 20.2 Test modification path
    - Test pattern discovery with user-requested changes
    - Test re-execution with updated parameters
    - _Requirements: 4.3, 4.4_
  
  - [ ]* 20.3 Test error recovery
    - Test API failure with retry
    - Test partial results handling
    - _Requirements: Error handling_

- [ ]* 21. Create documentation
  - [ ]* 21.1 Write README.md
    - Document installation steps
    - Explain configuration options
    - Provide usage examples
    - Include architecture overview
  
  - [ ]* 21.2 Write API documentation
    - Document all agent interfaces
    - Document data models
    - Document callback system
  
  - [ ]* 21.3 Create example scripts
    - Create example usage scenarios
    - Add sample configuration files
    - Include mock data for testing
