# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 22:51:14 2022

@author: ATA
"""
def Frequencies():
    """ function to read word_count text file and return a dictionary 
    that contains words as key as well as word frequencies as value"""
    
    try:
        fhand = open('C:\\Users\\ATA\\Documents\\UCSD\\CSE 250A\\HW1\\hw1_word_counts_05.txt')
    except:
        print ('the file does not exist')
        
    d = dict()    
    for line in fhand:
                                 
        words = line.split()
        if len(words[0]) == 5 and words[0] not in d:
            d[words[0]] = float(words[1])
    
    total = sum(d.values())

    for words in d.keys(): 
        d[words] /= total 
        
    return d


if __name__ == "__main__" :
    
    d = Frequencies()
    print ("forteen least frequent words:")
    print(sorted(d, key = d.__getitem__)[0:14] )                              

    print ("fifteen most frequent words:")
    print(sorted(d, key = d.__getitem__)[-15:] )