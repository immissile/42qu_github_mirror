#! /usr/bin/env python
#coding=utf-8

class Errtip(object):
    def __init__(self, template="""<div class="errtip" id="errtip_%s">%s</div>"""):
        self._errtip = {}
        self._template = template

    def __getattr__(self, name):
        if name.startswith('_'):
            return self.__dict__[name]

        if self._errtip and name in self._errtip:
            v = self._errtip[name]
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
        return bool(self._errtip)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        elif value is not None:
            self.__dict__['_errtip'][name] = value

    def __contains__(self, name):
        return name in self._errtip

if __name__ == '__main__':
    errtip = Errtip()
    print bool(errtip)
    errtip.name = '程序'
    print bool(errtip)
    print errtip.nam2we
    print 'name' in errtip
    print 'x' in errtip
