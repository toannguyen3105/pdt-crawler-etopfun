from openpyxl import Workbook
from scrapy.http import Request
import csv
import os.path
import scrapy
import glob
from decouple import config

headers = {
    'Cookie': config('COOKIE')
}


class StoreitemsSpider(scrapy.Spider):
    name = 'storeItems'
    allowed_domains = ['etopfun.com']

    def start_requests(self):
        yield Request(
            url='https://www.etopfun.com/api/ingotitems/realitemback/list.do?appid=730',
            headers=headers
        )

    def parse(self, response):
        items = response.json()['datas']['list']
        for item in items:
            name = item['pop']['topName']['tag']
            value = item['value']

            yield {
                'name': name,
                'value': value
            }

        pager = response.json()['datas']['pager']
        print(response.json()['datas']['pager'])
        current = pager['current']
        print(current)
        pages = pager['pages']
        if current < pages:
            yield Request(
                response.urljoin('list.do?appid=730&page={}'.format(current + 1)),
                headers=headers,
                callback=self.parse,
            )

    def close(self, reason):
        csv_file = max(glob.iglob('*csv'), key=os.path.getctime)

        wb = Workbook()
        ws = wb.active

        with open(csv_file, 'r') as f:
            for row in csv.reader(f):
                ws.append(row)

        wb.save(csv_file.replace('.csv', '') + '.xlsx')
