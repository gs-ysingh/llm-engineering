# Problem: Use OLLAMA to summerize a given web page

# Imports
import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display

# Constants
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
}
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

class Website:
    """
    Represents a website and extracts its title and text content using BeautifulSoup.
    """
    def __init__(self, url):
        """
        Initialize a Website object with the given URL.
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        self.title = soup.title.string if soup.title else "No title found"
        
        # Remove irrelevant tags
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        
        # Extract text content
        self.text = soup.body.get_text(separator="\n", strip=True)

def user_prompt_for(website):
    """
    Generate a user-specific prompt based on the website content.
    """
    user_prompt = f"You are looking at a website titled {website.title}\n"
    user_prompt += (
        "The contents of this website is as follows; "
        "please provide a short summary of this website in markdown. "
        "If it includes news or announcements, then summarize these too.\n\n"
    )
    user_prompt += website.text
    return user_prompt

system_prompt = (
    "You are an assistant that analyzes the contents of a website and provides a short summary, "
    "ignoring text that might be navigation related. Respond in markdown."
)

def messages_for(website):
    """
    Create the structured messages required for the API request.
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

def summarize(url):
    """
    Summarize the content of the given URL by interacting with the API.
    """
    website = Website(url)
    payload = {
        "model": MODEL,
        "messages": messages_for(website),
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
    return response.json()['message']['content']

# Display the summarized content
display(Markdown(summarize("https://www.microsoft.com/")))
