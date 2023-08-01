from distutils.command.sdist import sdist
from treelib import Tree
import pickle

from tools import check_ip, check_port, check_sim_v4, check_sim_v6

class node_para:
    def _init_(self):
        self.id = 0
        self.start_line = 0
        self.sen_num = 0
        self.times = 0
class node_sen:
    def __init__(self):
        self.id = 0
        self.line = 0
        self.wor_num = 0 
        self.times = 0
class node_word:
    def __init__(self):
        self.wor = 'wor'
        self.attr = 'attr'
                
def co_para(whtxt, start, end, pre_para, attr):
    para_now = whtxt[start: end]
    para_now_trs = []
    ipv4 = []
    sim_v4 = []
    ipv6 = []
    sim_v6 =[]
    port = []
    for sen in para_now:
        if(len(sen.replace(' ','').replace('\n', '')) == 0):
            continue
        srno = ''
        sen = sen.replace('\n', '')
        sen_cur = sen.split(' ')
        for item in sen_cur:
            if (item in attr):
                srno += 'key '
            elif(check_ip(item) == 4):
                if(item not in ipv4):
                    ipv4.append(item)
                srno += 'ipv4/' + str(ipv4.index(item)) + ' '
            elif(check_ip(item) == 6):
                if (item not in ipv6):
                    ipv6.append(item)
                srno += 'ipv6/' + str(ipv6.index(item)) + ' '
            elif(check_sim_v4(item)):
                if(item not in sim_v4):
                    sim_v4.append(item)
                srno += 'ipv4' + str(sim_v4.index(item)) + ' '
            elif(check_sim_v6(item)):
                if(item not in sim_v6):
                    sim_v6.append(item)
                srno += 'ipv6' + str(sim_v6.index(item)) + ' '
            elif(check_port(item)):
                if(item not in port):
                    port.append(item)
                srno += 'port' + str(port.index(item)) + ' '
            else:
                srno += 'others '
        srno = srno.rstrip()
        para_now_trs.append(srno)
    if(pre_para == para_now_trs):
        return True
    else:
        return para_now_trs
    
def create_sen_tree(whtxt, start, end, sen, startline, id_tackiopp, times):
    sen_cur = whtxt[start: end]
    sen_tree = Tree()
    sen_now = node_sen()
    sen_now.line = startline
    sen_now.times = times
    sen_now.wor_num = 0
    sen_tree.create_node(tag = 'sen', identifier = id_tackiopp, data = sen_now)
    ke_t = 0
        
    for item in sen:
        if(item == 'key'):
            ke_t += 1
        sen_word_in = item
        sen_word = node_word()
        sen_word.wor = 'wor'
        sen_word.attr = sen_word_in
        sen_tree.create_node(tag = 'word', data = sen_word, parent = id_tackiopp)
    return sen_tree, ke_t

def svdic_tree(dic, i):
    rpath = 'lgtree/'
    with open(rpath + i, 'w', encoding='utf-8') as file:
        file.write(str(pickle.dumps(dic)))
    file.close()

def svdic_tree_r(dic, i):
    rpath = 'rstree/'
    with open(rpath + i, 'w', encoding='utf-8') as file:
        file.write(str(pickle.dumps(dic)))
    file.close()