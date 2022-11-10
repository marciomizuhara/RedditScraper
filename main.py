import praw
import regex as re
import pandas as pd
import errno
import os, os.path
from os.path import exists
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request
import requests
from io import BytesIO
from PIL import Image
import time

# Set up the read-only instance
reddit_read_only = praw.Reddit(client_id='',  # your client id
                               client_secret='',  # your client secret
                               user_agent='')  # your user agent


# Set up the Authorized instance
reddit_authorized = praw.Reddit(client_id="",  # your client id
                                client_secret="",  # your client secret
                                user_agent="",  # your user agent
                                username="",  # your reddit username
                                password="")  # your reddit password

# Query for subreddit_name
subreddit_name = input('Please enter the subrredit name: ')
subreddit = reddit_read_only.subreddit(subreddit_name)


# Query for the download folder
download_folder = input('Please enter the download folder: ')
folder_path = f'{download_folder}' + f'\{subreddit_name}'
folder_path.replace("\\", "/")


# Set up function for folder creation
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# Some helpfull variables to deal with the scraping loop
counter = 0
not_supported = 0


# Main scraping code
try:
    for post in subreddit.new(limit=5):
        # A helper variable to avoid messing up with filenames
        setter = ''

        # Folder creation
        author = str(list(subreddit.new())[counter].__dict__['author'])
        author.replace(' ','')
        mkdir_p(f'{folder_path}')

        # Video scraping section
        try:
            video_url = post.__dict__['media_embed']['content'].split(' ')
            video_url = video_url[1].split('=')
            video_url = video_url[1].replace('"', '')
            my_url = Request(f"{video_url}", headers={'User-Agent': 'Mozilla/5.0'})
            uClient = uReq(my_url)
            time.sleep(0.5)
            page_html = uClient.read()
            time.sleep(0.5)
            uClient.close()
            page_soup = soup(page_html, "html.parser")
            webm = page_soup.findAll(property="og:video")
            webm_data = requests.get(webm[0]['content']).content
            filename = author + '_' + video_url.split('/')[-1]
            if exists(f'{folder_path}/{filename}.webm'):
                break
            else:
                with open(f'{folder_path}/{filename}.webm', 'wb') as handler:
                    handler.write(webm_data)
                print(f'video {filename} downloaded')
                setter = f'{folder_path}/{filename}.webm'
            counter += 1
        except:
            pass

        # Image scraping section
        try:
            img_url = list(subreddit.new())[counter].__dict__['preview']['images'][0]['source']['url']
            img = Image.open(BytesIO(requests.get(img_url).content)).convert('RGB')
            filename = author + '_' + img_url.split('=')[-1]
            if setter:
                pass
            else:
                if exists(f'{folder_path}/{filename}.jpg'):
                    break
                else:
                    img.save(f'{folder_path}/{filename}.jpg', 'jpeg')
                    print(f'image {filename} downloaded')
                counter += 1
        except:
            print('File format not supported.')
            not_supported += 1
            counter += 1
    total = counter - not_supported
    print(f'{total} media downloaded successfully!\n{not_supported} files cannot be downloaded')
except IndexError:
    print(f'{counter} media downloaded successfully!')















# link = list(subreddit.new())[2].__dict__['secure_media_embed']['media_domain_url']
# print(link)
#
#
# video_url = list(subreddit.new())[4].__dict__['preview']['reddit_video_preview']['fallback_url']



# while f'{folder_path}/{author_folder}/file_{number + 1}.jpg':
#     number += 1


# print(list(subreddit.new())[0].__dict__['author'])
# print(type(str(list(subreddit.new())[0].__dict__['author'])))


# non_formatted = thread_title[0].getText()
# folder_thread_title = re.sub('[/|!:,*)@#%(&$_?.^  ]', ' ', non_formatted)[:30]
# webm_link = webm[number].findChild("div",{'class': 'fileText'}).find('a')['href'][2:]
# webm_data = requests.get(f'https://{webm_link}').content
# mkdir_p(f'{folder_path}/{folder_thread_title}')
# with open(f'{folder_path}/{folder_thread_title}/video_{number+1}.webm','wb') as handler:
#     handler.write(webm_data)
# counter = counter + 1
