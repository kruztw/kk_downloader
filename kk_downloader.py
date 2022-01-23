# -*- coding: utf-8 -*-

from pytube import YouTube
from moviepy.editor import *
from threading import Thread, Lock

import time
import sys
import os
import re
import requests



MAX_THREAD_NUM = 1


OK = []
OK_lock = Lock()
special_chars = {'&lt;': '<', '&gt;': '>', "'": ""}


class Minion(Thread):
    cur_dir = os.getcwd() + "/"
    output_dir = cur_dir + "output/"

    def __init__(self, song):
        Thread.__init__(self)
        self.song = song

    
    def run(self)-> None:
        try:
            url = "https://www.youtube.com/results?search_query=" + self.song
            req = requests.get(url)
        
            video_url = self.getVideoUrl(req.text)
    
            if video_url == "":
                print(f"{self.song} not found")
                return
        
            print(f"{self.song} found")
            self.downloadSongs(video_url)
    
            OK_lock.acquire()
            OK.append(self.song)
            OK_lock.release()

        except Exception as e:
            #print(f"error: {e}")
            pass

        finally:
            try:
                OK_lock.release()
            except:
                pass

    
    
    def getVideoUrl(self, html: str) -> str:
        p = re.compile('watch\?v=[^"]*')
        results = p.findall(html)
    
        url = ""
        for res in results:
            url = 'https://www.youtube.com/' + res
            if self.song in requests.get(url).text:
                break
    
        return url
    
    
    def downloadSongs(self, url: str) -> None:
        file_name = YouTube(url).streams.first().download()
        self.video2mp3(file_name)
    

    def video2mp3(self, file_name: str) -> None:
        output_name = f'{self.output_dir}{self.song}.mp3'

        video = VideoFileClip(file_name)
        video.audio.write_audiofile(output_name)

        os.remove(file_name)
    

def usage():
    print(f'usage: ./kk_downloader.py <kbl_file>')


def parseSongs(inp_file: str) -> list:
    songs = []
    p = re.compile('[ ]*<song_name>(.*)</song_name>[ ]*')

    with open(inp_file, 'r') as f:
        while True:
            line = f.readline()

            if not line:
                break

            res = p.match(line)
            if res:
                song = res.group(1)
                for k,v in special_chars.items():
                    song.replace(k, v)
                    
                songs.append(song)

    return songs


def writeLog(songs: list) -> None:
    with open("OK", 'w') as _OK:
        with open("NOT_OK", 'w') as not_OK:
            for song in songs:
                if song in OK:
                    _OK.write(song + "\n")
                else:
                    not_OK.write(song + "\n")


def main():
    # TODO: argparse
    if len(sys.argv) < 2:
        usage()
        return
    
    with open('OK', 'r') as f:
        OK_songs = f.readlines()

    kbl = sys.argv[1]
    songs = parseSongs(kbl)

    try:
        threads = []
        for i in range(len(songs)):
            if songs[i] in OK_songs:
                continue
    
            threads.append(Minion(songs[i]))
            threads[-1].start()
    
            while len(threads) == MAX_THREAD_NUM or (i == len(songs)-1 and len(threads)):
                for thread in threads:
                    if not thread.isAlive():
                        threads.remove(thread)
    
                time.sleep(1)

    except Exception as e:
        print(f"error: {e}")

    finally:
        writeLog(songs)


if __name__ == '__main__':
    main()
