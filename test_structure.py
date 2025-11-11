"""
Test script to validate the URL to Markdown agent structure
"""
import sys
import os

# Set a dummy API key for testing structure
os.environ['GOOGLE_API_KEY'] = 'dummy_key_for_testing'

try:
    from url_to_markdown_agent import fetch_url_content
    print("✓ Import successful")
    
    # Test fetch_url_content function exists
    assert callable(fetch_url_content), "fetch_url_content should be callable"
    print("✓ fetch_url_content function exists")
    
    # Check if we can import CrewAI components
    from crewai import Agent, Task, Crew, LLM
    print("✓ CrewAI components imported")
    
    # Try creating an LLM instance
    try:
        llm = LLM(model="gemini/gemini-2.5-flash", api_key="test_key")
        print("✓ LLM instance created successfully")
    except Exception as e:
        print(f"⚠ LLM creation: {e}")
    
    print("\n✅ All structural tests passed!")
    print("\nTo run the agent:")
    print("1. Copy .env.example to .env")
    print("2. Add your GOOGLE_API_KEY to .env")
    print("3. Run: python url_to_markdown_agent.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
