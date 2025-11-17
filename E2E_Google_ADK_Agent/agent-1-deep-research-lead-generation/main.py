#!/usr/bin/env python3
"""
Deep Research Lead Generation Agent
Main entry point for the interactive lead generation system.
"""

import sys
import os
from pathlib import Path

# Ensure we're using the local modules
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("🎯 Deep Research Lead Generation Agent")
print("=" * 70)
print()

# Import and run
try:
    from agent import InteractiveLeadGenerator
    
    print("✅ Modules loaded successfully")
    print()
    print("Initializing agent...")
    
    agent = InteractiveLeadGenerator()
    
    print(f"✅ Agent ready!")
    print(f"📝 Session: {agent.session.session_id}")
    print()
    print("-" * 70)
    print("Instructions:")
    print("  - Describe what leads you're looking for")
    print("  - Type 'yes' to confirm and proceed")
    print("  - Type 'quit' to exit")
    print("-" * 70)
    print()
    print("Example: 'Find SaaS companies in California'")
    print()
    
    # Main loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("\n👋 Thank you! Goodbye!")
                break
            
            # Process
            print()
            response = agent.run(user_input)
            
            # Clean output
            print("─" * 70)
            print(f"Agent: {response}")
            print("─" * 70)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Session ended. Goodbye!")
            break
        except Exception as e:
            print(f"\n⚠️  Error: {str(e)}")
            print("Please try again or type 'quit' to exit.\n")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nPlease ensure dependencies are installed:")
    print("  python -m pip install google-genai python-dotenv pydantic")
    sys.exit(1)
except Exception as e:
    print(f"❌ Initialization error: {e}")
    print("\nPlease check:")
    print("  1. .env file exists with GOOGLE_API_KEY")
    print("  2. API key is valid")
    sys.exit(1)
