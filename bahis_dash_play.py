# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:14:48 2022

@author: yoshka
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
# import plotly.figure_factory as ff
# from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
import json 
from streamlit_plotly_events import plotly_events
# import datetime as dt
# import matplotlib.pyplot as plt


basepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around'
datapath = '/output/'
logopath = '/logos/'

txt_title="BAHIS dash"
txt_chart="Select file"
txt_select="Please select"
txt_farms="farms"
txt_geocluster="GeoClus"
txt_shpfiles="shpFiles"
txt_aviinvest="AvIInvest"
txt_avisample="AvISample"
txt_disinvest="Dis Invest"
txt_farmass="FarmAss"
txt_partlsass="PartLSAss"
txt_patreg="PatReg"
txt_missfarm="missFarm"

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# define page layout
st.set_page_config(layout="wide")

#50105485791.0 no mouza but upazila? 501054.0 yes


#### side window
#sidebar
st.sidebar.image("/Users/yoshka/Documents/GitHub/bahis-dash/play_around/logos/bahis-logo.png", use_column_width=True)




#########################################################old part
oldchoice = st.sidebar.checkbox("old program")
if oldchoice:
    option = st.sidebar.selectbox(
         txt_select,
         (txt_farms, txt_geocluster, txt_shpfiles, txt_aviinvest, txt_avisample,
         txt_disinvest, txt_farmass, txt_partlsass, txt_patreg, txt_missfarm))
    st.write('You selected:', option)
##########################################################      

reportchoice = st.sidebar.checkbox("report")

maptest= st.sidebar.checkbox("Maps")

if maptest:
 
    path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM0-all/geoBoundaries-BGD-ADM0.geojson" #1 Nation
    path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM1-all/geoBoundaries-BGD-ADM1.geojson" #8 Division
    path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM2-all/geoBoundaries-BGD-ADM2.geojson" #64 District
    path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM3-all/geoBoundaries-BGD-ADM3.geojson" #495 Upazila
    path4= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM4-all/geoBoundaries-BGD-ADM4.geojson" #4562 Union



    filename = basepath + datapath + 'STATICBAHIS_geo_cluster_202204301723.csv'
    bahis_datageo = pd.read_csv(filename)
    filename = basepath + datapath + 'formdata_Farm_Assessment_Monitoring.csv'
    def read_bahis_dataFarm(filename):
        return pd.read_csv(filename, low_memory=False) #bad way of mixed variables. but there were too many columns
    # (17,33,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69) have mixed types. and there was something with 3?
    bahis_dataFarm= read_bahis_dataFarm(filename)
    cases = bahis_dataFarm['district'].value_counts().to_frame()
    cases['districtname'] = cases.index
    cases= cases.loc[cases['districtname'] != 'nan']
    # cases=cases.dropna()
    subDist=bahis_datageo[(bahis_datageo["loc_type"]==2)]
    subDist['cases']=subDist.index
    for i in range(cases.shape[0]):
        cases['districtname'].iloc[i] = subDist.loc[subDist['value']==int(cases['districtname'].iloc[i]),'name'].iloc[0]
    #for i in range(cases.shape[0]):
        subDist['cases'][subDist.loc[subDist['name']==cases['districtname'].iloc[i]].index[0]] = cases['district'].iloc[i]
    cases=cases.sort_values('districtname')
    cases['districtname']=cases['districtname'].str.title()
    
    fig=px.bar(cases, x='districtname', y='district', labels= {'district':'incidences'})

    st.plotly_chart(fig)
    
     
#    @st.cache 
    def open_data(path):
        with open(path) as f:
            data = json.load(f)
            return data
        
    data = open_data(path1)
    
    for i in data['features']:
        i['id']= i['properties']['shapeName'].replace(" Division","") 
        
    fig = px.choropleth_mapbox(cases, geojson=data, locations='districtname', color='district',
                           color_continuous_scale="Viridis",
                           range_color=(0, cases['district'].max()),
                           mapbox_style="carto-positron",
                           zoom=6, center = {"lat": 23.7, "lon": 90},
                           opacity=0.5,
                           labels={'district':'district blah'}
                          )
    fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
 #   fig.on_click(st.write('works'))
 
    
 #########################
omaptest = st.sidebar.checkbox("OMaps")

