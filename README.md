# GoogleDriveUtils

The purpose of this repo is to provide simple funtionalities to work with google drive using python. Currently it supports
the follwing functions:

1. Download the files from the google drive
2. Search the files in the google drive

The code uses multiprocessing as of now to make the download faster. We plan to use it multithreading in the future version of 
the code since it is an I/O operation.

download_multiprocessing.py -> For downloading the files
search.py -> For searching the files using the specified MIME type
