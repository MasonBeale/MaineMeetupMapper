import requests
from bs4 import BeautifulSoup
class meetup_scraper:

    def scrape_events(locations=None, categories=None, max_events=50):
        # connnect to website, go to local events
        url = "https://www.meetup.com/find/?source=EVENTS&sortField=DATETIME&location=us--me--Portland"
        print("Scraping URL:", url)
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(response.content, 'html.parser')

        # gather data event by event
        # Find the first <h1> tag
        first_heading = soup.find("h1")
        print(first_heading.text)

        
        # store in some kind of list/dict
    scrape_events()