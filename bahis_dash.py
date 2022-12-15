# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:14:48 2022

@author: yoshka
"""

# with the import command, additional libraries can be used which can simplify the programming

import streamlit as st            # streamlit is a web publishing possibility
#import matplotlib.pyplot as plt
import pandas as pd               # pandas for datahandling
import plotly.express as px       #
import altair as alt              # altair for graphs
import json                       # json file format to import geodata
from datetime import datetime, timedelta

gifpath = 'logos/'
sourcepath = 'exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
sourcefilename =sourcepath + 'preped_data2.csv'
path0= "geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # found shapefiles from the data.humdata.org
path1= "geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
path2= "geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
path3= "geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
path4= "geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union

img_logo= 'logos/Logo.png'
st.set_page_config(layout="wide")                            # streamlit commands addressed with st (see import)
st.image(img_logo, width=400)

st.title('BAHIS dashboard')
   
tabs_font_css = """
<style>
button[data-baseweb="tab"] {
  font-size: 26px;
  font-weight: bold;
}
</style>
"""

st.write(tabs_font_css, unsafe_allow_html=True)

@st.cache
def fetchgeodata():
    return pd.read_csv(geofilename)
bahis_geodata= fetchgeodata()

@st.cache
def fetchsourcedata():
    bahis_sd = pd.read_csv(sourcefilename)
    bahis_sd['basic_info_division'] = pd.to_numeric(bahis_sd['basic_info_division'])
    bahis_sd['basic_info_district'] = pd.to_numeric(bahis_sd['basic_info_district'])
    bahis_sd['basic_info_upazila'] = pd.to_numeric(bahis_sd['basic_info_upazila'])
    bahis_sd['basic_info_date'] = pd.to_datetime(bahis_sd['basic_info_date'])
    return bahis_sd
bahis_sourcedata= fetchsourcedata()

# FILTER: get all data from 1.1.2019 
bahis_sourcedata=bahis_sourcedata.loc[bahis_sourcedata['basic_info_date']>=pd.to_datetime("20190101")]
start_date=min(bahis_sourcedata['basic_info_date']).date()
end_date=max(bahis_sourcedata['basic_info_date']).date()
dates=[start_date, end_date]

def show_metrics():
    bahis_sourcedata['basic_info_date']=pd.to_datetime(bahis_sourcedata.basic_info_date).dt.tz_localize(None).astype('datetime64[ns]')
    mask=(bahis_sourcedata['basic_info_date']> datetime.now()-timedelta(days=30)) & (bahis_sourcedata['basic_info_date'] < datetime.now())
    colInd0, colInd1, colInd2, colInd3 = st.columns(4)
    with colInd0:
        st.header('National numbers:')
    with colInd1:
        tmp_sub_data=bahis_sourcedata['basic_info_date'].loc[mask]
        diff=tmp_sub_data.shape[0]
        st.metric('cumulated reports and last 30 days reports in green', value=f"{bahis_sourcedata.shape[0]:,}", delta=diff)
    with colInd2:
        tmp_sub_data=bahis_sourcedata['patient_info_sick_number'].loc[mask]
        diffsick=int(tmp_sub_data.sum().item())
        st.metric('total reported sick animals and last 30 days in green', value=f"{int(bahis_sourcedata['patient_info_sick_number'].sum()):,}", delta= diffsick)  # less by one compared to libreoffice...?
    with colInd3:
        tmp_sub_data=bahis_sourcedata['patient_info_dead_number'].loc[mask]
        diffdead=int(tmp_sub_data.sum().item())
        st.metric('total reported dead animals and last 30 days in green', value=f"{int(bahis_sourcedata['patient_info_dead_number'].sum()):,}", delta = diffdead)
show_metrics()

takes_too_long=False

def set_dates():
    #st.header('Please select the date range for the following reports')
    colsdate, coledate, colplaceholder = st.columns([1,1,3])
    with colsdate:
        sdate= st.date_input('Select beginning date of report', value= start_date, min_value= start_date, max_value= end_date, key='sdate')
    with coledate:
        edate= st.date_input('Select ending date of report', value= end_date, min_value= start_date, max_value= end_date, key='edate')
    dates=[sdate, edate]
    st.subheader("Currently selected Date range: From " + str(dates[0]) + " until " + str(dates[1]))
    return (bahis_sourcedata['basic_info_date']>= pd.to_datetime(dates[0])) & (bahis_sourcedata['basic_info_date'] <= pd.to_datetime(dates[1]))
tmask=set_dates()

@st.cache
def date_subset():
    return bahis_sourcedata.loc[tmask]
sub_bahis_sourcedata=date_subset()

#@st.cache
def open_data(path):
    with open(path) as f:
        data = json.load(f)
        return data

#tabRep, tabDis, tabHeat, tabMonthComp, tabRepCase = st.tabs(['Reports', 'Diseases', 'Heat Map', 'Monthly Comparison', 'Disease reporting-case numbers'])
tabRep, tabHeat = st.tabs(['Reports', 'Heat Map'])

@st.cache
def pull_diseaselist():
    dislis= bahis_sourcedata['top_diagnosis'].unique()
    dislis= pd.DataFrame(dislis, columns=['Disease'])
    return dislis.sort_values(by=['Disease'])
diseaselist= pull_diseaselist()

def plot_map(path, loc, subd_bahis_sourcedata, title, pname, splace, variab, labl):
    subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]
    reports = subd_bahis_sourcedata[title].value_counts().to_frame()
    reports[pname] = reports.index
    reports= reports.loc[reports[pname] != 'nan']    
    data = open_data(path)
    for i in range(reports.shape[0]):
        reports[pname].iloc[i] = subDist.loc[subDist['value']==int(reports[pname].iloc[i]),'name'].iloc[0]
    reports[pname]=reports[pname].str.title()                   
    for i in data['features']:
        i['id']= i['properties']['shapeName'].replace(splace,"")

    fig = px.choropleth_mapbox(reports, geojson=data, locations=pname, color=title,
                            #color_continuous_scale="Viridis",
                            color_continuous_scale="YlOrBr",
                            range_color=(0, reports[title].max()),
                            mapbox_style="carto-positron",
                            zoom=6, center = {"lat": 23.7, "lon": 90},
                            opacity=0.9,
                            labels={variab:labl}
                          )
    fig.update_layout(autosize=True, width= 1000, height=600, margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale= False)
    return fig

def rep_plot(loc, subd_bahis_sourcedata, title, find):
    subDist= bahis_geodata[(bahis_geodata["loc_type"]==loc)]     
    geocodehit= subDist.loc[subDist['name'].str.capitalize()==find]['value']
    subs_bahis_sourcedata= subd_bahis_sourcedata.loc[subd_bahis_sourcedata[title]==int(geocodehit)]

    if subs_bahis_sourcedata.empty:
        st.write('no data')
    else: 
        tmp=subs_bahis_sourcedata['basic_info_date'].dt.date.value_counts()
        tmp=tmp.reset_index()
        tmp=tmp.rename(columns={'index':'date'})
        tmp['date'] = pd.to_datetime(tmp['date'])
        tots= str(subs_bahis_sourcedata.shape[0])
        
        line_chart= alt.Chart(tmp, height=600).mark_line(point=alt.OverlayMarkDef(color="red")).encode( #interpolate='basis').encode(
            alt.X('date:T', title='report date'),
            alt.Y('basic_info_date:Q', title='reports'),
            color=alt.Color('Category:N', legend=None)
            ).properties(title='Registered reports :  ' + tots)
        st.altair_chart(line_chart, use_container_width=True)
        
def dis_plot(loc, subd_bahis_sourcedata, title, find):
    subDist= bahis_geodata[(bahis_geodata["loc_type"]==loc)]     
    geocodehit= subDist.loc[subDist['name'].str.capitalize()==find]['value']
    subs_bahis_sourcedata= subd_bahis_sourcedata.loc[subd_bahis_sourcedata[title]==int(geocodehit)]
    if subs_bahis_sourcedata.empty:
        st.write('no data')
    else: 
        tmp=subs_bahis_sourcedata['patient_info_sick_number'].groupby(subd_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum()
        tmp=tmp.reset_index()
        tmp=tmp.rename(columns={'basic_info_date':'date'})
        tmp['date']=tmp['date'].astype(str)
        tmp['date'] = pd.to_datetime(tmp['date'])
        tots= str(int(subs_bahis_sourcedata['patient_info_sick_number'].sum()))
     
        st.subheader('Registered sick animals')                   
        line_chart= alt.Chart(tmp, height=250).mark_line(point=alt.OverlayMarkDef(color="red")).encode( #interpolate='basis').encode(
            alt.X('date:T', title='report date'),
            alt.Y('patient_info_sick_number:Q', title='reports'),
            color=alt.Color('Category:N', legend=None)
            ).properties(title='Registered sick animals :  ' + tots)
        st.altair_chart(line_chart, use_container_width=True)
        
        tmp=subs_bahis_sourcedata['patient_info_dead_number'].groupby(subd_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum()
        tmp=tmp.reset_index()
        tmp=tmp.rename(columns={'basic_info_date':'date'})
        tmp['date']=tmp['date'].astype(str)
        tmp['date'] = pd.to_datetime(tmp['date'])
        tots= str(int(subs_bahis_sourcedata['patient_info_dead_number'].sum()))
        
        st.subheader('Registered dead animals')                    
        line_chart= alt.Chart(tmp, height=250).mark_line(point=alt.OverlayMarkDef(color="red")).encode( #interpolate='basis').encode(
            alt.X('date:T', title='report date'),
            alt.Y('patient_info_dead_number:Q', title='reports'),
            color=alt.Color('Category:N', legend=None)
            ).properties(title='Registered dead animals :  ' + tots)
        st.altair_chart(line_chart, use_container_width=True)

def MC_plot(loc, subd_bahis_sourcedata, title, find):
    st.subheader('Registered sick animals')
    subDist= bahis_geodata[(bahis_geodata["loc_type"]==loc)]     
    geocodehit= subDist.loc[subDist['name'].str.capitalize()==find]['value']
    subs_bahis_sourcedata= subd_bahis_sourcedata.loc[subd_bahis_sourcedata[title]==int(geocodehit)]
    if subs_bahis_sourcedata.empty:
        st.write('no data')
    else: 
        tmp=subs_bahis_sourcedata['patient_info_sick_number'].groupby(subd_bahis_sourcedata['basic_info_date'].dt.to_period('M')).sum()
        tmp=tmp.reset_index()
        tmp=tmp.rename(columns={'basic_info_date':'date'})
        tmp['date']=tmp['date'].astype(str)
        tmp['date'] = pd.to_datetime(tmp['date'])
        tots= str(int(subs_bahis_sourcedata['patient_info_sick_number'].sum()))
        tmpdata={'sick':tmp['patient_info_sick_number'],
                  'date':tmp['date']}
        tmpdata=pd.DataFrame(tmpdata)
        bar_chart= alt.Chart(tmpdata, height=460).mark_bar().encode(
              alt.Column('month(date):N', ),
              alt.X('year(date):O', title='', scale=alt.Scale(8), axis=alt.Axis(labels=False, ticks=False)),
              alt.Y('sick:Q', title='reports'),
              alt.Color('year(date):O', scale=alt.Scale(scheme='dark2'),),
              ).properties(title='Registered sick animals :  ' + tots)
        st.altair_chart(bar_chart) 

def CN_plot(loc, subd_bahis_sourcedata, title, find):
    subDist= bahis_geodata[(bahis_geodata["loc_type"]==loc)]     
    geocodehit= subDist.loc[subDist['name'].str.capitalize()==find]['value']
    subs_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata[title]==int(geocodehit)]
    if subs_bahis_sourcedata.empty:
        st.write('no data')
    else: 
        poultry=['Chicken', 'Duck', 'Goose', 'Pegion', 'Quail', 'Turkey']
        sub_bahis_sourcedataP=subs_bahis_sourcedata[subs_bahis_sourcedata['species'].isin(poultry)]
        tmp= sub_bahis_sourcedataP.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
        tmp=tmp.sort_values(by='species', ascending=False)
        tmp=tmp.rename({'species' : 'counts'}, axis=1)
        tmp=tmp.head(10)
        line_chart= alt.Chart(tmp, height=300).mark_bar().encode(
            x='counts:Q',
            y=alt.Y('top_diagnosis:O', sort='-x')
            ).properties(title='Poultry Related Diseases')
        st.altair_chart(line_chart, use_container_width=True)             
        
        lanimal=['Buffalo', 'Cattle', 'Goat', 'Sheep']
        sub_bahis_sourcedataLA=subs_bahis_sourcedata[subs_bahis_sourcedata['species'].isin(lanimal)] 
        tmp= sub_bahis_sourcedataLA.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
        tmp=tmp.sort_values(by='species', ascending=False)
        tmp=tmp.rename({'species' : 'counts'}, axis=1)
        tmp=tmp.head(10)
        line_chart= alt.Chart(tmp, height=300).mark_bar().encode(
            x='counts:Q',
            y=alt.Y('top_diagnosis:O', sort='-x')
            ).properties(title='Large Animal Related Diseases')
        st.altair_chart(line_chart, use_container_width=True) 
        
def heat_map(path, loc, title, nname, repstr, labv, labt):
        #path= path1
        subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]
        reports = subd_bahis_sourcedata[title].value_counts().to_frame()
        reports[nname] = reports.index
        reports= reports.loc[reports[nname] != 'nan']
    
        data = open_data(path)
        for i in data['features']:
            i['id']= i['properties']['shapeName'].replace(" Division","")
        for i in range(reports.shape[0]):
            reports[nname].iloc[i] = subDist.loc[subDist['value']==int(reports[nname].iloc[i]),'name'].iloc[0]
        reports=reports.sort_values(nname)
        reports[nname]=reports[nname].str.capitalize()
        colMap, colBar = st.columns([1,2])
        with colMap:
            for i in data['features']:
                i['id']= i['properties']['shapeName'].replace(repstr,"")
    
            fig = px.choropleth_mapbox(reports, geojson=data, locations=nname, color=title,
                                    color_continuous_scale="YlOrBr",
                                    range_color=(0, reports[title].max()),
                                    mapbox_style="carto-positron",
                                    zoom=5.6, center = {"lat": 23.7, "lon": 90},
                                    opacity=0.9,
                                    labels={labv:labt}
                                  )
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        with colBar:
            fig=px.bar(reports, x=nname, y=title, labels= {labv:labt})# ,color='basic_info_division')
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

with tabRep:
    region_placeholder=st.empty()
    subDist = bahis_geodata[(bahis_geodata["loc_type"]==1)]['name']
    colph1, colph2, colph3 = st.columns(3)
    with colph1:
        itemlistDiseases=pd.concat([pd.Series(['Select All'], name='Disease'),diseaselist.squeeze()])
        disease_chosen_R= st.multiselect('Disease', itemlistDiseases, key='repDis')    

    if not takes_too_long:
        if 'Select All' in disease_chosen_R:
            subd_bahis_sourcedata=sub_bahis_sourcedata 
        else:
            subd_bahis_sourcedata=sub_bahis_sourcedata[sub_bahis_sourcedata['top_diagnosis'].isin(disease_chosen_R)] 
        
        if disease_chosen_R:
            
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                itemlistDiv=pd.concat([pd.Series(['Select'], name='name'),bahis_geodata[(bahis_geodata["loc_type"]==1)]['name'].str.capitalize()])
                findDiv = st.selectbox('Divsion', itemlistDiv, key = 'DivR')
            if findDiv != 'Select':
                indexDiv= subDist[subDist==findDiv.upper()].index[0]
                disList = bahis_geodata[bahis_geodata['parent']==int(bahis_geodata.iloc[[indexDiv]]['value'])]['name'].str.capitalize()
                itemlistDis=pd.concat([pd.Series(['Select'], name='name'),disList])
            with col2:
                if findDiv != 'Select':        
                    findDis= st.selectbox('District', itemlistDis, key = 'DisR')    
                    if findDis != 'Select':
                        indexDis= disList[disList==findDis].index[0]
                        upaList = bahis_geodata[bahis_geodata['parent']==int(bahis_geodata.iloc[[indexDis]]['value'])]['name'].str.capitalize()
                        itemlistUpa=pd.concat([pd.Series(['Select'], name='name'),upaList])
                else:
                    findDis = st.selectbox('District', ['Select'], key = 'DisR')

            with col3:
                if findDiv!= 'Select':
                    if findDis != 'Select':
                        findUpa= st.selectbox('Upazila', itemlistUpa, key = 'UpaR')
                        if findUpa != 'Select':
                            indexUpa = upaList[upaList==findUpa].index[0]
                            Upazila= int(bahis_geodata.iloc[[indexUpa]]['value'])
                    else:
                        findUpa = st.selectbox('Upazila', ['Select'], key = 'UpaR')
                else:
                    findUpa = st.selectbox('Upazila', ['Select'], key = 'UpaR')
        
            if findDiv == 'Select':
                colMap, colBars= st.columns([1,2])
                region_placeholder.header('Report Dynamics for: Bangladesh')
                with colMap:
                    overview = st.checkbox("Checked for overall view - Unchecked for clustered map" , key = 'togR')
                    if overview:
                        path= path0
                        subDist=bahis_geodata
                        data = open_data(path)
                        for i in data['features']:
                            i['id']= i['properties']['shapeName'].replace(" District","")
                        fig = px.choropleth_mapbox(data['features'],
                                               geojson=data,
                                               locations='id',
                                               mapbox_style="carto-positron",
                                               zoom=6,
                                               center = {"lat": 23.7, "lon": 90},
                                               opacity=0.5
                                              )
                        fig.update_layout(autosize=True, width= 1000, height=600, margin={"r":0,"t":0,"l":0,"b":0}, showlegend= False)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        loc=1
                        title='basic_info_division'
                        pname='divisionname'
                        splace=(' Division')
                        variab=('division')
                        labl=('Incidences per division')
                        fig = plot_map(path1, loc, subd_bahis_sourcedata, title, pname, splace, variab, labl)
                        st.plotly_chart(fig, use_container_width=True)
                with colBars:
                    tabR, tabD, tabMC, tabCN = st.tabs(['Reports', 'Diseased Animals', 'Monthly Comparison', 'Disease Case Numbers'])
                    with tabR:
                        tmp=subd_bahis_sourcedata['basic_info_date'].dt.date.value_counts()
                        tmp=tmp.reset_index()
                        tmp=tmp.rename(columns={'index':'date'})
                        tmp['date'] = pd.to_datetime(tmp['date'])    
                        tots= str(sub_bahis_sourcedata.shape[0])
                        
                        tmp2w= tmp
                        line_chart= alt.Chart(tmp2w, height=600).mark_line(point=alt.OverlayMarkDef(color="red")).encode( #interpolate='basis').encode(
                            alt.X('date:T', title='report date', axis= alt.Axis(format='%Y %B %d')), # scale= alt.Scale(nice={'interval': 'week', 'step': 4})), 
                            alt.Y('basic_info_date:Q', title='reports'),
                            color=alt.Color('Category:N', legend=None)
                            ).properties(title='Registered reports :  ' + tots)
                        st.altair_chart(line_chart, use_container_width=True)
                    with tabD:
                        st.subheader('Registered sick animals')
                        
                        tmp=subd_bahis_sourcedata['patient_info_sick_number'].groupby(subd_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum()
                        tmp=tmp.reset_index()
                        tmp=tmp.rename(columns={'basic_info_date':'date'})
                        tmp['date']=tmp['date'].astype(str)
                        tmp['date'] = pd.to_datetime(tmp['date'])
                        tots= str(int(subd_bahis_sourcedata['patient_info_sick_number'].sum()))
                        
                        line_chart= alt.Chart(tmp, height=250).mark_line(point=alt.OverlayMarkDef(color="red")).encode( #interpolate='basis').encode(
                            alt.X('date:T', title='report date'),
                            alt.Y('patient_info_sick_number:Q', title='reports'),
                            color=alt.Color('Category:N', legend=None)
                            ).properties(title='Registered sick animals :  ' + tots)
                        st.altair_chart(line_chart, use_container_width=True)
                        
                        st.subheader('Registered dead animals')            
                        tmp=subd_bahis_sourcedata['patient_info_dead_number'].groupby(subd_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum()
                        tmp=tmp.reset_index()
                        tmp=tmp.rename(columns={'basic_info_date':'date'})
                        tmp['date']=tmp['date'].astype(str)
                        tmp['date'] = pd.to_datetime(tmp['date'])
                        tots= str(int(subd_bahis_sourcedata['patient_info_dead_number'].sum()))
                        
                        line_chart= alt.Chart(tmp, height=250).mark_line(point=alt.OverlayMarkDef(color="red")).encode( #interpolate='basis').encode(
                            alt.X('date:T', title='report date'),
                            alt.Y('patient_info_dead_number:Q', title='reports'),
                            color=alt.Color('Category:N', legend=None)
                            ).properties(title='Registered dead animals :  ' + tots) 
                        st.altair_chart(line_chart, use_container_width=True)
                    with tabMC:
                        st.subheader('Registered sick animals')
                        tmp=subd_bahis_sourcedata['patient_info_sick_number'].groupby(subd_bahis_sourcedata['basic_info_date'].dt.to_period('M')).sum()
                        tmp=tmp.reset_index()
                        tmp=tmp.rename(columns={'basic_info_date':'date'})
                        tmp['date']=tmp['date'].astype(str)
                        tmp['date'] = pd.to_datetime(tmp['date'])
                        tots= str(int(subd_bahis_sourcedata['patient_info_sick_number'].sum()))
                        tmpdata={'sick':tmp['patient_info_sick_number'],
                                  'date':tmp['date']}
                        tmpdata=pd.DataFrame(tmpdata)
                        bar_chart= alt.Chart(tmpdata, height=460).mark_bar().encode(
                              alt.Column('month(date):N', ),
                              alt.X('year(date):O', title='', scale=alt.Scale(8), axis=alt.Axis(labels=False, ticks=False)),
                              alt.Y('sick:Q', title='reports'),
                              alt.Color('year(date):O', scale=alt.Scale(scheme='dark2'),),
                              ).properties(title='Registered sick animals :  ' + tots)
                        st.altair_chart(bar_chart) #, use_container_width=True)
                    with tabCN:
                        poultry=['Chicken', 'Duck', 'Goose', 'Pegion', 'Quail', 'Turkey']
                        sub_bahis_sourcedataP=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(poultry)] 
                        tmp= sub_bahis_sourcedataP.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
                        tmp=tmp.sort_values(by='species', ascending=False)
                        tmp=tmp.rename({'species' : 'counts'}, axis=1)
                        tmp=tmp.head(10)
                        line_chart= alt.Chart(tmp, height=300).mark_bar().encode(
                            x='counts:Q',
                            y=alt.Y('top_diagnosis:O', sort='-x')
                            ).properties(title='Poultry Related Diseases')
                        st.altair_chart(line_chart, use_container_width=True)             
                        lanimal=['Buffalo', 'Cattle', 'Goat', 'Sheep']
                        sub_bahis_sourcedataLA=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(lanimal)] 
                        tmp= sub_bahis_sourcedataLA.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
                        tmp=tmp.sort_values(by='species', ascending=False)
                        tmp=tmp.rename({'species' : 'counts'}, axis=1)
                        tmp=tmp.head(10)
                        line_chart= alt.Chart(tmp, height=300).mark_bar().encode(
                            x='counts:Q',
                            y=alt.Y('top_diagnosis:O', sort='-x')
                            ).properties(title='Large Animal Related Diseases')
                        st.altair_chart(line_chart, use_container_width=True)  
                        
            if (findDiv != 'Select') and (findDis == 'Select'):
                colMap, colBar = st.columns([1,2])
                region_placeholder.header('Report Dynamics for: ' + findDiv.capitalize())
                with colMap:
                    overview = st.checkbox("Toggle: Overview Map - Clustered Map" , key = 'togR')
                    if overview:
                        subDist= bahis_geodata[(bahis_geodata["loc_type"]==1)]     
                        geocodehit= subDist.loc[subDist['name'].str.capitalize()==findDiv]['value']
                        subs_bahis_sourcedata= subd_bahis_sourcedata.loc[subd_bahis_sourcedata['basic_info_division']==int(geocodehit)]
                        if subs_bahis_sourcedata.empty:
                            st.write('no data')
                        else:  
                            loc=1
                            title='basic_info_division'
                            pname='divisionname'
                            splace=' Division' 
                            variab='division'
                            labl='Incidences per division'
                            fig = plot_map(path1, loc, subs_bahis_sourcedata, title, pname, splace, variab, labl)
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        subDist=bahis_geodata[(bahis_geodata["loc_type"]==1)]
                        geocodehit= subDist.loc[subDist['name'].str.capitalize()==findDiv]['value']
                        subs_bahis_sourcedata= subd_bahis_sourcedata.loc[subd_bahis_sourcedata['basic_info_division']==int(geocodehit)]
                        if subs_bahis_sourcedata.empty:
                            st.write('no data')
                        else:             
                            loc=2
                            title='basic_info_district'
                            pname='districtname'
                            splace=' District'
                            variab='district'
                            labl='Incidences per district'
                            fig = plot_map(path2, loc, subs_bahis_sourcedata, title, pname, splace, variab, labl)
                            st.plotly_chart(fig, use_container_width=True)
                        
                with colBar:
                    loc=1
                    title='basic_info_division'
                    find=findDiv
                    tabR, tabD, tabMC, tabCN = st.tabs(['Reports', 'Diseased Animals', 'Monthly Comparison', 'Disease Case Numbers'])
                    with tabR:
                        rep_plot(loc, subd_bahis_sourcedata, title, find)
                    with tabD:
                        dis_plot(loc, subd_bahis_sourcedata, title, find)
                    with tabMC:
                        MC_plot(loc, subd_bahis_sourcedata, title, find)
                    with tabCN:
                        CN_plot(loc, subd_bahis_sourcedata, title, find)   


            if (findDiv != 'Select') and (findDis != 'Select') and (findUpa =='Select'):
                colMap, colBar = st.columns([1,2])
                with colMap:
                    overview = st.checkbox("Toggle: Overview Map - Clustered Map", key = 'togR')
                    if overview:
                        subDist= bahis_geodata[(bahis_geodata["loc_type"]==2)]     
                        geocodehit= subDist.loc[subDist['name'].str.capitalize()==findDis]['value']
                        subs_bahis_sourcedata= subd_bahis_sourcedata.loc[subd_bahis_sourcedata['basic_info_district']==int(geocodehit)]
                        if subs_bahis_sourcedata.empty:
                            st.write('no data')
                        else:
                            loc=2
                            title='basic_info_district'
                            pname='districtname'
                            splace=' District'
                            variab='district'
                            labl='Incidences per district'
                            fig = plot_map(path2, loc, subs_bahis_sourcedata, title, pname, splace, variab, labl)
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        subDist=bahis_geodata[(bahis_geodata["loc_type"]==2)]
                        geocodehit= subDist.loc[subDist['name'].str.capitalize()==findDis]['value']
                        subs_bahis_sourcedata= subd_bahis_sourcedata.loc[subd_bahis_sourcedata['basic_info_district']==int(geocodehit)]               
                        if subs_bahis_sourcedata.empty:
                            st.write('no data')
                        else:          
                            loc=3
                            title='basic_info_upazila'
                            pname='upazilaname'
                            splace=' Upazila'
                            variab='upazila'
                            labl='Incidences per upazila'
                            fig = plot_map(path3, loc, subs_bahis_sourcedata, title, pname, splace, variab, labl)
                            st.plotly_chart(fig, use_container_width=True)
                        
                with colBar:
                    loc=2
                    title='basic_info_district'
                    find=findDis
                    tabR, tabD, tabMC, tabCN = st.tabs(['Reports', 'Diseased Animals', 'Monthly Comparison', 'Disease Case Numbers'])
                    with tabR:
                        rep_plot(loc, subd_bahis_sourcedata, title, find)
                    with tabD:
                        dis_plot(loc, subd_bahis_sourcedata, title, find)
                    with tabMC:
                        MC_plot(loc, subd_bahis_sourcedata, title, find)
                    with tabCN:
                        CN_plot(loc, subd_bahis_sourcedata, title, find)   

            if (findDiv != 'Select') and (findDis != 'Select') and (findUpa !='Select'):
                   colMap, colBar = st.columns([1,2])
                   region_placeholder.header('Report Dynamics for: ' + findUpa.capitalize())
                   with colMap:
                           overview = st.checkbox("Toggle: Overview Map - Clustered Map", disabled= True, key = 'togR')
                           subDist= bahis_geodata[(bahis_geodata["loc_type"]==3)]     
                           geocodehit= subDist.loc[subDist['name'].str.capitalize()==findUpa]['value']
                           subs_bahis_sourcedata= subd_bahis_sourcedata.loc[subd_bahis_sourcedata['basic_info_upazila']==int(geocodehit)]
                           if subs_bahis_sourcedata.empty:
                               st.write('no data')
                           else:  
                               loc=3
                               title='basic_info_upazila'
                               pname='upazilaname'
                               splace=' Upazila'
                               variab='upazila'
                               labl='Incidences per upazila'
                               fig = plot_map(path3, loc, subs_bahis_sourcedata, title, pname, splace, variab, labl)
                               st.plotly_chart(fig, use_container_width=True) 
                   with colBar:
                        loc=3
                        title='basic_info_upazila'
                        find=findUpa
                        tabR, tabD, tabMC, tabCN = st.tabs(['Reports', 'Diseased Animals', 'Monthly Comparison', 'Disease Case Numbers'])
                        with tabR:
                           rep_plot(loc, subd_bahis_sourcedata, title, find)
                        with tabD:
                            dis_plot(loc, subd_bahis_sourcedata, title, find)
                        with tabMC:
                            MC_plot(loc, subd_bahis_sourcedata, title, find)             
                        with tabCN:
                            CN_plot(loc, subd_bahis_sourcedata, title, find)

with tabHeat:
    disease_placeholder=st.empty()
    subDist = bahis_geodata[(bahis_geodata["loc_type"]==1)]['name']  
    st.header('Please select disease(s) for the report:')
    colph1, colph2, colph3 = st.columns(3)
    with colph1:
        itemlistDiseases=pd.concat([pd.Series(['Select All'], name='Disease'),diseaselist.squeeze()])
        disease_chosen_H= st.multiselect('Disease', itemlistDiseases, key= 'HeatDisC')

    if 'Select All' in disease_chosen_H:
        subd_bahis_sourcedata=sub_bahis_sourcedata 
    else:
        subd_bahis_sourcedata=sub_bahis_sourcedata[sub_bahis_sourcedata['top_diagnosis'].isin(disease_chosen_H)] 

    if disease_chosen_H:
        disease_placeholder.header('Heat Map for: ' + ', '.join(disease_chosen_H))
        st.subheader('Please select geographic resolution for the report:')
        colph1, colph2, colph3 = st.columns(3)
        with colph1:
            values = ['0: Nation' , '1: Division', '2: District', '3: Upazila']
            defaultV = values.index('0: Nation')  # default value
            granularity= st.selectbox('Select level', values, index=defaultV, key='HeatGran') #, horizontal= True)
    
        if granularity=='0: Nation':
            path= path0
            subDist=bahis_geodata
            data = open_data(path)
        
            colMap, colBar = st.columns([1,2])
            with colMap:                           # map chart with visits
                data = open_data(path)
        
                for i in data['features']:
                    i['id']= i['properties']['shapeName'].replace(" District","")
        
                fig = px.choropleth_mapbox(data['features'],
                                       geojson=data,
                                       locations='id',
                                       mapbox_style="carto-positron",
                                       zoom=5.6,
                                       center = {"lat": 23.7, "lon": 90},
                                       opacity=0.5
                                      )
                fig.update_layout(autosize=True, width= 1000, height=500, margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig, use_container_width=True)
        
            with colBar:                         # in numbers
                st.metric(label= 'Reports', value= subd_bahis_sourcedata.shape[0] )
            
        if granularity=='1: Division':
            loc=1
            title='basic_info_division'
            nname='divisionname'
            repstr=" Division"
            labv= 'division'           
            labt='Incidences per division'
            heat_map(path1, loc, title, nname, repstr, labv, labt)
            # path= path1
            # subDist=bahis_geodata[(bahis_geodata["loc_type"]==1)]
            # reports = subd_bahis_sourcedata['basic_info_division'].value_counts().to_frame()
            # reports['divisionname'] = reports.index
            # reports= reports.loc[reports['divisionname'] != 'nan']
        
            # data = open_data(path)
            # for i in data['features']:
            #     i['id']= i['properties']['shapeName'].replace(" Division","")
            # for i in range(reports.shape[0]):
            #     reports['divisionname'].iloc[i] = subDist.loc[subDist['value']==int(reports['divisionname'].iloc[i]),'name'].iloc[0]
            # reports=reports.sort_values('divisionname')
            # reports['divisionname']=reports['divisionname'].str.capitalize()
            # colMap, colBar = st.columns([1,2])
            # with colMap:
            #     for i in data['features']:
            #         i['id']= i['properties']['shapeName'].replace(" Division","")
        
            #     fig = px.choropleth_mapbox(reports, geojson=data, locations='divisionname', color='basic_info_division',
            #                             color_continuous_scale="YlOrBr",
            #                             range_color=(0, reports['basic_info_division'].max()),
            #                             mapbox_style="carto-positron",
            #                             zoom=5.6, center = {"lat": 23.7, "lon": 90},
            #                             opacity=0.9,
            #                             labels={'division':'Incidences per division'}
            #                           )
            #     fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            #     st.plotly_chart(fig, use_container_width=True)
            # with colBar:
            #     fig=px.bar(reports, x='divisionname', y='basic_info_division', labels= {'division':'incidences'})# ,color='basic_info_division')
            #     fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            #     st.plotly_chart(fig, use_container_width=True)
            
        if granularity=='2: District':
            loc=2
            title='basic_info_district'
            nname='districtname'
            repstr=" District"
            labv= 'district'           
            labt='Incidences per district'
            heat_map(path2, loc, title, nname, repstr, labv, labt)
            
            # path= path2
            # subDist=bahis_geodata[(bahis_geodata["loc_type"]==2)]
            # reports = subd_bahis_sourcedata['basic_info_district'].value_counts().to_frame()
            # reports['districtname'] = reports.index
            # reports= reports.loc[reports['districtname'] != 'nan']
        
            # data = open_data(path)
            # for i in data['features']:
            #     i['id']= i['properties']['shapeName'].replace(" District","")
            # for i in range(reports.shape[0]):
            #     reports['districtname'].iloc[i] = subDist.loc[subDist['value']==int(reports['districtname'].iloc[i]),'name'].iloc[0]
            # reports=reports.sort_values('districtname')
            # reports['districtname']=reports['districtname'].str.capitalize()
            # colMap, colBar = st.columns([1,2])
            # with colMap:
            #     for i in data['features']:
            #         i['id']= i['properties']['shapeName'].replace(" District","")
        
            #     fig = px.choropleth_mapbox(reports, geojson=data, locations='districtname', color='basic_info_district',
            #                             color_continuous_scale="YlOrBr",
            #                             range_color=(0, reports['basic_info_district'].max()),
            #                             mapbox_style="carto-positron",
            #                             zoom=5.6, center = {"lat": 23.7, "lon": 90},
            #                             opacity=0.9,
            #                             labels={'district':'Incidences per district'}
            #                           )
            #     fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            #     st.plotly_chart(fig, use_container_width=True)
            # with colBar:
            #     fig=px.bar(reports, x='districtname', y='basic_info_district', labels= {'district':'incidences'})
            #     fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            #     st.plotly_chart(fig, use_container_width=True)
            
        if granularity=='3: Upazila':
            loc=3
            title='basic_info_upazila'
            nname='upazilaname'
            repstr=" Upazila"
            labv= 'upazila'           
            labt='Incidences per upazila'
            heat_map(path3, loc, title, nname, repstr, labv, labt)
            
            # path= path3
            # subDist=bahis_geodata[(bahis_geodata["loc_type"]==3)]
        
            # reports = subd_bahis_sourcedata['basic_info_upazila'].value_counts().to_frame()
            # reports['upazilaname'] = reports.index
            # reports= reports.loc[reports['upazilaname'] != 'nan']
            # data = open_data(path)
            # for i in data['features']:
            #     i['id']= i['properties']['shapeName'].replace(" upazila","")
            # for i in range(reports.shape[0]):
            #     reports['upazilaname'].iloc[i] = subDist.loc[subDist['value']==int(reports['upazilaname'].iloc[i]),'name'].iloc[0]
            # reports=reports.sort_values('upazilaname')
            # reports['upazilaname']=reports['upazilaname'].str.capitalize()
            
            # colMap, colBar = st.columns([1,2])
            # with colMap:
            #     for i in data['features']:
            #         i['id']= i['properties']['shapeName'].replace(" Upazila","")
        
            #     fig = px.choropleth_mapbox(reports, geojson=data, locations='upazilaname', color='basic_info_upazila',
            #                             color_continuous_scale="YlOrBr",
            #                             range_color=(0, reports['basic_info_upazila'].max()),
            #                             mapbox_style="carto-positron",
            #                             zoom=5.6, center = {"lat": 23.7, "lon": 90},
            #                             opacity=0.9,
            #                             labels={'upazila':'Incidences per Upazila'}
            #                           )
            #     fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            #     st.plotly_chart(fig, use_container_width=True)
            # with colBar:
            #     fig=px.bar(reports, x='upazilaname', y='basic_info_upazila', labels= {'upazila':'incidences'})
            #     fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            #     st.plotly_chart(fig, use_container_width=True)
   

