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


#### figure 12
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



st.write("figure 13 Frequency histogram of antibiotics used (U2C)")
st.write("figure 14 Antibiotics Usage")
st.write("figure 15 Antibiotics")

#subQ = bahis_dataFarm[bahis_dataFarm['date_initial_visit']=]
#### figure 18
st.write("figure 18 Access control farm entry")
# v-aa


#### figure 19
st.write("figure 19 Access control loading area")
#ab-ae

#### figure 20
st.write("figure 20 Personell managements")
#af-ai

#### figure 21
st.write("figure 21 Equipment managements")
#aj-ak










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
            
            
            