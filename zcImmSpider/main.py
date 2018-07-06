from scrapy.cmdline import execute
from zcImmSpider import create_app

app = create_app('default')

if __name__ == '__main__':
     app.run(port=8080, debug=True)

# execute(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={"wtype": 3, "startDate": "2018-06-01", "endDate": "2018-06-03"}'])
execute(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={"wtype": 3, "lsName": "欧洲杯"}'])
