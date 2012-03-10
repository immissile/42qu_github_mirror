#coding:utf-8

from model.zsite_star import zsite_star_get

def _can_admin(callback):
    def __can_admin(func):
        def _(self, id, *args, **kwds):

            zsite = zsite_star_get(id)
            if zsite:
                star = zsite.star
                if star and star.can_admin(self.current_user_id):
                    self.zsite = zsite
                    func(self, id, *args, **kwds)
                    return

            callback(self) 

        return _
    return __can_admin

can_admin = _can_admin(
    lambda self:self.redirect("/")
)
can_admin_json = _can_admin(
    lambda self:self.finish("{login:1}")
) 

if __name__ == "__main__":
    pass



