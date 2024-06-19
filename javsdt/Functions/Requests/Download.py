# -*- coding:utf-8 -*-
import requests
from PIL import Image


# 下载图片，无返回
# 参数：图片地址，存放路径，代理
def download_pic(url, path, proxy):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36',
        'referer': url,
    }

    for retry in range(5):
        try:
            if proxy:
                r = requests.get(url, proxies=proxy, stream=True, timeout=(6, 10), headers=headers)
                with open(path, 'wb') as pic:
                    for chunk in r:
                        pic.write(chunk)
            else:
                r = requests.get(url, stream=True, timeout=(6, 10), headers=headers)
                with open(path, 'wb') as pic:
                    for chunk in r:
                        pic.write(chunk)
        except requests.exceptions.ProxyError:
            # print(format_exc())
            print('    >通过局部代理失败，重新尝试...')
            continue
        except:
            # print(format_exc())
            print('    >下载失败，重新下载...')
            continue
        # 如果下载的图片打不开，则重新下载
        try:
            img = Image.open(path)
            img.load()
            return
        except OSError:
            print('    >下载失败，重新下载....')
            continue
    raise Exception('    >下载多次，仍然失败！')