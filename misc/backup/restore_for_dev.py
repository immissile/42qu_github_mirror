import socket
hostname = socket.gethostname()
if hostname != "e1":
    raise "hostname is not e1"


#import _env
#from model.vps import Vps
#from model.mail import Ma


