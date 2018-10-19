#coding=utf-8

import requests
import json
from Crypto.Cipher import AES
import base64

# first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"100\", csrf_token:\"\"}"
# first_param =  "{s:\"the best of me andrea\",type:10}"

iv = "0102030405060708"
nonce = "0CoJUm6Qyw8W8jud" #蜜钥？
publicKey = "010001"
modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"

def encodeParams(jsonstr):
    second_key = 16 * 'F'
    h_encText = AES_encrypt(jsonstr, nonce, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

# def AES_decrypt(text, key, iv):
#     encrypt_text = base64.b64decode(text)
#     pad = 16 - len(text) % 16
#     text = text[:-pad]
#     encryptor = AES.new(key, AES.MODE_CBC, iv)
#     encrypt_text = encryptor.decrypt(encrypt_text)
#     return encrypt_text

# def decodeParams(params):
#     second_key = 16 * 'F'
#     h_encText = AES_decrypt(params, second_key, iv)
#     h_encText = AES_decrypt(h_encText, nonce, iv)
#     return h_encText

def getJson(url, params):
    print '#####start networking'
    print url
    data = None
    if params:
        print params
        jsonStr = json.dumps(params)
        encodeP = encodeParams(jsonStr)
        data = {
            "params": encodeP,
            "encSecKey": "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        }
        print "post data:" + json.dumps(data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Referer': 'http://music.163.com/'
    }   
    response = requests.post(url, headers=headers, data=data)
    print '#####end networking'
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
    url = 'http://music.163.com/eapi/v3/playlist/detail'
    params = {
        'csrf_token':'',
        'n':100000,
        'id':playlistId,
        's':8
    }
    print params
    # url = "http://music.163.com/playlist?id=%d"%playlistId
    return getJson(url,params)

def getSongDetail(songId): #2160833
    params = {
        'c':str([{'id':str(songId)}]),
        'ids':[str(songId)],
        'csrf_token':""
    }
    url = "http://music.163.com//weapi/v3/song/detail"
    return getJson(url,params)

if __name__ == "__main__":
    # print searchAlbum('the best of me andrea')
    # print getAlbum(217758)
    # print getSong(2160833)

    # result = search("r&b classic og",1000)
    # print result
    # result = json.loads(result)
    # js = {
    #     "result":{
    #         "playlists":[
    #             {
    #                 "id":971002652,
    #                 "name":"R&B CLASSIC OG",
    #                 "coverImgUrl":"http://p1.music.126.net/ZSeCJ4A2OHy7Y8li6HzzXA==/109951163599501306.jpg",
    #                 "creator":{
    #                     "nickname":"-zjj",
    #                     "userId":73206996,
    #                     "userType":0,
    #                     "authStatus":0,
    #                     "expertTags":"",
    #                     "experts":""
    #                 },
    #                 "subscribed":False,
    #                 "trackCount":103,
    #                 "userId":73206996,
    #                 "playCount":49,
    #                 "bookCount":0,
    #                 "description":"黑人唱歌就是好听",
    #                 "highQuality":False,
    #                 "alg":"alg_playlist_basic"
    #             }
    #         ],
    #         "playlistCount":301
    #     },
    #     "code":200
    # }

    # playlists = json['result']['playlists']
    # print 'count' + str(len(playlists))
    # for pl in playlists:
    #     print pl['name']
    #     userId = pl['creator']['userId']
    #     if userId == 73206996:
    #         #is my playlist
    #         plId = pl['id']
    print getPlaylistDetail(971002652)
