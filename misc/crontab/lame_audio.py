#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.po import Po
from model.fs import fs_file_audio, fs_set_audio
from os.path import exists, dirname
import os
import shutil
from model.cid import CID_AUDIO
from model.po_audio import AUDIO_ORIGINAL, AUDIO_COMPRESSED
from zweb.orm import ormiter
import subprocess

def audio_compress():
    c = Po.raw_sql("select id from po where rid=%s and cid=%s limit 1",\
                   AUDIO_ORIGINAL, CID_AUDIO)
    x = c.fetchone()
    if x:
        mark_id = x[0]
        for i in ormiter(Po, 'id>=%s and cid=%s'%\
                         (mark_id, CID_AUDIO)): 
            input_filename = fs_file_audio('mp3', i.id)
            output_filename = '/tmp/temp.mp3' 
            subprocess.call([ 
                "lame", 
                "--quiet", 
                "--mp3input", 
                "--abr", 
                "64", 
                input_filename, 
                output_filename 
            ]) 
            shutil.copy(output_filename, input_filename)
            i.rid = AUDIO_COMPRESSED
            i.save()

if __name__ == "__main__":
    audio_compress()

