#!/usr/bin/env python3

from urllib.request import Request, urlopen, urlretrieve
import requests
from re import findall, match, search, compile, sub
import os.path
import sys
import pathlib
import argparse
from multiprocessing import Pool
import threading
import datetime
from time import time
import sqlite3

start_time = time()
abc_ = []

# https://www.xvideos.com/amateur-channels/angiecarime1
# Descargar fotos
# https://www.xvideos.com/amateurs-index/mexico

f = open('links.txt', 'r')
fl = f.readlines()
n_videos = str(len(fl))
for x in fl:
    abc_.append(x)

def ReplaceName(name):
    return sub('[^a-zA-Z0-9]', '_', name).lower()

def download_(url, filename):
    try:
        urlretrieve(url, filename)
        print('Descargado: '+filename +' '+ str(datetime.datetime.now()))
    except Exception as e:
        print('Error en url: ' + str(e))

def requestUrlInt(web):
    try:
        q = Request(web)
        q.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36')
        a = urlopen(q).read()
        a = a.decode('utf-8')
        return a
    except Exception as e:
        return 'Error con la url2 '+web + str(e)
    
def searchDownloadLink(url):
        a = requestUrlInt(url)
        m = search('html5player.setVideoUrlHigh\(\'(.*?)\'\);', a)
        title = search('<title>(.*?) - XVIDEOS.COM</title>', a)
        m = m.group(1)
        title = title.group(1)
        nombre = ReplaceName(title)+'.mp4'
        file = pathlib.Path('./videos/'+nombre)
        if file.exists():
            print('El archivo ya existe '+nombre)
        else:
            print('Iniciando descarga...'+nombre)
            download_(m, './videos/'+nombre)

def crawlerBestVideos(url,c):
    f = open('info.txt', 'a+')
    web_z = url+'/videos/best/'+str(c)
    print(web_z)
    a2 = requestUrlInt(web_z)
    matches5 = findall('<div class="thumb"><a href="/prof-video-click/([A-Za-z0-9\-\_]+)/([A-Za-z0-9\-\_]+)/([A-Za-z0-9\-\_]+)/([A-Za-z0-9\-\_]+)">', a2)
    for m5 in matches5:
        print('https://www.xvideos.com/video'+m5[2]+'/'+m5[3])
        f.write('https://www.xvideos.com/video'+m5[2]+'/'+m5[3]+'\r\n')
    matches6 = findall('<div class="thumb"><a href="/prof-video-click/([A-Za-z0-9\-\_]+)/([A-Za-z0-9\-\_]+)/([A-Za-z0-9\-\_]+)/([A-Za-z0-9\-\_]+)/([A-Za-z0-9\-\_]+)">', a2)
    for m6 in matches6:
        print('https://www.xvideos.com/video'+m6[2]+'/'+m6[4])
        f.write('https://www.xvideos.com/video'+m6[2]+'/'+m6[4]+'\r\n')
    f.close()

def DownloadVideo(url):
    if 'profiles' in url:  # profiles
        web = url+'/videos/best'
        print('PERFIL')
        a = requestUrlInt(web)
        matches_pagination = findall('">([0-9]*)</a>', a)
        print(len(matches_pagination))
        if len(matches_pagination) <= 1:
            print('Solo tiene una pagina de videos')
            crawlerBestVideos(url, 0)
        else:
            print('Tiene varias paginas de videos')
            list1 = []
            for ma in matches_pagination:
                q = int(ma[0])-1
                list1.append(q)
            clear_list = list(set(list1))
            for c in clear_list:
                    print(c)
                    crawlerBestVideos(url, c)
    else:
        searchDownloadLink(url)
    
    # try:
    #     q = Request(url)
    #     q.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
    #     a = urlopen(q).read()
    #     a = a.decode('utf-8')
    #     m = search('html5player.setVideoUrlHigh\(\'(.*?)\'\);', a)
    #     title = search('<title>(.*?) - XVIDEOS.COM</title>', a)
    #     m = m.group(1)
    #     title = title.group(1)
    #     nombre = ReplaceName(title)+'.mp4'
    #     file = pathlib.Path('./videos/'+nombre)
    #     if file.exists():
    #         print('El archivo ya existe '+nombre)
    #     else:
    #         download_(m, './videos/'+nombre)
    # except Exception as e:
    #     print('No existe url: '+url +'  '+ str(e))
        # Usar lo siguente solo si se quiere almacenar en la DB
    # try:
    #     bd = sqlite3.connect('links.db')
    #     cursor = bd.cursor()
    #     time_ = str(datetime.datetime.now())
    #     reg = ('mp4', url, title, nombre, time_, 1)
    #     cursor.execute("INSERT INTO xvideos (type_, url, name, file, date_created, status_)VALUES(?,?,?,?,?,?)", reg)
    #     bd.commit()
    # except sqlite3.OperationalError as error:
    #     print('Error al db:', error)

# ap = argparse.ArgumentParser()
# ap.add_argument('-f', '--file', required=False, help='Ingresa el nombre del archivo')
# args = vars(ap.parse_args())

# if(args['profile']):
#     profile_ = args['profile']
if __name__ == '__main__':
    p = Pool(processes=20)
    p.map(DownloadVideo, abc_)
    elapsed_time = time() - start_time
    elapsed_time_minutes = elapsed_time / 60
    print(n_videos+' videos descargados en %.2f minutos.' % elapsed_time_minutes)
