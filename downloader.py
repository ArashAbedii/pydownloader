import math
import operator
import os
import random
import threading
import urllib
from logging import exception
from urllib.parse import urlparse

import requests
import simplejson


def download(url, filename="test.txt", headers=None, result="", part=1):
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
        }
    # print('downloading part'+str(part)+ '...')
    page = requests.get(url, headers=headers)
    content = page.content

    with open(filename, "wb") as file:
        file.write(content)

    fileInfo = {"part": part, "file_name": filename}
    result.append(fileInfo)

    # print('part '+str(part)+ ' downloaded')


def string_generator():
    string = "abcdefghijklmnopqrstuwwxyz"
    listy = list(string)
    random.shuffle(listy)
    return "".join(listy)


def downloader(url, count_workers, filename="", extension=""):

    # send request
    response = requests.get(
        url=url,
        stream=True,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
        },
    )

    # get filename
    readableurl = urlparse(url=url)

    if filename == "":
        filename = urllib.parse.unquote(os.path.basename(readableurl.path))

    if extension == "":
        extension = os.path.splitext(filename)[1]
    else:
        filename = filename + extension

    content_length = response.headers["Content-Length"]

    chunk_len = math.floor(int(content_length) / count_workers)
    final_chunk = int(content_length) % count_workers

    parts = 0
    start = 0
    results = []
    workers = []

    while count_workers > 0:
        parts += 1

        if count_workers == 0 and final_chunk > 0:
            end = start + final_chunk
        else:
            end = start + chunk_len

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
            "Range": f"bytes={start}-{end}",
        }
        chunkName = f"{string_generator()}-part{parts}.{extension}"

        worker = threading.Thread(
            target=download, args=(url, chunkName, headers, results, parts)
        )

        workers.append(worker)
        worker.start()
        start += chunk_len + 1

        count_workers -= 1

    for workerTrade in workers:
        workerTrade.join()

    newlist = sorted(results, key=operator.itemgetter("part"))

    orgFile = open(filename, "ab+")

    for chunk in newlist:

        partial = open(chunk["file_name"], "rb")
        partialContent = partial.read()
        orgFile.write(partialContent)
        partial.close
        os.unlink(chunk["file_name"])

    orgFile.close

    response = {"file_name": filename}

    return simplejson.dumps(response)
