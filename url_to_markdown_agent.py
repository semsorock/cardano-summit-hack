"""
CrewAI Agent to Transform URL Content to Markdown using Gemini API
"""
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in .env file")


def fetch_url_content(url):
    """
    Fetch and parse content from a URL.
    
    Args:
        url: The URL to fetch content from
        
    Returns:
        str: The cleaned text content from the URL, or an error message
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        return f"Error fetching URL: {str(e)}"


def create_url_to_markdown_crew(url):
    """
    Create a crew to transform URL content to markdown.
    
    Args:
        url: The URL to fetch and transform
        
    Returns:
        Crew: A configured CrewAI crew with agents and tasks
    """
    
    # Initialize Gemini LLM using CrewAI's LLM class
    gemini_llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=GOOGLE_API_KEY
    )
    
    # Fetch content from URL
    url_content = fetch_url_content(url)
    
    # Create Proposal Details Scraper Agent
    content_scraper = Agent(
        role='Proposal Details Scraper',
        goal=f'Extract exact proposal details from the web content at {url} without analysis',
        backstory='You are an expert at scraping web content and extracting exact details '
                  'from proposals, including all titles, descriptions, dates, budgets, and other information '
                  'exactly as they appear on the page.',
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )
    
    # Create Markdown Formatter Agent
    markdown_formatter = Agent(
        role='Markdown Documentation Specialist',
        goal='Transform scraped proposal details into well-structured markdown format without analysis or interpretation',
        backstory='You are a skilled technical writer who excels at creating clean, '
                  'well-organized markdown documentation that preserves exact details from the source '
                  'without adding interpretation or analysis.',
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )
    
    # Task to scrape exact content
    scrape_task = Task(
        description=f"""
        Scrape the following web content from {url} and extract ALL proposal details exactly as they appear:
        
        Content:
        {url_content[:8000]}  
        
        Extract the exact details including:
        - Main title/heading (exact text)
        - Complete proposal description (verbatim)
        - All key details (budget, dates, status, team, etc.) exactly as shown
        - All sections and subsections with their exact content
        - Links and references
        - Any other information present on the page
        
        DO NOT analyze, interpret, or summarize. Provide the exact details as they appear on the page.
        """,
        agent=content_scraper,
        expected_output='A complete extraction of all exact proposal details from the webpage without analysis'
    )
    
    # Task to convert to markdown
    markdown_task = Task(
        description="""
        Take the scraped proposal details and transform them into well-formatted markdown.
        
        The markdown should:
        - Preserve ALL exact details from the scraped content without interpretation
        - Have a clear hierarchical structure with appropriate headers (# ## ###)
        - Use bullet points and lists where appropriate
        - Include all links exactly as they appear
        - Be well-organized and easy to read
        - Use markdown formatting features like bold, italic, code blocks, etc. where appropriate
        - NOT add any analysis, commentary, or interpretation
        
        Create a comprehensive markdown document with the exact proposal details.
        """,
        agent=markdown_formatter,
        expected_output='A well-formatted markdown document containing all exact proposal details from the webpage without analysis'
    )
    
    # Create crew
    crew = Crew(
        agents=[content_scraper, markdown_formatter],
        tasks=[scrape_task, markdown_task],
        verbose=True
    )
    
    return crew


def main():
    """Main function to run the URL to Markdown agent"""
    # Example URL
    url = "https://www.catalystexplorer.com/en/proposals/cardano-india-developers-community-hub-f14/details"
    
    print(f"\n{'='*80}")
    print(f"Converting URL to Markdown: {url}")
    print(f"{'='*80}\n")
    
    # Create and run the crew
    crew = create_url_to_markdown_crew(url)
    result = crew.kickoff()
    
    print(f"\n{'='*80}")
    print("RESULT - Markdown Output:")
    print(f"{'='*80}\n")
    print(result)
    
    # Save to file
    output_file = "output.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(result))
    
    print(f"\n{'='*80}")
    print(f"Markdown saved to: {output_file}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
