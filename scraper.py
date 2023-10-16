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
        latest_chapter_link = chapter.find('a').get('href')

        manga = {url: 
                    {
                        "title": title,
                        "latest_chapter": latest_chapter_name,
                        "latest_chapter_link": latest_chapter_link,
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
    

def check_chapters(user):
    updated_mangas = []

    with open('data.json','r+') as file:    
        file_data = json.load(file)
    
        for index, manga in enumerate(file_data[user]):
            url = next(iter(manga)) 
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'lxml')

            chapter = soup.find('li', class_ = 'a-h')
            latest_chapter_name = chapter.find('a').text
            latest_chapter_link = chapter.find('a').get('href')

            if latest_chapter_name != file_data[user][index][url]["latest_chapter"]:
                file_data[user][index][url]["latest_chapter"] = latest_chapter_name
                file_data[user][index][url]["latest_chapter_link"] = latest_chapter_link

                with open('data.json', 'w') as file:
                    json.dump(file_data, file, indent = 4)
                
                updated_mangas.append(file_data[user][index])

    return updated_mangas 


def check_all_users():
    updated_mangas = {}

    with open('data.json','r+') as file:    
        file_data = json.load(file)

        for user in file_data:
            updates = check_chapters(user)
            if updates:
                updated_mangas[user] = updates
    
    return updated_mangas


def add_manga(user, manga):
    with open('data.json','r+') as file:
        file_data = json.load(file)

        if user not in file_data:
            file_data[user] = []
        
        url = next(iter(manga))

        if not any(url in d for d in file_data[user]):
            file_data[user].append(manga)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
            return "Successfully added"
        else:
            return "Already exists"


def remove_manga(user, id):
    if id < 0:
         return "Enter positive number"
     
    with open('data.json','r+') as file:
        file_data = json.load(file)

        if user not in file_data:
            file_data[user] = []

        try:
            manga = file_data[user][id]
            del file_data[user][id]
            with open('data.json', 'w') as file:
                json.dump(file_data, file, indent = 4)
            return manga
        except IndexError:
            return "Invalid index"


def remove_all_manga(user):
    with open('data.json','r+') as file:
        file_data = json.load(file)
        file_data[user] = []

        with open('data.json', 'w') as file:
            json.dump(file_data, file, indent = 4)
            
        return "Removed all manga from list"


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

        if user not in file_data:
            file_data[user] = []

        return file_data[user]
