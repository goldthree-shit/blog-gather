import time

import requests
import os
import re
class Info:
    def __init__(self):
        super().__init__()
        self.__session = requests.session()
        self.__headers = {
            'cookie': '_ga=GA1.1.1370470478.1710342025; lastPath=/%E4%B8%93%E6%A0%8F/10x%E7%A8%8B%E5%BA%8F%E5%91%98%E5%B7%A5%E4%BD%9C%E6%B3%95;',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'content-type': 'application/x-www-form-urlencoded'
        }
        self.__main_url = "http://learn.lianglianglee.com/"

    def spider(self):
        # todo: 目前是先判断本地是否存在首页，若存在直接从本地读取专栏目录，但无法应对更新
        if not os.path.exists("./blogs"):
            os.mkdir("./blogs/")
        if not os.path.exists("./blogs/index.html"):
            resp = self.__session.get(self.__main_url, headers=self.__headers)
            with open("./blogs/index.html", mode="wb") as f:
                f.write(resp.text.encode("utf-8"))
            resp.close()
        with open("./blogs/index.html", mode="r", encoding="utf-8") as f:
            special_columns = re.compile(r"<li><a href=\"/专栏/(?P<special_columns>.*?)\"", re.S).findall(f.read())

        # 获取全部专栏
        # ['10x程序员工作法', '12步通关求职面试-完',...,]
        # print(special_columns)
        # 遍历全部专栏并保存
        for special_column in special_columns:
            print("正在爬取专栏----" + special_column)
            # 如果不存在专栏所在的目录，则创建
            if not os.path.exists("./blogs/" + special_column):
                os.mkdir("./blogs/" + special_column)
            # 如果不存在，下载专栏首页
            if not os.path.exists("./blogs/" + special_column + "/index.html"):
                resp = self.__session.get(self.__main_url + "/专栏/" + special_column)
                with open("./blogs/" + special_column + "/index.html", mode="wb") as f:
                    f.write(resp.text.encode("utf-8"))
                resp.close()
            with open("./blogs/" + special_column + "/index.html", mode="r", encoding="utf-8") as f:
                title_names = re.compile(r"<a class =\"menu-item\" id=\"(?P<title_name>.*?)\"", re.S).findall(f.read())
            # ['00 开篇词 程序员解决的问题，大多不是程序问题.md', ...,]
            # print(title_names)
            for title_name in title_names:
                print("正在爬取文章----" + title_name)
                # 如果不存在
                if not os.path.exists("./blogs/" + special_column + "/" + title_name[:-3] + ".html"):
                    blog_resp = self.__session.get(self.__main_url + "专栏/" + special_column + "/" + title_name)
                    # http://learn.lianglianglee.com/专栏/10x程序员工作法/结束语 少做事，才能更有效地工作.md
                    # print(self.__main_url + "专栏/" + special_column + "/" + title_name)
                    with open("./blogs/" + special_column + "/" + title_name[:-3] + ".html", mode="wb") as f:
                        f.write(blog_resp.text.encode("utf-8"))
                    blog_resp.close()
                    # 增加两秒时延，避免被识别
                    time.sleep(2)
                # 如果存在则跳过


