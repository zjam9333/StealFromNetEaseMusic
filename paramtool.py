#coding=utf-8
from Crypto.Cipher import AES
import base64
import json

iv = "0102030405060708"
nonce = "0CoJUm6Qyw8W8jud" #蜜钥？
publicKey = "010001"
modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"

def _encodeParams(jsonstr):
    second_key = 16 * 'F'
    h_encText = _AES_encrypt(jsonstr, nonce, iv)
    h_encText = _AES_encrypt(h_encText, second_key, iv)
    return h_encText

def _AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

def encodedict(params):
    jsonStr = json.dumps(params)
    encodeP = _encodeParams(jsonStr)
    data = {
        "params": encodeP,
        "encSecKey": "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    }
    return data