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

api_key = u'b28ec210280050d5d1760ff978e0404a'
api_secret = u'59131beaddb61785'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

tag_set = [['graceful',10000]]
# initial tags

RATE = 0.5
THRESHOLD = 1000
TOTAL = 1000000
THREAD_NUM = 8

def readInInitSet():
    global tag_set
    tag_set = []
    total_photo = 0
    init_tag = open('filtered_tags.txt','r')
    lines = init_tag.readlines()
    for line in lines:
        line = line.split(' ')
        total_photo += int(line[1])
        tag_set.append((line[0],int(line[1])))
    RATE = 1.0 * total_photo / TOTAL
    print 'rate:',RATE
        

def downLoadPicFromURL(dest_dir,URL): 
    try:
        urllib.urlretrieve(URL,dest_dir)
    except Exception,ex:
        print '\tError retrieving the URL:',dest_dir
        print ex
        
def getTagsByPhoto(photo_id):
    try:
        res = flickr.tags.getListPhoto(api_key=api_key,photo_id=photo_id)
        tags = res.get('photo').get('tags').get('tag')
    except Exception,ex:
        print 'error in getTagsByPhoto'
        print Exception,':',ex
        
    return tags

def getPhotosByTag(tag_name, photo_num_per_tag):
    page = 1
    left = photo_num_per_tag - (page - 1) * 100
    while left > 0:
        try:
            photos = flickr.photos.search(extras='url_z', tags = tag_name, page = page)
            photos = photos['photos']['photo']
            # print photos
            if left < 100:
                photos = photos[0:left]
            #print photos
            yield photos
            page += 1
            left = photo_num_per_tag - (page - 1) * 100
        except Exception,ex:
            print 'error in getPhotosByTag'
            print ex
            
def calPhotoNum(origin_num):
    if origin_num <= 0:
        return 0
    return int(min(max(RATE * origin_num, THRESHOLD),origin_num))
        
def crawl(tag_set,name):
    for tag_entry in tag_set:
        tag = tag_entry[0]
        dir = '../data/' + tag + '/'
        try:
            os.makedirs(dir)
        except Exception,ex:
            pass
            # print ex
        
        print tag + ' ' + str(calPhotoNum(tag_entry[1])) + ' ' + str(len(os.listdir(dir)))
        ret = getPhotosByTag(tag, calPhotoNum(tag_entry[1]) - len(os.listdir(dir)))
        #print ret
        for photo_list in ret:
            for photo in photo_list:
                try:
                    myurl = photo.get('url_z')
                    myid = photo.get('id')
                    print myurl + ' ' + myid + ' ' + name
                    # print getTagsByPhoto(myid)
                    dest = dir + myid + '.jpg'
                    downLoadPicFromURL(dest, myurl)
                except Exception:
                    print 'error in url'
                   
class MyThread(threading.Thread):
    def __init__(self,arg):
        super(MyThread, self).__init__()
        self.arg = arg
    def run(self):
        crawl(self.arg,self.getName())
                
def main():
    
    readInInitSet()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    start = time.clock()
    thread_list = []
    
    start = time.clock()
    
    for i in xrange(THREAD_NUM):
        t = MyThread([tag_set[j] for j in range(len(tag_set)) if j % THREAD_NUM == i])
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
    