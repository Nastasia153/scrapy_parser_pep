import csv
import datetime as dt
from collections import Counter

from pep_parse.settings import BASE_DIR, DATETIME_FORMAT


class PepParsePipeline:

    def __init__(self):
        self.results_dir = BASE_DIR / 'results'
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def open_spider(self, spider):
        self.statuses = []
        self.result = [('Статус', 'Количество')]

    def process_item(self, item, spider):
        status = item['status']
        self.statuses.append(status)
        return item

    def close_spider(self, spider):
        cnt = Counter(self.statuses)

        for status, qnt in cnt.items():
            self.result.append((status, qnt))
        self.result.append(('Total:', sum(cnt.values())))
        now = dt.datetime.now()
        now_format = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_format}.csv'
        file_path = BASE_DIR / 'results' / file_name

        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(self.result)
