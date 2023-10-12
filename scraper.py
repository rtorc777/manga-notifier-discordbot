from bs4 import BeautifulSoup
import requests

def scrape_manga(url):
    if 'manganato.com/manga' in url:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        title = soup.find('h1').text
        image = soup.find('div', class_ = 'story-info-left').find('img').get('src')
        chapter = soup.find('li', class_ = 'a-h')

        chapter_name = chapter.find('a').text
        link = chapter.find('a').get('href')

        # print(title)
        # print(chapter_name)
        # print(image)
        # print(link)
        return chapter_name
    else:
        #print("Invalid link")
        return "Invalid link"

def compare_chapter(url, latest_chapter):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    chapter = soup.find('li', class_ = 'a-h')
    chapter_name = chapter.find('a').text

    if chapter_name != latest_chapter:
        return 1