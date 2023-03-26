import praw
import random
import requests
import ctypes
from pathlib import Path


def get_creds():
    cred_file_path = Path('cred.txt')

    if cred_file_path.is_file() is False:
        file = open('cred.txt', 'w')
        client_id = input("Enter Reddit API Client ID: ")
        client_secret = input("Enter Reddit API Client Secret: ")
        user_agent = input("Enter app name: ")
        file.writelines([client_id + " ", client_secret + " ", user_agent])
        file.close()

    file = open('cred.txt', 'r')
    creds = file.readline().split()

    client_id = creds[0]
    client_secret = creds[1]
    user_agent = creds[2]

    file.close()

    return client_id, client_secret, user_agent,


def fetch_img(subreddit):
    posts = [post for post in subreddit.top(limit=25, time_filter='day')]

    img_location = str(Path.cwd()) + '\\images\\'
    if Path(img_location).is_dir() is False:
        loc = Path(img_location)
        loc.mkdir()

    while True:
        try:
            random_idx = random.randint(0, len(posts))
            post_obj = posts[random_idx]
            if post_obj.url.endswith(('.jpg', '.png', '.jpeg')):
                extension = '.jpg'
                if '.png' in post_obj.url:
                    extension = '.png'
                print("Post title: " + post_obj.title)

                post_title = "".join(ch for ch in post_obj.title if ch.isalnum())
                img_name = post_title + extension
                directory = img_location + img_name

                if Path(directory).is_file() is False:
                    response = requests.get(post_obj.url)
                    if response.status_code == 200:
                        with open(directory, 'wb') as img:
                            img.write(response.content)
                        print("Image downloaded at: " + directory)
                        ctypes.windll.user32.SystemParametersInfoW(20, 0, directory, 3)
                        print("Wallpaper: " + post_obj.title + " applied")
                    else:
                        print("Wallpaper couldn't be retrieved")
                else:
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, directory, 3)
                    print("Wallpaper: " + post_obj.title + " applied")
                break
        except Exception:
            print("Error occurred")


client_id, client_secret, user_agent = get_creds()
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
subreddit = reddit.subreddit("wallpaper")
fetch_img(subreddit)
