#coding:utf-8

import flickrapi
import os
import sys
import socket
import inspect
import nltk
import random

api_key = u'b28ec210280050d5d1760ff978e0404a'
api_secret = u'59131beaddb61785'
#flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

tag_set = ['graceful']
# initial tags
tag_set = set(tag_set)
photo_set = set()
# initial photos visited

def judgeAdj(tag):
# judge whether the word is adj
    if tag.find(' ') != -1:
        return False
    text = nltk.word_tokenize(tag)
    res = nltk.pos_tag(text)
    #print res
    return res[0][1] == 'JJ'

def getPhotosByTag(tag_name):
    try:
        photos = flickr.photos.search(extras='url_z', tags = tag_name)
        photos = photos['photos']['photo']
    except Exception:
        print 'error in getPhotosByTag'
        
    return photos
    '''        
    try:
        for photo in photos:
            myurl = photo.get('url_z')
            photo_id = photo.get('id')
            if myurl is not None:
                print myurl,photo_id

    except Exception,ex:
        print 'error'
        print Exception,':',ex
    '''
        
def getTagsByPhoto(photo_id):
    try:
        res = flickr.tags.getListPhoto(api_key=api_key,photo_id=photo_id)
        tags = res.get('photo').get('tags').get('tag')
    except Exception,ex:
        print 'error in getTagsByPhoto'
        print Exception,':',ex
        
    return tags
        
def run(max_depth, rate):
    global tag_set
    ret_set = set()
    ret_set.update(tag_set)
    cnt = 0
    while(cnt < max_depth):
        new_tag_set = set()
        for tag in tag_set:
            try:
                photos = getPhotosByTag(tag)
                # get photos of a tag
                rand_list = random.sample(range(0, len(photos)), int(rate * len(photos) + 1))
                photos = [photos[i] for i in rand_list]
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
                        print myurl,photo_id
                        tags_of_photo = getTagsByPhoto(photo_id)
                        # get all tags of a photo
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
                                    new_tag_set.add(tag_name)
                                # transfer to lower format and add to set
                                print 'add tag:',tag_name,is_adj
                            except Exception,ex:
                                print 'error when process a tag of a photo'
                                print Exception,':',ex

                    except Exception,ex:
                        print 'error when process a photo'
                        print Exception,':',ex

            except Exception,ex:
                print 'error when process a tag in tag_set'
                print Exception,':',ex
        
        tag_set = new_tag_set
        # tags to be visited in the next loop
        ret_set.update(tag_set)
        # add them to return tag set
        print 'end a round of tag scanning'
        print 'tag for next loop:'
        print tag_set
        cnt += 1
    print 'total tag num:',len(ret_set)
    return ret_set
        
def main():
    reload(sys)
    #print sys.getdefaultencoding()
    sys.setdefaultencoding('utf-8')
    #print sys.getdefaultencoding()
    print run(1,0.1)
    #getPhotosByTag("black-and-white")
    #getTagsByPhoto('34716887764')

if __name__ == '__main__':
    main()
    #print judgeAdj('happy')
    