if omaptest:

    filename = basepath + datapath + 'STATICBAHIS_geo_cluster_202204301723.csv'
    bahis_datageo = pd.read_csv(filename)
    filename = basepath + datapath + 'formdata_Farm_Assessment_Monitoring.csv'
    def read_bahis_dataFarm(filename):
        return pd.read_csv(filename, low_memory=False) #bad way of mixed variables. but there were too many columns
    # (17,33,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69) have mixed types. and there was something with 3?
    bahis_dataFarm= read_bahis_dataFarm(filename)
    cases = bahis_dataFarm['district'].value_counts().to_frame()
    cases['districtname'] = cases.index
    cases= cases.loc[cases['districtname'] != 'nan']
    # cases=cases.dropna()
    subDist=bahis_datageo[(bahis_datageo["loc_type"]==2)]
    subDist['cases']=subDist.index
    for i in range(cases.shape[0]):
        cases['districtname'].iloc[i] = subDist.loc[subDist['value']==int(cases['districtname'].iloc[i]),'name'].iloc[0]
    #for i in range(cases.shape[0]):
        subDist['cases'][subDist.loc[subDist['name']==cases['districtname'].iloc[i]].index[0]] = cases['district'].iloc[i]
    cases=cases.sort_values('districtname')
    cases['districtname']=cases['districtname'].str.title()
    
    # fig=px.bar(cases, x='districtname', y='district', labels= {'district':'incidences'})

    # st.plotly_chart(fig)
    
     
#    @st.cache 
    def open_data(path):
        with open(path) as f:
            data = json.load(f)
            return data
    
    granularity= st.selectbox('level',('0: Nation' ,'1: Division', '2: District', '3: Upazila', '4: Union'))
    if granularity=='0: Nation':
        path= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM0-all/geoBoundaries-BGD-ADM0.geojson" #1 Nation     
    if granularity=='1: Division':
        path= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM1-all/geoBoundaries-BGD-ADM1.geojson" #8 Division
    if granularity=='2: District':
        path= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM2-all/geoBoundaries-BGD-ADM2.geojson" #64 District
    if granularity=='3: Upazila':
        path= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM3-all/geoBoundaries-BGD-ADM3.geojson" #495 Upazila
    if granularity=='4: Union':
        path= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM4-all/geoBoundaries-BGD-ADM4.geojson" #4562 Union
        
    data = open_data(path)
    
    for i in data['features']:
        i['id']= i['properties']['shapeName'].replace(" Division","") 
        
    fig = px.choropleth_mapbox(data['features'], 
                           geojson=data, 
                           locations='id', 
#                           locations='districtname', 
#                           color='district',
#                           color_continuous_scale="Viridis",
#                           range_color=(0, cases['district'].max()),
                           mapbox_style="carto-positron",
                           zoom=5, 
                           center = {"lat": 23.7, "lon": 90},
                           opacity=0.5
#                           labels={'district':'district blah'}
                          )
    #fig.update_layout(autosize=True, width= 1000, height=500, margin={"r":0,"t":0,"l":0,"b":0})
    # st.plotly_chart(fig, use_container_width=True)

    mouseselect=plotly_events(fig)
    st.write(mouseselect)
    st.write(mouseselect[0]['pointNumber'])
 
 #############
 
othermaptest = st.sidebar.checkbox("OtherMaps")

