import _env
from model.event import EventJoiner, event_review_registration, EVENT_JOIN_STATE_NEW
import time

def buzz_registration_review_mail():
    ago = int(time.time()) - 16*60*60
    c = EventJoiner.raw_sql("select distinct(event_id) from event_joiner where state=%s and create_time<%s;",EVENT_JOIN_STATE_NEW, ago)
    event_id_list = c.fetchall()
    print event_id_list
    for event_id in event_id_list:
        event_review_registration(event_id[0])

if __name__=="__main__":
    buzz_registration_review_mail()
