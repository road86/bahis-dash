# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:14:48 2022

@author: yoshka
"""

# with the import command, additional libraries can be used which can simplify the programming

import streamlit as st            # streamlit is a web publishing possibility
import pandas as pd               # pandas for datahandling
#import pydeck as pdk             #
#import plotly.graph_objects as go # plotly for graphic visualisation, pydeck is an alternative, but it became plotly
import plotly.express as px       #
import altair as alt              # altair for graphs
import json                       # json file format to import geodata
#import datetime as dt
from datetime import datetime, timedelta
#import numpy as np


gifpath = 'logos/'
sourcepath = 'exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
sourcefilename =sourcepath + 'preped_data.csv'
path0= "geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # found shapefiles from the data.humdata.org
path1= "geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
path2= "geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
path3= "geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
path4= "geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union

bahis_geodata = pd.read_csv(geofilename)
bahis_sourcedata = pd.read_csv(sourcefilename)

bahis_sourcedata['basic_info_division'] = pd.to_numeric(bahis_sourcedata['basic_info_division'])
bahis_sourcedata['basic_info_district'] = pd.to_numeric(bahis_sourcedata['basic_info_district'])
bahis_sourcedata['basic_info_upazila'] = pd.to_numeric(bahis_sourcedata['basic_info_upazila'])
bahis_sourcedata['basic_info_date'] = pd.to_datetime(bahis_sourcedata['basic_info_date'])

start_date=min(bahis_sourcedata['basic_info_date']).date()
end_date=max(bahis_sourcedata['basic_info_date']).date()
dates=[start_date, end_date]
sub_bahis_sourcedata=bahis_sourcedata

value1='division'
geocode= 1
path=path1
subDist=bahis_geodata[(bahis_geodata["loc_type"]==geocode)]
divisions=list(bahis_geodata[(bahis_geodata["loc_type"]==1)]['name'])

reports = sub_bahis_sourcedata['basic_info_'+str(value1)].value_counts().rename_axis('basic_info_'+str(value1)).reset_index(name='counts')
reports= reports.loc[reports['basic_info_'+str(value1)] != 'nan']

finger = reports.shape
subDist.set_index('name')
for i in range(reports.shape[0]):
        reports['basic_info_'+str(value1)].iloc[i] = subDist.loc[subDist['value']==int(reports['basic_info_'+str(value1)].iloc[i]),'name'].iloc[0]
reports=reports.sort_values('basic_info_'+str(value1))
reports['basic_info_'+str(value1)]=reports['basic_info_'+str(value1)].str.title()


img_logo= 'logos/Logo.png'

st.set_page_config(layout="wide")                            # streamlit commands addressed with st (see import)

st.image(img_logo, width=400)

st.title('bahis dashboard')

bahis_sourcedata['basic_info_date']=pd.to_datetime(bahis_sourcedata.basic_info_date).dt.tz_localize(None).astype('datetime64[ns]')
mask=(bahis_sourcedata['basic_info_date']> datetime.now()-timedelta(days=30)) & (bahis_sourcedata['basic_info_date'] < datetime.now())

colInd1, colInd2, colInd3 = st.columns(3)
with colInd1:
    tmp_sub_data=bahis_sourcedata['basic_info_date'].loc[mask]
    diff=tmp_sub_data.shape[0]
    st.metric('total national reports and last 30 days', value=bahis_sourcedata.shape[0], delta=diff)
with colInd2:
    tmp_sub_data=bahis_sourcedata['patient_info_sick_number'].loc[mask]
    diffsick=tmp_sub_data.sum().item()
    st.metric('total reported sick and last 30 days', value=bahis_sourcedata['patient_info_sick_number'].sum(), delta= diffsick)  # less by one compared to libreoffice...?
with colInd3:
    tmp_sub_data=bahis_sourcedata['patient_info_dead_number'].loc[mask]
    diffdead=tmp_sub_data.sum().item()
    st.metric('total reported dead and last 30 days', value=bahis_sourcedata['patient_info_dead_number'].sum(), delta = diffdead)

def open_data(path):
    with open(path) as f:
        data = json.load(f)
        return data

data = open_data(path)

for i in data['features']:
    i['id']= i['properties']['shapeName'].replace(" "+str(value1).capitalize(),"")


date_placeholder=st.empty()

dates = st.slider('Select date', start_date, end_date, (start_date, end_date))
tmask=(bahis_sourcedata['basic_info_date']> pd.to_datetime(dates[0])) & (bahis_sourcedata['basic_info_date'] < pd.to_datetime(dates[1]))
date_placeholder.subheader("Selected Date range: From " + str(dates[0]) + " until " + str(dates[1]))


reports = bahis_sourcedata['basic_info_district'].value_counts().to_frame()
reports['districtname'] = reports.index
reports= reports.loc[reports['districtname'] != 'nan']


#@st.cache
def open_data(path):
    with open(path) as f:
        data = json.load(f)
        return data
    
    
with st.expander('regional view'):
    #st.header('Region selection')
    
    subDist = bahis_geodata[(bahis_geodata["loc_type"]==1)]['name']
    col1, col2 = st.columns([1,4])
    with col1:
        itemlistDiv=pd.concat([pd.Series(['Select'], name='name'),bahis_geodata[(bahis_geodata["loc_type"]==1)]['name'].str.capitalize()])
        findDiv = st.selectbox('Divsion', itemlistDiv)
    if findDiv != 'Select':
        indexDiv= subDist[subDist==findDiv.upper()].index[0]
        sub_bahis_sourcedata=bahis_sourcedata.loc[tmask]
        
        disList = bahis_geodata[bahis_geodata['parent']==int(bahis_geodata.iloc[[indexDiv]]['value'])]['name'].str.capitalize()
        itemlistDis=pd.concat([pd.Series(['Select'], name='name'),disList])
    col1, col2 = st.columns([1,4])
    with col1:
        if findDiv != 'Select':        
            findDis= st.selectbox('District', itemlistDis)    
            if findDis != 'Select':
                indexDis= disList[disList==findDis].index[0]
                #sub_bahis_sourcedata=bahis_sourcedata.loc[tmask]
    
                upaList = bahis_geodata[bahis_geodata['parent']==int(bahis_geodata.iloc[[indexDis]]['value'])]['name'].str.capitalize()
                itemlistUpa=pd.concat([pd.Series(['Select'], name='name'),upaList])
    col1, col2 = st.columns([1,4])
    with col1:
        if findDiv!= 'Select':
            if findDis != 'Select':
                findUpa= st.selectbox('Upazila', itemlistUpa)
                if findUpa != 'Select':
                    indexUpa = upaList[upaList==findUpa].index[0]
                    Upazila= int(bahis_geodata.iloc[[indexUpa]]['value'])
    
    sub_bahis_sourcedata=bahis_sourcedata.loc[tmask]
    
    if findDiv == 'Select':
        colMap, colBars= st.columns(2)
        with colMap:
            overview = st.checkbox("Toggle: Overview Map - Clustered Map")
            if overview:
                path= path0
                subDist=bahis_geodata
                data = open_data(path)
                #data = open_data(path)
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
                fig.update_layout(autosize=True, width= 1000, height=600, margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig, use_container_width=True)
            else:
                path= path1
                subDist=bahis_geodata[(bahis_geodata["loc_type"]==1)]
                reports = sub_bahis_sourcedata['basic_info_division'].value_counts().to_frame()
                reports['divisionname'] = reports.index
                reports= reports.loc[reports['divisionname'] != 'nan']    
                data = open_data(path)
                for i in range(reports.shape[0]):
                    reports['divisionname'].iloc[i] = subDist.loc[subDist['value']==int(reports['divisionname'].iloc[i]),'name'].iloc[0]
    #            reports=reports.sort_values('divisionname')
                reports['divisionname']=reports['divisionname'].str.capitalize()
                for i in data['features']:
                    i['id']= i['properties']['shapeName'].replace(" Division","")
    
                fig = px.choropleth_mapbox(reports, geojson=data, locations='divisionname', color='basic_info_division',
                                        color_continuous_scale="Viridis",
                                        range_color=(0, reports['basic_info_division'].max()),
                                        mapbox_style="carto-positron",
                                        zoom=5.6, center = {"lat": 23.7, "lon": 90},
                                        opacity=0.5,
                                        labels={'division':'Incidences per division'}
                                      )
                fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig, use_container_width=True)
        with colBars:
            #st.subheader('Reports')
            sub_bahis_sourcedata=bahis_sourcedata.loc[tmask]
            st.line_chart(sub_bahis_sourcedata['basic_info_date'].value_counts(), height=200)
            #st.subheader('Sick Counts')
            st.line_chart(sub_bahis_sourcedata['patient_info_sick_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum(), height=200)
            #st.subheader('Dead Counts')
            st.line_chart(sub_bahis_sourcedata['patient_info_dead_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum(), height=200)
    
    if (findDiv != 'Select') and (findDis == 'Select'):
        colMap, colBar = st.columns([1,2])
        with colMap:
            overview = st.checkbox("Toggle: Overview Map - Clustered Map")
            if overview:
                path= path1
                subDist= bahis_geodata[(bahis_geodata["loc_type"]==1)]     
                geocodehit= subDist.loc[subDist['name'].str.capitalize()==findDiv]['value']
                subs_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_division']==int(geocodehit)]
                if subs_bahis_sourcedata.empty:
                    st.write('empty')
                else:  
                    reports = subs_bahis_sourcedata['basic_info_division'].value_counts().to_frame()
                    reports['divisionname'] = reports.index
                    reports= reports.loc[reports['divisionname'] != 'nan']
                    data = open_data(path)
                    for i in range(reports.shape[0]):
                        reports['divisionname'].iloc[i] = subDist.loc[subDist['value']==int(reports['divisionname'].iloc[i]),'name'].iloc[0]
                    reports=reports.sort_values('divisionname')
                    reports['divisionname']=reports['divisionname'].str.capitalize()          
                    for i in data['features']:
                        i['id']= i['properties']['shapeName'].replace(" Division","")
            
                    fig = px.choropleth_mapbox(reports, geojson=data, locations='divisionname', color='basic_info_division',
                                            color_continuous_scale="Viridis",
                                            range_color=(0, reports['basic_info_division'].max()),
                                            mapbox_style="carto-positron",
                                            zoom=5.6, center = {"lat": 23.7, "lon": 90},
                                            opacity=0.5,
                                            labels={'division':'Incidences per division'}
                                          )
                    fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
                    st.plotly_chart(fig, use_container_width=True)
            else:
                path= path2
                subDist=bahis_geodata[(bahis_geodata["loc_type"]==1)]
                geocodehit= subDist.loc[subDist['name'].str.capitalize()==findDiv]['value']
                subs_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_division']==int(geocodehit)]
                if subs_bahis_sourcedata.empty:
                    st.write('empty')
                else:                
                    reports = subs_bahis_sourcedata['basic_info_district'].value_counts().to_frame()
                    reports['districtname'] = reports.index
                    reports= reports.loc[reports['districtname'] != 'nan']
                    subDist=bahis_geodata[(bahis_geodata["loc_type"]==2)]
                    data = open_data(path)
                    for i in range(reports.shape[0]):
                        reports['districtname'].iloc[i] = subDist.loc[subDist['value']==int(reports['districtname'].iloc[i]),'name'].iloc[0]
                    reports=reports.sort_values('districtname')
                    reports['districtname']=reports['districtname'].str.capitalize()
                    for i in data['features']:
                        i['id']= i['properties']['shapeName'].replace(" District","")
                    fig = px.choropleth_mapbox(reports, geojson=data, locations='districtname', color='basic_info_district',
                                            color_continuous_scale="Viridis",
                                            range_color=(0, reports['basic_info_district'].max()),
                                            mapbox_style="carto-positron",
                                            zoom=5.6, center = {"lat": 23.7, "lon": 90},
                                            opacity=0.5,
                                            labels={'district':'Incidences per district'}
                                          )
                    fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
                    st.plotly_chart(fig, use_container_width=True)
                
        with colBar:
            #st.subheader('Reports')
            subDist= bahis_geodata[(bahis_geodata["loc_type"]==1)]     
            geocodehit= subDist.loc[subDist['name'].str.capitalize()==findDiv]['value']
            subs_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_division']==int(geocodehit)]
            subs_bahis_sourcedata=subs_bahis_sourcedata.loc[tmask]
            #st.dataframe(subs_bahis_sourcedata)
            if subs_bahis_sourcedata.empty:
                st.write('empty')
            else: 
                st.line_chart(subs_bahis_sourcedata['basic_info_date'].value_counts(), height=200)
                st.line_chart(subs_bahis_sourcedata['patient_info_sick_number'].groupby(subs_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum(), height=200)
                st.line_chart(subs_bahis_sourcedata['patient_info_dead_number'].groupby(subs_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum(), height=200)
         

    if (findDiv != 'Select') and (findDis != 'Select') and (findUpa =='Select'):
        colMap, colBar = st.columns([1,2])
        with colMap:
            overview = st.checkbox("Toggle: Overview Map - Clustered Map")
            if overview:
                path= path2
                subDist= bahis_geodata[(bahis_geodata["loc_type"]==2)]     
                geocodehit= subDist.loc[subDist['name'].str.capitalize()==findDis]['value']
                subs_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_district']==int(geocodehit)]
                if subs_bahis_sourcedata.empty:
                    st.write('empty')
                else:  
                    reports = subs_bahis_sourcedata['basic_info_district'].value_counts().to_frame()
                    reports['districtname'] = reports.index
                    reports= reports.loc[reports['districtname'] != 'nan']
                    data = open_data(path)
                    for i in range(reports.shape[0]):
                        reports['districtname'].iloc[i] = subDist.loc[subDist['value']==int(reports['districtname'].iloc[i]),'name'].iloc[0]
                    reports=reports.sort_values('districtname')
                    reports['districtname']=reports['districtname'].str.capitalize()          
                    for i in data['features']:
                        i['id']= i['properties']['shapeName'].replace(" District","")
            
                    fig = px.choropleth_mapbox(reports, geojson=data, locations='districtname', color='basic_info_district',
                                            color_continuous_scale="Viridis",
                                            range_color=(0, reports['basic_info_district'].max()),
                                            mapbox_style="carto-positron",
                                            zoom=5.6, center = {"lat": 23.7, "lon": 90},
                                            opacity=0.5,
                                            labels={'district':'Incidences per district'}
                                          )
                    fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
                    st.plotly_chart(fig, use_container_width=True)
            else:
                path= path3
                subDist=bahis_geodata[(bahis_geodata["loc_type"]==2)]
                geocodehit= subDist.loc[subDist['name'].str.capitalize()==findDis]['value']
                subs_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_district']==int(geocodehit)]               
                if subs_bahis_sourcedata.empty:
                    st.write('empty')
                else:                
                    reports = subs_bahis_sourcedata['basic_info_upazila'].value_counts().to_frame()
                    reports['upazilaname'] = reports.index
                    reports= reports.loc[reports['upazilaname'] != 'nan']
                    subDist=bahis_geodata[(bahis_geodata["loc_type"]==3)] 
                    data = open_data(path)
                    for i in range(reports.shape[0]):
                        reports['upazilaname'].iloc[i] = subDist.loc[subDist['value']==int(reports['upazilaname'].iloc[i]),'name'].iloc[0]
                    reports=reports.sort_values('upazilaname')
                    reports['upazilaname']=reports['upazilaname'].str.capitalize()
                    for i in data['features']:
                        i['id']= i['properties']['shapeName'].replace(" Upazila","")
                    fig = px.choropleth_mapbox(reports, geojson=data, locations='upazilaname', color='basic_info_upazila',
                                            color_continuous_scale="Viridis",
                                            range_color=(0, reports['basic_info_upazila'].max()),
                                            mapbox_style="carto-positron",
                                            zoom=5.6, center = {"lat": 23.7, "lon": 90},
                                            opacity=0.5,
                                            labels={'upazila':'Incidences per upazila'}
                                          )
                    fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
                    st.plotly_chart(fig, use_container_width=True)
                
        with colBar:
            #st.subheader('Reports')
            subDist= bahis_geodata[(bahis_geodata["loc_type"]==2)]     
            geocodehit= subDist.loc[subDist['name'].str.capitalize()==findDis]['value']
            subs_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_district']==int(geocodehit)]
            subs_bahis_sourcedata=subs_bahis_sourcedata.loc[tmask]
            #st.dataframe(subs_bahis_sourcedata)
            if subs_bahis_sourcedata.empty:
                st.write('empty')
            else: 
                st.line_chart(subs_bahis_sourcedata['basic_info_date'].value_counts(), height=200)
                st.line_chart(subs_bahis_sourcedata['patient_info_sick_number'].groupby(subs_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum(), height=200)
                st.line_chart(subs_bahis_sourcedata['patient_info_dead_number'].groupby(subs_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum(), height=200)
      
                  
    if (findDiv != 'Select') and (findDis != 'Select') and (findUpa !='Select'):
           colMap, colBar = st.columns([1,2])
           with colMap:
 #              overview = st.checkbox("Toggle: Overview Map - Clustered Map")
           #    if overview:
                   path= path3
                   subDist= bahis_geodata[(bahis_geodata["loc_type"]==3)]     
                   geocodehit= subDist.loc[subDist['name'].str.capitalize()==findUpa]['value']
                   subs_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_upazila']==int(geocodehit)]
                   if subs_bahis_sourcedata.empty:
                       st.write('empty')
                   else:  
                       reports = subs_bahis_sourcedata['basic_info_upazila'].value_counts().to_frame()
                       reports['upazilaname'] = reports.index
                       reports= reports.loc[reports['upazilaname'] != 'nan']
                       data = open_data(path)
                       for i in range(reports.shape[0]):
                           reports['upazilaname'].iloc[i] = subDist.loc[subDist['value']==int(reports['upazilaname'].iloc[i]),'name'].iloc[0]
                       reports=reports.sort_values('upazilaname')
                       reports['upazilaname']=reports['upazilaname'].str.capitalize()          
                       for i in data['features']:
                           i['id']= i['properties']['shapeName'].replace(" Upazila","")
               
                       fig = px.choropleth_mapbox(reports, geojson=data, locations='upazilaname', color='basic_info_upazila',
                                               color_continuous_scale="Viridis",
                                               range_color=(0, reports['basic_info_upazila'].max()),
                                               mapbox_style="carto-positron",
                                               zoom=5.6, center = {"lat": 23.7, "lon": 90},
                                               opacity=0.5,
                                               labels={'upazila':'Incidences per upazila'}
                                             )
                       fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
                       st.plotly_chart(fig, use_container_width=True)
                   
           with colBar:
               #st.subheader('Reports')
               subDist= bahis_geodata[(bahis_geodata["loc_type"]==3)]    
               #st.dataframe(subDist)
               geocodehit= subDist.loc[subDist['name'].str.capitalize()==findUpa]['value']
               subs_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_upazila']==int(geocodehit)]
               subs_bahis_sourcedata=subs_bahis_sourcedata.loc[tmask]
               #st.dataframe(subs_bahis_sourcedata)
               if subs_bahis_sourcedata.empty:
                   st.write('empty')
               else: 
                   st.line_chart(subs_bahis_sourcedata['basic_info_date'].value_counts(), height=200)
                   st.line_chart(subs_bahis_sourcedata['patient_info_sick_number'].groupby(subs_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum(), height=200)
                   st.line_chart(subs_bahis_sourcedata['patient_info_dead_number'].groupby(subs_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum(), height=200)
                   
                   
                   
                
    #st.header('Reports')
    
    #sub_bahis_sourcedata=bahis_sourcedata.loc[mask]
    #st.line_chart(sub_bahis_sourcedata['basic_info_date'].value_counts())

with st.expander('overview'):
    values = ['0: Nation' , '1: Division', '2: District', '3: Upazila']
    defaultV = values.index('2: District')  # default value
    granularity= st.selectbox('Select level', values, index=defaultV) #, horizontal= True)
    
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
            st.metric(label= 'Reports', value= sub_bahis_sourcedata.shape[0] )
    
    
    
    if granularity=='1: Division':
        path= path1
        subDist=bahis_geodata[(bahis_geodata["loc_type"]==1)]
        reports = sub_bahis_sourcedata['basic_info_division'].value_counts().to_frame()
        reports['divisionname'] = reports.index
        reports= reports.loc[reports['divisionname'] != 'nan']
    
        data = open_data(path)
        for i in data['features']:
            i['id']= i['properties']['shapeName'].replace(" Division","")
        for i in range(reports.shape[0]):
            reports['divisionname'].iloc[i] = subDist.loc[subDist['value']==int(reports['divisionname'].iloc[i]),'name'].iloc[0]
        reports=reports.sort_values('divisionname')
        reports['divisionname']=reports['divisionname'].str.capitalize()
        colMap, colBar = st.columns([1,2])
        with colMap:
            for i in data['features']:
                i['id']= i['properties']['shapeName'].replace(" Division","")
    
            fig = px.choropleth_mapbox(reports, geojson=data, locations='divisionname', color='basic_info_division',
                                    color_continuous_scale="Viridis",
                                    range_color=(0, reports['basic_info_division'].max()),
                                    mapbox_style="carto-positron",
                                    zoom=5.6, center = {"lat": 23.7, "lon": 90},
                                    opacity=0.5,
                                    labels={'division':'Incidences per division'}
                                  )
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        with colBar:
            fig=px.bar(reports, x='divisionname', y='basic_info_division', labels= {'division':'incidences'})# ,color='basic_info_division')
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
    
    
    if granularity=='2: District':
        path= path2
        subDist=bahis_geodata[(bahis_geodata["loc_type"]==2)]
        reports = sub_bahis_sourcedata['basic_info_district'].value_counts().to_frame()
        reports['districtname'] = reports.index
        reports= reports.loc[reports['districtname'] != 'nan']
    
        data = open_data(path)
        for i in data['features']:
            i['id']= i['properties']['shapeName'].replace(" District","")
        for i in range(reports.shape[0]):
            reports['districtname'].iloc[i] = subDist.loc[subDist['value']==int(reports['districtname'].iloc[i]),'name'].iloc[0]
        reports=reports.sort_values('districtname')
        reports['districtname']=reports['districtname'].str.capitalize()
        colMap, colBar = st.columns([1,2])
        with colMap:
            for i in data['features']:
                i['id']= i['properties']['shapeName'].replace(" District","")
    
            fig = px.choropleth_mapbox(reports, geojson=data, locations='districtname', color='basic_info_district',
                                    color_continuous_scale="Viridis",
                                    range_color=(0, reports['basic_info_district'].max()),
                                    mapbox_style="carto-positron",
                                    zoom=5.6, center = {"lat": 23.7, "lon": 90},
                                    opacity=0.5,
                                    labels={'district':'Incidences per district'}
                                  )
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        with colBar:
            fig=px.bar(reports, x='districtname', y='basic_info_district', labels= {'district':'incidences'})
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
    
    
    if granularity=='3: Upazila':
        path= path3
        subDist=bahis_geodata[(bahis_geodata["loc_type"]==3)]
    
        reports = sub_bahis_sourcedata['basic_info_upazila'].value_counts().to_frame()
        reports['upazilaname'] = reports.index
        reports= reports.loc[reports['upazilaname'] != 'nan']
        data = open_data(path)
        for i in data['features']:
            i['id']= i['properties']['shapeName'].replace(" upazila","")
        for i in range(reports.shape[0]):
            reports['upazilaname'].iloc[i] = subDist.loc[subDist['value']==int(reports['upazilaname'].iloc[i]),'name'].iloc[0]
        reports=reports.sort_values('upazilaname')
        reports['upazilaname']=reports['upazilaname'].str.capitalize()
    
        colMap, colBar = st.columns([1,2])
    
        with colMap:
            for i in data['features']:
                i['id']= i['properties']['shapeName'].replace(" Upazila","")
    
            fig = px.choropleth_mapbox(reports, geojson=data, locations='upazilaname', color='basic_info_upazila',
                                    color_continuous_scale="Viridis",
                                    range_color=(0, reports['basic_info_upazila'].max()),
                                    mapbox_style="carto-positron",
                                    zoom=5.6, center = {"lat": 23.7, "lon": 90},
                                    opacity=0.5,
                                    labels={'upazila':'Incidences per Upazila'}
                                  )
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        with colBar:
            fig=px.bar(reports, x='upazilaname', y='basic_info_upazila', labels= {'upazila':'incidences'})
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

with st.expander('Upazila data'):
    #st.header('Upazila data')
    
    #colUpa1, colUpa2 = st.columns([1,4]) #, colUpa3 = st.columns([1,4,2])
    #with colUpa1:
    subDist = bahis_geodata[(bahis_geodata["loc_type"]==1)]['name']
    findDiv = st.selectbox('Divsion', bahis_geodata[(bahis_geodata["loc_type"]==1)]['name'].str.capitalize())
    indexD= subDist[subDist==findDiv.upper()].index[0]
    #with colUpa2:
    correcttraining= False #st.checkbox('Delete first')
    sub_bahis_sourcedata=bahis_sourcedata.loc[mask]
    
    st.subheader(bahis_geodata.iloc[[indexD]]['name'].str.capitalize().to_string(index=False))
    if sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_division']==int(bahis_geodata.iloc[[indexD]]['value'])]['basic_info_date'].value_counts().size == 0:
        st.write('No reports submitted')
    else:
       df=sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_division']==int(bahis_geodata.iloc[[indexD]]['value'])]['basic_info_date'].dt.date.value_counts()
       df=df.sort_index()
    #       st.dataframe(df)
       c=alt.Chart(df.reset_index()).mark_bar().encode(
           x=alt.X('index',axis=alt.Axis(format='%Y/%m/%d', title='Date')),
           y=alt.Y('basic_info_date', axis=alt.Axis(title='Reports')),
           )
       st.altair_chart(c, use_container_width=True)
    
    # #    st.write(bahis_geodata.iloc[[indexU]]['name'].str.capitalize())
    #     if sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_district']==int(bahis_geodata.iloc[[indexU]]['value'])]['basic_info_date'].value_counts().size == 0:
    #         st.write('No reports submitted')
    #     else:
    #        df=sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_district']==int(bahis_geodata.iloc[[indexU]]['value'])]['basic_info_date'].dt.date.value_counts()
    #        df=df.sort_index()
    # #       st.dataframe(df)
    #        c=alt.Chart(df.reset_index()).mark_bar().encode(
    #            x=alt.X('index',axis=alt.Axis(format='%Y/%m/%d', title='Date')),
    #            y=alt.Y('basic_info_date', axis=alt.Axis(title='Reports')),
    #            )
    #        st.altair_chart(c, use_container_width=True)
    
    # #    st.write(bahis_geodata.iloc[[indexUS]]['name'].str.capitalize())
    #     if sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_upazila']==Upazila]['basic_info_date'].value_counts().size != 0:
    # #    if sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_upazila']==Upazila]['basic_info_date'].value_counts().size == 0:
    # #        st.write('No reports submitted')
    # #    else:
    #        df=sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_upazila']==Upazila]['basic_info_date'].dt.date.value_counts()
    #        df=df.sort_index()
    # #       st.dataframe(df)
    #        if correcttraining:
    #            df=df.sort_index()
    #            df.drop(index=df.index[0],
    #                axis=0,
    #                inplace=True)
    #        c=alt.Chart(df.reset_index()).mark_bar().encode(
    #            x=alt.X('index',axis=alt.Axis(format='%Y/%m/%d', title='Date')),
    #            y=alt.Y('basic_info_date', axis=alt.Axis(title='Reports')),
    #            )
    #        st.altair_chart(c, use_container_width=True)
    
    #with colUpa3:
    
    #colUpa1, colUpa2 = st.columns([1,4]) #, colUpa3 = st.columns([1,4,2])
    #with colUpa1:
    disList = bahis_geodata[bahis_geodata['parent']==int(bahis_geodata.iloc[[indexD]]['value'])]['name'].str.capitalize()
    findDis= st.selectbox('District', disList)
    indexU= disList[disList==findDis].index[0]
    #with colUpa2:
    sub_bahis_sourcedata=bahis_sourcedata.loc[mask]
    st.subheader(bahis_geodata.iloc[[indexU]]['name'].str.capitalize().to_string(index=False))
    if sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_district']==int(bahis_geodata.iloc[[indexU]]['value'])]['basic_info_date'].value_counts().size == 0:
        st.write('No reports submitted')
    else:
       df=sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_district']==int(bahis_geodata.iloc[[indexU]]['value'])]['basic_info_date'].dt.date.value_counts()
       df=df.sort_index()
    #       st.dataframe(df)
       c=alt.Chart(df.reset_index()).mark_bar().encode(
           x=alt.X('index',axis=alt.Axis(format='%Y/%m/%d', title='Date')),
           y=alt.Y('basic_info_date', axis=alt.Axis(title='Reports')),
           )
       st.altair_chart(c, use_container_width=True)
    
    #colUpa1, colUpa2 = st.columns([1,4]) #, colUpa3 = st.columns([1,4,2])
    #with colUpa1:
    upaList = bahis_geodata[bahis_geodata['parent']==int(bahis_geodata.iloc[[indexU]]['value'])]['name'].str.capitalize()
    findUpa= st.selectbox('Upazila', upaList)
    indexUS = upaList[upaList==findUpa].index[0]
    Upazila= int(bahis_geodata.iloc[[indexUS]]['value'])
    #with colUpa2:
    sub_bahis_sourcedata=bahis_sourcedata.loc[mask]
    st.subheader(bahis_geodata.iloc[[indexUS]]['name'].str.capitalize().to_string(index=False))
    if sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_upazila']==Upazila]['basic_info_date'].value_counts().size != 0:
    #    if sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_upazila']==Upazila]['basic_info_date'].value_counts().size == 0:
    #        st.write('No reports submitted')
    #    else:
       df=sub_bahis_sourcedata[sub_bahis_sourcedata['basic_info_upazila']==Upazila]['basic_info_date'].dt.date.value_counts()
       df=df.sort_index()
    #       st.dataframe(df)
       if correcttraining:
           df=df.sort_index()
           df.drop(index=df.index[0],
               axis=0,
               inplace=True)
       c=alt.Chart(df.reset_index()).mark_bar().encode(
           x=alt.X('index',axis=alt.Axis(format='%Y/%m/%d', title='Date')),
           y=alt.Y('basic_info_date', axis=alt.Axis(title='Reports')),
           )
       st.altair_chart(c, use_container_width=True)
    

st.header('Disease cases')

diseases = bahis_sourcedata['top_diagnosis'].value_counts().to_frame()

st.bar_chart(diseases) #sub_bahis_sourcedata['top_diagnosis'].value_counts())

