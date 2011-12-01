#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM

class SiteSync(Model):
    pass


def site_sync_new(po_id):
    ss = SiteSync.get_or_create(po_id=po_id)
    ss.save()

def site_sync_get(po_id):
    return SiteSync.get(po_id=po_id)

def site_sync_rm(po_id):
    return SiteSync.where(po_id=po_id).delete()
