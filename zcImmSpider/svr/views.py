from . import main
from flask import request
from ..main import app
import subprocess
import json
import arrow


@main.route('/')
def index():
    return '足彩爬虫服务'


@main.route('/imm')
def immdeiate():
    params = json.loads('{}')
    params['wtype'] = app.config['WT_IMMDEIATE']
    subprocess.call(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={0}'.format(json.dumps(params))])
    return '{"status":0, "msg":"任务已完成"}'


@main.route('/ls')
def liansai():
    params = json.loads('{}')
    params['wtype'] = app.config['WT_LIANSAI']
    subprocess.call(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={0}'.format(json.dumps(params))])
    return '{"status":0, "msg":"任务已完成"}'


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
    params['ou'] = request.args.get('ou', 0, type=int)
    params['ya'] = request.args.get('ya', 0, type=int)
    params['dx'] = request.args.get('dx', 0, type=int)
    params['rq'] = request.args.get('rq', 0, type=int)
    params['bf'] = request.args.get('bf', 0, type=int)
    s1 = 'params={0}'.format(json.dumps(params))
    subprocess.call(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={0}'.format(json.dumps(params))])

    return '{"status":0, "msg":"任务已顺利执行"}'


@main.route('/wc', methods=['GET', 'POST'])
def worldcup():
    params = json.loads('{}')
    params['wtype'] = app.config['WT_WORLDCUP']
    subprocess.call(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={0}'.format(json.dumps(params))])
    return '任务已完成({0})'.format(arrow.utcnow())


@main.route('/og', methods=['GET', 'POST'])
def ouguan():
    params = json.loads('{}')
    params['wtype'] = app.config['WT_OUGUAN']
    lsname = request.args.get('ls', '-1', type=str)
    if lsname == "-1":
        return '缺少参数: ls(联赛名称)'
    params['lsName'] = lsname

    subprocess.call(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={0}'.format(json.dumps(params))])


@main.route('/oc', methods=['GET', 'POST'])
def oucup():
    params = json.loads('{}')
    params['wtype'] = app.config['WT_OUCUP']
    lsname = request.args.get('ls', '-1', type=str)
    if lsname == "-1":
        return '缺少参数: ls(联赛名称)'
    params['lsName'] = lsname
    subprocess.call(['scrapy', 'crawl', 'zcImmSpider', '-a', 'params={0}'.format(json.dumps(params))])
