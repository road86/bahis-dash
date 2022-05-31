# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:50:50 2022

@author: yoshka
"""

# References: https://docs.streamlit.io/library/get-started

# Install: conda install streamlit
# Run: streamlit run NAME.py

import streamlit as st

st.sidebar.write('sidebar.write')

st.title('title')
st.header('header')
st.subheader('subheader')
st.write('write')
st.caption('caption')

col1, col2 = st.columns(2)
col1.header('Column1')
col1.write('Text below Column1')
col2.header('Column2')
col2.write('Text below Column2')

st.checkbox('Checkbox')
st.radio('Radio', ('1', '2'))
st.selectbox("SelectBox",('Choice 1', 'Choice 2'))
st.slider("Slider with Values", value=(1, 15))

st.metric(label="Infections", value="200", delta="2")

st.line_chart([0,5])