# 共通のインポート
import os
import pprint

# downloadFileのインポート
import time
import urllib.error
import urllib.request

# uploadFileのインポート
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def downloadFile(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
            local_file.write(web_file.read())
        return 0
    except urllib.error.URLError as e:
        return e

def uploadFile(file,folder_id):
    try:
        gauth = GoogleAuth()
        #gauth.LocalWebserverAuth()
        gauth.CommandLineAuth()
        drive = GoogleDrive(gauth)
        f = drive.CreateFile({"parents": [{"id": folder_id}]})
        f.SetContentFile(file)
        f.Upload()
        #pprint.pprint(f)
        return f['id']
    except:
        import traceback
        return traceback.print_exc()

def removeFile(file):
    try:
        os.remove(file)
        return 0
    except:
        import traceback
        return traceback.print_exc()