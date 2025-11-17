from google import genai
from google.genai.types import Tool, GenerateContentConfig, FunctionDeclaration
from config import GEN_ADVANCED_MODEL
from models import IntentExtractionResult, PatternReport, LeadReport
from sub_agents.intent_extractor.agent import extract_intent
from sub_agents.pattern_discovery.agent import pattern_discovery_workflow
from sub_agents.lead_generation.agent import lead_generation_workflow
from callbacks.state_manager import load_or_create_session, save_session
from tools.user_interaction import get_user_choice
from typing import Optional

ROOT_AGENT_INSTRUCTION = """You are an Interactive Lead Generator assistant. Your mission is to help users find high-quality leads by:

1. Understanding their intent (industry, country, goals)
2. Discovering patterns in successful companies
3. Getting user approval on patterns
4. Generating qualified leads based on approved patterns

Be conversational, proactive, and guide users through each step. Always confirm before proceeding to the next phase.

Available tools:
- extract_intent: Parse user request into structured data
- discover_patterns: Find success patterns in companies
- generate_leads: Find leads matching patterns
- get_user_confirmation: Ask user for approval

Workflow:
1. Extract intent from user request
2. Confirm intent with user
3. Run pattern discovery
4. Present patterns and get approval
5. Run lead generation
6. Present final report"""


