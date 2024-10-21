import requests
from bs4 import BeautifulSoup
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Function to scrape hyperlinks from any e-commerce website
def scrape_hyperlinks(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the page title
        title = soup.find('title').get_text(strip=True)
        print(f'Page Title: {title}')
        
        # Extract all hyperlinks
        links = []
        link_elements = soup.find_all('a')
        for link in link_elements:
            href = link.get('href')
            text = link.text.strip() or "No Text"
            links.append({'text': text, 'url': href})
        
        if not links:
            return "No hyperlinks found on this page."
        
        return links
    else:
        return f'Failed to retrieve content: {response.status_code}'

# Function to summarize hyperlinks using Google Generative AI with a generalized prompt
def summarize_hyperlinks(links, google_api_key):
    # Prepare hyperlinks information for the prompt
    links_info = "\n".join([f"Text: {link['text']}, URL: {link['url']}" for link in links])

    # Set up the generalized prompt template for a concise summary
    prompt_template = PromptTemplate(
        input_variables=["links"],
        template="""You are an assistant that summarizes product listings found on an e-commerce webpage. Provide a concise summary of the product offerings in paragraph form, without listing all individual products.

Here are the product links scraped from the site:
Links: {links}

Please summarize the products found on this site in a single paragraph, focusing on the product categories, key features, and offerings."""
    )

    # Initialize the language model (Google Generative AI - gemini-1.5-flash)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=google_api_key)

    # Define the LLMChain
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)

    # Run the summarization
    summary = llm_chain.run(links=links_info)
    return summary

# Main function to run the scraping and summarization
def main():
    # Google API key (replace with your actual key)
    google_api_key = "ur api key"  # Replace with your Google API key

    # URL of the homepage to scrape
    url = 'https://Example.in/'  # Replace with the target website URL

    # Scrape the homepage for hyperlinks
    links = scrape_hyperlinks(url)

    # If links were successfully scraped, summarize them
    if isinstance(links, list) and links:
        print("Links scraped successfully. Generating summary...")
        summary = summarize_hyperlinks(links, google_api_key)
        print("\nSummary of product listings:")
        print(summary)
    else:
        print(links)

if __name__ == "__main__":
    main()
