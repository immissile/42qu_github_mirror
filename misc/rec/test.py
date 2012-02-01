#coding:utf-8
import _env
from redis import Redis

redis_client = Redis(
    host='localhost', port=6379, db=0, password=None, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None
)
help(redis_client)
print redis_client.get(1)
redis_client.set(1, 2)
print redis_client.get(1)

