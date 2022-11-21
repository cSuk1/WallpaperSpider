import threading
from spider import down_load_img

# threadLock = threading.Lock()

class myThread (threading.Thread):
    def __init__(self, threadID, name, imgurl, imgtitle, imgkind):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.imgurl = imgurl
        self.imgtitle = imgtitle
        self.imgkind = imgkind

    def run(self):
        print("开启线程： " + self.name + '\n')
        down_load_img(self.threadID, self.imgurl, self.imgtitle, self.imgkind)
        print("线程" + str(self.threadID) + "下载完成")