
def jsonp(self, txt):
    callback = self.get_argument('callback', None)
    if callback:
        txt = '%s(%s)'%(callback, txt)
        content_type = 'text/javascript'
    else:
        content_type = 'text/plain'
    self.set_header('Content-Type', content_type)
    return txt
