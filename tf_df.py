# -*- coding: utf-8 -*-
from curses.ascii import isdigit
from ipaddress import ip_address
from os import path
from tabnanny import check
from typing import Counter
from sklearn.feature_extraction.text import CountVectorizer 
import numpy as np
from operator import itemgetter
import re
from listdir_inmac import listdirInMac
from tools import Merge, SumDict, check_ip, check_para, check_port, check_simip, is_num


def get_files(path):
    filelist = listdirInMac(path)
    return filelist

def document_frequency(path, filelist):
    df_all = {}
    for file in filelist:
        file_path = path + '/' + file
        with open(file_path, 'r') as f:
            file_txt = f.read()
            word_file = list(set(file_txt.split()))
            word_file = list(filter(lambda x: not str(x).isdigit(), word_file))
            word_dict = dict(zip(word_file, [1]*len(word_file)))
            for key in list(word_dict.keys()):
                if (check_ip(str(key)) == 4 or check_ip(str(key)) == 6):
                    del word_dict[key]
                elif (check_simip(str(key)) == True):
                    del word_dict[key]
                elif (check_port(str(key)) == True):
                    del word_dict[key]
                elif (check_para(str(key)) == True):
                    del word_dict[key]
                elif (is_num(str(key)) == True):
                    del word_dict[key]
                elif (len(key) >= 30 or key == ''):
                    del word_dict[key]
        df_all = Merge(df_all, word_dict)
        f.close()
    for k in list(df_all.keys()):
        if (df_all[k] <= len(filelist)/6):
            del df_all[k]
    # df_all = {k: v / total for total in (sum(df_all.values()),) for k, v in df_all.items()}
    df_all = dict(sorted(df_all.items(), key=lambda x: x[1], reverse=True))
    return df_all
        

def tf_df(path,filelist):     
    txt_corpus = []
    from define_occr import ot_tfc
    word_tf = {}
    tf_all = {}
    for file in filelist:
        file_path = path + '/' + file
        with open(file_path, 'r') as f:
            word_list = f.read()
            word_list = word_list.split()
            txt_corpus = list(filter(lambda x: not is_num(str(x)), word_list))
            txt_corpus = list(filter(lambda x: not str(x).isdigit(), txt_corpus))
            txt_corpus = list(filter(lambda x: not check_para(str(x)), txt_corpus))
            txt_corpus = list(filter(lambda x: not check_ip(str(x)), txt_corpus))
            txt_corpus = list(filter(lambda x: not check_port(str(x)), txt_corpus))
            txt_corpus = list(filter(lambda x: not check_simip(str(x)), txt_corpus))
            txt_corpus = list(filter(lambda x: not len(str(x)) >= 30, txt_corpus))
        f.close()
        for item in txt_corpus:
            if item in word_tf:
                word_tf[item] += 1
            else:
                word_tf[item] = 1
        tf_all = dict(Counter(word_tf) + Counter(tf_all))
    for key in list(tf_all.keys()):
        if(tf_all[key] <= 3 * len(filelist)):
            del tf_all[key]
    tf_all = dict(sorted(tf_all.items(), key=lambda x: x[1], reverse=True))
    return tf_all



def attribute(df_all, tf_all):
    
    '''
    +++++++++++++++++++++
    create keyword language base
    +++++++++++++++++++++
    use Deviation method, research when the df & tf both high value
    #####################
    get two parmater:
        1. 0.0005
        2. 5e-05
    #####################
    You need to repeat the experiment to complete the “key.txt” ,
    fine-tune the parameters when necessary
    '''
    
    df_all = {k: v / total for total in (sum(df_all.values()),) for k, v in df_all.items()}
    tf_all = {k: v / total for total in (sum(tf_all.values()),) for k, v in tf_all.items()}
    for key in list(df_all.keys()):
        if(df_all[key] <= 0.0005):
            del df_all[key]
    for key in list(tf_all.keys()):
        if(tf_all[key] <= 5e-05):
            del tf_all[key]
    all_attr = list(tf_all.keys() & df_all.keys())
    
    attr_file = open('key.txt', 'w')
    for key in all_attr:
        attr_file.write(key+'\n')
    attr_file.close()
    