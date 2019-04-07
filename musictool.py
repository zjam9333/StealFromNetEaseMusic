#coding=utf-8
import os
from hashlib import md5
import json
import requests
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
import neteasetool
from multiprocessing import Pool

myFilePath = "StolenMusic"

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

def downloadFile(source_url, save_path):
    if os.path.exists(save_path):
        print "file exists : " + save_path
        if save_path.endswith('.jpg'):
            return True
        if save_path.endswith('.mp3'):
            # 如何判断要不要重新下载？
            return True

    print "downloading file...to " + save_path
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Referer': 'http://music.163.com/'
    } 
    res = requests.get(source_url, stream = True, headers = headers)
    with open(save_path, 'wb') as savefile:
        for chunk in res.iter_content(chunk_size = 1024):
            savefile.write(chunk)
    
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

    pool = Pool(5)
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

def fileExisted(filepath):
    if os.path.exists(filepath):
        if filepath.endswith('.jpg'):
            return True
        if filepath.endswith('.mp3'):
            return True
    return False

def downloadSong(songdict,saveDir):
    '''
    {"data":[{"id":2979310,"url":"http://m10.music.126.net/20181101170546/a7cf5aeeb99762762be132bb804edb51/ymusic/b6f7/69aa/e638/65947efd75d12b00cb6cb3d776aefba4.mp3","br":128000,"size":4394182,"md5":"65947efd75d12b00cb6cb3d776aefba4","code":200,"expi":1200,"type":"mp3","gain":-2.0E-4,"fee":0,"uf":null,"payed":0,"flag":0,"canExtend":false,"freeTrialInfo":null}],"code":200}
    '''
    s_name = songdict['name']
    s_id = songdict['id']
    s_artist = songdict['artists'][0]['name']
    s_album = songdict['album']['name']
    s_pic_url = songdict['album']['picUrl']

    print "<title: %s, artist: %s, album: %s"%(s_name, s_artist, s_album)

    songfilename = ("%s - %s"%(s_name, s_artist)).replace("/","")
    albumfilename = ("%s - %s"%(s_album, s_artist)).replace("/","")

    mp3filepath = saveDir + songfilename + ".mp3"
    jpgfilepath = saveDir + albumfilename + ".jpg"

    if fileExisted(mp3filepath):
        print "file exist: " + mp3filepath
        return
    # don't request mp3 url if file existed, it will shut you down

    songinfo = json.loads(neteasetool.getSongUrl(s_id))
    s_mp3_url = songinfo['data'][0]['url']
    # s_mp3_md5 = songinfo['data'][0]['md5']
    # s_mp3_size = songinfo['data'][0]['size']
    # print songdict

    downloadedmp3 = downloadFile(s_mp3_url,mp3filepath)
    if downloadedmp3:
        downloadedjpg = downloadFile(s_pic_url,jpgfilepath)
        if downloadedjpg:
            setSongInfo(mp3filepath, s_name, s_artist, s_album, jpgfilepath)

if __name__ == "__main__":

    downloadPlaylistSongs(971002652) #rnb