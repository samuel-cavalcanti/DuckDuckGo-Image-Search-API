import requests
import re
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import logging
from tqdm import tqdm


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
    __output_dir: Path
    debug: bool

    def __init__(self, debug=False):
        if debug:
            self.debug = debug
            logging.basicConfig(level=logging.INFO)

    def __get_token(self, keywords: str):

        search_obj = self.__first_search(keywords)

        if not search_obj:
            logging.info("Token Parsing Failed !")
            self.__del__()

        self.__token = search_obj.group(1)

        logging.info("Obtained Token {}".format(self.__token))

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

        logging.info("Hitting DuckDuckGo for Token")

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

        message = "searching images"

        with tqdm(total=max_results) as progress_bar:
            progress_bar.set_description(message)

            while len(images) <= max_results:

                progress_bar.update(len(images))

                data = self.__try_to_request(
                    requests_url, self.__headers, params)

                logging.info("Hitting Url Success : %s", requests_url)
                self.__print_jsons(data["results"])

                images += data["results"]

                if "next" not in data:
                    logging.info("No Next Page - Exiting")
                    break

                requests_url = self.__url + data["next"]

            if len(images) > max_results:
                desired_images = images[:max_results]
            else:
                desired_images = images
            progress_bar.set_description(
                f"total images : {len(desired_images)}")

        return desired_images

    def search_and_download(self, keywords: str, output_dir="downloads", max_results=1, max_workers=1):
        url_and_titles = self.search(keywords, max_results)

        self.__output_dir = Path(output_dir)

        self.__output_dir.mkdir(exist_ok=True)

        self.__download_images(max_workers, url_and_titles)

    def __try_to_request(self, requests_url: str, headers: dict, params: tuple) -> dict:

        number_of_tries = 5
        seconds = 1

        for i in range(number_of_tries):

            res = requests.get(requests_url, headers=headers, params=params)
            try:
                return json.loads(res.text)
            except ValueError:
                logging.error(
                    f"{i}-{number_of_tries} Hitting Url Failure - Sleeping for {seconds} second(s) and Retry: {requests_url}\n")
                time.sleep(1)

        raise DuckDuckGoApiExeception(
            f"Unable to hit: {requests_url}, API is temporary down")

    def __fetch_url(self, json_data: dict):
        url: str = json_data["image"]

        title_without_special_chars = "".join(
            char for char in json_data["title"] if char.isalnum())

        type_image = url.split(".")[-1][:3].lower()  # .png ,.jpg ...

        file_path = Path(f'{title_without_special_chars}.{type_image}')

        output_path = self.__output_dir.joinpath(file_path)

        try:
            result = requests.get(url, stream=True)

            if result.status_code == 200:
                output_path.write_bytes(result.content)

        except:

            print("Request error !\nurl {}".format(url))

    def __download_images(self, workers: int, url_and_titles: list):

        message = 'Downloading images'

        total_downloads = len(url_and_titles)
        with tqdm(total=total_downloads) as progress_bar:
            progress_bar.set_description(message)

            with ThreadPoolExecutor(max_workers=workers) as executor:
                number_of_downloads = 0
                for _ in executor.map(self.__fetch_url, url_and_titles):

                    progress_bar.update(number_of_downloads)

                    number_of_downloads += 1

                progress_bar.update(number_of_downloads)

    @staticmethod
    def print_json(json_object: dict):

        logging.info("__________")
        logging.info("Width {}, Height {}".format(
            json_object["width"], json_object["height"]))
        logging.info("Thumbnail {}".format(json_object["thumbnail"]))
        logging.info("Url {}".format(json_object["url"]))
        logging.info("Title {}".format(json_object["title"].encode('utf-8')))
        logging.info("Image {}".format(json_object["image"]))
        logging.info("__________")

    def __print_jsons(self, jsons: list):
        for json_obj in jsons:
            self.print_json(json_obj)


class DuckDuckGoApiExeception(Exception):
    pass
