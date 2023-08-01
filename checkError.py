
# -*- coding: UTF-8 -*-
import csv

import joblib
from func_paratools import ck_paa, kkw, pre_cls, reads, vf_cs, write_correct_paragraph
from listdir_inmac import listdirInMac
import os
import sys
from define_occr import ptnum,vfnum,vsnum

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, ".."))
import re
lath = r'load_file' # load setting file path
cath = r'check' # load check file
k_modal = r'set.pkl'
if __name__ == '__main__':
    clf = joblib.load(k_modal)
    erc_list = pre_cls(clf, cath)
    class error_c:
        def __init__(self):
            self.umv = [0] * 2
            self.umv_l = [0] * 2
            self.umv_n = False
    files = listdirInMac(cath)
    vf_cs(cath)
    ounlikfg = ck_paa(ptnum, vfnum, vsnum)
    fd = []
    #find()
    for file in erc_list:
        lines = reads(cath,file)
        for i in range(len(lines)):
            fd = fd + write_correct_paragraph(lines,i,file)
    erro = ounlikfg + fd + kkw(cath)


    f = open('error.txt', 'w')
    for i in erro:
        f.write(i)
        f.write('\n')
    f.close()