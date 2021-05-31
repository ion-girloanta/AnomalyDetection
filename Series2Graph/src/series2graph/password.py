# -*- coding: utf-8 -*-
"""
Created on Sun May  2 18:09:45 2021

@author: ion_g
"""
import itertools
import zipfile
from tqdm import tqdm

zip_file = "d:/downloads/SourceCode (2).zip"
# initialize the Zip File object
zip_file = zipfile.ZipFile(zip_file)
# count the number of words in this wordlist

def foo(l, i):
     yield from itertools.product(*([l] * i)) 
s1='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for i in range(6):
   for x in foo('abcdefghijklmnopqrstuxywzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+{}[]?><', i + 1):
        print(''.join(x))
        try:
            zip_file.extractall(pwd=''.join(x))
        except:
            continue
        else:
            print("[+] Password found:", ''.join(x))
            exit(0)

