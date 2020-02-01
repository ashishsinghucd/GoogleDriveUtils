import io
import os
import pickle
import sys
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import threading
from multiprocessing.pool import ThreadPool
import pandas as pd
from queue import Queue
SCOPES = ['https://www.googleapis.com/auth/drive']


creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

service = build('drive', 'v3', credentials=creds)
files_id_df = pd.read_csv("./files_id.csv")

output_path = "./Videos"


def download_file(name, file_id):
    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(output_path + "/" + name, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
    except Exception as e:
        print(str(e))


q = Queue(maxsize=0)
num_theads = 10
urls = list(zip(files_id_df.VideoName, files_id_df.ID))
results = [{} for x in urls]

for i in range(len(urls)):
    q.put((urls[0], urls[1]))

# urls = list(zip(files_id_df.VideoName, files_id_df.ID))
threads = [threading.Thread(target=download_file, args=(name, file_id,)) for name, file_id
           in z]


for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