if othermaptest:
    
    path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM0-all/geoBoundaries-BGD-ADM0.geojson" #1 Nation
    path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM1-all/geoBoundaries-BGD-ADM1.geojson" #8 Division
    path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM2-all/geoBoundaries-BGD-ADM2.geojson" #64 District
    path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM3-all/geoBoundaries-BGD-ADM3.geojson" #495 Upazila
    path4= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM4-all/geoBoundaries-BGD-ADM4.geojson" #4562 Union

    filename = basepath + datapath + 'STATICBAHIS_geo_cluster_202204301723.csv'
    bahis_datageo = pd.read_csv(filename)
    filename = basepath + datapath + 'formdata_Farm_Assessment_Monitoring.csv'
    def read_bahis_dataFarm(filename):
        return pd.read_csv(filename, low_memory=False) #bad way of mixed variables. but there were too many columns
    # (17,33,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69) have mixed types. and there was something with 3?
    bahis_dataFarm= read_bahis_dataFarm(filename)
    cases = bahis_dataFarm['district'].value_counts().to_frame()
    cases['districtname'] = cases.index
    cases= cases.loc[cases['districtname'] != 'nan']
    # cases=cases.dropna()
    subDist=bahis_datageo[(bahis_datageo["loc_type"]==2)]
    subDist['cases']=subDist.index

    for i in range(cases.shape[0]):
        cases['districtname'].iloc[i] = subDist.loc[subDist['value']==int(cases['districtname'].iloc[i]),'name'].iloc[0]
    #for i in range(cases.shape[0]):
        subDist['cases'][subDist.loc[subDist['name']==cases['districtname'].iloc[i]].index[0]] = cases['district'].iloc[i]
    cases=cases.sort_values('districtname')
    cases['districtname']=cases['districtname'].str.title()
    
    def open_data(path):
        with open(path) as f:
            data = json.load(f)
            return data
        
    data = open_data(path1)
    
    for i in data['features']:
        i['id']= i['properties']['shapeName'].replace(" Division","")         
 
    selection_lookup = {feature['properties']['shapeName']: feature 
                       for feature in data['features']}
    def get_highlights(selections, geojson=data, place_lookup=selection_lookup):
        geojson_highlights = dict()
        for k in geojson.keys():
            if k != 'features':
                geojson_highlights[k] = geojson[k]
            else:
                geojson_highlights[k] = [selection_lookup[selection] for selection in selections]        
        return geojson_highlights
        
        
    def get_figure(selections):
        # Base choropleth layer --------------#
        fig = px.choropleth_mapbox(cases, geojson=data, locations='districtname', 
                               # color='district',
                               # color_continuous_scale="Viridis",
                               # range_color=(0, cases['district'].max()),
                               mapbox_style="carto-positron",
                               zoom=6, center = {"lat": 23.7, "lon": 90},
                               opacity=0.5,
                               labels={'district':'district blah'}
                              )
        
                                # (df, geojson=data, 
                                #    color="Bergeron",                               
                                #    locations="district", 
                                #    featureidkey="properties.district",
                                #    opacity=0.5)
    
        # Second layer - Highlights ----------#
        if len(selections) > 0:
            # highlights contain the geojson information for only 
            # the selected districts
            highlights = get_highlights(selections)
            fig.add_trace(
                px.choropleth_mapbox(cases, geojson=highlights, locations='districtname', 
                                       # color='district',
                                       # color_continuous_scale="Viridis",
                                       # range_color=(0, cases['district'].max()),
                                       mapbox_style="carto-positron",
                                       zoom=10, center = {"lat": 23.7, "lon": 90},
                                       opacity=0.5,
                                       labels={'district':'district blah'}
                                      )
                
            #                     (df, geojson=highlights, 
            #                          color="Bergeron",
            #                          locations="district", 
            #                          featureidkey="properties.district",                                 
            #                          opacity=1).data[0]
             )
    
        #------------------------------------#
    
    fig = px.choropleth_mapbox(cases, geojson=data, locations='districtname', 
                            # color='district',
                            # color_continuous_scale="Viridis",
                            # range_color=(0, cases['district'].max()),
                            mapbox_style="carto-positron",
                            zoom=5.5, center = {"lat": 23.7, "lon": 90},
                            opacity=0.5,
                            labels={'district':'district blah'}
                            )
    # fig.update_layout(mapbox_style="carto-positron", 
    #                       mapbox_zoom=5.5,
    #                       mapbox_center={"lat": 23.7, "lon": 90},
    #                       margin={"r":0,"t":0,"l":0,"b":0},
    #                       uirevision='constant')
        
  #      return fig
#    fig.show() 
    
#    st.plotly_chart(fig, use_container_width=True)
    mouseselect=plotly_events(fig)
    st.write(mouseselect)


