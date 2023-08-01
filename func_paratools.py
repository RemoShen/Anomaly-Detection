
from os import listdir
import re
from collections import Counter
import numpy as np

from sklearn import preprocessing
from create_tree import create_single_tree
import tools
from CorrectWords import correct
import define_occr
from listdir_inmac import listdirInMac
from train_tree import vctpara
from tree_tools import svdic_tree_r

count_correct = 0

punkt_list = define_occr.punkt_list


def words(text): return re.findall(r'\w+', text)

WORDS_ol = []
with open ('key.txt', 'r') as f:
    for word in f.readlines():
        WORDS_ol.append(word.strip('\n'))

WORDS = Counter(WORDS_ol)


def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

import csv
def create_csv(name):
    with open(name,'w') as f:
        csv_write = csv.writer(f)
        csv_head = ["ipv4","text","line"]
        csv_write.writerow(csv_head)

def write_csv(name,data):
    with open(name,'a+') as f:
        csv_write = csv.writer(f)
        data_row = data
        csv_write.writerow(data_row)



def correction(word): 
    return max(candidates(word), key=P)

def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    return set(w for w in words if w in WORDS)

def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def vf_error(vf_num):
    with open(vf_num, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        index = [row for row in reader]
        er = []
        for ptax in range(len(index)-4):
            if(index[ptax]['line'] == index[ptax]['line']):
                if(index[ptax+2]['line'] == index[ptax+3]['line']):
                    if(index[ptax]['ipv4'] == index[ptax+3]['ipv4'] ):
                        if(index[ptax+1]['ipv4'] == index[ptax+2]['ipv4']):
                            er.append(error_vf(index[ptax+2]['text'],index[ptax+2]['line']))
    return er

def check_error(i):
    
    # ipv6 = r'((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:)))(%.+)?(\/.+)?'
    # ipv4 = r'X?(\d{0,4}\.){3,9}(?:25[0-9]|2[0-9]\d|1\d{2}|[0-9]?\d)\/?(\d+)?'
    # port = r'\d{2,7}:\d{1,7}(:\d+)?'
    if i == '':
        return ''
    elif(tools.check_ip(i) == 6 or tools.check_sim_v6(i) == True):
        return 'v_s'
    elif(tools.check_ip(i) == 4 or tools.check_sim_v4(i) == True):
        return 'v_f'
    elif(tools.check_port(i) == True):
        return 'p_n'
    # elif re.match(ipv6, i) != None:
    #     return 'v_s'
    # elif re.match(ipv4, i) != None:
    #     return 'v_f'
    # elif re.match(port, i) != None:
    #     return 'p_n'
    else:
        i_new = correction(i)
        if i_new != i :
            return i_new
        else:
            return i

def vs_error(vf_num):
    with open(vf_num, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        index = [row for row in reader]
        er = []
        for ptax in range(len(index)-4):
            if(index[ptax]['line'] == index[ptax+1]['line']):
                if(index[ptax+2]['line'] == index[ptax+3]['line']):
                    if(index[ptax]['ipv4'] == index[ptax+3]['ipv4'] ):
                        if(index[ptax+1]['ipv4'] == index[ptax+2]['ipv4']):
                            er.append(error_vf(index[ptax+2]['text'],index[ptax+2]['line']))
    return er

def minDistance(word1, word2):
    if not word1:
        return len(word2 or '') or 0

    if not word2:
        return len(word1 or '') or 0

    size1 = len(word1)
    size2 = len(word2)

    last = 0
    tmp = list(range(size2 + 1))
    value = None

    for i in range(size1):
        tmp[0] = i + 1
        last = i
        for j in range(size2):
            if word1[i] == word2[j]:
                value = last
            else:
                value = 1 + min(last, tmp[j], tmp[j + 1])
            last = tmp[j+1]
            tmp[j+1] = value
    return value

def error_vf(file, line):
    return (file+'第'+line+'行， 交换ip前后顺序')

def f_fils(file, line):
    return file
def int_count(word):
    int_count = 0
    for i in word:
        if (i.isdigit() == True and i != 4 and i != 6):
            int_count += 1
    return int_count

def int_xie(word):
    int_xie = 0
    for i in word:
        if(i == '-'):
            int_xie += 1
    return int_xie

def vf_cs(cath):
    files = listdirInMac(cath)
    name1 = 'vflist.csv'
    create_csv(name1)
    name2 = 'vslist.csv'
    create_csv(name2)
    name3 = 'pt.csv'
    create_csv(name3)

    for file in files: 
        with open(cath+'/'+file, 'r') as f:
            i = 1
            for l in f:
                l_new = l.replace('\n', '')
                vf = re.findall(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}/?\d+?', str(l_new))
                vs = re.finditer(r'((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:)))(%.+)?/?\d+?', str(l_new))
                vp = re.finditer(r'\d{5,7}:\d{3,7}',str(l_new))
                word = l_new.split(' ')
                for element in vf:
                    datav4 = [element, file, i]
                    write_csv(name1,datav4)

                for element in vs:
                    datav6 = [element[0], file, i]
                    write_csv(name2, datav6)

                for element in vp:
                    datavp = [element[0], file, i]
                    write_csv(name3,datavp)
                i += 1



def error_kk(file,line,w):
    return (str(file) + '第' + str(line) + '行 ' + str(w) + ' 发生异常，请查看关键字之间是否缺少空格或存在拼写异常')
def error_po(file,line,w):
    return (str(file) + '第' + str(line) + '行 ' + str(w) + ' 发生异常，请检查端口号参数是否异常')
def error_pv(file,line,w):
    return(str(file)+ '第' + str(line) + '行 ' + str(w) + '发生异常，请检查参数或ip地址是否正常')
def kk_fl(file,line,w):
    return file
def po_fl(file,line,w):
    return file
def pv_fl(file,line,w):
    return file
def kkw(cath):
    kk = []
    files = listdirInMac(cath)
    list_port_after = define_occr.list_port_after
    list_port_before = define_occr.list_port_before
    list_port_ip4 = define_occr.list_port_ip4
    # list_port_ip6 = ['rt']
    lei_ip = define_occr.lei_ip
    ip_together = define_occr.ip_together
    ip6_ed = define_occr.ip6_ed
    ip4_ed = define_occr.ip4_ed
    for file in files: 
        with open(cath+'/'+file, 'r') as f:
            i = 1
            for l in f:
                l_new = l.replace('\n', '')
                word = l_new.split(' ')
                for count in range(len(word)):
                    if (word[count] not in WORDS and
                        '_' not in word[count] and 
                        '.' not in word[count] and
                        ':' not in word[count] and
                        '/' not in word[count] and
                        ',' not in word[count] and
                        '|' not in word[count] and
                        '=' not in word[count] and
                        '!' not in word[count] and
                        '？' not in word[count] and
                        len(word[count]) != 8  and
                        len(word[count]) != 32 and
                        '*' not in word[count] and
                        '#' not in word[count] and
                        '@' not in word[count] and
                        '&' not in word[count] and
                        '(' not in word[count] and
                        word[count] not in WORDS and
                        word[count].isdigit() == False
                        ):
                        if('-' in word[count]):
                            if(int_xie(word[count]) == 2 and len(word[count]) > 12):
                                kk.append(error_kk(file, i, word[count]))
                            elif(int_xie(word[count]) == 1 and len(word[count]) > 10):
                                kk.append(error_kk(file, i, word[count]))
                        else:
                            if(len(word[count]) > 5 and int_count(word[count]) < 2):
                                kk.append(error_kk(file, i, word[count]))
                for count in range(len(word)-1):
                    if(word[count] in list_port_after and (not re.fullmatch('\d+:\d+',word[count + 1]))):
                        if(not word[count+1].isdigit() and word[count+1] not in['route-target','matches-any']):
                            kk.append(error_po(file,i,word[count]))
                    elif(word[count] == 'name' and word[count-1] == 'community' 
                    and (not re.fullmatch('\d+:\d+',word[count + 1]) or word[count+1]) in ['fromMCR_A','fromMCR_B']):
                        if(not word[count + 1].isdigit()):
                            kk.append(error_po(file,i,word[count]))
                    elif(word[count] in list_port_ip4 and  
                    not re.fullmatch('X?(\d{0,4}\.){3,9}(?:25[0-9]|2[0-9]\d|1\d{2}|[0-9]?\d)\/?(\d+)?',word[count + 1])):
                        if(word[count + 1] not in ip4_ed):
                            kk.append(error_pv(file,i,word[count]))
                    elif(word[count] in ip_together 
                    and not re.fullmatch('((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:)))(%.+)?(\/.+)?',word[count + 1])
                    and not re.fullmatch('X?(\d{0,4}\.){3,9}(?:25[0-9]|2[0-9]\d|1\d{2}|[0-9]?\d)\/?(\d+)?',word[count + 1])):    
                        if(word[count] != 'permit'):
                            if(word[count + 1] not in ip6_ed and not re.fullmatch('\d+:\d+',word[count + 1])):
                                kk.append(error_pv(file,i,word[count]))
                        else:
                            if(word[count + 1] not in ip6_ed and not re.fullmatch('\d+:\d+',word[count + 1]) and not re.fullmatch('\d+',word[count + 1])): 
                                kk.append(error_pv(file,i,word[count]))


                for count in range(len(word)):
                    if(word[count] in list_port_before and (not re.fullmatch('\d+:\d+',word[count - 1]))):
                            kk.append(error_po(file,i,word[count]))
                i += 1
    return kk

def f_list_fl(vf_num, y_pred):
    with open(vf_num, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        index = [row for row in reader]
        er = []
        y_p = y_pred # maybe adding set info
        for ptax in range(len(index)-4):
            if(index[ptax]['line'] == index[ptax]['line']):
                if(index[ptax+2]['line'] == index[ptax+3]['line']):
                    if(index[ptax]['ipv4'] == index[ptax+3]['ipv4'] ):
                        if(index[ptax+1]['ipv4'] == index[ptax+2]['ipv4']):
                            er.append(f_fils(index[ptax+2]['text'],index[ptax+2]['line']))
    f_fls = list(set(er))
    return f_fls

def error_p_seq(file,line):
    return(file+'第'+line+"行，交换端口号前后顺序")

def er_fls_p(file, line):
    return file
def error_p_er(file,line,p_new,p):
    return(file+' 第'+line+'行，将'+p_new+"改为"+p)
def er_fls_p_er(file, line, p_new, p):
    return file
def p_error(ptnum):
    with open(ptnum, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]
        tax = 0
        tp = 0
        error_po = []
        pt_all = []
        for i in rows:
            pt_all.append(i['ipv4'])
        p_d = Counter(pt_all)
        for i in rows:
            p_new = i['ipv4']
            p_new_pre = p_new.split(':')[0]
            p_new_nex = p_new.split(':')[1]
            seq1 = rows[tax+1]['ipv4'].split(':')[0] 
            seq2 = rows[tax+1]['ipv4'].split(':')[1]
            if(p_new_pre == seq2 and p_new_nex == seq1):
                error_po.append(error_p_seq(rows[tax+1]['text'],rows[tax+1]['line']))
                rows[tax+1]['ipv4'] = p_new_pre+':'+p_new_nex
            if(rows[tp]['ipv4'].split(':')[0] == rows[tp+1]['ipv4'].split(':')[0]):
                if(minDistance(rows[tp]['ipv4'],rows[tp+1]['ipv4']) == 1 and rows[tp+1]['ipv4'] != rows[tp+2]['ipv4']):
                    if(p_d[rows[tp+1]['ipv4']] == 1):
                        error_po.append(error_p_er(rows[tp+1]['text'],rows[tp+1]['line'],rows[tp+1]['ipv4'],rows[tp]['ipv4']))              
            if tax<len(rows) - 2:
                tax += 1
            if tp<len(rows) - 3:
                tp += 1
    return error_po

def error_word(file,line,correct,word):
    return str(file+' 第'+str(line)+'行，将'+word+"改为"+correct)
def wor_ls(file,line,correct,word):
    return file
def s_list_fl(vf_num, y_pred):
    with open(vf_num, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        index = [row for row in reader]
        er = []
        py = y_pred # maybe adding set info
        for ptax in range(len(index)-4):
            if(index[ptax]['line'] == index[ptax+1]['line']):
                if(index[ptax+2]['line'] == index[ptax+3]['line']):
                    if(index[ptax]['ipv4'] == index[ptax+3]['ipv4'] ):
                        if(index[ptax+1]['ipv4'] == index[ptax+2]['ipv4']):
                            er.append(f_fils(index[ptax+2]['text'],index[ptax+2]['line']))
    s_ls_f = list(set(er))
    return s_ls_f
def write_correct_paragraph(lines,i,file):
    er = []
    global count_correct
    sentences = lines[i]
    words_list = sentences.split(' ')
    for word in words_list:
        if word not in punkt_list:
            correct_word = correct(word)
            correct_word = correct_word.strip()
            word = re.sub(r'[^A-Za-z0-9 -_!<>]+=', '', word)
            word = word.lstrip()

            if bool(re.search(r'\d',word)) == False and word!='':
                if (not str.isdigit(word)) and len(word) < 20 and len(word)>1:
                    if correct_word is not word:
                        print(file)
                        print(i)
                        print(correct_word)
                        print(word)
                        line_n = i+1
                        er.append(error_word(file,line_n,correct_word,word))
    return er


def p_fils(ptnum, y_pred):
    with open(ptnum, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]
        tax = 0
        tp = 0
        error_po = []
        pt_all = []
        y_p = y_pred # maybe adding set info
        for i in rows:
            pt_all.append(i['ipv4'])
        p_d = Counter(pt_all)
        for i in rows:
            p_new = i['ipv4']
            p_new_pre = p_new.split(':')[0]
            p_new_nex = p_new.split(':')[1]
            seq1 = rows[tax+1]['ipv4'].split(':')[0] 
            seq2 = rows[tax+1]['ipv4'].split(':')[1]
            if(p_new_pre == seq2 and p_new_nex == seq1):
                error_po.append(er_fls_p(rows[tax+1]['text'],rows[tax+1]['line']))
                rows[tax+1]['ipv4'] = p_new_pre+':'+p_new_nex
            if(rows[tp]['ipv4'].split(':')[0] == rows[tp+1]['ipv4'].split(':')[0]):
                if(minDistance(rows[tp]['ipv4'],rows[tp+1]['ipv4']) == 1 and rows[tp+1]['ipv4'] != rows[tp+2]['ipv4']):
                    if(p_d[rows[tp+1]['ipv4']] == 1):
                        error_po.append(er_fls_p_er(rows[tp+1]['text'],rows[tp+1]['line'],rows[tp+1]['ipv4'],rows[tp]['ipv4']))              
            if tax<len(rows) - 2:
                tax += 1
            if tp<len(rows) - 3:
                tp += 1
        er_list= list(set(error_po))
    return er_list
def reads(cath,file):
    file_new = cath+'/'+file
    lines = []
    with open(file_new,'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)
    return lines
def cp_ls(lines,i,file):
    er = []
    global count_correct
    sentences = lines[i]
    words_list = sentences.split(' ')
    for word in words_list:
        if word not in punkt_list:
            correct_word = correct(word)
            correct_word = correct_word.strip()
            word = re.sub(r'[^A-Za-z0-9 -_!<>]+=', '', word)
            word = word.lstrip()

            if bool(re.search(r'\d',word)) == False and word!='':
                if (not str.isdigit(word)) and len(word) < 20 and len(word)>1:
                    if correct_word is not word:
                        line_n = i+1
                        er.append(wor_ls(file,line_n,correct_word,word))
    return er
def seq_err(file,line):
    return (str(file) + '第' + str(line) + '行 ' + ' 发生异常，请查看句子顺序或是否有冗余或缺失')
def ls_l_fl(cath):
    kk = []
    files = listdirInMac(cath)
    list_port_after = define_occr.list_port_after
    list_port_before = define_occr.list_port_before
    list_port_ip4 = define_occr.list_port_ip4
    # list_port_ip6 = ['rt']
    lei_ip = define_occr.lei_ip
    ip_together = define_occr.ip_together
    ip6_ed = define_occr.ip6_ed
    ip4_ed = define_occr.ip4_ed
    for file in files: 
        with open(cath+'/'+file, 'r') as f:
            i = 1
            for l in f:
                l_new = l.replace('\n', '')
                word = l_new.split(' ')
                for count in range(len(word)):
                    if (word[count] not in WORDS and
                        '_' not in word[count] and 
                        '.' not in word[count] and
                        ':' not in word[count] and
                        '/' not in word[count] and
                        ',' not in word[count] and
                        '|' not in word[count] and
                        '=' not in word[count] and
                        '!' not in word[count] and
                        '？' not in word[count] and
                        len(word[count]) != 8  and
                        len(word[count]) != 32 and
                        '*' not in word[count] and
                        '#' not in word[count] and
                        '@' not in word[count] and
                        '&' not in word[count] and
                        '(' not in word[count] and
                        word[count] not in WORDS and
                        word[count].isdigit() == False
                        ):
                        if('-' in word[count]):
                            if(int_xie(word[count]) == 2 and len(word[count]) > 12):
                                kk.append(kk_fl(file, i, word[count]))
                            elif(int_xie(word[count]) == 1 and len(word[count]) > 10):
                                kk.append(kk_fl(file, i, word[count]))
                        else:
                            if(len(word[count]) > 5 and int_count(word[count]) < 2):
                                kk.append(kk_fl(file, i, word[count]))
                for count in range(len(word)-1):
                    if(word[count] in list_port_after and (not re.fullmatch('\d+:\d+',word[count + 1]))):
                        if(not word[count+1].isdigit() and word[count+1] not in['route-target','matches-any']):
                            kk.append(po_fl(file,i,word[count]))
                    elif(word[count] == 'name' and word[count-1] == 'community' 
                    and (not re.fullmatch('\d+:\d+',word[count + 1]) or word[count+1]) in ['fromMCR_A','fromMCR_B']):
                        if(not word[count + 1].isdigit()):
                            kk.append(po_fl(file,i,word[count]))
                    elif(word[count] in list_port_ip4 and  
                    not re.fullmatch('X?(\d{0,4}\.){3,9}(?:25[0-9]|2[0-9]\d|1\d{2}|[0-9]?\d)\/?(\d+)?',word[count + 1])):
                        if(word[count + 1] not in ip4_ed):
                            kk.append(pv_fl(file,i,word[count]))
                    elif(word[count] in ip_together 
                    and not re.fullmatch('((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:)))(%.+)?(\/.+)?',word[count + 1])
                    and not re.fullmatch('X?(\d{0,4}\.){3,9}(?:25[0-9]|2[0-9]\d|1\d{2}|[0-9]?\d)\/?(\d+)?',word[count + 1])):    
                        if(word[count] != 'permit'):
                            if(word[count + 1] not in ip6_ed and not re.fullmatch('\d+:\d+',word[count + 1])):
                                kk.append(pv_fl(file,i,word[count]))
                        else:
                            if(word[count + 1] not in ip6_ed and not re.fullmatch('\d+:\d+',word[count + 1]) and not re.fullmatch('\d+',word[count + 1])): 
                                kk.append(pv_fl(file,i,word[count]))


                for count in range(len(word)):
                    if(word[count] in list_port_before and (not re.fullmatch('\d+:\d+',word[count - 1]))):
                            kk.append(error_po(file,i,word[count]))
                i += 1
    return kk
def seq(cath):
    kk = []
    files = listdirInMac(cath)
    for file in files:
        with open(cath + '/' + file, 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if ('import' in lines[i] and 'import-route direct' not in lines[i] and 'import-route static' not in lines[i]
                and 'route-policy' not in lines[i]):
                    if(('export' not in lines[i - 1] and 'export' not in lines[i - 2])
                    and ('export' not in lines[i + 1] and 'export' not in lines[i + 2])):
                        kk.append(seq_err(file,i+1))
                elif('export' in lines[i] and 'route-policy' not in lines[i]):
                    if(('import' not in lines[i - 1] and 'import' not in lines[i - 2])
                    and ('import' not in lines[i + 1] and 'import' not in lines[i + 2])):
                        kk.append(seq_err(file,i+1))
    return kk
def pre_rt(cath, y_pred):
    files = listdirInMac(cath)
    vf_cs(cath)
    ptnum = 'pt.csv'
    vfnum = 'vflist.csv'
    vsnum = 'vslist.csv'
    p_list = p_fils(ptnum, y_pred)
    f_list = f_list_fl(vfnum, y_pred)
    s_list = s_list_fl(vsnum, y_pred)
    fd = []
    for file in files:
        lines = reads(cath,file)
        for i in range(len(lines)):
            fd = fd + cp_ls(lines,i,file)
    pd_lst =  list(set(fd))
    kk_ls = list(set(ls_l_fl(cath)))
    
    pre_fl = list(set(p_list + f_list + s_list + pd_lst + kk_ls))
    return pre_fl



def pre_cls(clf, catch):
    attr = 'key.txt'
    ladk_path = listdir(catch)
    file_len = 0 
    vc = []
    for file in ladk_path:
        single_tree, kt =  create_single_tree(catch,file, attr)
        par_pra = vctpara(file, single_tree, kt) 
        todic = single_tree.to_dict()
        vc.append(par_pra)
        svnm = str(file_len) + '.txt'
        svdic_tree_r(todic, svnm)
        file_len += 1 
    with open('rc.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for item in vc:
            writer.writerow(item)
    csvfile.close()
    data = []
    with open('rc.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([row[1], row[2], row[3]])
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
    A = np.array(data)
    X=min_max_scaler.fit_transform(A)
    y_pred = clf.predict(X)
    fls = pre_rt(catch, y_pred)
    return fls

def ck_paa(ptnum, vfnum, vsnum):
    vp = p_error(ptnum)
    vf = vf_error(vfnum)
    vs = vs_error(vsnum)
    ckpaa = vp + vf + vs
    return ckpaa