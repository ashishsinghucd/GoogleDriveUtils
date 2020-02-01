import io
import os
import pickle
from googleapiclient.discovery import build
import pandas as pd

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

page_token = None
service = build('drive', 'v3', credentials=creds)
file_id_list = []
while True:
    response = service.files().list(q="mimeType='video/mp4'", spaces='drive', fields='nextPageToken, files(id, name)',
                                    pageToken=page_token).execute()
    for file in response.get('files', []):
        # Process change
        file_id_list.append({"VideoName": file.get('name'), "ID": file.get('id')})
        print('Found file: %s (%s) ' % (file.get('name'), file.get('id')))
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break

files_id_df = pd.DataFrame(file_id_list)
files_id_df.to_csv("./files_id.csv", index=False)
