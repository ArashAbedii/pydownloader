import downloader

#download from direct link (fill file name with headers)
print(downloader.downloader("https://static.videezy.com/system/resources/previews/000/033/826/original/pattaya-aerial-view30.mp4",8))

#download from direct link (custom file name)
print(downloader.downloader("https://static.videezy.com/system/resources/previews/000/033/826/original/pattaya-aerial-view30.mp4",8,'my-video','.mp4'))
