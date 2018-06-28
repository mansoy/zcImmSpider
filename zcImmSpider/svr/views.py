from . import main
from flask import request
from ..main import app
import subprocess
import json


@main.route('/')
def index():
    return '足彩爬虫服务'


@main.route('/history', methods=['GET', 'POST'])
def history():
    begindate = request.args.get('startdate', '-1', type=str)
    enddate = request.args.get('enddate', '-1', type=str)
    if begindate == '-1':
        return '缺少参数: startdate'
    if enddate == '-1':
        return '缺少参数: enddate'

    params = json.loads('{}')
    params['wtype'] = app.config['WT_HISTORY']
    params['startDate'] = begindate
    params['endDate'] = enddate
    subprocess.call(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={0}'.format(json.dumps(params))])


@main.route('/wc', methods=['GET', 'POST'])
def worldcup():
    params = json.loads('{}')
    params['wtype'] = app.config['WT_WORLDCUP']
    subprocess.call(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={0}'.format(json.dumps(params))])
    return 'OK'
