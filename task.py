from psutil import process_iter 
from glob import glob 
from os import path, popen

def taskkill(dirpath:str):
    allprocess = set()

    for p in process_iter():
        #print(p.name())
        allprocess.add(p.name())

    for file_path in glob(dirpath +'\\*.exe'):
        #print(filename)
        (filepath, tempfilename) = path.split(file_path)
        #(filename,extension) = os.path.splitext(tempfilename)
        if(tempfilename in allprocess):
            #print("kill " + tempfilename)
            b = popen("taskkill /f /im " + tempfilename)
            print(b.read())


if __name__ == '__main__':
    taskkill("E:\\MoonServer_Final")