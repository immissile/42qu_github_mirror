#coding:utf-8
import _env
from redis import Redis

redis_client = Redis(
    host='localhost', port=6379, db=0, password=None, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None
)
print redis_client.get('key1')
redis_client.set('key1','value1')
print redis_client.get('key2')


