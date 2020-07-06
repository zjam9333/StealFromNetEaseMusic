#coding=utf-8
import musictool
import argparse

if __name__ == "__main__": 

    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--id", type = str, default = "2745605518") #民歌蔡琴
    userArgs = vars(parser.parse_args())
    id = userArgs["id"]
    musictool.downloadPlaylistSongs(id)