if reportchoice: 
    
    
    ## new part:
    
    filename = basepath + datapath + 'STATICBAHIS_geo_cluster_202204301723.csv'
    bahis_datageo = pd.read_csv(filename)
            
    
        
    filename = basepath + datapath + 'formdata_Patients_Registry.csv'
    #@st.cache
    def read_bahis_dataPat(filename):
        return pd.read_csv(filename, low_memory=False) #bad way of mixed variables. but there were too many columns
    # (17,33,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69) have mixed types. and tehre was something with 3?
    bahis_dataPat= read_bahis_dataPat(filename)
    bahis_dataPat['date'] = pd.to_datetime(bahis_dataPat['date'],format='%Y/%m/%d')
    st.dataframe(bahis_dataPat)
    
    ##### figure 1
    st.write("figure 1 Livestock disease cases")
    # speciesid  speciesname ['species'] list could be extracted from  datasource list species
    # 1 	Buffalo
    # 2 	Cat
    # 3 	Cattle
    # 4 	Dog
    # 5 	Goat
    # 6 	Horse
    # 7 	Pig
    # 8 	Sheep
    # 21 	Chicken
    # 22 	Duck
    # 23 	Goose
    # 24 	Moyana
    # 25 	Pegion
    # 26 	Quail
    # 27 	Turkey
    # 28 	Parrot
    # poultry is 21-23,25-27
    # large animal is 1,3,5,8
    
    # slider
    
    # dates = st.slider('Select date', start_date, end_date, (start_date, end_date)) 
    # sub_cst_data=cst_data.loc[cst_data['updated_at'].between(pd.to_datetime(dates[0]), pd.to_datetime(dates[1]))]
    # date_placeholder.subheader("Selected Date range: From " + str(dates[0]) + " until " + str(dates[1]))
    # subtable(sub_cst_data) 
    
    subPoultry = bahis_dataPat[(bahis_dataPat['species']==21) | 
                             (bahis_dataPat['species']==22) | 
                             (bahis_dataPat['species']==23) | 
                             (bahis_dataPat['species']==25) |
                             (bahis_dataPat['species']==26) | 
                             (bahis_dataPat['species']==27) ]
    DoccurPoultry= subPoultry['tentative_diagnosis'].value_counts()
    #DoccurPoultry= DoccurPoultry.to_dict()
    subLarge = bahis_dataPat[(bahis_dataPat['species']==1) | 
                             (bahis_dataPat['species']==3) | 
                             (bahis_dataPat['species']==5) | 
                             (bahis_dataPat['species']==8) ]
    DoccurLarge = subLarge['tentative_diagnosis'].value_counts()
    
    figP= px.bar(DoccurPoultry[9::-1], x='tentative_diagnosis', labels={"tentative_diagnosis":"Incidences", "index":"Disease"}, title="Poultry Top10", orientation='h')
    figL= px.bar(DoccurLarge[9::-1], x='tentative_diagnosis', labels={"tentative_diagnosis":"Incidences", "index":"Disease"}, title="Large Animals Top10", orientation='h')
    st.write(figP,figL)
    
    ##### figure 2
    st.write("figure 2 FMD cases")
    # ['tentative diagnosis']
    subFMD = bahis_dataPat[(bahis_dataPat['tentative_diagnosis']=="['Foot and Mouth Disease (FMD)']")]
    cases=subFMD['date'].groupby(subFMD.date.dt.to_period("M")).agg({'count'})
    cases.index=cases.index.astype(str)
    cases.index=pd.to_datetime(cases.index)
    cases['date']=cases.index
    subFMD2019 = cases[cases['date'].dt.year == 2019]
    subFMD2020 = cases[cases['date'].dt.year == 2020]
    subFMD2021 = cases[cases['date'].dt.year == 2021]
    subFMD2022 = cases[cases['date'].dt.year == 2022]
    
    fig = go.Figure()
    # fig.add_trace(go.Bar(
    #     x=months,
    #     y=subFMD2019['count'],
    #     name='2019',
    #     marker_color='indianred'
    # ))
    fig.add_trace(go.Bar(
        x=months,
        y=subFMD2020['count'],
        name='2020',
        marker_color='cornflowerblue'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=subFMD2021['count'],
        name='2021',
        marker_color='darkorange'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=subFMD2022['count'],
        name='2022',
        marker_color='gold'
    ))
    
    st.plotly_chart(fig)
    
    #### figure 3
    st.write("figure 3 PPR cases (goat)")
    subPPR = bahis_dataPat[(bahis_dataPat['tentative_diagnosis']=="['Pesti des Petits Ruminants']")]
    cases=subPPR['date'].groupby(subPPR.date.dt.to_period("M")).agg({'count'})
    cases.index=cases.index.astype(str)
    cases.index=pd.to_datetime(cases.index)
    cases['date']=cases.index
    subPPR2020 = cases[cases['date'].dt.year == 2020]
    subPPR2021 = cases[cases['date'].dt.year == 2021]
    subPPR2022 = cases[cases['date'].dt.year == 2022]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=subPPR2020['count'],
        name='2020',
        marker_color='cornflowerblue'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=subPPR2021['count'],
        name='2021',
        marker_color='darkorange'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=subPPR2022['count'],
        name='2022',
        marker_color='gold'
    ))
    
    st.plotly_chart(fig)
    
    
    #### figure 4
    st.write("figure 4 mycoplasma cases (poultry)")
    subMP = bahis_dataPat[(bahis_dataPat['tentative_diagnosis']=="['Mycoplasmosis']")]
    cases=subMP['date'].groupby(subMP.date.dt.to_period("M")).agg({'count'})
    cases.index=cases.index.astype(str)
    cases.index=pd.to_datetime(cases.index)
    cases['date']=cases.index
    subMP2020 = cases[cases['date'].dt.year == 2020]
    subMP2021 = cases[cases['date'].dt.year == 2021]
    subMP2022 = cases[cases['date'].dt.year == 2022]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=subMP2020['count'],
        name='2020',
        marker_color='cornflowerblue'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=subMP2021['count'],
        name='2021',
        marker_color='darkorange'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=subMP2022['count'],
        name='2022',
        marker_color='gold'
    ))
    
    st.plotly_chart(fig)
    
    
    #### figure 5
    st.write("figure 5 ND cases (poultry)")
    subND = bahis_dataPat[(bahis_dataPat['tentative_diagnosis']=="['Newcastle Disease']")]
    cases=subND['date'].groupby(subND.date.dt.to_period("M")).agg({'count'})
    cases.index=cases.index.astype(str)
    cases.index=pd.to_datetime(cases.index)
    cases['date']=cases.index
    subND2020 = cases[cases['date'].dt.year == 2020]
    subND2021 = cases[cases['date'].dt.year == 2021]
    subND2022 = cases[cases['date'].dt.year == 2022]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=subND2020['count'],
        name='2020',
        marker_color='cornflowerblue'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=subND2021['count'],
        name='2021',
        marker_color='darkorange'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=subND2022['count'],
        name='2022',
        marker_color='gold'
    ))
    
    st.plotly_chart(fig)
    #st.bar_chart(cases)
    
    
    st.write("figure 6-9 skipped bc LBM data unavailable")
    st.write("figure 10 skipped, bc antibiotics in specific module")
    st.write("figure 11 outbreaks not needed at the moment")
    
    filename = basepath + datapath + 'formdata_Farm_Assessment_Monitoring.csv'
    # @st.cache
    def read_bahis_dataFarm(filename):
        return pd.read_csv(filename, low_memory=False) #bad way of mixed variables. but there were too many columns
    # (17,33,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69) have mixed types. and tehre was something with 3?
    bahis_dataFarm= read_bahis_dataFarm(filename)
    bahis_dataFarm['district'] = pd.to_numeric(bahis_dataFarm['district'])
    bahis_dataFarm.loc[:, "district"] = bahis_dataFarm["district"].map('{:.0f}'.format)
    bahis_dataFarm['date_initial_visit'] = pd.to_datetime(bahis_dataFarm['date_initial_visit'],format='%Y/%m/%d')
    
    st.dataframe(bahis_dataFarm)
    
    
    #### figure 12 per district
    st.write("figure 12 district wise U2C report (Feb2017 to March 2019)")
    cases = bahis_dataFarm['district'].value_counts().to_frame()
    cases['districtname'] = cases.index
    cases= cases.loc[cases['districtname'] != 'nan']
    # cases=cases.dropna()
    subDist=bahis_datageo[(bahis_datageo["loc_type"]==2)]
    subDist['cases']=subDist.index
    for i in range(cases.shape[0]):
        cases['districtname'].iloc[i] = subDist.loc[subDist['value']==int(cases['districtname'].iloc[i]),'name'].iloc[0]
    #for i in range(cases.shape[0]):
        subDist['cases'][subDist.loc[subDist['name']==cases['districtname'].iloc[i]].index[0]] = cases['district'].iloc[i]
    cases=cases.sort_values('districtname')
    fig=px.bar(cases, x='districtname', y='district', labels= {'district':'incidences'})
    # cases["districtname"]= cases["districtname"].replace({subDist['value'],subDist['name']}, inplace=True)
    # searchindex=bahis_datageo[bahis_datageo["value"]==searchplace]
    # st.map(searchindex)
    # st.write("Here is the selected place:", bahis_datageo[bahis_datageo["value"]==searchplace]['name'])
    st.plotly_chart(fig)
    #st.bar_chart(cases)
    ###connect to geolocation list, select date period
            
    st.pydeck_chart(pdk.Deck(
          map_style='mapbox://styles/mapbox/light-v9',
          initial_view_state=pdk.ViewState(
              latitude=22.4,
              longitude=90.3,
              zoom=7,
              pitch=400,
          ),
          layers=[
                    pdk.Layer(
                        'ColumnLayer',
                        data=subDist,
                        get_position='[longitude, latitude]',
                        get_elevation="cases",
                        elevation_scale=300,
                        get_color='[200, 30, 0, 160]',
                        radius=5000,
                    ),
                ],
            ))
    
    filename = basepath + datapath + 'AWaReclass.csv'
    # @st.cache
    def read_bahis_dataAWaRe(filename):
        return pd.read_csv(filename) 
    bahis_dataAware = read_bahis_dataAWaRe(filename)
    
    filename = basepath + datapath + 'Antibiotics.csv'
    # @st.cache
    def read_bahis_dataAB(filename):
        return pd.read_csv(filename) 
    bahis_dataAB = read_bahis_dataAB(filename)
    
    
    st.write("figure 13 Frequency histogram of antibiotics used (U2C)")
    st.write("figure 14 Antibiotics Usage")
    st.write("figure 15 Antibiotics")
    
    #subQ = bahis_dataFarm[bahis_dataFarm['date_initial_visit'].dt.year == 2022 ]
    start_date='2022-01-01'
    end_date='2022-04-01'
    mask=(bahis_dataFarm['date_initial_visit']>= start_date) & (bahis_dataFarm['date_initial_visit'] < end_date)
    subQ = bahis_dataFarm.loc[mask]
    
    
    #### figure 18
    st.write("figure 18 Access control farm entry")
    # v-aa
    tmp = subQ['outside_worker_do_not_enter_farm'].value_counts()
    a1=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['only_workers_approved_visitor_enter_farm'].value_counts()
    a2=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['no_manure_collector_enter_farm'].value_counts()
    a3=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['fenced_duck_chicken_proof'].value_counts()
    a4=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['dead_birds_disposed_safely'].value_counts()
    a5=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['sign_posted'].value_counts()
    a6=tmp[0]/(tmp[0]+tmp[1])
    st.bar_chart([a1,a2,a3,a4,a5,a6])
    
    
    
    #### figure 19
    st.write("figure 19 Access control loading area")
    #ab-ae
    tmp = subQ['no_vehical_in_out_production_area'].value_counts()
    b1=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['only_workers_enter_production_area'].value_counts()
    b2=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['visitors_enter_production_if_approve_manager'].value_counts()
    b3=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['access_control_loading_production_sign_posted'].value_counts()
    b4=tmp[0]/(tmp[0]+tmp[1])
    st.bar_chart([b1,b2,b3,b4])
    
    
    
    #### figure 20
    st.write("figure 20 Personell managements")
    #af-ai
    tmp = subQ['footwear_left_outside'].value_counts()
    c1=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['change_clothes_entering_farm'].value_counts()
    c2=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['uses_dedicated_footwear'].value_counts()
    c3=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['shower_entering_farm'].value_counts()
    c4=tmp[0]/(tmp[0]+tmp[1])
    
    tmp = bahis_dataFarm['footwear_left_outside'].value_counts()
    c1t=tmp[0]/(tmp[0]+tmp[1])
    tmp = bahis_dataFarm['change_clothes_entering_farm'].value_counts()
    c2t=tmp[0]/(tmp[0]+tmp[1])
    tmp = bahis_dataFarm['uses_dedicated_footwear'].value_counts()
    c3t=tmp[0]/(tmp[0]+tmp[1])
    tmp = bahis_dataFarm['shower_entering_farm'].value_counts()
    c4t=tmp[0]/(tmp[0]+tmp[1])
    
    source = pd.DataFrame({
        '% of Total Farm': ['c1. Outside footwear left outside farm',
                            'c2. Workers and visitors change clothes upon entering farm',
                            'c3. Workers and visitors use only dedicated footwear in production area',
                            'c4. Workers and visitors shower upon entering farm'],
        '% of Total Farm (timeperiod; n=)': [c1, c2, c3, c4],
        '% of Cumulative Total Farm (timeperiod; n=)': [c1t, c2t, c3t, c4t]
    })
    
    bar = alt.Chart(source).mark_bar().encode(
        x='% of Total Farm:O',
        y='% of Total Farm (timeperiod; n=):Q'
    ).properties(
        width=alt.Step(120)  # controls width of bar.
    )
    
    point = alt.Chart(source).mark_point(
        color='black',
      #  size=120 * 0.9,  # controls width of tick.
    ).encode(
        x='% of Total Farm:O',
        y='% of Cumulative Total Farm (timeperiod; n=):Q'
    )
    fig=bar+point
    st.altair_chart(fig)  
    st.altair_chart(bar, use_container_width=True)  
    st.altair_chart(point, use_container_width=True)   
    # bar + tick
    
    # st.bar_chart([c1,c2,c3,c4])
    
    #### figure 21
    st.write("figure 21 Equipment managements")
    #aj-ak
    tmp = subQ['returning_materials_cleaned'].value_counts()
    d1=tmp[0]/(tmp[0]+tmp[1])
    tmp = subQ['returning_materials_disinfect'].value_counts()
    d2=tmp[0]/(tmp[0]+tmp[1])
    source = pd.DataFrame({'Percentage of (%) total farm': [d1,d2],
                           '% of Total Farm': ['d1. Materials returning from market or other farm cleaned with soap and water before entereing farm', 
                                               'd2. Materials returning from market or ther farm disinfected before entering the farm']
                           })
    
    bar_chart = alt.Chart(source).mark_bar().encode(
        y='Percentage of (%) total farm:Q',
        x='% of Total Farm:O',
        )
     
    st.altair_chart(bar_chart, use_container_width=True)                      
                           
    
    #st.bar_chart([d1,d2])
    
    
    
    





