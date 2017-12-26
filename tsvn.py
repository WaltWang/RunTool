#from pprint import pprint
import pprint
import os
import shutil

import svn.local

# svn_path = 'E:/moonserver'

def remove_dir(dir):
    dir = dir.replace('\\', '/')
    if(os.path.isdir(dir)):
        for p in os.listdir(dir):
            remove_dir(os.path.join(dir,p))
        if(os.path.exists(dir)):
            os.rmdir(dir)
    else:
        if(os.path.exists(dir)):
            os.remove(dir)



def kill(exename):
    os.system('taskkill /F /IM ' + exename)

def update(svn_path, backupdir):
    r = svn.local.LocalClient(svn_path)
    #info = r.status()
    # pprint.pprint(info)
    #from collections import namedtuple
    localchangelist = []
    for e in r.status():
        # pprint.pprint(e)
        if e.type == 9:
            localchangelist.append(e.name)
            # print(e.name)
        # print(e.type)
        # e.type

    if len(localchangelist)==0:
        return
    # move 2 backup dir
    os.chdir(svn_path)
    # backupdir =  os.path.join(svn_path , '.svnbackup')
    print("backupdir", backupdir)
    #if os.path.exists(backupdir):
    remove_dir(backupdir)
    #
    for f in localchangelist:
        if os.path.splitext(f)[1] == '.exe':
            kill(f)
    for f in localchangelist:
        # pass
        #print(os.path.split(f) )
        # print()
        dstdir = os.path.relpath(os.path.dirname(f))
        dstpathdir = os.path.join(backupdir, dstdir)
        print("dstpathdir", dstpathdir)
        if not os.path.exists(dstpathdir):
            os.makedirs(dstpathdir)

        shutil.move(f, dstpathdir)

    info = r.update()
    pprint.pprint(info)


if __name__ == '__main__':
    import sys
    # path = 'E:\\moonserver'
    # backupdir = os.path.join(sys.argv[1], sys.argv[2])
    # print(backupdir)
    print(sys.argv[1], sys.argv[2])
    update(sys.argv[1], sys.argv[2])
