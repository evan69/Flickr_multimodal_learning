#coding:utf-8

import flickrapi
import os
import sys
import socket
import inspect
import nltk

api_key = u'b28ec210280050d5d1760ff978e0404a'
api_secret = u'59131beaddb61785'
#flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

tag_set = ['graceful']
tag_set = set(tag_set)
photo_set = set()

def judgeAdj(tag):
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
        print 'error'
        
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
    #res = flickr.photos.getInfo(api_key=api_key,photo_id=photo_id)
    try:
        res = flickr.tags.getListPhoto(api_key=api_key,photo_id=photo_id)
        tags = res.get('photo').get('tags').get('tag')
        return tags
        #print tags
        for tag in tags:
            print tag.get('id'),tag.get('raw').encode('utf8')
        #print res
    except Exception,ex:
        print 'error'
        print Exception,':',ex
        
def run(max_depth):
    global tag_set
    cnt = 0
    while(cnt < max_depth):
        new_tag_set = set()
        for tag in tag_set:
            photos = getPhotosByTag(tag)
            try:
                for photo in photos:
                    myurl = photo.get('url_z')
                    photo_id = photo.get('id')
                    if photo_id in photo_set:
                        continue
                    photo_set.add(photo_id)
                    print myurl,photo_id
                    tags_of_photo = getTagsByPhoto(photo_id)
                    for tag in tags_of_photo:
                        tag_name = tag.get('raw')
                        is_adj = judgeAdj(tag_name)
                        try:
                            print 'add tag:',tag_name,is_adj
                        except Exception,ex:
                            print ex
                        if is_adj:
                            new_tag_set.add(tag_name)

            except Exception,ex:
                print 'error'
                print Exception,':',ex
        
        tag_set = new_tag_set
        print 'end a round of tag scanning'
        print 'tag for next loop:'
        print tag_set
        cnt += 1
    print 'total photo num:',cnt
        
def main():
    reload(sys)
    #print sys.getdefaultencoding()
    sys.setdefaultencoding('utf-8')
    #print sys.getdefaultencoding()
    run(1)
    #getPhotosByTag("black-and-white")
    #getTagsByPhoto('34716887764')

if __name__ == '__main__':
    main()
    #print judgeAdj('happy')
    