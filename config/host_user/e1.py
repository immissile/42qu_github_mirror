from glob import glob

USER = glob("/home/z*")
USER = [
    i[6:] for i in USER if i[7:].isdigit()
]
#print USER
 
