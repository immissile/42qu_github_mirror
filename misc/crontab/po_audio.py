#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.po import Po
from model.fs import fs_file_audio
from os.path import exists, dirname, join
import shutil
from model.cid import CID_AUDIO
from zweb.orm import ormiter
import subprocess
from zkit.single_process import single_process
from model.kv_misc import KV_PO_AUDIO, kv_int
from config import SITE_DOMAIN


@single_process
def audio_compress():
    id = kv_int.get(KV_PO_AUDIO)

    for i in ormiter(Po, 'cid=%s and id>%s'%(
        CID_AUDIO,
        id
    )):
        id = i.id

        input_filename = fs_file_audio(id)

        if not exists(input_filename):
            continue

        output_filename = '/tmp/po.audio.%s'%SITE_DOMAIN

        #if not isdir(output_filename):
        #    os.mkdir(output_filename)

        subprocess.call([
            'lame',
            '--quiet',
            '--mp3input',
            '--abr',
            '64',
            input_filename,
            output_filename
        ])

        if not exists(output_filename):
            continue

        shutil.move(output_filename, input_filename)

    kv_int.set(KV_PO_AUDIO, id)

if __name__ == '__main__':
    audio_compress()

