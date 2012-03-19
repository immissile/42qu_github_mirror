import gdata.contacts
import gdata.contacts.service
import gdata.auth

SIG_METHOD = gdata.auth.OAuthSignatureMethod.HMAC_SHA1
#try:
#except:
GOOGLE_CONSUMER_KEY = '518129477934.apps.googleusercontent.com'
GOOGLE_CONSUMER_SECRET = 'FRWbGhiNb8gau-Ku2i5Fnh-J'


def load_friend(TOKEN, TOKEN_SECRET, GOOGLE_CONSUMER_KEY=GOOGLE_CONSUMER_KEY, GOOGLE_CONSUMER_SECRET=GOOGLE_CONSUMER_SECRET):
    client = gdata.contacts.service.ContactsService(source=GOOGLE_CONSUMER_KEY)
    client.SetOAuthInputParameters(SIG_METHOD, GOOGLE_CONSUMER_KEY, consumer_secret=GOOGLE_CONSUMER_SECRET)

    token = gdata.auth.OAuthToken(key=TOKEN, secret=TOKEN_SECRET)
    token.scopes = 'http://www.google.com/m8/feeds/'
    token.oauth_input_params = client._oauth_input_params
    client.SetOAuthToken(token)


    query = gdata.contacts.service.ContactsQuery()
    query.max_results = 99999
    #query.start_index = 1
    feed = client.GetContactsFeed(query.ToUri())

    result = [] #email,name,info
    print result, '!!!!!!!!'
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


if __name__ == '__main__':
    fr = load_friend('1/9N-3MPx_MoI3GsWv6sR8IyKei3qj_4CQdPDiJqR4XGQ', 'P0msFzqqj-AXZ5zuaCHuxe4p')
    print fr
