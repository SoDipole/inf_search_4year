import re
import requests
from bs4 import BeautifulSoup

def get_links(main_url, page_url):
    links_list = []
    r = requests.get(main_url + page_url)
    if r:
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")
        
        while links:
            links2 = []
            for link in links: 
                page_url = link.get("href")
                
                if (page_url 
                    and page_url.startswith("/wiki/") 
                    and page_url not in links_list
                    and not re.search("\..{2,3}$", page_url)):
                    links_list.append(page_url)
                    print(page_url)
                    
                    r = requests.get(main_url + page_url)
                    if r:
                        html = r.text
                        soup = BeautifulSoup(html, "html.parser")
                        links2 += soup.find_all("a")
            links = links2
    return links_list
                
def main():
    n_articles = 0
    main_url = "https://ro.wikipedia.org"
    page_url = "/wiki/Pagina_principală"
        
    links_list = get_links(main_url, page_url)
    
    print(len(links_list))

if __name__ == "__main__":
    main()