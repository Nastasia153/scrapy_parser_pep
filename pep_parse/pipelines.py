import csv
import datetime as dt

from pep_parse.settings import BASE_DIR, DATETIME_FORMAT, RESULTS_DIR


class PepParsePipeline:

    def __init__(self):
        self.results_dir = RESULTS_DIR
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def open_spider(self, spider):
        self.statuses = {}
        self.result = [('Статус', 'Количество')]

    def process_item(self, item, spider):
        status = item.get('status', default=None)
        if status:
            self.statuses[status] = self.statuses.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        now = dt.datetime.now()
        now_format = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_format}.csv'
        file_path = BASE_DIR / 'results' / file_name
        for status, qnt in self.statuses.items():
            self.result.append((status, qnt))
        self.result.append(('Total', sum(self.statuses.values())))

        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(self.result)
