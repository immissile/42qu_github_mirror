# 
# Takes a pyflakes output file "out.flakes" and try to cleanup
# unecessary import according to the file informations
#
import re
from tempfile import mkstemp
from shutil import move
from os import remove, close
from import_ignore import import_ignore

unused_import = r"([a-zA-Z/_\.]+):([0-9+]): '([a-zA-Z_]+)' imported but unused"

":[0-9+]: '[a-zA-Z_]+' imported but unused"

def replace_line(filename, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(filename)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(filename)
    #Move new file
    move(abs_path, filename)

replacements = []
def lazy_replace_line(filename, pattern, subst):
    replacements.append((filename, pattern, subst))

def commit_replace_line():
    for rep in replacements:
        replace_line(*rep)

fh = open('out.flakes', 'r')

filename_pre = None

for flakeline in fh.readlines():
    match = re.match(unused_import, flakeline)
    if match:
        filename, linenumber, name = match.groups(1)
        fname = flakeline.strip()
        rfh = open(filename, 'r')
        line = rfh.readlines()[int(linenumber)-1]
        if import_ignore(line):
            continue
        print('----------------------------------------')
        print(fname)
        new_line = line
        new_line = new_line.replace(', '+name+'\n', '\n').replace(
            ' '+name+'\n', '\n').replace(' '+name+', ', ' ')
        if new_line.strip().endswith(' import') or new_line.strip().endswith(' as'):
            new_line = ''
        print('Before: ' + line.replace('\n', ''))
        print('After : ' + new_line.replace('\n', ''))
        print('----------------------------------------')
        replace = raw_input("Do you want to remove this import? [y/N] ")
        if replace.lower() == 'y':

            if filename_pre and filename != filename_pre: 
                for rep in replacements:
                    print(rep)
                commit_replace_line()
            lazy_replace_line(filename, line, new_line)

        filename_pre = filename
