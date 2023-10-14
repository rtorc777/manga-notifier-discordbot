from bs4 import BeautifulSoup
import requests
import json

def scrape_manga(url, user):
    if valid_link(url):
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

        
        save_manga = add_manga(user, manga)

        if save_manga == "Successfully added":
            return manga
        else: 
            return "Already tracking this link"
    else:
        return "Invalid link"
    

def compare_chapter(url, user):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    chapter = soup.find('li', class_ = 'a-h')
    latest_chapter_name = chapter.find('a').text
    latest_chapter_link = chapter.find('a').get('href')

    with open('data.json','r+') as file:    
        file_data = json.load(file)
    
        for i,manga in enumerate(file_data[user]):
            if url in manga:
                index = i
                break

        if latest_chapter_name != file_data[user][index][url]["latest_chapter"]:
            print("new chapter: " + latest_chapter_link)

            file_data[user][index][url]["latest_chapter"] = latest_chapter_name

            with open('data.json', 'w') as file:
                json.dump(file_data, file, indent = 4)
        else:
            print("nothing")


def add_manga(user, data):
     with open('data.json','r+') as file:
        file_data = json.load(file)

        if user not in file_data:
            file_data[user] = []
        
        url = list(data.keys())[0]

        if not any(url in d for d in file_data[user]):
            file_data[user].append(data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
            return "Successfully added"
        else:
            return "Already exists"


def remove_manga(user, id):
     with open('data.json','r+') as file:
        file_data = json.load(file)

        try:
            del file_data[user][id]
            with open('data.json', 'w') as file:
                json.dump(file_data, file, indent = 4)
            return "Successfully removed"
        except IndexError:
            return "Invalid index"


def valid_link(url):
    if 'manganato.com/manga' in url:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        if soup.find('li', class_ = 'a-h'):
            return True
        else:
            return False
    else:
        return False


def get_user_list(user):
    with open('data.json','r+') as file:    
        file_data = json.load(file)
        if user in file_data:
            return file_data[user]
        else:
            return "Use !add (link) to get started"
