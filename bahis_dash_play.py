# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:14:48 2022

@author: yoshka
"""

import streamlit as st
import pandas as pd
import pydeck as pdk

basepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/play around'
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

# define page layout
st.set_page_config(layout="wide")

#### side window
#sidebar
# logo !!!!!SOURCE
st.sidebar.image(basepath + logopath + "bahis-logo.png", width=150)
option = st.sidebar.selectbox(
     txt_select,
     (txt_farms, txt_geocluster, txt_shpfiles, txt_aviinvest, txt_avisample,
     txt_disinvest, txt_farmass, txt_partlsass, txt_patreg, txt_missfarm))
      

st.write('You selected:', option)


if option == txt_farms:
    filename = basepath + datapath + 'farms_matched.csv'
    bahis_data = pd.read_csv(filename)
    st.dataframe(bahis_data)

if option == txt_geocluster:
    filename = basepath + datapath + 'STATICBAHIS_geo_cluster_202204301723.csv'
    bahis_data = pd.read_csv(filename)
    df=bahis_data.fillna(0)
    st.map(df) 
    st.dataframe(bahis_data)
    
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
 #   occurencesDC = bahis_data['date_completed'].value_counts()
    bahis_data['date_completed']=pd.to_datetime(bahis_data['date_completed'])
 # take this when fixed   occurencesDates=bahis_data.groupby([bahis_data['date_completed'].dt.year.rename('year'), bahis_data['date_completed'].dt.month.rename('month')]).agg({'count'})
 # take this too   occurencesDates=bahis_data.groupby([bahis_data['date_completed'].dt.year.rename('year') , bahis_data['date_completed'].dt.month.rename('month')]).agg({'count'})
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
      min_val, max_val, 1)
st.write('Values:', values)