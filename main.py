from thread import myThread
from spider import YuanQi

if __name__ == '__main__':
    # 捕捉异常错误
    try:
        threads = []

        spider = YuanQi()
        spider.run()

        # 获取爬到的图片资源地址和信息
        imgurl = spider.picUrl
        imgtitle = spider.picTitle
        imgkind = spider.kind

        # 创建线程
        thread1 = myThread(1, "Thread-1", imgurl, imgtitle, imgkind)
        thread2 = myThread(2, "Thread-2", imgurl, imgtitle, imgkind)
        thread3 = myThread(3, "Thread-3", imgurl, imgtitle, imgkind)
        thread4 = myThread(4, "Thread-4", imgurl, imgtitle, imgkind)

        # 开启新线程
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()


        # 等待所有线程完成
        for t in threads:
            t.join()
        print("退出主线程")

    except Exception as e:
        print("错误:", e)