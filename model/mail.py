#coding:utf-8
from _db import McCache
from config import render, SMTP, SMTP_USERNAME, SMTP_PASSWORD, SENDER_MAIL, SENDER_NAME, SITE_HTTP

from email.MIMEText import MIMEText
from email.Header import Header
from os.path import join
from decorator import decorator
from email.Utils import parseaddr, formataddr
from base64 import encodestring
import smtplib

NOT_SUPPORT_UTF8_DOMAIN = set(['tom.com', 'hotmail.com', 'msn.com', 'yahoo.com'])

def ignore_encode(s, enc):
    return s.decode('utf-8', 'ignore').encode(enc, 'ignore')


def sendmail_imp(
        smtp,
        sender, sender_name,
        recipient, recipient_name,
        subject, body, enc='utf-8',
        format='plain'
    ):
    if not subject:
        return

    at = recipient.find('@')
    if at <= 0:
        return

    domain = recipient[at+1:].strip()
    if domain not in NOT_SUPPORT_UTF8_DOMAIN:
        enc = 'utf-8'
    else:
        enc = "gb18030"

    if enc.lower() != 'utf-8':
        sender_name = ignore_encode(sender_name, enc)
        recipient_name = ignore_encode(recipient_name, enc)
        body = ignore_encode(body, enc)
        subject = ignore_encode(subject, enc)

    msg = MIMEText(body, format, enc)
    msg['Subject'] = Header(subject, enc)

    sender_name = str(Header(sender_name, enc))
    msg['From'] = formataddr((sender_name, sender))

    recipient_name = str(Header(recipient_name, enc))
    msg['To'] = formataddr((recipient_name, recipient))

    smtp.sendmail(sender, recipient, msg.as_string())


def render_template(uri, **kwds):
    txt = render(uri, **kwds).strip()
    r = txt.split("\n", 1)

    if len(r) < 2:
        r.append(txt[0])

    if uri.endswith(".txt"):
        r[1] = r[1].replace("\n", "\n\n")
    return r

NOEMAIL = "kanrss_noemail@googlegroups.com"

def sendmail(subject, text, email, name=None, sender=SENDER_MAIL, sender_name=SENDER_NAME):
    if not email:
        email = NOEMAIL
        subject = "->%s : %s"%(name, subject)

    if name is None:
        name = email.rsplit("@", 1)[0]
    server = smtplib.SMTP(SMTP)
    server.ehlo()
    server.esmtp_features["auth"] = "LOGIN PLAIN"
    server.login(SMTP_USERNAME, SMTP_PASSWORD)

    text = str(text)
    subject = str(subject)
    sendmail_imp(server, sender, sender_name, email, name, subject, text)

    if email != NOEMAIL:
        subject = "%s %s %s"%(name, subject, email)
        sendmail_imp(server, sender, sender_name, "kanrss_backup@googlegroups.com", name, subject, text)

    server.quit()


def rendermail(
        uri, email, name=None, sender=SENDER_MAIL, sender_name=SENDER_NAME, **kwds
    ):
    if name is None:
        name = email.split("@", 1)[0]
    kwds['name'] = name
    kwds['email'] = email
    kwds['sender'] = sender
    kwds['sender_name'] = sender_name
    kwds['site_http'] = SITE_HTTP
    subject, text = render_template(uri, **kwds)
    subject = str(subject)
    text = str(text)
    sendmail(subject, text, email, name, sender, sender_name)

from mq import mq_client
mq_rendermail = mq_client(rendermail)

if "__main__" == __name__:
    #sendmail("122", "2345", "zsp007@gmail.com")
    import sys
    #rendermail()
    mq_rendermail("/mail/auth/register.txt", "zsp007@gmail.com", "张沈鹏")
