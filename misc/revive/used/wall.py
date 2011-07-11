#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.man_wall import ManWall, ManWallReply
from qu.mysite.util.orm import ormiter
from model.zsite import Zsite
from model.wall import Wall, wall_id_by_from_id_to_id
from model.state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from model.days import epoch_seconds
from model.zsite import Zsite



def init_wall():
    for o in ormiter(ManWall, 'state>3'):
        from_id = o.from_id
        to_id = o.to_id
        from_ = Zsite.get(from_id)
        to = Zsite.get(to_id)
        if from_ and to:
            to.reply_new(from_, o.txt, o.state, epoch_seconds(o.create_time))
            wall_id = wall_id_by_from_id_to_id(from_id, to_id)
            wall = Wall.get(wall_id)
            for r in o.reply_list():
                user = Zsite.get(r.man_id)
                wall.reply_new(user, r.txt, r.state, epoch_seconds(o.create_time))


if __name__ == '__main__':
    init_wall()
