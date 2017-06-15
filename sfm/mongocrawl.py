#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

**中文文档**

mongocrawl是一个使用MongoDB作为数据持久层, 广度优先的定向爬虫框架。非常适合于
数据资源所在的Url是树状层级结构的爬虫项目。

举例来说, 我们希望抓取全国所有的邮政编码。而邮政编码数据网站的结构是:
'1个国家有a个省, 1个省有b个市, 1个市有c个区, 1个区有d个邮政编码', 类似这种的
层级结构。所以我们要遍历所有省的页面找到所有的市, 然后遍历所有的市的页面找到
所有的区... 这样层层向下遍历, 从而最终获得所有的邮政编码。
"""

import json
import pickle
import logging
import pymongo
import mongoengine
from crawlib.spider import spider
from loggerFactory import StreamOnlyLogger
from multiprocessing.dummy import Pool
from sfm.mongoengine_mate import ExtendedDocument

logging.getLogger("requests").setLevel(logging.WARNING)


class Task(ExtendedDocument):

    """

    **中文文档**

    由于是广度优先爬虫, 所以在对下一级的Url进行抓取时, 上一级全部的Url列表应该
    是已知的 (当然我们不一定需要完整的Url列表, 这一点之后再谈)。

    :meth:`Task.target_url`:

    每一个Url必然是不相同的。而我们有时可以不必使用Url作为主键, 因为有时Url可以
    通过运算得出, 而不必储存完整Url占据过多的磁盘资源。

    :attr:`Task.status`:

    status项标记了该资源是否被成功抓取过。初始状态下status = 0, 而再抓取过后可以
    将其修改为1。默认情况下mongocrawl只能识别0, 1两种状态。当然用户可以定义更多
    的状态码以应对不同的情况。

    对单个url资源进行抓取需要经过如下几个步骤:

    1. 获得url, :meth:`Task.target_url` 方法。用户需根据具体情况自行定义。
    2. 获得html, :meth:`Task.get_html` 方法。在网站无法通过restful的request请求
      获得html时需要重新自定义。
    3. 抓取data, :meth:`Task.fetch_data` 方法。用户需根据具体情况自行定义。
    4. 存入database, :meth:`Task.crawl_one` 方法。
    """
    _id = mongoengine.StringField(primary_key=True)
    status = mongoengine.IntField()
    json = mongoengine.StringField()
    pickle = mongoengine.BinaryField()

    meta = {"abstract": True}

    use_json = None

    logger = StreamOnlyLogger()

    @property
    def target_url(self):
        """

        **中文文档**

        获得数据所在的真实Url地址。
        """
        raise NotImplementedError

    def get_html(self):
        """

        **中文文档**

        从Url上获得Html。默认使用自动检测文本编码的crawlib中的
        spider.get_html(url)方法。不过有些网站需要用到cookie登陆。可以通过重写
        该方法来实现。
        """
        return spider.get_html(self.target_url)

    @staticmethod
    def fetch_data(html):
        """

        :param html: str, html
        :returns data: dict like data

        **中文文档**

        从得到的Html中解析出数据。支持对json友好的自典型数据。若对json不友好。
        则后面跟数据的操作需要用到pickle接口。
        """
        raise NotImplementedError

    @classmethod
    def crawl_one(cls, task):
        """

        **中文文档**

        抓取一个Url页面。
        """
        url = task.target_url
        cls.logger.info("crawl %s, %s left ..." % (url, task.left_counter))

        try:
            html = spider.get_html(url)
        except Exception as e:
            cls.logger.info("http error: %s" % e, 1)
            return

        try:
            data = task.fetch_data(html)
            if task.__class__.use_json:
                cls.objects(_id=task._id).update(
                    json=json.dumps(data), status=1)
            else:
                cls.objects(_id=task._id).update(
                    pickle=pickle.dumps(data), status=1)
            cls.logger.info("success! data: %s" % data, 1)
        except Exception as e:
            cls.logger.info("parse error: %s" % e, 1)
            return

    @classmethod
    def crawl_all(cls, use_json=True):
        """

        **中文文档**

        多线程爬虫。
        """
        # Add left counter
        counter = cls.objects(status=0).count()
        todo = list()
        for task in cls.objects(status=0):
            task.left_counter = counter
            counter -= 1
            todo.append(task)

        task.__class__.use_json = use_json

        pool = Pool(6)
        pool.map(cls.crawl_one, todo)

    @classmethod
    def set_finished(cls, _id):
        """Mark a task as 'finished'.
        """
        cls.objects(_id=_id).update(status=1)

    @classmethod
    def set_not_finished(cls, _id):
        """Mark a task as 'not finished'.
        """
        cls.objects(_id=_id).update(status=0)



#--- Use Case ---
# Crawl CVS store information from http://www.cvs.com/store-locator/
if __name__ == "__main__":
    from bs4 import BeautifulSoup
    from loggerFactory import SingleFileLogger

    domain = "http://www.cvs.com"
    connect = mongoengine.connect("cvs")  # use cvs database

    class CVSTask(Task):
        meta = {"abstract": True}

        @property
        def target_url(self):
            return domain + self._id

    class State(CVSTask):
        """A State Page.

        Example: http://www.cvs.com/store-locator/cvs-pharmacy-locations/Virginia
        """
        name = mongoengine.StringField()

        meta = {"collection": "state"}

        @staticmethod
        def fetch_data(html):
            data = list()
            soup = BeautifulSoup(html)

            div = soup.find("div", class_="states")
            for a in div.find_all("a"):
                data.append(
                    {"href": a["href"], "name": " ".join(a.text.strip().split(" ")[:-1])})
            return data

    class City(CVSTask):
        """A City Page.

        Example: http://www.cvs.com/store-locator/cvs-pharmacy-locations/Virginia/Alexandria
        """
        name = mongoengine.StringField()

        meta = {"collection": "city"}

        @staticmethod
        def fetch_data(html):
            data = list()
            soup = BeautifulSoup(html)

            div_ = soup.find("div", class_="stores-wrap")
            for div in div_.find_all("div", class_="each-store"):
                d = dict()
                try:
                    p = div.find("p", class_="store-address")
                    d["address"] = p.text.strip()
                except:
                    pass

                try:
                    p = div.find("p", class_="phone-number")
                    d["phone"] = p.text.strip().split("#")[0].strip()
                    d["store_number"] = p.text.strip().split("#")[-1].strip()
                except:
                    pass

                p = div.find("p", class_="directions-link")
                a = p.find("a")
                d["href"] = a["href"]
                if d:
                    data.append(d)

            return data

    import string
    alpha_letter = set(string.ascii_letters + string.digits + " ")

    def extract_alpha_letter(text):
        """Extract only alpha and digits characters from text.
        """
        chunks = list()
        for char in text:
            if char in alpha_letter:
                chunks.append(char)
        return "".join(chunks)

    class Store(CVSTask):
        """A Store Page.

        Example: http://www.cvs.com/store-locator/cvs-pharmacy-address/415+Monroe+Avenue-Alexandria-VA-22301/storeid=1410
        """
        address = mongoengine.StringField()
        phone = mongoengine.StringField()
        store_number = mongoengine.StringField()

        meta = {"collection": "store"}

        @staticmethod
        def fetch_data(html):
            data = dict()
            soup = BeautifulSoup(html)

            try:
                ul = soup.find("ul", id="serviceBadges")
                data["services"] = [
                    extract_alpha_letter(li.text.strip()).strip() for li in ul.find_all("li")]
            except:
                pass

            return data

    #--- Unittest ---
    def test_State_fetch_data():
        url = "http://www.cvs.com/store-locator/cvs-pharmacy-locations/Virginia"
        html = spider.get_html(url)
        data = State.fetch_data(html)
        js.pprint(data)

    # test_State_fetch_data()

    def test_City_fetch_data():
        url = "http://www.cvs.com/store-locator/cvs-pharmacy-locations/Virginia/Alexandria"
        html = spider.get_html(url)
        data = City.fetch_data(html)
        js.pprint(data)

    # test_City_fetch_data()

    def test_Store_fetch_data():
        url = "http://www.cvs.com/store-locator/cvs-pharmacy-address/415+Monroe+Avenue-Alexandria-VA-22301/storeid=1410"
        html = spider.get_html(url)
        data = Store.fetch_data(html)
        js.pprint(data)

    # test_Store_fetch_data()

    #--- Project Code ---
    def fill_state():
        """Put 51 states as entry points from
        http://www.cvs.com/store-locator/cvs-pharmacy-locations.
        """
        data = list()

        url = "http://www.cvs.com/store-locator/cvs-pharmacy-locations"
        html = spider.get_html(url)
        soup = BeautifulSoup(html)
        div = soup.find("div", class_="states")
        for a in div.find_all("a"):
            state = State(_id=a["href"], name=a.text.strip(), status=0)
            data.append(state)

        State.smart_insert(data)

    # fill_state()

    # State.crawl_all(use_json=True)

    def fill_city():
        """Take city data from state collection, and fill into city collection.
        """
        data = list()
        for state in State.objects(_id__ne=0):
            try:
                for d in json.loads(state.json):
                    city = City(_id=d["href"], name=d["name"], status=0)
                    data.append(city)
            except:
                pass
        City.smart_insert(data)

    # fill_city()

    # City.crawl_all(use_json=True)

    def fill_store():
        """Take city data from city collection, and fill into store collection.
        """
        data = list()
        for city in City.objects(_id__ne=0):
            try:
                for d in json.loads(city.json):
                    store = Store(_id=d["href"],
                                  address=d.get("address"),
                                  phone=d.get("phone"),
                                  store_number=d.get("store_number"),
                                  status=0)
                    data.append(store)
            except:
                pass
        Store.smart_insert(data)

#     fill_store()

#     Store.crawl_all(use_json=True)
