"""
Simple usage example for the URL to Markdown agent
"""
import os
from url_to_markdown_agent import create_url_to_markdown_crew

# Set your API key (or use .env file)
os.environ['GOOGLE_API_KEY'] = 'your-api-key-here'

# Example 1: Process a Catalyst Explorer proposal
url = "https://www.catalystexplorer.com/en/proposals/cardano-india-developers-community-hub-f14/details"
crew = create_url_to_markdown_crew(url)
result = crew.kickoff()
print(result)

# Example 2: Process any other URL
# url = "https://example.com/article"
# crew = create_url_to_markdown_crew(url)
# result = crew.kickoff()
# 
# # Save to custom file
# with open('custom_output.md', 'w') as f:
#     f.write(str(result))
