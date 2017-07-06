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
    global downloaded_pic
    try:
        pic = requests.get(URL, timeout=10)
        fp = open(dest_dir,'wb')
        fp.write(pic.content)
        fp.close()
        downloaded_pic += 1
        if downloaded_pic % 100 == 0:
            print str(downloaded_pic) + ' images have been downloaded'
    except Exception,ex:
        print 'error in download pic'
        print ex
    return

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
            photos = flickr.photos.search(api_key=api_key, extras='url_z', tags = tag_name, page = page, sort = 'interestingness-desc')
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
                    # print myurl + ' ' + myid + ' ' + name
                    # print getTagsByPhoto(myid)
                    dest = dir + myid + '.jpg'
                    if str(myid + '.jpg') in os.listdir(dir):
                        continue
                    downLoadPicFromURL(dest, myurl)
                except Exception:
                    print 'error in url'

def date2timestamp(date):
    return int(time.mktime(date.timetuple()))

def unsupervisedDownload(id):
    min_time = LO_DATE + datetime.timedelta(days = id * 30)
    max_time = min_time + datetime.timedelta(days = 1)
    for day in range(30):
        dir = '../data/unsupervised/' + min_time.strftime("%y_%m_%d") + '/'
        try:
            os.makedirs(dir)
        except Exception,ex:
            pass
        for page in range(1,100):
            photos = flickr.photos.search(api_key=api_key, extras='url_z', sort = 'interestingness-desc',
                min_upload_date=date2timestamp(min_time), max_upload_date=date2timestamp(max_time), per_page=100, page=page)

            for ph in photos['photos']['photo']:
                if ph.get('url_z') == None:
                    continue
                # print os.listdir(dir)
                if str(ph.get('id') + '.jpg') in os.listdir(dir):
                    continue
                downLoadPicFromURL(dir + ph.get('id') + '.jpg',ph.get('url_z'))

        min_time += timedelta(days = 1)
        max_time += timedelta(days = 1)
                   
class MyThread(threading.Thread):
    def __init__(self,flag,arg,id):
        super(MyThread, self).__init__()
        self.flag = flag
        self.arg = arg
        self.id = id
    def run(self):
        if self.flag:
        # supervised
            crawl(self.arg,self.getName())
        else:
        # unsupervised
            unsupervisedDownload(self.id)

def main():
    
    readInInitSet()
    reload(sys)
    sys.setdefaultencoding('utf-8')

    thread_list = []
    if sys.argv[1] == '-s':
        flag = True
    else:
        if sys.argv[1] == '-u':
            flag = False
        else:
            print 'error in parameters'
            return
    
    start = time.clock()

    for i in xrange(THREAD_NUM):
        t = MyThread(flag,[tag_set[j] for j in range(len(tag_set)) if j % THREAD_NUM == i],i)
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
    