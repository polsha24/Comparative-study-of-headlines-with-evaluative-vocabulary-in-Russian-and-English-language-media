import os
import requests
from bs4 import BeautifulSoup
import csv
import json
import urllib.request

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
}


class Source:
    def __init__(self, folder_name, url):
        self.folder_name = folder_name
        self.url = url

    def _convert_to_csv(self):
        with open(f"{self.folder_name}/articles_info.json", "r", encoding="utf-8") as file:
            data_list = json.load(file)
        with open(f"{self.folder_name}/articles_data.csv", "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data_list)


class Ria(Source):
    def __init__(self, folder_name, url):
        super().__init__(folder_name, url)

    def _get_articles(self):
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

        cnt = 0
        articles_info = [("Заголовок", "Дата публикации", "Источник")]
        add_url = "services/tagsearch/?tags[]=world&date="
        date = '20230101'
        try:
            for i in range(24):
                req = requests.get(self.url + add_url + date, headers)

                soup = BeautifulSoup(req.text, "lxml")
                articles = soup.find_all("div", class_="list-item")
                for article in articles:
                    article_heading = article.find("a", class_="list-item__title color-font-hover-only").text
                    article_date = article.find("div", class_="list-item__date").text
                    articles_info.append([article_heading, article_date, "РИА"])
                print(articles_info)
                date = (int(date) + 1)
                date = str(date + 100 * (date % 2))

                print(f"[+] Processed: {cnt}")
                cnt += 1

            with open(f"{self.folder_name}/articles_info.json", "w", encoding="utf-8") as file:
                json.dump(articles_info, file, indent=4, ensure_ascii=False)

        except Exception as _ex:
            print(_ex)

        return "[INFO] Data collected successfully!"

    def parse_this_source(self):
        self._get_articles()
        self._convert_to_csv()


class Tass(Source):
    def __init__(self, folder_name, url):
        super().__init__(folder_name, url)

    def _get_articles(self):
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

        cnt = 0
        articles_info = [("Заголовок", "Дата публикации", "Источник")]
        add_url = "tbp/api/v1/content?limit=20&lang=ru&rubrics=/mezhdunarodnaya-panorama&last_es_updated_dt="
        changing_month = 1
        changing_day = 5

        try:
            for i in range(24):
                date = f"2023-{changing_month}-{changing_day}T18:50:00"
                with urllib.request.urlopen(self.url + add_url + date) as url_:
                    req = json.load(url_)

                for j in range(20):
                    article_heading = req.get("result")[j].get("title")
                    article_date = req.get("result")[j].get("published_dt")
                    articles_info.append([article_heading, article_date, "ТАСС"])
                changing_day += 1
                changing_month += changing_day % 2

                print(f"[+] Processed: {cnt}")
                cnt += 1

            with open(f"{self.folder_name}/articles_info.json", "w", encoding="utf-8") as file:
                json.dump(articles_info, file, indent=4, ensure_ascii=False)

        except Exception as _ex:
            print(_ex)

        return "[INFO] Data collected successfully!"

    def parse_this_source(self):
        self._get_articles()
        self._convert_to_csv()


class NYTimes(Source):
    def __init__(self, folder_name, url):
        super().__init__(folder_name, url)

    def _get_articles(self):
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

        cnt = 0
        articles_info = [("Заголовок", "Дата публикации", "Источник")]
        add_url = "issue/todayspaper/2023/"
        changing_month = 1
        changing_day = 7
        day_a_month = 0

        try:
            for i in range(84):
                if (changing_day < 10) and (changing_month < 10):
                    date = f"0{changing_month}/0{changing_day}/todays-new-york-times"
                elif changing_day >= 10:
                    date = f"0{changing_month}/{changing_day}/todays-new-york-times"
                elif changing_month >= 10:
                    date = f"{changing_month}/0{changing_day}/todays-new-york-times"
                else:
                    date = f"{changing_month}/{changing_day}/todays-new-york-times"
                req = requests.get(self.url + add_url + date, headers)
                print("got requests")

                soup = BeautifulSoup(req.text, "lxml")
                print("got soup")
                articles = soup.find("ol", class_="css-1ncf02q").find_all("h2", class_="css-ds6ff4 e1b0gigc0")
                for article in articles:
                    article_heading = article.text
                    article_date = f"{changing_day}.{changing_month}.2023"
                    articles_info.append([article_heading, article_date, "New York Times"])
                print(articles_info)
                changing_day += 1
                day_a_month += 1
                if changing_month > 6:
                    break
                if day_a_month > 13:
                    changing_month += 1
                    changing_day = 7
                    day_a_month = 0

                print(f"[+] Processed: {cnt}")
                print(f"[+] Articles now: {len(articles_info)}")
                cnt += 1

            with open(f"{self.folder_name}/articles_info.json", "w", encoding="utf-8") as file:
                json.dump(articles_info, file, indent=4, ensure_ascii=False)

        except Exception as _ex:
            print(_ex)

        return "[INFO] Data collected successfully!"

    def parse_this_source(self):
        self._get_articles()
        self._convert_to_csv()


class WashingtonPost(Source):
    def __init__(self, folder_name, url):
        super().__init__(folder_name, url)

    def _get_articles(self):
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

        cnt = 0
        articles_info = [("Заголовок", "Дата публикации", "Источник")]
        add_url = "sitemap/2023/"
        changing_month = 1
        changing_day = 7
        day_a_month = 0

        try:
            for i in range(24):
                date = f"{changing_month}/{changing_day}"
                req = requests.get(self.url + add_url + date, headers)
                print("got requests")

                soup = BeautifulSoup(req.text, "lxml")
                print("got soup")
                articles = soup.find_all("li", class_="wpds-c-hiKtwk wpds-c-ljEyWA")
                print(articles)
                for article in articles:
                    article_url = article.find("a").get("href")
                    article_theme = article_url.split("/")[3]
                    if article_theme == "world":
                        article_heading = article.find("a", class_="wpds-c-cxwMLl").text
                        article_date = f"{changing_day}.{changing_month}.2023"
                        articles_info.append([article_heading, article_date, "Washington Post"])
                print(articles_info)
                changing_day += 1
                day_a_month += 1
                if day_a_month > 3:
                    changing_month += 1
                    changing_day = 7
                    day_a_month = 0

                print(f"[+] Processed: {cnt}")
                print(f"[+] Articles now: {len(articles_info)}")
                cnt += 1

            with open(f"{self.folder_name}/articles_info.json", "w", encoding="utf-8") as file:
                json.dump(articles_info, file, indent=4, ensure_ascii=False)

        except Exception as _ex:
            print(_ex)

        return "[INFO] Data collected successfully!"

    def parse_this_source(self):
        self._get_articles()
        self._convert_to_csv()


def main():
    ria = Ria("ria", "https://ria.ru/")
    # ria.parse_this_source()
    tass = Tass("tass", "https://tass.ru/")
    # tass.parse_this_source()
    washington = WashingtonPost("washington", "https://www.washingtonpost.com/")
    # washington.parse_this_source()
    nytimes = NYTimes("nytimes", "https://www.nytimes.com/")
    # nytimes.parse_this_source()


if __name__ == "__main__":
    main()
