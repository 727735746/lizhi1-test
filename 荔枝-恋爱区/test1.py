from lxml import etree
import requests
import json
import csv
import time
# 一级网页提取数据
def get_index():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://www.lizhi.fm/label/24229798160629936/2.html",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "sec-ch-ua": "^\\^Google",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^"
    }
    cookies = {
        "Hm_lvt_45dcc777b283462d0db81563b6c09dbe": "1687488702",
        "page-type": "play",
        "page": "^%^7B^%^22hiddenPh^%^22^%^3A^%^22mJ17WARtcjM^%^22^%^2C^%^22band^%^22^%^3A18459^%^2C^%^22rid^%^22^%^3A6931495515974784^%^2C^%^22uid^%^22^%^3A11953^%^2C^%^22userName^%^22^%^3A^%^22^%^E4^%^BF^%^AE^%^E7^%^82^%^BC^%^E7^%^88^%^B1^%^E6^%^83^%^85^%^E2^%^9C^%^A8^%^E5^%^BC^%^82^%^E5^%^9C^%^B0^%^E6^%^81^%^8B^%^E7^%^92^%^90^%^E7^%^92^%^90^%^22^%^2C^%^22radioName^%^22^%^3A^%^22^%^E4^%^BF^%^AE^%^E7^%^82^%^BC^%^E7^%^88^%^B1^%^E6^%^83^%^85^%^F0^%^9F^%^8E^%^88^%^E5^%^BC^%^82^%^E5^%^9C^%^B0^%^E6^%^81^%^8B^%^22^%^2C^%^22title^%^22^%^3A^%^22Vol.759^%^20^%^E7^%^88^%^B1^%^E4^%^B8^%^80^%^E4^%^B8^%^AA^%^E4^%^B8^%^8D^%^E5^%^96^%^9C^%^E6^%^AC^%^A2^%^E4^%^BD^%^A0^%^E7^%^9A^%^84^%^E4^%^BA^%^BA^%^22^%^2C^%^22duration^%^22^%^3A318^%^2C^%^22url^%^22^%^3A^%^22^%^22^%^2C^%^22id^%^22^%^3A^%^222907349938499047942^%^22^%^2C^%^22cover^%^22^%^3A^%^22https^%^3A^%^2F^%^2Fcdnimg103.lizhi.fm^%^2Fradio_cover^%^2F2016^%^2F11^%^2F30^%^2F2571155323974400516.jpg^%^22^%^2C^%^22payflag^%^22^%^3A0^%^2C^%^22islistenfirst^%^22^%^3A0^%^7D",
        "page-ts": "1687488729823",
        "repeater": "1",
        "box": "372ae70",
        "box-ts": "1687488730146",
        "Hm_lpvt_45dcc777b283462d0db81563b6c09dbe": "1687488871"
    }
    data_list = []
    # 循环获取指定页面的内容，此处为第1页
    for i in range(1, 2):

        print(f'正在下载{i}页')
        url = f"https://www.lizhi.fm/label/24229798160629936/{i}.html"
        res = requests.get(url, headers=headers, cookies=cookies)
        html = etree.HTML(res.text)

        # 提取一级页面的数据
        text_list = html.xpath('/html/body/div/div[2]/div[1]/div/ul/li/p/@data-user-name')
        img_list = html.xpath('/html/body/div/div[2]/div[1]/div/ul/li/a/img/@data-echo')

        # 提取二级页面的链接
        se_list = html.xpath('/html/body/div/div[2]/div[1]/div/ul/li/a/@href')

        # 请求二级页面内容
        for index in se_list:
            time.sleep(0.2)
            items = []   # 存储json列表
            id_list = []  # 创建一个列表提取id
            time_list = [] # 创建一个列表提取时间
            get_mp3 = []  # 创建一个列表存储音频

            # 拼接请求的url
            get_http = 'https://www.lizhi.fm'+ index
            res1 = requests.get(get_http,headers=headers)
            html1 = etree.HTML(res1.text)

            # 提取音频的id信息
            mp3_list = html1.xpath('/html/body/div/div[2]/div[5]/ul/li/a/@href')
            for info in mp3_list:
                data = info.split('/')[2]
                id_list.append(data)

            # 提取音频的创建时间
            mp3_creat = html1.xpath('/html/body/div/div[2]/div[5]/ul/li/a/div[1]/p[2]/text()')
            for info in mp3_creat:
                data = info.split('\xa0')[0]
                data_next = data.replace('-','/')
                time_list.append(data_next)

            # 将音频的id和创建时间合并拼接成url音频
            for id,create in zip(id_list,time_list):
                mp3_get = f'https://cdn5.lizhi.fm/audio/{create}/{id}_hd.mp3'
                get_mp3.append(mp3_get)

            # 构建一级页面的数据
            for text,img in zip(text_list, img_list):
                item = {}
                item['一级页面文字'] = text
                item['一级页面的图片'] = img
                item['作者前10音频'] = get_mp3
                items.append(item)
                print(item)

    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['一级页面文字', '一级页面的图片', '作者前10音频']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)


if __name__ == '__main__':
    get_index()