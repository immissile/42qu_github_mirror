#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.po import Po
from model.fs import fs_file_audio, fs_set_audio
from os.path import exists, dirname
from os import makedirs
from model.cid import CID_AUDIO
from model.po_audio import AUDIO_ORIGINAL, AUDIO_COMPRESSED
from zweb.orm import ormiter
import subprocess

def audio_compress():
    #Po.where('rid=%s', AUDIO_ORIGINAL).order_by('id desc').limit(1)
    c = Po.raw_sql("select id from po where rid=%s and cid=%s limit 1",\
                   AUDIO_ORIGINAL, CID_AUDIO)
    if c:
        mark_id = c.fetchone()[0]
        for i in ormiter(Po, 'id>=%s and cid=%s'%\
                         (mark_id, CID_AUDIO)): 
            input_filename = fs_file_audio(AUDIO_ORIGINAL, i.id)
            output_filename = fs_file_audio(AUDIO_COMPRESSED, i.id)
            dirpath = dirname(output_filename)
            if not exists(dirpath):
                makedirs(dirpath)
            subprocess.call([ 
                "lame", 
                "--quiet", 
                "--mp3input", 
                "--abr", 
                "64", 
                input_filename, 
                output_filename 
            ]) 
            i.rid = AUDIO_COMPRESSED
            i.save()

if __name__ == "__main__":
    audio_compress()
        