### old part
if oldchoice:
    if option == txt_farms:
        filename = basepath + datapath + 'farms_matched.csv'
        bahis_data = pd.read_csv(filename)
        st.dataframe(bahis_data)
        choice = st.checkbox("age arrival farm bahis")
        if choice:
            occurencesFarmsA=bahis_data['age_arrival_farm_bahis'].value_counts()
            st.bar_chart(occurencesFarmsA)
            cola1, cola2, cola3 = st.columns(3) 
            
            with cola1:
                st.metric(label='adult', value="{:0,.0f}".format(int(occurencesFarmsA['Adult'])))
                
            with cola2:
                st.metric(label='doc', value="{:0,.0f}".format(int(occurencesFarmsA['DOC'])))
            
            with cola3:
                st.metric(label='pullet', value="{:0,.0f}".format(int(occurencesFarmsA['Pullet'])))
    
        occurencesFarmsB=bahis_data['antibacterial_frequency_product1_bahis'].value_counts()
        st.bar_chart(occurencesFarmsB)
        occurencesFarmsB=bahis_data['antibacterial_usage_salesman_product1'].value_counts()
        st.dataframe(occurencesFarmsB)
        occurencesFarmsB=bahis_data['birds_production_purpose_bahis'].value_counts()
        st.bar_chart(occurencesFarmsB)    
        occurencesFarmsB=bahis_data['type_species_bahis'].value_counts()
        st.bar_chart(occurencesFarmsB)
    
        # concept via st.empty if you want to fill something being loaded later in the program
        # placeholder=st.empty()  
        
        st.line_chart(bahis_data['date_initial_visit_bahis'].value_counts())
        bahis_data['date_initial_visit_bahis']=pd.to_datetime(bahis_data['date_initial_visit_bahis'])
        min_date=bahis_data['date_initial_visit_bahis'].min().to_pydatetime()
        max_date=bahis_data['date_initial_visit_bahis'].max().to_pydatetime()
        values = st.slider('Select date', min_date, max_date)
        st.write('Values:', values)
      
        
    ######XXXXXX
        # with st.expander("a map for the cases logged for that day can be shown"):
        #     searchcolumn=bahis_data["upazila_bahis"]
        #     searchplace=int(searchcolumn.iloc[values])
            
        #     filename = basepath + datapath + 'STATICBAHIS_geo_cluster_202204301723.csv'
        #     bahis_datageo = pd.read_csv(filename)
        #     searchindex=bahis_datageo[bahis_datageo["value"]==searchplace]
        #     st.map(searchindex)
        #     st.write("Here is the selected place:", bahis_datageo[bahis_datageo["value"]==searchplace]['name'])
            
            
     
        
        
    if option == txt_geocluster:
        filename = basepath + datapath + 'STATICBAHIS_geo_cluster_202204301723.csv'
        bahis_data = pd.read_csv(filename)
        df=bahis_data.fillna(0)
        st.map(df) 
        st.dataframe(bahis_data)
        
        # polygon and shpaefile did not work because of map base and geopandas.
    #if option == txt_shpfiles:
        # polygon = gpd.read_file(r"C:/Users/yoshka/Documents/GitHub/bahis_dash/bangladesh-geojson-master/bangladesh.geojson")
        # polygon=polygon.set_crs('epsg:4326')
        # fig, aaa = plt.subplots()
        # aaa.set_aspect('equal')
     ##   fig1, axiss =plt.subplots()
     ##   upas=polygon.plot(figsize=(2,2), ax=axiss, color='white', edgecolor ='black')
        
        # filename = basepath + 'STATICBAHIS_geo_cluster_202204301723.csv'
        # bahis_data = pd.read_csv(filename)
        # df=bahis_data.fillna(0)
        # locs=df.plot(ax=axiss, marker='o', color='red', markersize=0)
      #  cx.add_basemap(axisss, crs=polygon.crs.to_string())
     ##   st.pyplot()
    
        
    if option == txt_aviinvest:
        filename = basepath + datapath + 'formdata_Avian_Influenza_Investigation.csv'
        bahis_data = pd.read_csv(filename)
     # ?  occurencesDC = bahis_data['date_completed'].value_counts()
        bahis_data['date_completed']=pd.to_datetime(bahis_data['date_completed'])
     # take this? when fixed   occurencesDates=bahis_data.groupby([bahis_data['date_completed'].dt.year.rename('year'), bahis_data['date_completed'].dt.month.rename('month')]).agg({'count'})
     # take this? too   occurencesDates=bahis_data.groupby([bahis_data['date_completed'].dt.year.rename('year') , bahis_data['date_completed'].dt.month.rename('month')]).agg({'count'})
        occurencesDates=bahis_data.groupby([bahis_data['date_completed'].dt.month.rename('month')]).agg({'count'})
        occurencesDates=occurencesDates['date_completed']
        occurencesDates= pd.to_datetime(occurencesDates.index)
        st.bar_chart(occurencesDates)
      
        occurencesAN = bahis_data['admin_name1'].value_counts()
        st.bar_chart(occurencesAN)
        occurencesS = bahis_data['sex'].value_counts()
        st.bar_chart(occurencesS)
        occurencesDiv = bahis_data['division'].value_counts()
        st.bar_chart(occurencesDiv)    
        occurencesD = bahis_data['district'].value_counts()
        st.bar_chart(occurencesD)
        occurencesU = bahis_data['upazila'].value_counts()
        st.bar_chart(occurencesU)
        
        st.dataframe(bahis_data)
        
     #   bahis_data.groupby([bahis_data['date_completed'].dt.year.rename('year'), bahis_data['date_completed'].dt.month.rename('month')]).agg({'count'})
    
    
    if option == txt_avisample:
        filename = basepath + datapath + 'formdata_Avian_Influenza_Sample.csv'
        bahis_data = pd.read_csv(filename)  
        st.dataframe(bahis_data)
        
    if option == txt_disinvest:
        filename = basepath + datapath + 'formdata_Disease_Investigation.csv'
        bahis_data = pd.read_csv(filename)
        st.dataframe(bahis_data)
    
    if option == txt_farmass:
        filename = basepath + datapath + 'formdata_Farm_Assessment_Monitoring.csv'
        bahis_data = pd.read_csv(filename)
        st.dataframe(bahis_data)
    
    if option == txt_partlsass:
        filename = basepath + datapath + 'formdata_Participatory_Livestock_Assessment.csv'
        bahis_data = pd.read_csv(filename)
        occurences = bahis_data['upazila'].value_counts()
        st.bar_chart(occurences)
        st.dataframe(bahis_data)
        
    if option == txt_patreg:
        # filename = basepath + 'formdata_Patients_Registry.csv'
        # bahis_data = pd.read_csv(filename)
        
        filename = basepath + datapath + 'STATICBAHIS_geo_cluster_202204301723.csv'
        bahis_data = pd.read_csv(filename)
        df=bahis_data.dropna()
        st.dataframe(bahis_data)
        
        # df = pd.DataFrame(
        # np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        # columns=['latitude', 'longitude'])
        st.pydeck_chart(pdk.Deck(
             map_style='mapbox://styles/mapbox/light-v9',
             initial_view_state=pdk.ViewState(
                 latitude=22.4,
                 longitude=90.3,
                 zoom=7,
                 pitch=50,
             ),
             layers=[
                 pdk.Layer(
                    'HexagonLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    radius=800,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                 ),
                 pdk.Layer(
                     'ScatterplotLayer',
                     data=df,
                     get_position='[longitude, latitude]',
                     get_color='[200, 30, 0, 160]',
                     get_radius=200,
                 ),
             ],
         ))
    
    
    if option == txt_missfarm:
        filename = basepath + datapath + 'missing_farms.csv'
        bahis_data = pd.read_csv(filename)
        st.dataframe(bahis_data)
    

    min_val=0
    max_val=bahis_data.shape[0]
    values = st.slider(
          'Select entry',
          min_val, max_val, 1)-1
    st.write('Values:', values)
    tableordataframe = st.checkbox("dataframe if checked otherwise table")
    if tableordataframe:
        st.table(bahis_data.iloc[values,:].astype(str))
    else:
        st.dataframe(bahis_data.iloc[values,:].astype(str))
    
    if option == txt_farms:
        st.write("The selected place from farms shown on the following map")
        with st.expander("a map can be shown"):
            searchcolumn=bahis_data["upazila_bahis"]
            searchplace=int(searchcolumn.iloc[values])
            
            filename = basepath + datapath + 'STATICBAHIS_geo_cluster_202204301723.csv'
            bahis_datageo = pd.read_csv(filename)
            searchindex=bahis_datageo[bahis_datageo["value"]==searchplace]
            st.map(searchindex)
            st.write("Here is the selected place:", bahis_datageo[bahis_datageo["value"]==searchplace]['name'])
            
            
            