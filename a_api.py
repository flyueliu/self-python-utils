from database_client import MYSQLClient

a = '😟'
client = MYSQLClient(host='192.168.8.171', port=3306, user='root', passwd='root', db='test')

client.execute("insert into test values (%(key1)s)", {'key1': a})

client.close()
