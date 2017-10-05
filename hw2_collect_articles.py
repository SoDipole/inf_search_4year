import os
import requests
from bs4 import BeautifulSoup

def write_to_file(n_articles, title, date, url, text):
    if not os.path.exists("acricles"):
        os.makedirs("acricles")
        
    output = "@au Noname\n"+"@ti "+title+"\n@da "+date+"\n@topic\n@url "+url+"\n"+text

    fw = open("acricles/"+str(n_articles)+".txt", "w", encoding = "utf-8")
    fw.write(output)
    fw.close()

def parce_page(html):
    soup = BeautifulSoup(html, "html.parser")
    
    newsdeails = soup.find("ul", attrs={"class":"newsdeails"})
    
    title = newsdeails.find("h1").text
    
    date = newsdeails.find(attrs={"class":"date_start"}).text
    year, month, day = date.split("-")
    date = ".".join([day, month, year])
    
    text = newsdeails.find(attrs={"class":"intro"}).text
    
    return title, date, text

def main():
    n_articles = 0
    main_url = "http://yaskluch.ru/"
    news_url = "?module=news&action=list&id=0&page="
    page = 1
    
    while n_articles < 1000:
        r = requests.get(main_url + news_url + str(page))
        if r:
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            
            newslist = soup.find("ul", attrs={"class":"newslist"})
            
            for link in newslist.find_all("a", attrs={"class":"link_name"}):
                article_url = link.get("href")
                r = requests.get(main_url + article_url)
                if r:
                    n_articles += 1
                    html = r.text
                    
                    title, date, text = parce_page(html)
                    write_to_file(n_articles, title, date, main_url+article_url, text)
                    
                    print(n_articles)
        else:
            break
        page += 1

if __name__ == "__main__":
    main()