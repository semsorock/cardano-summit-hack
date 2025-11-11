# Example Output

This is an example of what the agent produces when processing a URL.

## How It Works

1. **Fetches Content**: The agent fetches the HTML content from the provided URL
2. **Cleans Data**: Removes scripts, styles, and unnecessary whitespace
3. **Scrapes Details**: The Proposal Details Scraper agent extracts exact information like:
   - Titles and headings (exact text)
   - Complete descriptions (verbatim)
   - Dates and budgets (as shown)
   - Important sections (exact content)
   - Links and references

4. **Formats to Markdown**: The Markdown Formatter agent transforms the scraped content into:
   - Well-structured headers (# ## ###)
   - Bullet points and lists
   - Properly formatted text with **bold**, *italic*, etc.
   - Clean, readable markdown
   - Preserves exact details without analysis or interpretation

## Sample Input

URL: `https://www.catalystexplorer.com/en/proposals/cardano-india-developers-community-hub-f14/details`

## Sample Output Structure

The output would be a markdown file containing:
- Project title as main header
- Project summary and description
- Budget information
- Timeline and dates
- Team information
- Links to related resources
- All other relevant details from the page

The actual output will vary based on the content of the URL being processed.
