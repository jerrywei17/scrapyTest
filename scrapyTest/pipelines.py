import pymysql
from pymongo import MongoClient


class PttPipeline:
    def process_item(self, item, spider):
        item["push"] = int(item["push"])
        return item


class MongoDBPipeline:
    def open_spider(self, spider):
        db_uri = spider.settings.get("MONGODB_URI", "mongodb://localhost:27017")
        db_name = spider.settings.get("MONGODB_DB_NAME", "ptt_scrapy")
        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]

    def process_item(self, item, spider):
        self.insert_article(item)
        return item

    def insert_article(self, item):
        item = dict(item)
        self.db.article.insert_one(item)

    def close_spider(self, spider):
        self.db_client.close()


class MySqlPipeline(object):
    old_data_from_sql = []

    def open_spider(self, spider):
        # DataBase Settings
        db = spider.settings.get("MYSQL_DB_NAME")
        host = spider.settings.get("MYSQL_DB_HOST")
        port = spider.settings.get("MYSQL_PORT")
        user = spider.settings.get("MYSQL_USER")
        password = spider.settings.get("MYSQL_PASSWORD")
        # DataBase Connecting
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=int(port),
            db=db,
            cursorclass=pymysql.cursors.DictCursor,
        )
        pass

    def close_spider(self, spider):
        self.connection.close()
        pass

    def process_item(self, item, spider):
        self.filter_repeat_data(item)
        pass

    def filter_repeat_data(self, item):
        # Getting Old Data from DB
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM news"
            cursor.execute(sql)
            for row in cursor:
                self.old_data_from_sql.append(row["title"])

        if item["title"] not in self.old_data_from_sql:
            self.insert_to_mysql(item)

    def insert_to_mysql(self, item):
        values = (
            item["title"],
            item["content"],
            item["img"],
            item["time"],
        )
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `news` (`title`, `content`, `img`, `time`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, values)
            self.connection.commit()
