# merge all tags of (un)supervised pictures
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

THREAD_NUM = 8
TAG_FILE_NAME = 'tags_data.txt'
HI_DATE = datetime.datetime(2017, 6, 1)
LO_DATE = HI_DATE - datetime.timedelta(days = 30 * THREAD_NUM)
print LO_DATE

def unsMerge():
    for month in range(8):
        init = LO_DATE + datetime.timedelta(days = 30 * month)
        for i in range(30):
            dir = '../data/unsupervised/' + init.strftime("%y_%m_%d") + '/'
            print 'process ' + dir
            try:
                tag_file = open(dir + TAG_FILE_NAME,'r')
                lines = tag_file.readlines()
                for line in lines:
                    fout.write('u ')
                    fout.write(dir)
                    fout.write(' ')
                    fout.write(line)
                tag_file.close()
                init += datetime.timedelta(days = 1)
            except Exception,ex:
                print 'error in unsup merge'
                print ex
                
            
def supMerge():
    tag_cnt_file = open('pic_tag_cnt_new.txt','r')
    all_tags = tag_cnt_file.readlines()
    all_tags = [line.split(' ')[0] for line in all_tags]
    tag_cnt_file.close()
    
    for tag in all_tags:
        dir = '../data/' + tag + '/'
        print 'process ' + dir
        try:
            tag_file = open(dir + TAG_FILE_NAME,'r')
            lines = tag_file.readlines()
            for line in lines:
                fout.write('s ')
                fout.write(dir)
                fout.write(' ')
                fout.write(line)
            tag_file.close()
        except Exception,ex:
            print 'error in sup merge'
            print ex
            
def mergePart():
    cnt = 0
    
    si = set()
    fin = open('image_modal_data.txt','r')
    lines = fin.readlines()
    for line in lines:
        sp = line.split(' ')
        info = sp[0] + sp[1] + sp[2]
        si.add(info)
        cnt += 1
        if cnt % 1000 == 0:
            print cnt
    fin.close()
    
    st = set()
    fin = open('text_modal_data.txt','r')
    lines = fin.readlines()
    for line in lines:
        sp = line.split(' ')
        info = sp[0] + sp[1] + sp[2]
        st.add(info)    
        cnt += 1
        if cnt % 1000 == 0:
            print cnt
    fin.close()
    
    final_set = si & st
    
    smallSet = dict()
    fin = open('image_modal_data.txt','r')
    fout = open('image_modal_train.txt','w')
    i = 0
    lines = fin.readlines()
    for line in lines:
        sp = line.split(' ')
        info = sp[0] + sp[1] + sp[2]
        if info not in final_set:
            continue
        smallSet[info] = i
        fout.write(line)
        i += 1
        cnt += 1
        if cnt % 1000 == 0:
            print cnt
    fin.close()
    fout.close()
    
    keys_set = smallSet.keys()
    assert len(final_set) == len(keys_set)
    assert i == len(final_set)
    
    out = ['#'] * len(final_set)
    
    fin = open('text_modal_data.txt','r')
    lines = fin.readlines()
    for line in lines:
        sp = line.split(' ')
        info = sp[0] + sp[1] + sp[2]
        if info in keys_set:
            out[smallSet[info]] = line
        cnt += 1
        if cnt % 1000 == 0:
            print cnt
    fin.close()
    
    fout = open('text_modal_train.txt','w')
    for line in out:
        fout.write(line)
    fout.close()
    
if __name__ == '__main__':
    if sys.argv[1] == '-a':
        fout = open('text_modal_data.txt','w')
        supMerge()
        # unsMerge()
        fout.close()
    else:
        mergePart()
    
