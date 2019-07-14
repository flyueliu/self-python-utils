import time
from abc import abstractmethod
from slfj_logger import Sl4jLogger

logging = Sl4jLogger()


class BaseClient(object):

    def __init__(self, host: str, port: int, user: str, passwd: str, db: str):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.conn = self.init()

    """
        @:return connection object
    """

    @abstractmethod
    def init(self):
        pass

    def get_cursor(self):
        try:
            return self.conn.cursor()
        except Exception as e:
            logging.error("create cursor failed!,try connect again!")
            logging.exception(e)
            while True:
                time.sleep(3)
                self.close()
                self.conn = self.init()
                try:
                    return self.conn.cursor()
                except Exception as e:
                    logging.error("create cursor failed!")
                    logging.exception(e)
                    continue

    def query(self, sql: str, param: tuple = None, get_title: bool = False):
        cursor = self.get_cursor()
        try:
            logging.debug("{}", sql)
            logging.debug("params: {}", param)
            cursor.execute(sql, param)
            result = cursor.fetchall()
            data_title = []
            if get_title:
                for item in cursor.description:
                    data_title.append(item[0])
                return tuple(data_title), result
            return result
        except Exception as e:
            logging.error("mysql query error: {}", e)
            raise e
        finally:
            cursor.close()

    def select_one(self, sql, param: tuple = None, get_title: bool = False):
        if get_title:
            title, real_result = self.query(sql, param, get_title=get_title)
        else:
            real_result = self.query(sql, param, get_title=get_title)
        if real_result:
            real_result = real_result[0]
        if get_title:
            return title, real_result
        else:
            return real_result

    def execute(self, sql, param=None):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, param)
            self.conn.commit()
            affected_row = cursor.rowcount
        except Exception as e:
            logging.error("mysql execute error: {}", e)
            return 0
        finally:
            cursor.close()
        return affected_row

    def executemany(self, sql: str, params: tuple = None):
        cursor = self.get_cursor()
        try:
            logging.debug("{} ", sql)
            logging.debug("params: {}", params)
            cursor.executemany(sql, params)
            self.conn.commit()
            affected_rows = cursor.rowcount
        except Exception as e:
            logging.error("mysql executemany error: {}", e)
            return 0
        finally:
            cursor.close()
        return affected_rows

    def close(self):
        if not self.conn:
            return
        try:
            self.conn.close()
        except Exception as e:
            logging.error("close connection error!")
            logging.exception(e)
            raise e


class MYSQLClient(BaseClient):

    def init(self):
        import pymysql
        try:
            return pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                database=self.db,
                charset='utf8'
            )
        except Exception as e:
            logging.error("connect database error!")
            logging.exception(e)
            raise e


class SQLServerClient(BaseClient):

    def init(self):
        import pymssql
        try:
            return pymssql.connect(host=self.host, user=self.user,
                                   password=self.passwd, database=self.db,
                                   charset="utf8"
                                   , as_dict=False)
        except Exception as e:
            logging.error("connect database error!")
            logging.exception(e)
            raise e


class PostgresClient(BaseClient):

    def init(self):
        import psycopg2
        try:
            return psycopg2.connect(database=self.db, user=self.user,
                                    password=self.passwd,
                                    host=self.host,
                                    port=self.port)
        except Exception as e:
            logging.error("connect database error!")
            logging.exception(e)
            raise e


if __name__ == '__main__':
    # test_mysql()
    client = PostgresClient(host="127.0.0.1", port=5432, user="postgres", passwd="****", db="db")
    title, result = client.select_one("select * from test_table where task->>%s=%s;", ('key', '值'),
                                      get_title=True)
    print(result)
    print(title)
    for item in result:
        print(item)
    client.close()
