import gdata.contacts
import gdata.contacts.service
import gdata.auth
from gdata.service import RequestError

SIG_METHOD = gdata.auth.OAuthSignatureMethod.HMAC_SHA1
#try:
from config import GOOGLE_CONSUMER_SECRET, GOOGLE_CONSUMER_KEY
#except:
#    GOOGLE_CONSUMER_KEY = "kanrss.com"
#    GOOGLE_CONSUMER_SECRET = "sQ0H34M+w1nY9sTjD+DRU3n5"


def load_friend(TOKEN, TOKEN_SECRET):
    client = gdata.contacts.service.ContactsService(source=GOOGLE_CONSUMER_KEY)
    client.SetOAuthInputParameters(SIG_METHOD, GOOGLE_CONSUMER_KEY, consumer_secret=GOOGLE_CONSUMER_SECRET)

    token = gdata.auth.OAuthToken(key=TOKEN, secret=TOKEN_SECRET)
    token.scopes = "http://www.google.com/m8/feeds/"
    token.oauth_input_params = client._oauth_input_params
    client.SetOAuthToken(token)


    query = gdata.contacts.service.ContactsQuery()
    query.max_results = 99999
    #query.start_index = 1
    feed = client.GetContactsFeed(query.ToUri())

    result = [] #email,name,info
    for entry in feed.entry:
        name = entry.title.text
        for email in entry.email:
            email_address = email.address
        if email_address:
            email_address = email_address.strip().lower()
            if name is not None:
                name = name.strip()
            result.append((name, email_address, None))

    return result

