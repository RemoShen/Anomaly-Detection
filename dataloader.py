
'''
    loader attr to create tree 
'''

def ldk(attr):
    '''
        attr is the path of the file saving 
        the key words that achived from all of 
        the setting files whose tf & df are both high
         
    '''
    with open(attr, 'r') as f:
        file_txt = f.read()
    return file_txt.split()