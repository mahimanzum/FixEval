import os
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from argparse import ArgumentParser

# 'settings.yaml' file should be in the same directory as this script
# 'settings.yaml' should contain the following:
# try locally once because the client_secrets.json file is created for local host. Then once the credentials.json is saved in a file you can upload in the remote server to run there.
'''
Some useful links
pydrive in local pc: https://www.youtube.com/watch?v=2mnKE9IERt4&t=103s
simple auth: https://pythonhosted.org/PyDrive/quickstart.html#authentication
remote auth with setting: https://pythonhosted.org/PyDrive/oauth.html
'''
"""
client_config_backend: settings
client_config:
  client_id: GET_FROM_GOOGLE_API_CONSOLE
  client_secret: GET_YOUR_OWN_CLIENT_SECRET

save_credentials: True
save_credentials_backend: file
save_credentials_file: credentials.json

get_refresh_token: True

oauth_scope:
  - https://www.googleapis.com/auth/drive.file
  - https://www.googleapis.com/auth/drive.install
"""


def authenticate():
    settings_path = 'settings.yaml'
    gauth = GoogleAuth(settings_file=settings_path)
    return GoogleDrive(gauth)


def create_folder(drive, folder_name, parent_folder_id):
    """
    Create folder on Google Drive
    """
    folder_metadata = {
        'title': folder_name,
        # Define the file type as folder
        'mimeType': 'application/vnd.google-apps.folder',
        # ID of the parent folder
        'parents': [{"kind": "drive#fileLink", "id": parent_folder_id}]
    }

    folder = drive.CreateFile(folder_metadata)
    folder.Upload()

    # Return folder information
    print('title: %s, id: %s' % (folder['title'], folder['id']))
    return folder['id']


def upload_folder(drive, folder_id, src_folder):
    """
    Upload files in the local folder to Google Drive
    """
    os.chdir(src_folder)
    # Auto-iterate through all files in the folder
    for file in os.listdir('.'):
        if os.path.isdir(file):
            print('the folder to be uploaded cannot contain a folder')
        # Check the file's size
        statinfo = os.stat(file)
        if statinfo.st_size > 0:
            print('uploading ' + file)
            # Upload file to folder
            f = drive.CreateFile({
                "parents": [{"kind": "drive#fileLink", "id": folder_id}]
            })
            f.SetContentFile(file)
            start = time.time()
            f.Upload()
            done = time.time()
            print('took {}s to upload'.format(done - start))


if __name__ == '__main__':
    #python upload_to_drive.py --source ../for_uploading --destination 1rKWODQ_bLKGeOgv2JSmFI0M-7roHIJ_8
    # this uploads all files in the folder named for_uploading
    parser = ArgumentParser(description="Upload local file/folder to Google Drive")
    parser.add_argument('-s', '--source', type=str, help='Folder path to upload')
    parser.add_argument('-d', '--destination', type=str, help='Destination Folder ID in Google Drive')
    args = parser.parse_args()



    # following requires in our servers
    # httplib2==0.15.0, google-api-python-client==1.6
    drive = authenticate()

    # Ex. destination = 1k8CsfdxtFpYYD_GEyFTvPsO3hJ9u1Hu4
    if os.path.isdir(args.source):
        folder_name = os.path.basename(args.source)
        folder_id = create_folder(drive, folder_name, args.destination)
        upload_folder(drive, folder_id, args.source)
    else:
        file = drive.CreateFile({'parents': [{'id': args.destination}]})
        file.SetContentFile(args.source)
        file.Upload()