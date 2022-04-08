import requests
import json
from datetime import date

TOKEN = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"


class VKApi:
    url = "https://api.vk.com/method/"

    def __init__(self, user_id=input('Введите id пользователя: ')):
        self.params = {"owner_id": user_id,
                       "album_id": "profile",
                       "extended": "1",
                       "access_token": TOKEN,
                       "v": "5.131"}
        response = requests.get(VKApi.url + "photos.get", params=self.params)
        self.data = response.json()

    def get_name_and_links(self):
        about_file = []
        name_and_link = {}
        for items in self.data['response']['items']:
            number_of_likes = items['likes']['count']
            post_date = date.fromtimestamp(items['date'])
            link_dict = {}
            about_file_dict = {}
            for sizes in items['sizes']:
                link_dict[sizes['height'] * sizes['width']] = sizes['url']
            if number_of_likes not in name_and_link.keys():
                name_and_link[number_of_likes] = link_dict[max(link_dict)]
            else:
                name_and_link[str(post_date)] = link_dict[max(link_dict)]
            about_file.append(about_file_dict)
        return name_and_link

    def get_json(self):
        name_list = []
        size_list = []
        for items in self.data['response']['items']:
            size_dict = {}
            type_size = {}
            for sizes in items['sizes']:
                type_size[sizes['height'] * sizes['width']] = sizes['type']

            size_dict['size'] = type_size[max(type_size)]
            size_list.append(size_dict)
        for name in self.get_name_and_links().keys():
            name_list.append({'file_name': str(name)})
        result = []
        with open('data.json', 'w') as f:
            for name, sizes in zip(name_list, size_list):
                about_file = {}
                about_file.update(name)
                about_file.update(sizes)
                result.append(about_file)
            json.dump(result, f)


