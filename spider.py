import os
import requests
import random
import bs4
from ua_info import ua_list


# 爬虫类
class YuanQi(object):

    # 初始化
    def __init__(self):
        self.url = None
        self.kind = None
        self.page_end = 0
        self.page_begin = 0
        self.page_now = 0
        self.picUrl = []
        self.picTitle = []

    # 选择下载漫画类型
    def select(self):
        print("请选择需要下载的壁纸类型：")
        print("1.动漫\n2.风景\n3.美女")
        dir = os.getcwd() + '\\'
        slt = int(input())
        if slt == 1:
            self.url = 'https://bizhi.cheetahfun.com/dn/c2j/'
            self.kind = '动漫'
            path = dir + self.kind
            self.mk_dir(path)
        elif slt == 2:
            self.url = 'https://bizhi.cheetahfun.com/dn/c1j/'
            self.kind = '风景'
            path = dir + self.kind
            self.mk_dir(path)
        else:
            self.url = 'https://bizhi.cheetahfun.com/dn/c3j/'
            self.kind = '美女'
            path = dir + self.kind
            self.mk_dir(path)
        print('选择成功！！！\n')
        self.page_begin = int(input('请输入下载的起始页：'))
        self.page_end = int(input('请输入下载的结束页：'))
        self.page_now = self.page_begin
        print('开始下载！！！\n')

    # 请求函数
    def get_html(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        req = requests.get(url=url, headers=headers)
        html_file = open('index.html', 'wb')
        for chunk in req.iter_content(10000):
            html_file.write(chunk)

        html_file.close()

    def mk_dir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.mkdir(path)
            return True
        else:
            return False

    # 获取图片资源地址和一些信息
    def get_imgUrl(self):
        html_file = open('index.html', encoding='utf-8')
        soup = bs4.BeautifulSoup(html_file.read(), 'html.parser')
        elems = soup.select('img[class="w-full h-full object-fill"]')
        # 获取图片的资源地址
        for i in range(0, 18):
            # headers = {'User-Agent': random.choice(ua_list)}
            img_url = elems[i].get('src')
            title = elems[i].get('title')
            self.picUrl.append(img_url)
            self.picTitle.append(title)

    # 翻页
    def next_page(self):
        self.page_now += 1
        next_url = self.url + 'p' + str(self.page_now)
        return next_url

    # 主函数
    def run(self):
        self.select()
        link = self.url + 'p' + str(self.page_begin)
        for i in range(self.page_begin, self.page_end + 1):
            self.get_html(link)
            self.get_imgUrl()
            link = self.next_page()


# 下载图片函数
def down_load_img(id, imgurl, imgtitle, imgkind):
    headers = {'User-Agent': random.choice(ua_list)}
    for url,title in zip(imgurl, imgtitle):
        file_ad = imgkind + '/' + title.replace("?", "") + '.jpg'
        isExists = os.path.exists(file_ad)
        if not isExists:
            img_req = requests.get(url=url, headers=headers)
            # print("线程" + str(id) + "正在下载" + title.replace("?", "") + '\n')
            jpg = open(file_ad, 'wb')
            for chunk in img_req.iter_content(10000):
                jpg.write(chunk)
        else:
            continue

    jpg.close()