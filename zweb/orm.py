#coding:utf-8

def ormiter(orm, where=''):
    id = 0
    while True:
        if where:
            r = orm.where(where)
        else:
            r = orm
        total = tuple(r.where('id>%s', id).order_by('id')[:500])
        if total:
            for i in total:
                #print i.id
                yield i
            id = total[-1].id
        else:
            break
