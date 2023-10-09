# -*- coding:utf-8 -*-
import re, os, requests
# from traceback import format_exc

# 功能：请求各大jav网站和arzon的网页
# 参数：网址url，请求头部header/cookies，代理proxy
# 返回：网页html，请求头部


# 搜索javbus，或请求javbus上jav所在网页，返回html
def get_bus_html(url, proxy):
    cookies = {
        'existmag': 'all',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36',
    }
    for retry in range(10):
        try:
            if proxy:       # existmag=all为了 获得所有影片，而不是默认的有磁力的链接
                rqs = requests.get(url, proxies=proxy, timeout=(6, 7), cookies=cookies, headers=headers)
            else:
                # print('request1')
                rqs = requests.get(url, timeout=(6, 7), cookies=cookies, headers=headers)
                # rqs = requests.get('https://www.buscdn.cfd/search/waaa-201&type=&parent=ce', cookies=cookies,
                #                         headers=headers)
                # conn = http.client.HTTPSConnection("www.buscdn.cfd")

                # headers = {'cookie': "existmag=mag"}

                # conn.request("GET", "/search/waaa-201&type=&parent=ce", headers=headers)

                # res = conn.getresponse()
                # data = res.read()
        except requests.exceptions.ProxyError:
            # print(format_exc())
            print('    >通过局部代理失败，重新尝试...')
            continue
        except:
            # print(format_exc())
            print('    >打开网页失败，重新尝试...')
            continue
        rqs.encoding = 'utf-8'
        rqs_content = rqs.text
        # rqs_content = data.decode("utf-8")
        if re.search(r'JavBus', rqs_content):
            return rqs_content
        else:
            print('    >打开网页失败，空返回...重新尝试...')
            continue
    print('>>请检查你的网络环境是否可以打开：', url)
    os.system('pause')


# 去javbus搜寻系列、在javbus的封面链接
# 返回：系列名称，图片链接，状态码
def find_series_cover_bus(car, url_bus, proxy):
    # 需要这两个东西
    series = url_cover_bus = ''
    # 状态码，标记是否在javbus上搜索到多个结果（如果有多个结果，javlibrary整理时还是从javlibrary上下载封面）
    status = 0    # 0表示javbus是唯一的搜索结果
    # jav在javbus上的url，一般就是javbus网址+车牌
    url_on_bus = url_bus + car
    print('    >获取系列：', url_on_bus)
    # 获得影片在javbus上的网页
    html_bus = get_bus_html(url_on_bus, proxy)
    if not re.search(r'404 Page', html_bus):
        # DVD封面cover
        coverg = re.search(r'bigImage" href="(.+?)">', html_bus)
        if str(coverg) != 'None':
            url_cover_bus = coverg.group(1)
        # 系列:</span> <a href="https://www.cdnbus.work/series/kpl">悪質シロウトナンパ</a>
        seriesg = re.search(r'系列:</span> <a href=".+?">(.+?)</a>', html_bus)
        if str(seriesg) != 'None':
            series = seriesg.group(1)
    # 这部jav在javbus的网址不简单
    else:
        # 还是老老实实去搜索
        url_search_bus = url_bus + 'search/' + car.replace('-', '') + '&type=1&parent=ce'
        print('    >搜索javbus：', url_search_bus)
        html_bus = get_bus_html(url_search_bus, proxy)
        # 搜索结果的网页，大部分情况一个结果，也有可能是多个结果的网页
        # 尝试找movie-box
        list_search_results = re.findall(r'movie-box" href="(.+?)">', html_bus)  # 匹配处理“标题”
        if list_search_results:
            jav_pref = car.split('-')[0]  # 匹配车牌的前缀字母
            jav_suf = car.split('-')[-1].lstrip('0')  # 当前车牌的后缀数字 去除多余的0
            list_fit_results = []  # 存放，车牌符合的结果
            for i in list_search_results:
                url_end = i.split('/')[-1].upper()
                url_suf = re.search(r'[-_](\d+)', url_end).group(1).lstrip('0')  # 匹配box上影片url，车牌的后缀数字，去除多余的0
                if jav_suf == url_suf:  # 数字相同
                    url_pref = re.search(r'([A-Z]+2?8?)', url_end).group(1).upper()  # 匹配处理url所带车牌前面的字母“n”
                    if jav_pref == url_pref:  # 数字相同的基础下，字母也相同，即可能车牌相同
                        list_fit_results.append(i)
            # 有结果
            if list_fit_results:
                # 有多个结果，发个状态码，警告一下用户
                if len(list_fit_results) > 1:
                    status = 1
                # 默认用第一个搜索结果
                url_first_result = list_fit_results[0]
                print('    >获取系列：', url_first_result)
                html_bus = get_bus_html(url_first_result, proxy)
                # DVD封面cover
                coverg = re.search(r'bigImage" href="(.+?)">', html_bus)
                if str(coverg) != 'None':
                    url_cover_bus = coverg.group(1)
                # 系列:</span> <a href="https://www.cdnbus.work/series/kpl">悪質シロウトナンパ</a>
                seriesg = re.search(r'系列:</span> <a href=".+?">(.+?)</a>', html_bus)
                if str(seriesg) != 'None':
                    series = seriesg.group(1)
    return series, url_cover_bus, status

