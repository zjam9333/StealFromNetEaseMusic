#coding=utf-8
import requests
import json
import paramtool

def getJson(url, params):
    print url
    data = None
    if params:
        print params
        data = paramtool.encodedict(params)
        # print "post data:" + json.dumps(data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Referer': 'http://music.163.com/'
    }   
    response = requests.post(url, headers=headers, data=data)
    return response.content

def search(keyword,type):
    params = {
        # '''
        #     搜索类型；默认为 1 即单曲 , 取值意义 : 
        #     1: 单曲, 
        #     10: 专辑, 
        #     100: 歌手, 
        #     1000: 歌单, 
        #     1002: 用户, 
        #     1004: MV, 
        #     1006: 歌词, 
        #     1009: 电台, 
        #     1014: 视频
        # '''
        's':keyword,
        'type':type, 
        'offset':0
        # 'limit':100,
    }
    url = "http://music.163.com/weapi/search/get?csrf_token="
    return getJson(url,params)

def getAlbum(albumId): #217758
    url = "http://music.163.com/weapi/v1/album/" + str(albumId)
    params = {
        'csrf_token': ""
    }
    return getJson(url,params)

def getPlaylistDetail(playlistId): #971002652
    # url = 'http://music.163.com/eapi/v3/playlist/detail'
    # params = {
    #     'csrf_token':'',
    #     'n':100000,
    #     'id':playlistId,
    #     's':8
    # }
    # print params
    params = None
    url = "https://music.163.com/api/playlist/detail?id=%d"%playlistId
    return getJson(url,params)

def getSongDetail(songId): #2160833
    params = {
        'c':str([{'id':str(songId)}]),
        'ids':[str(songId)],
        'csrf_token':""
    }
    url = "http://music.163.com/weapi/v3/song/detail"
    return getJson(url,params)

def getSongUrl(songId):
    # params = None
    # url = "http://music.163.com/song/media/outer/url?id=%d.mp3"%songId
    # return url

    url = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="
    params = {
        'ids':[songId],
        'br':128000,
        'csrf_token':''
    }
    result = getJson(url,params)
    print result
    result = json.loads(result)
    mp3url = result['data'][0]['url']
    return mp3url
    # return getJson(url,params)

def encryptedSongId(id): #dfsId是很长的id，目前已消失
    byte1 = bytearray('3go8&$8*3*3h0k(2)2')
    byte2 = bytearray(id)
    byte1_len = len(byte1)
    for i in xrange(len(byte2)):
        byte2[i] = byte2[i]^byte1[i%byte1_len]
    m = md5.new()
    m.update(byte2)
    result = m.digest().encode('base64')[:-1]
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result

