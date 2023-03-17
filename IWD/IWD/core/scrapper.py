import requests
from bs4 import BeautifulSoup

def scrapper():
    # Specify the root URL of the website you want to scrape
    root_url = 'https://medium.com/tag/addiction'
    site_url = 'https://medium.com/'

    # Send an HTTP request to the root URL
    response = requests.get(root_url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links to articles on the page using the find_all method
    article_links = soup.find_all('article')

    # Loop through each link and extract the relevant information from each page
    for link in article_links:
        # Construct the URL of the article page by appending the link to the root URL
        article_url = site_url + link.get('href')
        
        # Send an HTTP request to the article URL
        article_response = requests.get(article_url)
        
        # Parse the HTML content of the page using BeautifulSoup
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        
        # Extract the relevant information from the article page using the find method
        article_title = article_soup.find('h1', {'class': 'article-title'}).get_text()
        article_body = article_soup.find('div', {'class': 'article-body'}).get_text()
        
        # Print the result
        return (article_title)