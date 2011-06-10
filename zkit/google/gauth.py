#!/usr/bin/env python
#coding:utf-8

"""
gauth.py

Adam Hupp <adam at hupp.org>

module for transparent authentication to (some) google services

"""

import httplib
import urllib2
import urllib
import cgi
import logging

SERVICE_AUTH = "https://www.google.com/accounts/ServiceLoginAuth?"

class ParsedURL(object):
    """
    A class for parsing and building URLs.
    """
    def __init__(self, url):
        scheme, netloc, path, query, fragment = httplib.urlsplit(url)
        self.scheme = scheme
        self.netloc = netloc
        self.path = path

        # If there is only one item, extract from list
        query = cgi.parse_qs(query)
        for k, v in query.items():
            if len(v) == 1:
                query[k] = v[0]
        self.query = query
        self.fragment = fragment



class GoogleAuthHandler(urllib2.HTTPRedirectHandler):
    """
    A urllib2 URL handler that detects access to authenticated
    Google services and automtically logs in.

    Errata: Some services use a redirect from CheckCookie (e.g. gmail)
    that is unrelated to the continue parameter.  For those services,
    the CheckCookie branch of the below test should do nothing.

    Usage:

    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                  gauth.GoogleAuthHandler(user, passwd))
    res = opener.open("http://google.com/some/authenticated/page")


    """
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        pu = ParsedURL(newurl)
        if pu.netloc.endswith("google.com"):
            if pu.path == "/accounts/ServiceLogin":
                cont = pu.query["continue"]
                service = pu.query["service"]
                urlparam = urllib.urlencode({"Email" : self.email,
                                             "Passwd" : self.passwd,
                                             "PersistentCookie" : "yes",
                                             "continue" : cont,
                                             "service" : service})
                self.urlparam = urlparam
            elif pu.path == "/accounts/CheckCookie":
                """ The CheckCookie page will uses some javascript to set
               the page location to the value of the continue param

               Note that some services do not used the continue
               parameter, and instead use a completely unrelated
               redirect to send you on your way.  That can be easily
               handled by commenting out the next line, but I'm not
               sure how to to handle both at once in the context of
               a handler like this.
               """
                newurl = pu.query["continue"]
            return urllib2.HTTPRedirectHandler.redirect_request(self, req,
                                                                fp, code,
                                                                msg, headers,
                                                                newurl)

import cookielib, urllib2, Cookie
#    'GDSESS', 



def build_opener(username, passwd):
    import cookielib, urllib2
    cookies = cookielib.CookieJar()
    #cookies.set_cookie(GoogleCookie)
    #  cookie = cookielib.Cookie(
    #      0, 'GDSESS',
    #      'ID=5bc58a99dc2400cb:EX=1297861625:S=ADSvE-eeHAGtFhpUXFqc46ks2pcord7YBA',
    #      None, False, '.google.com', True, False, '/', True, False, None, True, None, None, {}
    #  )
    #  cookies._cookies[cookie.domain] = {
    #      cookie.path:{
    #          cookie.name:cookie
    #      }
    #  }

    handler = GoogleAuthHandler(username, passwd)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), handler)
    res = opener.open("https://reader.google.com/").read()
    #print cookies._cookies
    res = res.split('<')
    para = {}
    for i in res:
        if i.startswith("input"):
            i = i.replace("'", '"').replace("\n", " ")
            #print i
            name = None
            value = None
            for j in i.split(" "):
                j = j.strip('"')
                if j.startswith("name"):
                    name = j.split('"')[-1].strip()
                elif j.startswith("value"):
                    value = j.split('"', )[-1].strip()
            if name and value and name != "name" and value != "value":
                #print name, value
                para[name] = value
    para['Email'] = username
    para['Passwd'] = passwd
    para = urllib.urlencode(para)
    res = opener.open(SERVICE_AUTH+handler.urlparam, para)
    return opener