class InteractiveLeadGenerator:
    def __init__(self, session_id: Optional[str] = None):
        self.client = genai.Client()
        self.session = load_or_create_session(session_id)
        self.model = GEN_ADVANCED_MODEL
        
    def run(self, user_input: str) -> str:
        """Main conversation loop."""
        
        # Add to conversation history
        self.session.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Route based on current stage
        if self.session.current_stage == "intent":
            response = self._handle_intent_stage(user_input)
        elif self.session.current_stage == "pattern_discovery":
            response = self._handle_pattern_discovery_stage(user_input)
        elif self.session.current_stage == "review":
            response = self._handle_review_stage(user_input)
        elif self.session.current_stage == "lead_generation":
            response = self._handle_lead_generation_stage(user_input)
        elif self.session.current_stage == "complete":
            response = self._handle_complete_stage(user_input)
        else:
            response = "I'm not sure what to do next. Let's start over. What industry and country are you interested in?"
            self.session.current_stage = "intent"
        
        # Save session
        self.session.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        save_session(self.session)
        
        return response
    
    def _handle_intent_stage(self, user_input: str) -> str:
        """Handle intent extraction stage."""
        try:
            print("\n🎯 Extracting intent...")
            intent = extract_intent(user_input)
            self.session.intent_data = intent
            
            # Confirm with user
            confirmation = f"""I understand you're looking for leads in:
- Industry: {intent.industry}
- Country: {intent.country}
- Goal: {intent.user_intent}

Is this correct? (yes/no)"""
            
            self.session.current_stage = "pattern_discovery"
            return confirmation
            
        except Exception as e:
            return f"I had trouble understanding your request. Could you please specify the industry and country you're interested in? Error: {str(e)}"
    
    def _handle_pattern_discovery_stage(self, user_input: str) -> str:
        """Handle pattern discovery stage."""
        user_input_lower = user_input.lower().strip()
        
        if user_input_lower in ["no", "n", "incorrect", "wrong"]:
            self.session.current_stage = "intent"
            return "Let me try again. What industry and country are you interested in?"
        
        if user_input_lower not in ["yes", "y", "correct", "ok", "proceed"]:
            return "Please confirm if the intent is correct (yes/no):"
        
        # Run pattern discovery
        try:
            print("\n🔬 Running pattern discovery workflow...")
            pattern_report = pattern_discovery_workflow(self.session.intent_data)
            self.session.pattern_report = pattern_report
            self.session.current_stage = "review"
            
            # Present patterns
            patterns_text = "\n".join([
                f"\n{i+1}. {p.description}\n   - Confidence: {p.confidence_score:.2f}\n   - Found in {p.frequency} companies"
                for i, p in enumerate(pattern_report.patterns[:5])
            ])
            
            return f"""✅ Pattern Discovery Complete!

I analyzed {pattern_report.total_companies_analyzed} companies and found these success patterns:
{patterns_text}

Would you like to proceed with lead generation based on these patterns? (yes/no/modify)"""
            
        except Exception as e:
            return f"I encountered an error during pattern discovery: {str(e)}\n\nWould you like to try again?"
    
    def _handle_review_stage(self, user_input: str) -> str:
        """Handle pattern review stage."""
        user_input_lower = user_input.lower().strip()
        
        if user_input_lower in ["modify", "change", "adjust"]:
            self.session.current_stage = "intent"
            return "What would you like to modify? Please provide updated criteria."
        
        if user_input_lower in ["no", "n", "cancel"]:
            return "Understood. Would you like to start over with different criteria?"
        
        if user_input_lower not in ["yes", "y", "proceed", "ok", "continue"]:
            return "Please confirm if you'd like to proceed with lead generation (yes/no/modify):"
        
        # Run lead generation
        try:
            print("\n🚀 Running lead generation workflow...")
            lead_report = lead_generation_workflow(self.session.pattern_report)
            self.session.lead_report = lead_report
            self.session.current_stage = "complete"
            
            # Present report
            high_priority_text = "\n".join([
                f"  - {lead.lead.company.name}: {lead.lead.company.description[:100]}..."
                for lead in lead_report.high_priority_leads[:5]
            ])
            
            return f"""🎉 Lead Generation Complete!

{lead_report.executive_summary}

High Priority Leads ({len(lead_report.high_priority_leads)} total - showing first 5):
{high_priority_text}

Medium Priority Leads: {len(lead_report.medium_priority_leads)}

Recommendations:
{chr(10).join([f"- {rec}" for rec in lead_report.recommendations[:3]])}

💡 Type 'show all' or 'more details' to see the complete list of all {len(lead_report.high_priority_leads)} leads.
   Type 'new' to start a new search."""
            
        except Exception as e:
            return f"I encountered an error during lead generation: {str(e)}\n\nWould you like to try again?"
    
    def _handle_lead_generation_stage(self, user_input: str) -> str:
        """Handle lead generation stage (if needed)."""
        return "Lead generation is in progress..."
    
    def _handle_complete_stage(self, user_input: str) -> str:
        """Handle completion stage."""
        user_input_lower = user_input.lower().strip()
        
        if any(word in user_input_lower for word in ["new", "another", "different", "start"]):
            self.session.current_stage = "intent"
            self.session.intent_data = None
            self.session.pattern_report = None
            self.session.lead_report = None
            return "Great! Let's start a new search. What industry and country are you interested in?"
        
        if "detail" in user_input_lower or "more" in user_input_lower or "all" in user_input_lower or "full" in user_input_lower or "show" in user_input_lower:
            if self.session.lead_report:
                # Show all high priority leads with details
                all_high = "\n\n".join([
                    f"{i+1}. {lead.lead.company.name}\n   Industry: {lead.lead.company.industry}\n   Country: {lead.lead.company.country}\n   Description: {lead.lead.company.description[:150]}...\n   Match Score: {lead.lead.match_score:.2f}\n   Validation Score: {lead.validation.validation_score:.2f}\n   Recommendation Score: {lead.signals.recommendation_score:.2f}\n   Key Signals: {', '.join(lead.signals.detected_signals[:3])}"
                    for i, lead in enumerate(self.session.lead_report.high_priority_leads)
                ])
                
                medium_summary = ""
                if self.session.lead_report.medium_priority_leads:
                    medium_summary = f"\n\nMedium Priority Leads ({len(self.session.lead_report.medium_priority_leads)}):\n" + "\n".join([
                        f"  - {lead.lead.company.name} (Match: {lead.lead.match_score:.2f})"
                        for lead in self.session.lead_report.medium_priority_leads[:10]
                    ])
                
                return f"""📊 Complete Lead Report

HIGH PRIORITY LEADS ({len(self.session.lead_report.high_priority_leads)} total):

{all_high}{medium_summary}

Type 'new' to start a new search, or ask any questions about these leads."""
        
        return "The search is complete. You can ask for more details or start a new search."
