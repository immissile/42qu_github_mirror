import _env
from model.event import EventJoiner, event_review_join_apply, EVENT_JOIN_STATE_NEW, event_ready, EVENT_STATE_BEGIN, Event
import time

def buzz_join_apply_review_mail():
    ago = int(time.time()) - 18*60*60

    c = EventJoiner.raw_sql('select distinct(event_id) from event_joiner where state=%s and create_time<%s;', EVENT_JOIN_STATE_NEW, ago)

    event_id_list = c.fetchall()

    for event_id in event_id_list:
        event_review_join_apply(event_id[0])

def event_ready_mail():
    now = int(time.time())/60

    c = Event.raw_sql('select id from event where state = %s and begin_time >= %s and begin_time < %s',EVENT_STATE_BEGIN,now,now+24*2*60)
    
    event_id_list = c.fetchall()

    for event_id in event_id_list:
        event_ready(event_id[0])
if __name__ == '__main__':
    event_ready_mail()
    buzz_join_apply_review_mail()
