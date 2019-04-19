
from __future__ import print_function
import os.path, io, os
import mimetypes

# os.chdir(os.path.dirname(__file__))
import sys
sys.path.append('Cloud/cloud_handler/GoogleNetworking')


from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient import errors

from google_drive_handler import GoogleDriveHandler

drive_handler= GoogleDriveHandler(sys.argv)
drive_service = drive_handler.drive_service

from functools import partial
from threading import Thread

# Note the chunksize restrictions given in
# https://developers.google.com/api-client-library/python/guide/media_upload

#upload('file1.jpg', 'file1.jpg', 'image/jpeg')
#download('19_naVrwu6f1xgHfgB54qo_IL5eU_xk1_', 'cake.jpg')


class Uploader:

    def __init__(self,filepath):
        self.filename = os.path.basename(filepath)
        self.filepath = filepath
        self.mimetype = self.get_mime(self.filename)

    def get_mime(self, fileName):
        try:
            mime = mimetypes.guess_type(fileName)[0]
            if mime is None:
                return ""
            return mime
        except TypeError:
            return ""
        return ""


    def upload(self):
        metadata = {'name': self.filepath}

        media = MediaFileUpload(self.filepath,
                                mimetype=self.mimetype,
                                resumable=True)

        file = drive_service.files().insert(body=metadata, media_body=media, fields='id')
        response = None
        while response is None:
            status, response = file.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))

        print('File ID: %s' % file.get('id'))


class Downloader:

    def __init__(self, file_id, filepath, progress_bar, screen_manager,callback):
        self.filepath = filepath
        self.progress_bar = progress_bar
        self.done = False
        self.pause = False
        self.callback = callback


    def start(self):
        request = drive_service.files().get_media(fileId=file_id)
        self.fh = io.BytesIO()
        self.downloader = MediaIoBaseDownload(self.fh, request)
        screen_manager.current = 'downloading'
        Clock.schedule_once(self.start_download, 0)
        # self.thread = Thread(target=partial(self.start_download, self.progress_bar,0))
        # self.thread.start()

    def start_download(self, dt):
        status, self.done = self.downloader.next_chunk()
        self.progress_bar.value = int(status.progress() * 100)

        if not self.done or not self.pause:
            Clock.schedule_once(self.start_download, 0)
        elif self.done:
            with io.open(self.filepath, 'wb') as f:
                self.fh.seek(0)
                f.write(self.fh.read())
            self.callback(filepath)
                
    def pause(self):
        self.pause = True

    def countinue(self):
        self.pause = False
        Clock.schedule_once(self.start_download, 0)


def delete_file(file_id):
    """Permanently delete a file, skipping the trash.
    Args:
        service: Drive API service instance.
        file_id: ID of the file to delete. """

    try:
        drive_service.files().delete(fileId=file_id).execute()
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

    all_files = get_list(20)

    for file in all_files:
        delete_file(file)


def get_list(size):

    # Call the Drive v3 API
    results = drive_service.files().list().execute()
    items = results['items']
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
#            print(u'File Name: {0} id:({1})'.format(item['name'], item['id']))
	     pass

    return [item['id'] for item in items]

def download():
	request = drive_service.files().get_media(fileId='1ReivvY9kRhq03abDGikrVfToEGfokjZF')
	fh = io.BytesIO()
	downloader = MediaIoBaseDownload(fh, request)
	status, done = downloader.next_chunk()
	while not done:
		status, done = downloader.next_chunk()
		print(int(status.progress() * 100))

	with io.open('cake123.jpg', 'wb') as f:
		fh.seek(0)
		f.write(fh.read())


#get_list(10)
#delete_file('0B2uEo0v6hpDcc3RhcnRlcl9maWxl')

#Uploader('cake.jpg', 'cake.jpg', 'image/jpeg')

