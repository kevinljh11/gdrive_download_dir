#!/usr/bin/env python3

import sys
import json
import requests

GDRIVE_MAGIC_KEY = 'AIzaSyC1qbk75NzWBvSaDh6KnsjjA9pIrP4lYIE'
GDRIVE_HOST = 'https://clients6.google.com'

def get_filelist(folder_id):
    files = dict()
    next_page_token = ''
    while True:
        url = GDRIVE_HOST + '/drive/v2beta/files?' + \
              '&q=\'' + folder_id + '\' in parents' + \
              '&fields=items(mimeType,title,id),nextPageToken' + \
              '&maxResults=50' + \
              '&key=' + GDRIVE_MAGIC_KEY
        if next_page_token != '':
            url += '&pageToken=' + next_page_token
        resp = requests.get(url, headers={'referer': 'https://drive.google.com/drive/folders/' + \
                                                     sys.argv[1]})
        res = json.loads(resp.content.decode('utf8').replace('\'', '"'))
        for item in res['items']:
            files[item['id']] = item['title']
        if 'nextPageToken' in res.keys():
            next_page_token = res['nextPageToken']
        else:
            break # got all filenames and id's
    return files


def download_file(file_id, filename):
    print('Try to download ' + filename + ' from ' + file_id)
    resp = requests.get('https://docs.google.com/uc?id=' + file_id)
    file_jpeg = open(filename, 'wb+')
    file_jpeg.write(resp.content)
    file_jpeg.close()

def main():
    print('Try to download files from folder id = ' + sys.argv[1])
    files = get_filelist(sys.argv[1])
    print('Start downloading ' + str(len(files)) + ' files')
    exit(0)

    for file_id, filename in files.items():
        download_file(file_id, filename)
    print('Done')


if __name__ == '__main__':
    main()
