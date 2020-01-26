from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

f = drive.CreateFile({'title': 'test.jpg', 'mimeType': 'image/jpeg'})
f.SetContentFile('http://concafenavi.com/wp-content/uploads/2019/12/コスプレBAR-G.jpg')
f.Upload()