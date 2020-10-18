# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql.cursors


class MySql:
    def __init__(self, host, port, user, pw, db):
        self.host = host
        self.port = port
        self.user = user
        self.pw = pw
        self.db = db

        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.pw,
            database=self.db,
            port=self.port,
            read_timeout=20,
            write_timeout=20,
            connect_timeout=8,
            charset='utf8mb4',)

        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()

        if exc_tb is None:
            self.conn.commit()

        else:
            self.conn.rollback()

        self.conn.close()


class MaoyanMysqlPipeline:
    def __init__(self, url, db):
        self.url = url
        self.db = db

        self.MySql = None
        self.data = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MYSQL_URL', '127.0.0.1'),
                   crawler.settings.get('MYSQL_DB', 'test'))

    def open_spider(self, spider):
        self.MySql = MySql(self.url, 3306, 'root', 'my-secret-pw', self.db)

    def process_item(self, item, spider):
        data = [value for k, value in item.items()]
        self.data.append(data)
        return item

    def close_spider(self, spider):
        if self.data:
            cmd = "INSERT INTO maoyan (movietype, name, onshow) " \
                  "VALUES (%s, %s, %s)"
            with self.MySql as mysql:
                mysql.executemany(cmd, self.data)
