from django.utils.html import strip_tags
import requests
import sys
import os
from pathlib import Path
import logging
import django
import random

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_devops_lab.settings')
django.setup()

from post.models import Post


class ScrapNewsLimonKG:

    def __init__(self):
        self.cookies = {
            'ao_li': 'c8d2c6be9e2a7e2abc6d64bd5c11340e',
            '_ym_uid': '173858201020593858',
            '_ym_d': '1738582010',
            '_ga': 'GA1.1.1808369441.1738582010',
            'AO_TOKEN': 'eb863188569dd7ce5e5f9a91b7ed4e6c',
            '_ym_isad': '1',
            '_ga_0TYHXB6H2L': 'GS1.1.1739985198.2.1.1739985516.0.0.0',
        }

        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cy;q=0.6',
            'dnt': '1',
            'priority': 'u=1, i',
            'referer': 'https://limon.kg/ru/catalog/?cat=84',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }


    def scrap_catalog(self):
        params = {
            'sort': '1',
            'lang': 'ru',
        }

        try:
            response = requests.get('https://limon.kg/api.php/catalog', params=params, cookies=self.cookies, headers=self.headers)
            data = response.json()['data']['catalog']['news']
            result = [id['id'] for id in data]
        except Exception as e:
            logging.error(e)

        return result


    def scrap_detail_news(self, news_ids):
        result = []
        count = 0
        len_news = len(news_ids)

        for id in news_ids:

            params = {
                'page': '0',
                'lang': 'ru',
                'id': f'{id}',
                'visitor': '038d4541a18a6bbd3ed189b6d085d734',
            }

            try:
                response = requests.get('https://limon.kg/api.php/news', params=params, cookies=self.cookies, headers=self.headers)
                data = response.json()['data']['news'][0]

                text = data['text']
                title = data['title']
                clean_text = strip_tags(text)

                news = {
                    'text':clean_text,
                    'title':title
                }
                
                result.append(news)
                logging.info(f'#{count}|{len_news}, scraped - {len(result)}')
                count+=1
            except Exception as e:
                logging.error(e)

        return result
    

    def save_to_database(self, data):

        count = 0
        len_data = len(data)
        for item in data:
            words = ["positive", "negative"]
            sentiment = random.choice(words)
            post = Post.objects.create(title = item['title'], post = item['text'], sentiment = sentiment)

            if post:
                logging.info(f'Created - #{count}|{len_data}')
                count += 1
            

    def start(self):
        logging.info('Start scrap catalog')
        data_catalog = self.scrap_catalog()
        
        logging.info(f'Total news - {len(data_catalog)}')

        logging.info('Start scrap news')
        news_data = self.scrap_detail_news(data_catalog)

        logging.info(f'Load news to database, news - {len(news_data)}')
        self. save_to_database(news_data)

        return
    

if __name__ == '__main__':
    start = ScrapNewsLimonKG().start()
    logging.info(f'Scrap is succesfuly')
    