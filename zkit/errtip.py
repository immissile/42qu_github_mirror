#! /usr/bin/env python
#coding=utf-8

class Errtip(object):
    def __init__(self, template="""<p class="error" id="error_%s">%s</p>"""):
        self._error = {}
        self._template = template

    def __getattr__(self, name):
        if name.startswith("_"):
            return self.__dict__[name]
        if self._error and name in self._error:
            v = self._error[name]
        else:
            v = ''


        html = self._template%(
            name,
            v
        )

        return html

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __nonzero__(self):
        return bool(self._error)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            self.__dict__[name] = value
        else:
            self.__dict__['_error'][name] = value

    def __contains__(self, name):
        return name in self._error

if __name__ == '__main__':
    errtip = Errtip()
    print bool(errtip)
    errtip.name = '程序'
    print bool(errtip)
    print errtip.name
    print 'name' in errtip
    print 'x' in errtip
