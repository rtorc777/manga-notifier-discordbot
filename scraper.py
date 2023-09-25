from bs4 import BeautifulSoup
import requests

def scrape_manga(manga):
    if 'manganato.com/manga' in manga:
        html_text = requests.get(manga).text
        soup = BeautifulSoup(html_text, 'lxml')

        title = soup.find('h1').text
        image = soup.find('div', class_ = 'story-info-left')
        image = image.find('img').get('src')

        chapter = soup.find('li', class_ = 'a-h')
        chapter_name = chapter.find('a').text
        link = chapter.find('a').get('href')

        print(title)
        print(chapter_name)
        print(image)
        print(link)
        return True
    else:
        print("Invalid link")
        return False


scrape_manga('https://chapmanganato.com/manga-lg988863')