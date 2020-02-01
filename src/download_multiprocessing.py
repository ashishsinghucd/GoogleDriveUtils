import io
import os
import pickle
import sys

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from multiprocessing import Pool
import pandas as pd
SCOPES = ['https://www.googleapis.com/auth/drive']


def load_creds(token_path):
    creds = None
    try:
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
    except Exception as e:
        print("Error loading the credentials: ", str(e))
    return creds


def create_drive_service(token_path, product='drive', version='v3'):
    service = None
    try:
        creds = load_creds(token_path)
        service = build(product, version, credentials=creds)
    except Exception as e:
        print("Error creating the service: {}, error: {}".format(product, str(e)))
    return service


def download_file(name, file_id, token_path):
    service = create_drive_service(token_path)
    # output_path, name, file_id = url[0], url[1][0], url[1][1]
    try:
        print("Downloading the file: {} id: {}".format(name, file_id))
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(output_path + "/" + name, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
    except Exception as e:
        print("Error downloading the name: {} error: {}".format(name, str(e)))


if __name__ == "__main__":
    file_id_path = sys.argv[1]
    output_path = sys.argv[2]
    token_path = sys.argv[3]
    try:
        no_of_process = sys.argv[4]
    except IndexError:
        no_of_process = 2
    file_id_df = pd.read_csv(file_id_path)
    token_path_list = [token_path] * file_id_df.shape[0]

    download_args = list(zip(file_id_df.VideoName, file_id_df.ID, token_path_list))

    pool = Pool(2)
    pool.starmap(download_file, download_args)
