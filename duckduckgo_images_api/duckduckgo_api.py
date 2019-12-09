import requests
import re
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor


class DuckDuckGoApi:
    __url = "https://duckduckgo.com/"
    __headers = {
        'dnt': '1',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'x-requested-with': 'XMLHttpRequest',
        'accept-language': 'en-GB,en-US q=0.8,en q=0.6,ms q=0.4',
        'user-agent': 'Mozilla/5.0 (X11  Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'accept': 'application/json, text/javascript, */*  q=0.01',
        'referer': 'https://duckduckgo.com/',
        'authority': 'duckduckgo.com',
    }
    __output_dir = "downloads"

    def __init__(self, debug=False):
        self.__debug = debug

    def __get_token(self, keywords: str):

        search_obj = self.__first_search(keywords)

        if not search_obj:
            print("Token Parsing Failed !")
            self.__del__()

        self.__token = search_obj.group(1)

        if self.__debug:
            print("Obtained Token {}".format(self.__token))

    def __del__(self):
        pass

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    def __first_search(self, keywords: str) -> re.Match:
        params = {
            'q': keywords
        }

        res = requests.post(self.__url, data=params)

        return re.search(r'vqd=([\d-]+)&', res.text, re.M | re.I)

    def search(self, keywords: str, max_results=1) -> list:

        self.__get_token(keywords)

        if self.__debug:
            print("Hitting DuckDuckGo for Token")

        params = (
            ('l', 'wt-wt'),
            ('o', 'json'),
            ('q', keywords),
            ('vqd', self.__token),
            ('f', ',,,'),
            ('p', '2')
        )

        requests_url = self.__url + "i.js"

        images = list()

        print("searching images")

        while len(images) <= max_results:

            print("searching {} %".format(round(len(images) / max_results * 100, 3)))

            data = self.__try_to_request(requests_url, self.__headers, params)

            if self.__debug:
                print("Hitting Url Success : %s", requests_url)
                self.__print_jsons(data["results"])

            images += data["results"]

            if "next" not in data:
                if self.__debug:
                    print("No Next Page - Exiting")

                print("total images : {}".format(len(images)))

                break

            requests_url = self.__url + data["next"]

        return images[:max_results]

    def search_and_download(self, keywords: str, output_dir="downloads", max_results=1, max_workers=1):
        url_and_titles = self.search(keywords, max_results)

        self.__output_dir = output_dir

        self.__make_output_dir()

        print("Downloading images")

        self.__download_images(max_workers, url_and_titles)

    def __try_to_request(self, requests_url: str, headers: dict, params: tuple):
        while True:
            try:
                res = requests.get(requests_url, headers=headers, params=params)

                return json.loads(res.text)
            except ValueError as e:
                if self.__debug:
                    print("Hitting Url Failure - Sleep and Retry: %s", requests_url)
                time.sleep(5)
                continue

    def __fetch_url(self, json_data: dict):
        url: str = json_data["image"]

        title_without_special_chars = "".join(char for char in json_data["title"] if char.isalnum())

        type_image = url.split(".")[-1].lower()  # .png ,.jpg ...

        file_path = os.path.join(self.__output_dir, "{}.{}".format(title_without_special_chars, type_image))

        try:
            result = requests.get(url, stream=True)

            if result.status_code == 200:
                open(file_path, "wb").write(result.content)
        except:

            print("Request error !\nurl {}".format(url))

    def __download_images(self, workers: int, url_and_titles: list):

        with ThreadPoolExecutor(max_workers=workers) as executor:
            fetchs = 0

            for _ in executor.map(self.__fetch_url, url_and_titles):
                print("downloading {}%".format(round(fetchs / len(url_and_titles) * 100, 3)))
                fetchs += 1

            print("downloading {}%".format(round(fetchs / len(url_and_titles) * 100, 3)))

    def __make_output_dir(self):
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)

    @staticmethod
    def print_json(json_object: dict):

        print("__________")
        print("Width {}, Height {}".format(json_object["width"], json_object["height"]))
        print("Thumbnail {}".format(json_object["thumbnail"]))
        print("Url {}".format(json_object["url"]))
        print("Title {}".format(json_object["title"].encode('utf-8')))
        print("Image {}".format(json_object["image"]))
        print("__________")

    def __print_jsons(self, jsons: list):
        for json_obj in jsons:
            self.print_json(json_obj)
