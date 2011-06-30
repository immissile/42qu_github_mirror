from config import SITE_DOMAIN
from urlparse import urlparse
from model.zsite_link import id_by_url
from model.zsite import Zsite
from model.user_mail import user_id_by_mail

def zsite_by_query(query):
    user_id = None

    if '@' in query:
        user_id = user_id_by_mail(query)
    elif SITE_DOMAIN in query:
        key = urlparse(query).netloc.split('.', 1)[0]
        user_id = id_by_url(key)
    elif query.isdigit():
        if Zsite.mc_get(query):
            user_id = query
    else:
        user_id = id_by_url(query) 
    return user_id
        
