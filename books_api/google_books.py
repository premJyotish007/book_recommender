import json
import requests as req
import pandas as pd
import time

class BookScraper:
    def __init__(self) -> None:
        self.base_url = "https://www.googleapis.com/books/v1/volumes?q="
        self.headers_file = "C:/Users/harsh/Desktop/spotify api/book_recommender/books_api/books_headers.txt"
        self.headers = []
        with open(self.headers_file, "r", encoding="UTF-8") as header_file:
            self.headers = [line.strip() for line in header_file.readlines()]
    
    def get_books_by_author(self, author):
        index = 0
        size = 0
        set_titles = set()
        list_titles = []
        names = author.split(" ")
        while (True):
            try:
                url = self.base_url + "+inauthor:" + author + "&maxResults=40&startIndex=" + str(index)
                response = req.get(url)
                print(url)
                json_format = json.loads(response.text)
                try:
                    for item in json_format["items"]:
                        if "title" in item["volumeInfo"]:
                            volumeInfo = item["volumeInfo"]
                            current_title = volumeInfo["title"]
                            for name in names:
                                if name in current_title.lower():
                                    continue
                            if (';' not in current_title):
                                set_titles.add(current_title)
                                if (len(set_titles) > size):
                                    valid = True
                                    for char in current_title:
                                        val = ord(char)
                                        if val >= 128:
                                            valid = False
                                            break
                                    if (valid):
                                        info = self.get_book_info(volumeInfo)
                                        if info["language"] == "en":
                                            list_titles.append(info)
                                        size += 1
                except:
                    break
                index += 40
            except:
                time.sleep(1)
        return list_titles

    def get_book_info(self, book, author):
        url = self.base_url + book + "inauthor:" + author
        return url

    def append_data(self, dicts, file) -> None:
        df = pd.DataFrame()
        try:
            df = pd.read_csv(file, usecols=self.headers)
        except:
            print("filling an empty file")
            df = pd.DataFrame()
        df = df.append(dicts, ignore_index=True)
        df.to_csv(file, index = False)

    def get_book_info(self, volumeInfo: dict = "", book = "", author = ""):
        to_return = {}
        if (len(volumeInfo) == 0):
            url = self.base_url + "+intitle:" + book + "&inauthor:" + author
            volumeInfo = json.loads(req.get(url).text)["items"][0]["volumeInfo"]
        for point in self.headers:
            try:
                to_return[point] = volumeInfo[point]
            except:
                to_return[point] = ""
        return to_return

    def append_books(self, file, output_file) -> None:
        with open(file, "r", encoding="UTF-8") as input_file:
            for line in input_file.readlines():
                line = line.strip()
                dicts = self.get_books_by_author(line)
                self.append_data(dicts, output_file)