# from scrapy.cmdline import execute
from zcImmSpider import create_app

app = create_app()

if __name__ == '__main__':
     app.run(port=8080, debug=True)

# execute(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={"wtype":0}'])
