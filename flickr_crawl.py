#coding:utf-8

import flickrapi
import os
import sys
import socket
import inspect
import nltk
import random
import time

api_key = u'b28ec210280050d5d1760ff978e0404a'
api_secret = u'59131beaddb61785'
#flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

tag_set = ['graceful']
# initial tags
tag_set = set(tag_set)
photo_set = set()
# initial photos visited

file_out = open('tags.txt','w')

def readInInitSet():
    global tag_set
    tag_set = set()
    init_tag = open('originTags.txt','r')
    lines = init_tag.readlines()
    for line in lines:
        tag_set.add(line)

def writeToFile(tag):
    global file_out
    file_out.write(tag)
    file_out.write('\n')

def judgeAdj(tag):
# judge whether the word is adj
    if tag.find(' ') != -1:
        return False
    text = nltk.word_tokenize(tag)
    res = nltk.pos_tag(text)
    #print res
    return res[0][1] == 'JJ'

def getPhotosByTag(tag_name, photo_num_per_tag):
    try:
        photos = flickr.photos.search(extras='url_z', tags = tag_name, per_page = photo_num_per_tag)
        photos = photos['photos']['photo']
    except Exception:
        print 'error in getPhotosByTag'
        
    return photos
        
def getTagsByPhoto(photo_id):
    try:
        res = flickr.tags.getListPhoto(api_key=api_key,photo_id=photo_id)
        tags = res.get('photo').get('tags').get('tag')
    except Exception,ex:
        print 'error in getTagsByPhoto'
        print Exception,':',ex
        
    return tags
        
def run(max_depth, photo_num_per_tag):
    global tag_set, file_out
    ret_set = set()
    ret_set.update(tag_set)
    cnt = 0
    last_len = 0
    while(cnt < max_depth):
        new_tag_set = set()
        for tag in tag_set:
            try:
                photos = getPhotosByTag(tag, photo_num_per_tag)
                # get photos of a tag
                # rand_list = random.sample(range(0, len(photos)), int(rate * len(photos) + 1))
                # photos = [photos[i] for i in rand_list]
                # choose photos randomly at given rate
                for photo in photos:
                    try:
                        myurl = photo.get('url_z')
                        # photo url
                        photo_id = photo.get('id')
                        if photo_id in photo_set:
                        # check if the photo is visited
                            continue
                        if myurl == None or photo_id == None:
                            continue
                        photo_set.add(photo_id)
                        # add photo id to set
                        # print myurl,photo_id
                        tags_of_photo = getTagsByPhoto(photo_id)
                        # get all tags of a photo

                        tmp_tag_set = set()

                        for tag in tags_of_photo: # traverse all tags of a photo
                            try:
                                tag_name = tag.get('raw')
                                if not tag_name.isalpha():
                                    continue
                                # ignore non-English words
                                is_adj = judgeAdj(tag_name)
                                # judge if is adj
                                if is_adj:
                                    tag_name = tag_name.lower()
                                    if tag_name in ret_set:
                                        continue
                                    # ignore visited tags
                                    tmp_tag_set.add(tag_name)
                                # transfer to lower format and add to set
                                # print 'add tag:',tag_name,is_adj
                            except Exception,ex:
                                print 'error when process a tag of a photo'
                                print Exception,':',ex

                        map(writeToFile, tmp_tag_set)
                        # print tmp tag in this scan
                        file_out.close()
                        file_out = open('tags.txt','a')
                        new_tag_set.update(tmp_tag_set)
                        # add to next loop tag scan set
                        ret_set.update(tmp_tag_set)
                        # add to total tag set

                    except Exception,ex:
                        print 'error when process a photo'
                        print Exception,':',ex

                    cur_len = len(ret_set)
                    if cur_len > last_len:
                        print "current tags num :", cur_len
                        last_len = cur_len

            except Exception,ex:
                print 'error when process a tag in tag_set'
                print Exception,':',ex
        
        tag_set = new_tag_set
        print 'End loop ' + str(cnt) + ' of tag scanning'
        cnt += 1
    print 'total tag num:',len(ret_set)
    file_out.close()
    return ret_set
        
def main():
    readInInitSet()
    reload(sys)
    #print sys.getdefaultencoding()
    sys.setdefaultencoding('utf-8')
    #print sys.getdefaultencoding()
    start = time.clock()
    print run(100,100)
    elapsed = (time.clock() - start)
    print "Time used:",elapsed
    #getPhotosByTag("black-and-white")
    #getTagsByPhoto('34716887764')

if __name__ == '__main__':
    main()
    #print judgeAdj('happy')
    