# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:14:48 2022

@author: yoshka
"""

import streamlit as st
import pandas as pd
#import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
import json 

# set paths and sources
basepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around'
datapath = '/output/'
logopath = '/logos/'
geofilename = basepath + datapath + 'STATICBAHIS_geo_cluster_202204301723.csv'
patfilename = basepath + datapath + 'formdata_Patients_Registry.csv'
farmfilename = basepath + datapath + 'formdata_Farm_Assessment_Monitoring.csv'
path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM0-all/geoBoundaries-BGD-ADM0.geojson" #1 Nation
path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM1-all/geoBoundaries-BGD-ADM1.geojson" #8 Division
path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM2-all/geoBoundaries-BGD-ADM2.geojson" #64 District
path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM3-all/geoBoundaries-BGD-ADM3.geojson" #495 Upazila
path4= "C:/Users/yoshka/Documents/GitHub/bahis-dash/play_around/geoBoundaries-BGD-ADM4-all/geoBoundaries-BGD-ADM4.geojson" #4562 Union


# set textfiles probably changeable language
#txtQrep = "quarterly report template"
txtTitle = "Information on Bahis Database"
txtInfections = "Reported Infections"
txtTempBars = "Explore Time Development"
txtMapChoice = "Explore Regional Status"
txtLMeasures = "Explore Measures"
txtRepStat = "Reporting Status"
txtLocalInfo = "Explore Situation at specific Region"
txtPoultry = "Poultry"
txtLAnimals = "Large Animals"


txt1Buffalo = 'Buffalo'
txt2Cat = 'Cat'
txt3Cattle = 'Cattle'
txt4Dog = 'Dog'
txt5Goat = 'Goat'
txt6Horse = 'Horse'
txt7Pig = 'Pig'
txt8Sheep = 'Sheep'
txt21Chicken = 'Chicken'
txt22Duck = 'Duck'
txt23Goose = 'Goose'
txt24Moyana = 'Moyana'
txt25Pigeon = 'Pigeon'
txt26Quail = 'Quail'
txt27Turkey = 'Turkey'
txt28Parrot = 'Parrot'
    

txtFMD = 'Cases of Foot and Mouth Disease'
txtPPR = 'Cases of Pesti de Petits Ruminants in goat'   
txtMP = 'Cases of mycoplasma in poultry'   
txtND = 'Cases of Newcastle Disease in poultry'   


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# define page layout
st.set_page_config(layout="wide")

# logos from sponsors in the sidebar
st.sidebar.image("/Users/yoshka/Documents/GitHub/bahis-dash/play_around/logos/bahis-logo.png", use_column_width=True)
st.sidebar.subheader(txtTitle)
choice= st.sidebar.selectbox('Choose', (txtInfections, txtTempBars, txtMapChoice, txtLMeasures, txtRepStat, txtLocalInfo))
#blnQrep = st.sidebar.checkbox(txtQrep)

st.sidebar.image("/Users/yoshka/Documents/GitHub/bahis-dash/play_around/logos/DGHS logo.png", use_column_width=True)
st.sidebar.image("/Users/yoshka/Documents/GitHub/bahis-dash/play_around/logos/FAO logo.png", use_column_width=True)
st.sidebar.image("/Users/yoshka/Documents/GitHub/bahis-dash/play_around/logos/USAID logo.png", use_column_width=True)

#@st.cache
def read_geoData():
    return pd.read_csv(geofilename)  
def read_patData():
    return pd.read_csv(patfilename, low_memory=False) #bad way of mixed variables. but there were too many columns
def read_farmData():
    return pd.read_csv(farmfilename, low_memory=False) #bad way of mixed variables. but there were too many columns

bahis_geodata = read_geoData()
bahis_patdata = read_patData()
bahis_patdata['date'] = pd.to_datetime(bahis_patdata['date'],format='%Y/%m/%d')
bahis_farmdata = read_farmData()
bahis_farmdata['division'] = pd.to_numeric(bahis_farmdata['division'])
bahis_farmdata['district'] = pd.to_numeric(bahis_farmdata['district'])
bahis_farmdata['upazila'] = pd.to_numeric(bahis_farmdata['upazila'])
bahis_farmdata.loc[:, "district"] = bahis_farmdata["district"].map('{:.0f}'.format)
bahis_farmdata['date_initial_visit'] = pd.to_datetime(bahis_farmdata['date_initial_visit'],format='%Y/%m/%d')
    
if choice == txtInfections: 

#    st.dataframe(bahis_patdata)

    start_date=min(bahis_patdata['date']).date()
    end_date=max(bahis_patdata['date']).date()
    date_placeholder=st.empty()    
    dates = st.slider('Select date', start_date, end_date, (start_date, end_date)) 
    sub_bahis_patdata=bahis_patdata.loc[bahis_patdata['date'].between(pd.to_datetime(dates[0]), pd.to_datetime(dates[1]))] 
    
    
    colPoultry, colLAnimals= st.columns(2)
    with colPoultry:
        st.subheader(txtPoultry)
        selectionP = st.multiselect('Selected species', [txt21Chicken, txt22Duck, txt23Goose, txt24Moyana, txt25Pigeon, txt26Quail, txt27Turkey, txt28Parrot],
                       [txt21Chicken, txt22Duck, txt23Goose, txt25Pigeon, txt26Quail, txt27Turkey])
        ############### todo
        # preselection to be modified and included into DF subPoultry
        # select either Top10 or all
        # select time range
        # select map accumulation
        subPoultry = None
        if txt21Chicken in selectionP:
            subPoultry = pd.concat([subPoultry,sub_bahis_patdata[(sub_bahis_patdata['species']==21)]])
        if txt22Duck in selectionP:
            subPoultry = pd.concat([subPoultry,sub_bahis_patdata[(sub_bahis_patdata['species']==22)]])
        if txt23Goose in selectionP:
            subPoultry= pd.concat([subPoultry,sub_bahis_patdata[(sub_bahis_patdata['species']==23)]])
        if txt24Moyana in selectionP:
            subPoultry = pd.concat([subPoultry,sub_bahis_patdata[(sub_bahis_patdata['species']==24)]])
        if txt25Pigeon in selectionP:
            subPoultry = pd.concat([subPoultry,sub_bahis_patdata[(sub_bahis_patdata['species']==25)]])
        if txt26Quail in selectionP:
            subPoultry = pd.concat([subPoultry,sub_bahis_patdata[(sub_bahis_patdata['species']==26)]])
        if txt27Turkey in selectionP:
            subPoultry = pd.concat([subPoultry,sub_bahis_patdata[(sub_bahis_patdata['species']==27)]])
        if txt28Parrot in selectionP:
            subPoultry = pd.concat([subPoultry,sub_bahis_patdata[(sub_bahis_patdata['species']==28)]])

        # subPoultry = bahis_patdata[(bahis_patdata['species']==21) | 
        #                           (bahis_patdata['species']==22) | 
        #                           (bahis_patdata['species']==23) | 
        #                           (bahis_patdata['species']==25) |
        #                           (bahis_patdata['species']==26) | 
        #                           (bahis_patdata['species']==27) ]
        DoccurPoultry= subPoultry['tentative_diagnosis'].value_counts()
        figP= px.bar(DoccurPoultry[9::-1], x='tentative_diagnosis', labels={"tentative_diagnosis":"Incidences", "index":"Disease"}, title="Poultry Top10", orientation='h')
        st.write(figP)
        
    with colLAnimals:
        st.subheader(txtLAnimals)
        selectionLA = st.multiselect('Selected Species', [txt1Buffalo, txt2Cat, txt3Cattle, txt4Dog, txt5Goat, txt6Horse, txt7Pig, txt8Sheep],
                       [txt1Buffalo, txt3Cattle, txt5Goat, txt8Sheep])
        ############### todo
        # select either Top10 or all
        # select map accumulation
        subLarge = None
        if txt1Buffalo in selectionLA:
            subLarge = pd.concat([subLarge, sub_bahis_patdata[(sub_bahis_patdata['species']==1)]])
        if txt2Cat in selectionLA:
            subLarge = pd.concat([subLarge, sub_bahis_patdata[(sub_bahis_patdata['species']==2)]])
        if txt3Cattle in selectionLA:
            subLarge = pd.concat([subLarge, sub_bahis_patdata[(sub_bahis_patdata['species']==3)]])
        if txt4Dog in selectionLA:
            subLarge = pd.concat([subLarge, sub_bahis_patdata[(sub_bahis_patdata['species']==4)]])
        if txt5Goat in selectionLA:
            subLarge = pd.concat([subLarge, sub_bahis_patdata[(sub_bahis_patdata['species']==5)]])
        if txt6Horse in selectionLA:
            subLarge = pd.concat([subLarge, sub_bahis_patdata[(sub_bahis_patdata['species']==6)]])
        if txt7Pig in selectionLA:
            subLarge = pd.concat([subLarge, sub_bahis_patdata[(sub_bahis_patdata['species']==7)]])
        if txt8Sheep in selectionLA:
            subLarge = pd.concat([subLarge, sub_bahis_patdata[(sub_bahis_patdata['species']==8)]])    
        
        # subLarge = bahis_patdata[(bahis_patdata['species']==1) | 
        #                           (bahis_patdata['species']==3) | 
        #                           (bahis_patdata['species']==5) | 
        #                           (bahis_patdata['species']==8) ]
        DoccurLarge = subLarge['tentative_diagnosis'].value_counts()    
        figL= px.bar(DoccurLarge[9::-1], x='tentative_diagnosis', labels={"tentative_diagnosis":"Incidences", "index":"Disease"}, title="Large Animals Top10", orientation='h')
        st.write(figL)


if choice == txtTempBars:
    
    DChoice = st.selectbox('Select Disease', (txtFMD, txtPPR, txtMP, txtND))
 
    #########to do
    # work with st.cache make function
    subFMD = bahis_patdata[(bahis_patdata['tentative_diagnosis']=="['Foot and Mouth Disease (FMD)']")]   
    subPPR = bahis_patdata[(bahis_patdata['tentative_diagnosis']=="['Pesti des Petits Ruminants']")]   
    subMP = bahis_patdata[(bahis_patdata['tentative_diagnosis']=="['Mycoplasmosis']")]   
    subND = bahis_patdata[(bahis_patdata['tentative_diagnosis']=="['Newcastle Disease']")]  
    
    if DChoice == txtFMD:
        ##### figure 2
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
        
        st.plotly_chart(fig, use_container_width=True)
    
    if DChoice == txtPPR:
        #### figure 3
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
        
        st.plotly_chart(fig, use_container_width=True)
    
    if DChoice == txtMP:   
        #### figure 4
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
        
        st.plotly_chart(fig, use_container_width=True)
    
    if DChoice == txtND:   
        #### figure 5
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
        
        st.plotly_chart(fig, use_container_width=True)
        
    
if choice == txtMapChoice:
    
    cases = bahis_farmdata['district'].value_counts().to_frame()
    cases['districtname'] = cases.index
    cases= cases.loc[cases['districtname'] != 'nan']
    # cases=cases.dropna()
    subDist=bahis_geodata[(bahis_geodata["loc_type"]==2)]
    subDist['cases']=subDist.index
    for i in range(cases.shape[0]):
        cases['districtname'].iloc[i] = subDist.loc[subDist['value']==int(cases['districtname'].iloc[i]),'name'].iloc[0]
    #for i in range(cases.shape[0]):
        subDist['cases'][subDist.loc[subDist['name']==cases['districtname'].iloc[i]].index[0]] = cases['district'].iloc[i]
    cases=cases.sort_values('districtname')
    cases['districtname']=cases['districtname'].str.title()
    
    fig=px.bar(cases, x='districtname', y='district', labels= {'district':'Incidences'})

    st.plotly_chart(fig)
    
     
#    @st.cache 
    def open_data(path):
        with open(path) as f:
            data = json.load(f)
            return data
        
    data = open_data(path2)
    
    for i in data['features']:
        i['id']= i['properties']['shapeName'].replace(" District","") 
        
    fig = px.choropleth_mapbox(cases, geojson=data, locations='districtname', color='district',
                            color_continuous_scale="Viridis",
                            range_color=(0, cases['district'].max()),
                            mapbox_style="carto-positron",
                            zoom=5.5, center = {"lat": 23.7, "lon": 90},
                            opacity=0.5,
                            labels={'district':'Incidences per district'}
                          )
    fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)




if choice == txtLMeasures:
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
    
    
    # st.write("figure 13 Frequency histogram of antibiotics used (U2C)")
    # st.write("figure 14 Antibiotics Usage")
    # st.write("figure 15 Antibiotics")
    
    #subQ = bahis_dataFarm[bahis_dataFarm['date_initial_visit'].dt.year == 2022 ]
    start_date='2021-01-01'
    end_date='2022-04-01'
    mask=(bahis_farmdata['date_initial_visit']>= start_date) & (bahis_farmdata['date_initial_visit'] < end_date)
    subQ = bahis_farmdata.loc[mask]
    
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
    
    tmp = bahis_farmdata['footwear_left_outside'].value_counts()
    c1t=tmp[0]/(tmp[0]+tmp[1])
    tmp = bahis_farmdata['change_clothes_entering_farm'].value_counts()
    c2t=tmp[0]/(tmp[0]+tmp[1])
    tmp = bahis_farmdata['uses_dedicated_footwear'].value_counts()
    c3t=tmp[0]/(tmp[0]+tmp[1])
    tmp = bahis_farmdata['shower_entering_farm'].value_counts()
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
    
if choice == txtRepStat:
    #######todo
    # at slider time period
    st.subheader('Reporting Status')
    
    # start_date, end_date = st.date_input('start date  - end date :', [pd.to_datetime('2020-01-01',format='%Y/%m/%d'), pd.to_datetime('today').floor('D')])
    # if start_date < end_date:
    #     pass
    # else:
    #     st.error('Error: End date must fall after start date.')

    # mask = (bahis_patdata['date'] > pd.Timestamp(start_date)) & (bahis_patdata['date'] <= pd.Timestamp(end_date))
    start_date=min(bahis_patdata['date']).date()
    end_date=max(bahis_patdata['date']).date()

    date_placeholder=st.empty()    
               
    dates = st.slider('Select date', start_date, end_date, (start_date, end_date)) 
    
    sub_bahis_patdata=bahis_patdata.loc[bahis_patdata['date'].between(pd.to_datetime(dates[0]), pd.to_datetime(dates[1]))]    
    sub_bahis_farmdata=bahis_farmdata.loc[bahis_farmdata['date_initial_visit'].between(pd.to_datetime(dates[0]), pd.to_datetime(dates[1]))]
    
    date_placeholder.subheader("Selected Date range: From " + str(dates[0]) + " until " + str(dates[1]))
    
    st.subheader('Patientdata')
    st.line_chart(sub_bahis_patdata['date'].value_counts())
    
###########
    cases = bahis_farmdata['district'].value_counts().to_frame()
    cases['districtname'] = cases.index
    cases= cases.loc[cases['districtname'] != 'nan']

    st.subheader('Farmdata')
    st.line_chart(sub_bahis_farmdata['date_initial_visit'].value_counts())
    
    
#     st.plotly_chart(fig)
    
     
#    @st.cache 
    def open_data(path):
        with open(path) as f:
            data = json.load(f)
            return data
    
#    values = ['<select>', '0: Nation' ,'1: Division', '2: District', '3: Upazila', '4: Union']
    values = ['<select>', '0: Nation' , '1: Division', '2: District', '3: Upazila']
    defaultV = values.index('2: District')
    granularity= st.selectbox('level', values, index=defaultV) 
    # if granularity=='0: Nation':
    #     path= path0    
    #     subDist=bahis_geodata[(bahis_geodata["loc_type"]==0)]
    
    if granularity=='0: Nation':
        path= path0
        subDist=bahis_geodata
        data = open_data(path)
  
        colTmp, colMap, colBar = st.columns(3)
        with colTmp:
            st.line_chart(sub_bahis_farmdata['date_initial_visit'].value_counts())        
        with colMap:
            data = open_data(path)
            
            for i in data['features']:
                i['id']= i['properties']['shapeName'].replace(" District","") 
    
            fig = px.choropleth_mapbox(data['features'], 
                                   geojson=data, 
                                   locations='id', 
                                   mapbox_style="carto-positron",
                                   zoom=5, 
                                   center = {"lat": 23.7, "lon": 90},
                                   opacity=0.5
                                  )
            fig.update_layout(autosize=True, width= 1000, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
            
        with colBar:
            st.metric(label= 'Cases', value= sub_bahis_farmdata.shape[0] )
            
    if granularity=='1: Division':
        path= path1
        subDist=bahis_geodata[(bahis_geodata["loc_type"]==1)]
        cases = sub_bahis_farmdata['division'].value_counts().to_frame()
        cases['divisionname'] = cases.index
        cases= cases.loc[cases['divisionname'] != 'nan']
        
        subDist['cases']=subDist.index    
        data = open_data(path)
        for i in data['features']:
            i['id']= i['properties']['shapeName'].replace(" Division","") 
        for i in range(cases.shape[0]):
            cases['divisionname'].iloc[i] = subDist.loc[subDist['value']==int(cases['divisionname'].iloc[i]),'name'].iloc[0]
        #for i in range(cases.shape[0]):
            subDist['cases'][subDist.loc[subDist['name']==cases['divisionname'].iloc[i]].index[0]] = cases['division'].iloc[i]
        cases=cases.sort_values('divisionname')
        cases['divisionname']=cases['divisionname'].str.title()
        colTmp, colMap, colBar = st.columns(3)
        with colTmp:
            st.line_chart(sub_bahis_farmdata['date_initial_visit'].value_counts())        
        with colMap:
            for i in data['features']:
                i['id']= i['properties']['shapeName'].replace(" Division","") 
                
            fig = px.choropleth_mapbox(cases, geojson=data, locations='divisionname', color='division',
                                    color_continuous_scale="Viridis",
                                    range_color=(0, cases['division'].max()),
                                    mapbox_style="carto-positron",
                                    zoom=5, center = {"lat": 23.7, "lon": 90},
                                    opacity=0.5,
                                    labels={'division':'Incidences per division'}
                                  )
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        with colBar:
            fig=px.bar(cases, x='divisionname', y='division', labels= {'division':'incidences'})
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
    
        
    if granularity=='2: District':
        path= path2
        subDist=bahis_geodata[(bahis_geodata["loc_type"]==2)]
        cases = sub_bahis_farmdata['district'].value_counts().to_frame()
        cases['districtname'] = cases.index
        cases= cases.loc[cases['districtname'] != 'nan']
        
        subDist['cases']=subDist.index    
        data = open_data(path)
        for i in data['features']:
            i['id']= i['properties']['shapeName'].replace(" District","") 
        for i in range(cases.shape[0]):
            cases['districtname'].iloc[i] = subDist.loc[subDist['value']==int(cases['districtname'].iloc[i]),'name'].iloc[0]
            subDist['cases'][subDist.loc[subDist['name']==cases['districtname'].iloc[i]].index[0]] = cases['district'].iloc[i]
        cases=cases.sort_values('districtname')
        cases['districtname']=cases['districtname'].str.title()
        colTmp, colMap, colBar = st.columns(3)
        with colTmp:
            st.line_chart(sub_bahis_farmdata['date_initial_visit'].value_counts())        
        with colMap:
            for i in data['features']:
                i['id']= i['properties']['shapeName'].replace(" District","") 
                
            fig = px.choropleth_mapbox(cases, geojson=data, locations='districtname', color='district',
                                    color_continuous_scale="Viridis",
                                    range_color=(0, cases['district'].max()),
                                    mapbox_style="carto-positron",
                                    zoom=5, center = {"lat": 23.7, "lon": 90},
                                    opacity=0.5,
                                    labels={'district':'Incidences per district'}
                                  )
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        with colBar:
            fig=px.bar(cases, x='districtname', y='district', labels= {'district':'incidences'})
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        
        # fig=px.bar(cases, x='districtname', y='district', labels= {'district':'incidences'})
        # fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
        # st.plotly_chart(fig, use_container_width=True)
        
        
    if granularity=='3: Upazila':
        path= path3
        subDist=bahis_geodata[(bahis_geodata["loc_type"]==3)]
        
        cases = sub_bahis_farmdata['upazila'].value_counts().to_frame()
        cases['upazilaname'] = cases.index
        cases= cases.loc[cases['upazilaname'] != 'nan']
        
        subDist['cases']=subDist.index    
        data = open_data(path)
        for i in data['features']:
            i['id']= i['properties']['shapeName'].replace(" upazila","") 
        for i in range(cases.shape[0]):
            cases['upazilaname'].iloc[i] = subDist.loc[subDist['value']==int(cases['upazilaname'].iloc[i]),'name'].iloc[0]
        #for i in range(cases.shape[0]):
            subDist['cases'][subDist.loc[subDist['name']==cases['upazilaname'].iloc[i]].index[0]] = cases['upazila'].iloc[i]
        cases=cases.sort_values('upazilaname')
        cases['upazilaname']=cases['upazilaname'].str.title()
        
        colTmp, colMap, colBar = st.columns(3)
        with colTmp:
            st.line_chart(sub_bahis_farmdata['date_initial_visit'].value_counts())        
        with colMap:
            for i in data['features']:
                i['id']= i['properties']['shapeName'].replace(" Upazila","") 
                
            fig = px.choropleth_mapbox(cases, geojson=data, locations='upazilaname', color='upazila',
                                    color_continuous_scale="Viridis",
                                    range_color=(0, cases['upazila'].max()),
                                    mapbox_style="carto-positron",
                                    zoom=5, center = {"lat": 23.7, "lon": 90},
                                    opacity=0.5,
                                    labels={'upazila':'Incidences per Upazila'}
                                  )
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        with colBar:
            fig=px.bar(cases, x='upazilaname', y='upazila', labels= {'upazila':'incidences'})
            fig.update_layout(autosize=True, width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
            

            
            