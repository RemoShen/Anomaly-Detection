from os import listdir
import joblib
from numpy import single
from create_tree import create_single_tree
from dataloader import ldk
from tf_df import attribute, document_frequency, get_files, tf_df
from tools import kkresu
from train_tree import vctpara
from tree_tools import svdic_tree
import csv

def main():
    path = 'load_file'
    ladk_path = 'key.txt'
    file_list = get_files(path)
    '''
        attr key 
    '''
    df = document_frequency(path, file_list)
    tf = tf_df(path, file_list)
    attribute(df,tf)
    kk = ldk(ladk_path)

def text():  
    path = 'load_file'
    attr = 'key.txt'
    ladk_path = listdir(path)
    file_len = 0 
    vc = []
    for file in ladk_path:
        single_tree, kt =  create_single_tree(path,file, attr)
        par_pra = vctpara(file, single_tree, kt) 
        todic = single_tree.to_dict()
        vc.append(par_pra)
        svnm = str(file_len) + '.txt'
        svdic_tree(todic, svnm)
        file_len += 1 
    with open('vc.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for item in vc:
            writer.writerow(item)
    csvfile.close()


main()
text()
kkresu()