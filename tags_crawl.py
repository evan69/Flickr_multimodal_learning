# get all tags of a picture
#coding:utf-8

import flickrapi
import os
import sys
import socket
import random
import time
import urllib
import threading
import time
import requests
import datetime
# import nltk

api_key = u'b28ec210280050d5d1760ff978e0404a'
api_secret = u'59131beaddb61785'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

tag_set = [['graceful',10000]]
# initial tags
downloaded_pic = 0

RATE = 0.5
THRESHOLD = 1000
TOTAL = 1000000
THREAD_NUM = 8
MAX_FILENUM = 50000

HI_DATE = datetime.datetime(2017, 6, 1)
LO_DATE = HI_DATE - datetime.timedelta(days = 30 * THREAD_NUM)
print LO_DATE

root_dir = '../data/unsupervised/'
cnt = 0

def judgeAdj(tag):
# judge whether the word is adj
    if tag.find(' ') != -1:
        return False
    text = nltk.word_tokenize(tag)
    res = nltk.pos_tag(text)
    #print res
    return res[0][1] == 'JJ'

def getTagsByPhoto(photo_id):
    global cnt
    while True:
        try:
            res = flickr.tags.getListPhoto(api_key=api_key,photo_id=photo_id)
            tags = res.get('photo').get('tags').get('tag')
            cnt += 1
            if cnt % 100 == 0:
                print 'have got tags of ' + str(cnt) + ' images'
        except Exception,ex:
            print 'error in getTagsByPhoto , now try again :',photo_id
            print Exception,':',ex
            if ex.code == 1:
                break
            continue
        break
    return tags

def crawl(dir,name):
    image_set = set()
    try:
        file_in = open(dir + 'tags_data.txt','r')
        lines = file_in.readlines()
        image_set = set([line.split(' ')[0] for line in lines])
        file_in.close()
    except Exception,ex:
        print ex
    
    file_out = open(dir + 'tags_data.txt','a')
    file_list = os.listdir(dir)
    # print file_list
    for pic in file_list:
        res = pic.split('.')
        if res[-1] != 'jpg':
            continue
        if res[0] in image_set:
            continue
        tags = getTagsByPhoto(res[0])
        if len(tags) == 0:
            continue
        file_out.write(res[0])
        for tag in tags:
            t = tag.get('raw')
            if ' ' not in t:
                # print t.decode('utf8')
                file_out.write(' ' + t)
        file_out.write(' \n')
        
    
class MyThread(threading.Thread):
    def __init__(self,id):
        super(MyThread, self).__init__()
        self.id = id
    def run(self):
        init = LO_DATE + datetime.timedelta(days = 30 * self.id)
        for i in range(30):
            dir = '../data/unsupervised/' + init.strftime("%y_%m_%d") + '/'
            crawl(dir,self.getName())
            init += datetime.timedelta(days = 1)

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    thread_list = []
    
    start = time.clock()

    for i in xrange(THREAD_NUM):
        t = MyThread(int(i))
        t.setDaemon(True)
        t.setName('thread-' + str(i))
        t.start()
        thread_list.append(t)
        
    for t in thread_list:
        while 1:
            if not t.isAlive():
                break
                
    elapsed = (time.clock() - start)
    print "Time used:",elapsed
    '''
    for i in xrange(THREAD_NUM):
        t = threading.Thread(target=crawl,args=([tag_set[j] for j in range(len(tag_set)) if j % THREAD_NUM == i],))
        t.start()
    '''
    print 'main thread end'

if __name__ == '__main__':
    main()
    