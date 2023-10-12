from bs4 import BeautifulSoup
import requests
import json

def scrape_manga(url):
    if 'manganato.com/manga' in url:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        title = soup.find('h1').text
        image = soup.find('div', class_ = 'story-info-left').find('img').get('src')

        chapter = soup.find('li', class_ = 'a-h')
        latest_chapter_name = chapter.find('a').text

        manga = {url: 
                    {
                        "title": title,
                        "latest_chapter": latest_chapter_name,
                        "image": image
                    }
                 }

        
        write_json("test", manga)

        return "Successfully added"
    else:
        return "Invalid link"
    

def compare_chapter(username, url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    chapter = soup.find('li', class_ = 'a-h')
    latest_chapter_name = chapter.find('a').text
    latest_chapter_link = chapter.find('a').get('href')

    with open('data.json','r+') as file:    
        file_data = json.load(file)
    
        for i,manga in enumerate(file_data[username]):
            if url in manga:
                index = i
                break

        if latest_chapter_name != file_data[username][index][url]["latest_chapter"]:
            print("new chapter")

            file_data[username][index][url]["latest_chapter"] = latest_chapter_name

            with open('data.json', 'w') as file:
                json.dump(file_data, file, indent = 4)
        else:
            print("nothing")


def write_json(username, data):
     with open('data.json','r+') as file:
        file_data = json.load(file)

        if username not in file_data:
            file_data[username] = []
        
        url = list(data.keys())[0]

        if not any(url in d for d in file_data[username]):
            file_data[username].append(data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
            print("Successfully added")
        else:
            print("Already exists")
            
    
#scrape_manga("https://chapmanganato.com/manga-lg988863")
#scrape_manga("https://chapmanganato.com/manga-iw985379")
compare_chapter("jjwaterz","https://chapmanganato.com/manga-iw985379")