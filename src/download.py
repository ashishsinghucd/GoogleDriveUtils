import io
import os
import pickle
import sys
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/drive']


creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('drive', 'v3', credentials=creds)


# https://drive.google.com/open?id=1wjhVa57wSWADY3IHKa8upSbWwaiyuRhv

file_id = '1wjhVa57wSWADY3IHKa8upSbWwaiyuRhv'  # '19EQCNp43d-UAvDj4mftwfvjkAWV5s9Cb'
request = service.files().get_media(fileId=file_id)
fh = io.FileIO("sample.html", mode='wb')  #io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%." % int(status.progress() * 100))