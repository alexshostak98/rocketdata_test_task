import requests
import json
import time
from datetime import datetime


class BaseParser:

    def __init__(self, url, save_path, keys, delay=0.2):
        self.url = url
        self.path = save_path
        self.keys = keys
        self.delay = delay
        # self.response = self.get_response()
        self.json_name = self.create_json()

    def get_response(self, url):
        counter = self.delay
        response = requests.get(url)
        while counter:
            if response.status_code == 200:
                return response
            else:
                time.sleep(self.delay)
                counter -= 0.1
        response.raise_for_status()

    def get_data(self):
        pass

    def prepare_to_json(self, data):
        result = []
        for item in data:
            result.append(dict(zip(self.keys, item)))
        return result

    def create_json(self):
        today = datetime.now().strftime('%d_%m_%Y')
        with open(self.path.joinpath(f'{today}_data.json'), 'w') as file:
            return file.name

    def update_json(self, data):
        with open(self.json_name, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=0, ensure_ascii=False)
