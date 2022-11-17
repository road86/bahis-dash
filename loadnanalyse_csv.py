# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:14:48 2022

@author: yoshka
"""

# with the import command, additional libraries can be used which can simplify the programming

import streamlit as st            # streamlit is a web publishing possibility
import pandas as pd               # pandas for datahandling
import os

st.set_page_config(layout="wide")  
colO, colN = st.columns(2)
with colO:
    oldpath="/old BAHIS data (form 30 April)/output/"

    #listold= [os.path.join(f) for (dirpath, dirnames, filenames) in os.walk(oldpath) for f in filenames]
    listold2=[]
    for (dirpath, dirnames, filenames) in os.walk(oldpath):
        for f in filenames:
             if os.path.splitext(f)[1] == '.csv':
                 listold2.append(os.path.join(f))

    listOData=pd.DataFrame()
    listOData['File']=listold2
    listOData['Elements']=[str(len(pd.read_csv(oldpath+i))) for i in listold2]
    st.dataframe(listOData)
    oldfile= st.selectbox("Old Files", listold2)
    olddata=pd.read_csv(oldpath + oldfile)
    columnheaderold=pd.DataFrame(olddata.columns.values.tolist(), columns = ['column_header'])
    st.dataframe(columnheaderold)
    st.write('Entries: ' + str(len(olddata)))


with colN:
    newpath="/new BAHIS data (July-Oct22)/"
    
    listnew= [os.path.join(f) for (dirpath, dirnames, filenames) in os.walk(newpath) for f in filenames]
    #listnew= [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(newpath) for f in filenames] # with complete path
    listnew2=[]
    for (dirpath, dirnames, filenames) in os.walk(newpath):
        for f in filenames:
             if os.path.splitext(f)[1] == '.csv':
                 listnew2.append(os.path.join(f))
     
    listNData=pd.DataFrame()
    listNData['File']=listnew2
    listNData['Elements']=[str(len(pd.read_csv(newpath+i))) for i in listnew2]
    st.dataframe(listNData)
    newfile=st.selectbox("New Files", listnew2)
    newdata=pd.read_csv(newpath + newfile)
    columnheadernew=pd.DataFrame(newdata.columns.values.tolist(), columns = ['column_header'])
    st.dataframe(columnheadernew)
    st.write('Entries: ' + str(len(newdata)))


