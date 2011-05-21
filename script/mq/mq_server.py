#ncoding:utf-8
import init_env

#from model.mail_mq import sendmail_mq
#from model.reply_notify import reply_notify_new_mq
#from model.note import note_viewer_new_mq
from model.mq import mq_server
from model.feed import mq_mc_flush_zsite_follow
from model.mail import mq_rendermail
mq_server()


