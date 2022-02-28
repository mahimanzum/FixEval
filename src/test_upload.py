from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
settings_path = 'settings.yaml'
gauth = GoogleAuth(settings_file=settings_path)

drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Hello.txt'})

file1.SetContentString('wtf') 

file1.Upload()
