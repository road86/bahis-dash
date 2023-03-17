# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 08:00:17 2023

@author: yoshka
"""
import mmap
import pandas as pd
import re

def savfile(tmp):
    if len(tmp)==1:
        sstr=tmp[0]
        sstr=sstr[10:]
        cutfilename=sstr[:sstr.find(' ')]
        startinfo=sstr.find('(')+1
        endinfo=sstr.rfind(')')
        data=sstr[startinfo:endinfo]
        words=data.split(', ')
        df= pd.DataFrame(columns=words)
    if len(tmp)>1:
        for sstr in tmp:    
            if sstr[:4]=='COPY':
                sstr=sstr[10:]
                cutfilename=sstr[:sstr.find(' ')]
                startinfo=sstr.find('(')+1
                endinfo=sstr.rfind(')')
                data=sstr[startinfo:endinfo]
                words=data.split(', ')
                df= pd.DataFrame(columns=words)
            elif sstr[:4]!='COPY':
                slis=re.split(r'\t+',sstr)
                df=df.append(pd.DataFrame([slis], columns=words))
        
    df.to_csv('C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/coredb_bk_230316/' + cutfilename + '.csv')

tmp=[]
with open(r'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/coredb_bk_230316/coredb_bk_230316.sql', 'rb', 0) as file:
#with open(r'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/coredb_bk_230316/tst.sql', 'rb', 0) as file:
    s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    #print(s.size())
    s.seek(0)
    s.seek(s.find(b'COPY core')-0) 
    pointer=s.tell()      
    s.seek(pointer)
    while s.tell()<1029994832+1:
        stop=s.find(b'\.')-0 
        if s.tell()<stop:
            line=s.readline().decode('utf-8')
            tmp.append(line) #.split(' '))
        elif s.tell()>=stop:
            savfile(tmp)
            tmp=[]
            s.seek(s.find(b'COPY core')-0) 
            pointer=s.tell()      
            s.seek(pointer)

# fd = open('C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/coredb_bk_230316/tst.sql', 'r', encoding="utf-8")
# sqlFile = fd.read()

# del fd
