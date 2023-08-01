from treelib import Node, Tree
from define_occr import setting_name, zx_par, hs_par, hw_par, sk_fh_par, other_par
from tree_tools import co_para, create_sen_tree

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
        
def create_para(whtxt, para_now, i, j ,id, attr, paraicdpokk, sen_times, sen_tim, times): # j-1
    para_tree = Tree()
    para_info = node_para()
    para_info.id = id
    para_info.start_line = i + 1
    para_info.sen_num = 0
    para_info.times = sen_times
    para_tree.create_node(identifier = paraicdpokk, tag = 'para', data = para_info)
    stline = 0
    id_tackiopp = 0
    kt_p = 0
            
    for i in range(len(sen_tim)): 
        id_tackiopp_new = str(para_tree.identifier) + '_' + str(id_tackiopp)
        sen = sen_tim[i].split(' ')
        print(sen)
        sen_now, kt_s = create_sen_tree(whtxt, i, j, sen, para_info.start_line + stline, id_tackiopp_new, times[i])
        # print(sen_now.to_json())
        kt_p += kt_s 
        para_tree.paste(paraicdpokk, sen_now)
        stline += 1
        id_tackiopp += 1
    return para_tree, kt_p
        
        
        
def create_single_tree(path, file, attr):
    single_tree = Tree()
    single_tree.create_node(tag = file, identifier = file)
    kt_t = 0
    with open (path + '/' + file, 'r') as singletx:
        whtxt = singletx.readlines()
        # while('\n' in whtxt):
        #     whtxt.remove('\n')
        if(setting_name[0] in file):
            pre_para = []
            i = 0
            j = 0
            id = 0
            lenk = 0
            paraicdpokk = 0
            sen_para_use = []
            
            while(j < len(whtxt)):
                if(whtxt[j].replace('\n', '') in zx_par):
                    para_now = co_para(whtxt, i, j, pre_para, attr)
                    print(para_now)
                    if(para_now != True):
                        sen_tim = []
                        times = []
                        flag = 0
                        start = 0
                        end = 0
                        sen_times = 0
                        while(end  < len(para_now)):
                            if(para_now[start] == para_now[end] and end < len(para_now)):
                                flag += 1
                                end += 1
                            else:
                                sen_tim.append(para_now[start])
                                times.append(flag)
                                flag = 0
                                start = end
                        sen_tim.append(para_now[start])
                        times.append(flag)
                        print(sen_tim, times)
                        if(sen_tim == sen_para_use):
                            sen_times += 1
                            sen_para_use = sen_tim
                        else :
                            sen_para_use = sen_tim   
                            para_tree_gend, kt_p = create_para(whtxt, para_now, i, j, id, attr, paraicdpokk, sen_times, sen_tim, times)
                            kt_t += kt_p
                            single_tree.paste(file, para_tree_gend)
                            paraicdpokk += 1
                        pre_para = para_now
                    else: 
                        pre_para = []
                    i = j
                    j += 1
                else:
                    j += 1
        elif(setting_name[1] in file):
            pre_para = []
            i = 0
            j = 0
            id = 0
            lenk = 0
            paraicdpokk = 0
            sen_para_use = []
            
            while(j < len(whtxt)):
                if(whtxt[j].replace('\n', '') in hs_par):
                    para_now = co_para(whtxt, i, j, pre_para, attr)
                    print(para_now)
                    if(para_now != True):
                        sen_tim = []
                        times = []
                        flag = 0
                        start = 0
                        end = 0
                        sen_times = 0
                        while(end  < len(para_now)):
                            if(para_now[start] == para_now[end] and end < len(para_now)):
                                flag += 1
                                end += 1
                            else:
                                sen_tim.append(para_now[start])
                                times.append(flag)
                                flag = 0
                                start = end
                        sen_tim.append(para_now[start])
                        times.append(flag)
                        print(sen_tim, times)
                        if(sen_tim == sen_para_use):
                            sen_times += 1
                            sen_para_use = sen_tim
                        else :
                            sen_para_use = sen_tim   
                            para_tree_gend, kt_p = create_para(whtxt, para_now, i, j, id, attr, paraicdpokk, sen_times, sen_tim, times)
                            kt_t += kt_p
                            single_tree.paste(file, para_tree_gend)
                            paraicdpokk += 1
                        pre_para = para_now
                    else: 
                        pre_para = []
                    i = j
                    j += 1
                else:
                    j += 1
        elif(setting_name[2] in file):
            pre_para = []
            i = 0
            j = 0
            id = 0
            lenk = 0
            paraicdpokk = 0
            sen_para_use = []
            
            while(j < len(whtxt)):
                if(whtxt[j].replace('\n', '') in hw_par):
                    para_now = co_para(whtxt, i, j, pre_para, attr)
                    print(para_now)
                    if(para_now != True):
                        sen_tim = []
                        times = []
                        flag = 0
                        start = 0
                        end = 0
                        sen_times = 0
                        while(end  < len(para_now)):
                            if(para_now[start] == para_now[end] and end < len(para_now)):
                                flag += 1
                                end += 1
                            else:
                                sen_tim.append(para_now[start])
                                times.append(flag)
                                flag = 0
                                start = end
                        sen_tim.append(para_now[start])
                        times.append(flag)
                        print(sen_tim, times)
                        if(sen_tim == sen_para_use):
                            sen_times += 1
                            sen_para_use = sen_tim
                        else :
                            sen_para_use = sen_tim   
                            para_tree_gend, kt_p = create_para(whtxt, para_now, i, j, id, attr, paraicdpokk, sen_times, sen_tim, times)
                            kt_t += kt_p
                            single_tree.paste(file, para_tree_gend)
                            paraicdpokk += 1
                        pre_para = para_now
                    else: 
                        pre_para = []
                    i = j
                    j += 1
                else:
                    j += 1
        elif(setting_name[3] in file or setting_name[4] in file):
            pre_para = []
            i = 0
            j = 0
            id = 0
            lenk = 0
            paraicdpokk = 0
            sen_para_use = []
            
            while(j < len(whtxt)):
                if(whtxt[j].replace('\n', '') in sk_fh_par):
                    para_now = co_para(whtxt, i, j, pre_para, attr)
                    print(para_now)
                    if(para_now != True):
                        sen_tim = []
                        times = []
                        flag = 0
                        start = 0
                        end = 0
                        sen_times = 0
                        while(end  < len(para_now)):
                            if(para_now[start] == para_now[end] and end < len(para_now)):
                                flag += 1
                                end += 1
                            else:
                                sen_tim.append(para_now[start])
                                times.append(flag)
                                flag = 0
                                start = end
                        sen_tim.append(para_now[start])
                        times.append(flag)
                        print(sen_tim, times)
                        if(sen_tim == sen_para_use):
                            sen_times += 1
                            sen_para_use = sen_tim
                        else :
                            sen_para_use = sen_tim   
                            para_tree_gend, kt_p = create_para(whtxt, para_now, i, j, id, attr, paraicdpokk, sen_times, sen_tim, times)
                            kt_t += kt_p
                            single_tree.paste(file, para_tree_gend)
                            paraicdpokk += 1
                        pre_para = para_now
                    else: 
                        pre_para = []
                    i = j
                    j += 1
                else:
                    j += 1
    return single_tree, kt_t    