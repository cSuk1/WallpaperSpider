import requests
import random
import bs4
from ua_info import ua_list
import os


class YuanQi(object):

    # 初始化
    def __init__(self):
        self.url = None
        self.kind = None
        self.page_end = 0
        self.page_begin = 0
        self.page_now = 0

    # 选择下载漫画类型
    def select(self):
        print("请选择需要下载的壁纸类型：\n")
        print("1.动漫\n2.风景\n3.美女\n")
        slt = int(input())
        if slt == 1:
            self.url = 'https://bizhi.cheetahfun.com/dn/c2j/'
            self.kind = '动漫'
            path = 'E:/元气壁纸爬虫/' + self.kind
            self.mk_dir(path)
        elif slt == 2:
            self.url = 'https://bizhi.cheetahfun.com/dn/c1j/'
            self.kind = '风景'
            path = 'E:/元气壁纸爬虫/' + self.kind
            self.mk_dir(path)
        else:
            self.url = 'https://bizhi.cheetahfun.com/dn/c3j/'
            self.kind = '美女'
            path = 'E:/元气壁纸爬虫/' + self.kind
            self.mk_dir(path)
        print('选择成功！！！\n请输入下载的起始页：\n')
        self.page_begin = int(input())
        self.page_end = int(input())
        self.page_now = self.page_begin
        print('正在下载中……\n')

    # 请求函数
    def get_html(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        req = requests.get(url=url, headers=headers)
        # req = requests.get(url=url)
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

    # 下载图片
    def download_img(self):
        html_file = open('index.html', encoding='utf-8')
        soup = bs4.BeautifulSoup(html_file.read(), 'html.parser')
        elems = soup.select('img[class="w-full h-full object-fill"]')
        # 获取图片的资源地址
        for i in range(0, 18):
            headers = {'User-Agent': random.choice(ua_list)}
            img_url = elems[i].get('src')
            title = elems[i].get('title')
            img_req = requests.get(url=img_url, headers=headers)
            try:
                file_ad = self.kind + '/' + title.replace("?", "") + '.jpg'
                jpg = open(file_ad, 'wb')
                for chunk in img_req.iter_content(10000):
                    jpg.write(chunk)

                jpg.close()
            except:
                file_ad = self.kind + '/第' + str(self.page_begin) + '页第' + str(i) + '张' + '.jpg'
                jpg = open(file_ad, 'wb')
                for chunk in img_req.iter_content(10000):
                    jpg.write(chunk)

                jpg.close()

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
            self.download_img()
            link = self.next_page()

        print('下载完成！！！')


if __name__ == '__main__':
    # 捕捉异常错误
    try:
        spider = YuanQi()
        spider.run()
    except Exception as e:
        print("错误:", e)
