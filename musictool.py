#coding=utf-8
import os
from hashlib import md5
import json
import requests
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
import neteasetool
from multiprocessing import Pool

myFilePath = "savedFiles"

def setSongInfo(songfilepath, songtitle, songartist, songalbum, songpicpath):
    audio = ID3(songfilepath)
    audio.update_to_v23()
    audio['TIT2'] = TIT2(
                    encoding=3,
                    text=[songtitle]
                )
    audio['TPE1'] = TPE1(
                    encoding=3,
                    text=[songartist]
                )
    audio['TALB'] = TALB(
                    encoding=3,
                    text=[songalbum]
                )
    with open(songpicpath,'r') as img:
        audio['APIC'] = APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3, 
                        desc=u'Cover',
                        data=img.read()
                    )
    audio.save()

def downloadFile(source_url, save_path, file_size = None, md5_value = None, retry_time = None):
    if os.path.exists(save_path):
        print "file exists : " + save_path
        if file_size:
            old_size = os.path.getsize(save_path)
            print "old size: %d, new size: %d"%(old_size,file_size)
            if old_size < file_size: #check size
                print "file should download again : " + save_path
                os.remove(save_path)
            else:
                return True
        else:
            return True

    print "downloading file...to " + save_path
    
    res = requests.get(source_url, stream = True)
    with open(save_path, 'wb') as savefile:
        for chunk in res.iter_content(chunk_size = 128):
            savefile.write(chunk)

    #check md5
    if md5_value:
        with open(save_path,'r') as downloadedfile:
            old_md5 = str(md5(downloadedfile.read()).hexdigest()).lower()
            if old_md5 != md5_value:
                print "delete file: " + save_path
                os.remove(save_path)
                if retry_time:
                    if retry_time < 5:
                        return downloadFile(source_url, save_path, file_size = file_size, md5_value = md5_value, retry_time = retry_time + 1)
                return False
    print "download completed: " + save_path
    return True

def downloadPlaylistSongs(playlistid):

    #download mp3 in playlist
    myplaylist = neteasetool.getPlaylistDetail(playlistid)
    myplaylist = json.loads(myplaylist)
    tracks = myplaylist['result']['tracks']
    print "song count: " + str(len(tracks))
    playlistname = myplaylist['result']['name']
    print "playlist name: " + playlistname

    #create dir if need
    saveDir = myFilePath + "/" + playlistname + "/"
    if not os.path.exists(myFilePath):
        os.mkdir(myFilePath)
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)

    pool = Pool(10)
    for song in tracks:
        pool.apply_async(func=downloadSong, args=(song, saveDir,))
        # downloadSong(song,saveDir)
    pool.close()
    pool.join()

    # delete old jpg files
    filenamelist = os.listdir(saveDir)
    print "clear up..."
    for filename in filenamelist:
        filepathtodelete = saveDir + filename
        if os.path.isfile(filepathtodelete):
            if filename.endswith('.jpg'):
                os.remove(filepathtodelete)
    print "finish"
    return

def downloadSong(songdict,saveDir):
    '''
    {"data":[{"id":2979310,"url":"http://m10.music.126.net/20181101170546/a7cf5aeeb99762762be132bb804edb51/ymusic/b6f7/69aa/e638/65947efd75d12b00cb6cb3d776aefba4.mp3","br":128000,"size":4394182,"md5":"65947efd75d12b00cb6cb3d776aefba4","code":200,"expi":1200,"type":"mp3","gain":-2.0E-4,"fee":0,"uf":null,"payed":0,"flag":0,"canExtend":false,"freeTrialInfo":null}],"code":200}
    '''
    s_name = songdict['name']
    s_id = songdict['id']
    s_artist = songdict['artists'][0]['name']
    s_album = songdict['album']['name']
    s_pic_url = songdict['album']['picUrl']

    songinfo = json.loads(neteasetool.getSongUrl(s_id))
    s_mp3_url = songinfo['data'][0]['url']
    s_mp3_md5 = songinfo['data'][0]['md5']
    s_mp3_size = songinfo['data'][0]['size']

    print "<song: name: %s, artist: %s, album: %s"%(s_name, s_artist, s_album)

    songfilename = ("%s - %s"%(s_name, s_artist)).replace("/","")
    albumfilename = ("%s - %s"%(s_album, s_artist)).replace("/","")

    mp3filepath = saveDir + songfilename + ".mp3"
    jpgfilepath = saveDir + albumfilename + ".jpg"

    downloadedmp3 = downloadFile(s_mp3_url,mp3filepath,file_size=s_mp3_size,md5_value=s_mp3_md5)
    if downloadedmp3:
        downloadedjpg = downloadFile(s_pic_url,jpgfilepath)
        if downloadedjpg:
            setSongInfo(mp3filepath, s_name, s_artist, s_album, jpgfilepath)

if __name__ == "__main__":

    downloadPlaylistSongs(971002652) #rnb