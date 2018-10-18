#coding=utf-8

import requests
import json
from Crypto.Cipher import AES
import base64

# first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"100\", csrf_token:\"\"}"
# first_param =  "{s:\"the best of me andrea\",type:10}"
# second_param = "010001"
# third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"

def getParams(jsonstr):
    iv = "0102030405060708"
    first_key = "0CoJUm6Qyw8W8jud" #蜜钥？
    second_key = 16 * 'F'
    h_encText = AES_encrypt(jsonstr, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

def getJson(url, params):
    data = {
        "params": params,
        "encSecKey": "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Referer': 'http://music.163.com/'
    }   
    response = requests.post(url, headers=headers, data=data)
    return response.content

def searchAlbum(keyword):
    params = getParams("{s:\"the best of me andrea\",type:10}")
    url = "http://music.163.com/weapi/cloudsearch/get/web?csrf_token="
    return getJson(url,params)


if __name__ == "__main__":
    #test 搜索专辑
    json_text = searchAlbum("the best of me")
    print json_text
    # print json_dict['total']
    # for item in json_dict['comments']:
    #     print item['content'].encode('utf-8', 'ignore')