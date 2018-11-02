from scrapy.cmdline import execute
from zcImmSpider import create_app

#app = create_app('default')

#if __name__ == '__main__':
#    app.run(port=8080, debug=True)

# execute(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={"wtype": 3, "startDate": "2018-08-01", "endDate": "2018-08-03"}'])
execute(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={"wtype": 2, "startDate": "2018-09-09", "endDate": "2018-09-10", "ou": 1, "ya": 0, "dx": 0, "rq": 0, "bf": 0}'])
