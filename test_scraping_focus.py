"""
Test script to validate that the agent focuses on scraping without analysis
"""
import os
import sys

# Set a dummy API key for testing
os.environ['GOOGLE_API_KEY'] = 'dummy_key_for_testing'

try:
    from url_to_markdown_agent import create_url_to_markdown_crew
    print("✓ Import successful")
    
    # Test that the crew is created with correct configuration
    test_url = "https://example.com"
    crew = create_url_to_markdown_crew(test_url)
    
    print("✓ Crew created successfully")
    
    # Verify that we have the correct number of agents
    assert len(crew.agents) == 2, "Should have 2 agents"
    print("✓ Correct number of agents (2)")
    
    # Verify agent roles
    agent_roles = [agent.role for agent in crew.agents]
    assert 'Proposal Details Scraper' in agent_roles, "Should have Proposal Details Scraper agent"
    assert 'Markdown Documentation Specialist' in agent_roles, "Should have Markdown Documentation Specialist agent"
    print("✓ Correct agent roles found")
    
    # Verify agent goals mention scraping without analysis
    scraper_agent = [agent for agent in crew.agents if agent.role == 'Proposal Details Scraper'][0]
    assert 'exact' in scraper_agent.goal.lower(), "Scraper goal should mention 'exact'"
    assert 'without analysis' in scraper_agent.goal.lower(), "Scraper goal should mention 'without analysis'"
    print("✓ Scraper agent goal emphasizes exact details without analysis")
    
    # Verify formatter agent goal mentions no analysis
    formatter_agent = [agent for agent in crew.agents if agent.role == 'Markdown Documentation Specialist'][0]
    assert 'without analysis' in formatter_agent.goal.lower() or 'without' in formatter_agent.goal.lower(), \
        "Formatter goal should mention avoiding analysis"
    print("✓ Formatter agent goal emphasizes no analysis")
    
    # Verify we have the correct number of tasks
    assert len(crew.tasks) == 2, "Should have 2 tasks"
    print("✓ Correct number of tasks (2)")
    
    # Verify task descriptions emphasize exact details
    task_descriptions = [task.description for task in crew.tasks]
    scrape_task_desc = task_descriptions[0]
    
    assert 'exact' in scrape_task_desc.lower(), "First task should mention 'exact'"
    assert 'do not analyze' in scrape_task_desc.lower() or 'without analysis' in scrape_task_desc.lower(), \
        "First task should explicitly say not to analyze"
    print("✓ Scrape task emphasizes exact details without analysis")
    
    markdown_task_desc = task_descriptions[1]
    assert 'preserve' in markdown_task_desc.lower() or 'exact' in markdown_task_desc.lower(), \
        "Markdown task should mention preserving exact details"
    assert 'not add any analysis' in markdown_task_desc.lower() or 'without interpretation' in markdown_task_desc.lower(), \
        "Markdown task should explicitly say not to add analysis"
    print("✓ Markdown task emphasizes preserving exact details without interpretation")
    
    print("\n✅ All scraping-focus tests passed!")
    print("\nThe agent is correctly configured to:")
    print("- Scrape exact proposal details")
    print("- Avoid analysis and interpretation")
    print("- Preserve details exactly as they appear")
    print("- Transform to markdown without adding commentary")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
