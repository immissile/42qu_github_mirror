import _env
from model.cid import CID_BUZZ_PO_REPLY
from model.buzz import Buzz

Buzz.raw_sql('delete from buzz where cid=%s', CID_BUZZ_PO_REPLY)
Buzz.raw_sql('delete from buzz where cid=%s', 222)
