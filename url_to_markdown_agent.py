"""
CrewAI Agent to Transform URL Content to Markdown using Gemini API
"""
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in .env file")

genai.configure(api_key=GOOGLE_API_KEY)


class GeminiLLM:
    """Custom LLM wrapper for Gemini API"""
    
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model = genai.GenerativeModel(model_name)
    
    def __call__(self, prompt):
        """Call the Gemini model with a prompt"""
        response = self.model.generate_content(prompt)
        return response.text


def fetch_url_content(url):
    """Fetch and parse content from a URL"""
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
    """Create a crew to transform URL content to markdown"""
    
    # Initialize Gemini LLM
    gemini_llm = GeminiLLM("gemini-2.5-flash")
    
    # Fetch content from URL
    url_content = fetch_url_content(url)
    
    # Create Web Content Analyzer Agent
    content_analyzer = Agent(
        role='Web Content Analyzer',
        goal=f'Extract and analyze key information from the web content at {url}',
        backstory='You are an expert at analyzing web content and identifying important information, '
                  'including titles, descriptions, dates, budgets, and other relevant details.',
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )
    
    # Create Markdown Formatter Agent
    markdown_formatter = Agent(
        role='Markdown Documentation Specialist',
        goal='Transform extracted information into well-structured markdown format',
        backstory='You are a skilled technical writer who excels at creating clean, '
                  'well-organized markdown documentation that is easy to read and understand.',
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )
    
    # Task to analyze content
    analyze_task = Task(
        description=f"""
        Analyze the following web content from {url} and extract all relevant information:
        
        Content:
        {url_content[:4000]}  
        
        Identify and extract:
        - Main title/heading
        - Project/proposal description
        - Key details (budget, dates, status, etc.)
        - Any important sections or subsections
        - Links and references
        - Any other relevant information
        
        Provide a structured summary of all important information.
        """,
        agent=content_analyzer,
        expected_output='A structured summary of all key information from the webpage'
    )
    
    # Task to convert to markdown
    markdown_task = Task(
        description="""
        Take the analyzed content and transform it into well-formatted markdown.
        
        The markdown should:
        - Have a clear hierarchical structure with appropriate headers (# ## ###)
        - Use bullet points and lists where appropriate
        - Include any important links
        - Be well-organized and easy to read
        - Preserve all important information
        - Use markdown formatting features like bold, italic, code blocks, etc. where appropriate
        
        Create a comprehensive markdown document.
        """,
        agent=markdown_formatter,
        expected_output='A well-formatted markdown document containing all the information from the webpage'
    )
    
    # Create crew
    crew = Crew(
        agents=[content_analyzer, markdown_formatter],
        tasks=[analyze_task, markdown_task],
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
