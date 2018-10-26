#coding=utf-8
import os
import json
import requests
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
import neteasetool

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

def downloadFile(source_url, save_path):
    if os.path.exists(save_path):
        print "file exists, skipped : " + save_path
        return False

    print "downloading file...to " + save_path
    
    res = requests.get(source_url)
    with open(save_path, 'wb') as savefile:
        for chunk in res.iter_content(chunk_size=128):
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

    for song in tracks:
        downloadSong(song,saveDir)

    # delete old jpg files
    filenamelist = os.listdir(saveDir)
    for filename in filenamelist:
        filepathtodelete = saveDir + filename
        if os.path.isfile(filepathtodelete):
            if filename.endswith('.jpg'):
                print "delete jpg: " + filepathtodelete
                os.remove(filepathtodelete)
    return

def downloadSong(songdict,saveDir):
    s_name = songdict['name']
    s_id = songdict['id']
    s_artist = songdict['artists'][0]['name']
    s_album = songdict['album']['name']
    s_pic_url = songdict['album']['picUrl']
    s_mp3_url = neteasetool.getSongUrl(s_id)

    print "<song: name: %s, artist: %s, album: %s pic: %s"%(s_name, s_artist, s_album, s_pic_url)

    songfilename = ("%s - %s"%(s_name, s_artist)).replace("/","")
    albumfilename = ("%s - %s"%(s_album, s_artist)).replace("/","")

    mp3filepath = saveDir + songfilename + ".mp3"
    jpgfilepath = saveDir + albumfilename + ".jpg"

    downloadFile(s_mp3_url,mp3filepath)
    downloadFile(s_pic_url,jpgfilepath)
    setSongInfo(mp3filepath, s_name, s_artist, s_album, jpgfilepath)