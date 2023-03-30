import requests
import csv
import time
import config
from querying_groups import query_groups
from upload_comments import save_comments
from model import app


def take_posts():
    count = '100'
    all_posts = []

    for group in query_groups():
        owner_id = f'-{group}'
        offset = 0
        request_wall_get(config.VK_TOKEN, config.VK_API_VERSION, owner_id, offset, count, all_posts)
    return all_posts


def request_wall_get(token, version, owner_id, offset, count, all_posts):
    while offset < 1000:
        response = requests.get('https://api.vk.com/method/wall.get', 
                                params={
                                    'access_token':token,
                                    'v':version,
                                    'owner_id':owner_id,
                                    'offset':offset,
                                    'count':count
                                })

        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)


def request_wall_get_comments(token, version, owner_id, post_id, offset, count, all_comments, data):
    while 'error' in data:
        response = requests.get('https://api.vk.com/method/wall.getComments', 
                                    params={
                                        'access_token':token,
                                        'v':version,
                                        'owner_id':owner_id,
                                        'post_id':post_id,
                                        'offset':offset,
                                        'count':count
                                    })
        data = response.json() 

    data = response.json()['response']['items']
    for com in data:
        comment = {'id_post':post_id, 
                   'text':com['text'], 
                   'id_group_from':abs(owner_id)
                   }
        all_comments.append(comment)
    return data, all_comments


def request_get_comments(posts):
    all_comments = []
    count = 100
    data = []

    for post in posts:
        post_id = post['id']
        owner_id = post['owner_id']
        data = ['error']
        offset = 0
        request_wall_get_comments(config.VK_TOKEN, config.VK_API_VERSION, owner_id, post_id, offset, count, all_comments, data)

        while len(data) == 100:
            data = ['error']
            offset += 100
            request_wall_get_comments(config.VK_TOKEN, config.VK_API_VERSION, owner_id, post_id, offset, count, all_comments, data)

    return all_comments


if __name__ == "__main__":
    with app.app_context():
        posts = take_posts()
        comments = request_get_comments(posts)
        save_comments(comments)
        