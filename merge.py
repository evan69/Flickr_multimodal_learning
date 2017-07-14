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
            
if __name__ == '__main__':
    fout = open('text_modal_data.txt','w')
    supMerge()
    unsMerge()
    fout.close()
