from openpyxl import Workbook
from scrapy.http import Request
import csv
import os.path
import scrapy
import glob
from decouple import config

headers = {
    'Cookie': "_ga=GA1.1.1006289195.1734923958; Hm_lvt_1cb9c842508c929123cd97ecd5278a28=1734923958; locale=en; SCRIPT_VERSION=29.31.15; DJSP_UUID=193f186b91a3f501bdc51d78; _ga_TDF3LV246N=GS1.1.1734923958.1.1.1734925316.0.0.0; DJSP_USER=fELYbixIZp8L0ejGnrHKxvuODqS9Lkk6bmSn4ih5NkhAF6aOVf%2FgC79S9oWEP99EXlUmc6qJzAa4MgSNqHG1xFGO3b480cc5I7m912Ud5v9Jf0jzeF2aYZyEAeGEtOAU; cf_clearance=kIjUSGnSlr9ctQqKSFtNQ6eHR9l_HjXBgJrXinaQ_X0-1735055170-1.2.1.1-juc33gsNbPYeAX5goYfI2CDV7Yzykp8vk7Q.x5OonSsdyKyh.NFlH3bIRbZlNHok7T.H8erkKZLLkoGmrELgM48B4JOua2aThteuciH_7VZ80JHVdsPKS1WbM2zTSJ6SjCmM.GRTa6CHGwt4taG67X.KVkusmRaQtBJzkgCANVTkkpkdw1DRhaU0CNnbq.W_ZF26zbdoFiwcg5uNIFZe2pEQjLrrcEIfCXC2Y5fhuSxQpgpUpejFcUG3QKEzbPDj1KrAJEX_V83gRCV7UhqOLasqnkkA2oWAH8xAJav6KJJkI1Hr.CER7NGlT91nC6fm2ZnfaL2SeH4z2Dsu0OV2CNQrShJJmLujXozfdftQCUIvV7iwLvlFHi__4fORwJPZ8JOqHDRuwlWSL0HRCVXY74iI6o3aDCZyjn3pVSEM_oM; JSESSIONID=3E47C5068BF45A8C59DBC0B04D5AD57E",
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
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
        current = pager['current']
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

        with open(csv_file, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                ws.append(row)

        wb.save(csv_file.replace('.csv', '') + '.xlsx')
