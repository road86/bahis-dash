# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:51:59 2023

@author: yoshka
"""

# Import necessary libraries 
import pandas as pd 
from datetime import date, timedelta
import numpy as np
from functools import reduce

sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
dgfilename = sourcepath + 'Diseaselist.csv'   # disease grouping info
sourcefilename =sourcepath + 'preped_data2.csv'   
path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/divdata.geojson" #8 Division
path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/distdata.geojson" #64 District
path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/upadata.geojson" #495 Upazila

bahis_sdtmp = pd.read_csv(sourcefilename) 
bahis_sdtmp['basic_info_date'] = pd.to_datetime(bahis_sdtmp['basic_info_date'])
    
bahis_dgdata= pd.read_csv(dgfilename)
bahis_dgdata= bahis_dgdata[['species', 'name', 'id', 'Disease type']]  
bahis_dgdata= bahis_dgdata[['name', 'Disease type']]
bahis_dgdata= bahis_dgdata.dropna() 

geodata = pd.read_csv(geofilename)
bahis_geodata = geodata.drop(geodata[(geodata['loc_type']==4) | (geodata['loc_type']==5)].index)
geodata= bahis_geodata[['value', 'name']].copy()
del bahis_geodata
geodata= geodata.sort_values(by=['value'])
geodata= geodata.set_index('value')


today=date(2023, 1, 1)
week=[today- timedelta(days=7), today]
sixw=[today- timedelta(weeks=6), today]

sixwmask= (bahis_sdtmp['basic_info_date']>= pd.to_datetime(sixw[0])) & (bahis_sdtmp['basic_info_date'] <= pd.to_datetime(sixw[1]))
sixwdata= bahis_sdtmp.loc[sixwmask]
del bahis_sdtmp
weekmask= (sixwdata['basic_info_date']>= pd.to_datetime(week[0])) & (sixwdata['basic_info_date'] <= pd.to_datetime(week[1]))
weekdata= sixwdata.loc[weekmask]

geodata['rd1']=np.nan #reports day 1
geodata['rd2']=np.nan
geodata['rd3']=np.nan
geodata['rd4']=np.nan
geodata['rd5']=np.nan
geodata['rd6']=np.nan
geodata['rd7']=np.nan
geodata['rw1']=np.nan #reports week 1
geodata['rw2']=np.nan
geodata['rw3']=np.nan
geodata['rw4']=np.nan
geodata['rw5']=np.nan
geodata['rw6']=np.nan
geodata['sd1']=np.nan #sick day 1
geodata['sd2']=np.nan
geodata['sd3']=np.nan
geodata['sd4']=np.nan
geodata['sd5']=np.nan
geodata['sd6']=np.nan
geodata['sd7']=np.nan
geodata['sw1']=np.nan #sick week 1
geodata['sw2']=np.nan
geodata['sw3']=np.nan
geodata['sw4']=np.nan
geodata['sw5']=np.nan
geodata['sw6']=np.nan
geodata['dd1']=np.nan #dead day 1
geodata['dd2']=np.nan
geodata['dd3']=np.nan
geodata['dd4']=np.nan
geodata['dd5']=np.nan
geodata['dd6']=np.nan
geodata['dd7']=np.nan #sick week 1
geodata['dw1']=np.nan
geodata['dw2']=np.nan
geodata['dw3']=np.nan
geodata['dw4']=np.nan
geodata['dw5']=np.nan
geodata['dw6']=np.nan
geodata['TTPw1']=np.nan #Top Ten Poultry week 1
geodata['TTRw1']=np.nan #Top Ten Ruminant week 1
geodata['TTZPw1']=np.nan #Top Ten Zoonotic Poultry week 1
geodata['TTZRw1']=np.nan #Top Ten Zoonotic Ruminant week 1
geodata['TTPw6']=np.nan
geodata['TTRw6']=np.nan
geodata['TTZPw6']=np.nan
geodata['TTZRw6']=np.nan



tmpdis=weekdata['basic_info_district'].value_counts().to_frame()
tmpdis.index=tmpdis.index.astype(int)
tmpdis=tmpdis.rename(columns={'basic_info_district': 'reports'})
result=tmpdis.merge(geodata, left_index=True, right_index=True, how='outer')

tmpdiv=weekdata['basic_info_division'].value_counts().to_frame()
tmpdiv.index=tmpdiv.index.astype(int)
tmpdiv=tmpdiv.rename(columns={'basic_info_division': 'reports'})
#result=tmp.merge(result, left_index=True, right_index=True, how='outer')
tmpupa=weekdata['basic_info_upazila'].value_counts().to_frame()
tmpupa.index=tmpupa.index.astype(int)
tmpupa=tmpupa.rename(columns={'basic_info_upazila': 'reports'})
tmptot=[tmpdis, tmpdiv, tmpupa]
result = geodata.merge(tmpdiv, left_index=True, right_index=True, how='outer').merge(tmpdis, left_index=True, right_index=True, how='outer').merge(tmpupa, left_index=True, right_index=True, how='outer')
#df6 = df1.merge(df2,how ='left').merge(df3,how ='left')

tmp=weekdata['patient_info_sick_number'].groupby(weekdata['basic_info_division']).sum()
tmp=weekdata['patient_info_sick_number'].groupby(weekdata['basic_info_district']).sum()
tmp=weekdata['patient_info_sick_number'].groupby(weekdata['basic_info_upazila']).sum()
tmp=weekdata['patient_info_dead_number'].groupby(weekdata['basic_info_division']).sum()
tmp=weekdata['patient_info_dead_number'].groupby(weekdata['basic_info_district']).sum()
tmp=weekdata['patient_info_dead_number'].groupby(weekdata['basic_info_upazila']).sum()

for index, row in geodata.iterrows():
    
    index
    geodata['rd1'][row]=weekdata[weekdata]
    geodata['rd2'][row]=np.nan
    geodata['rd3'][row]=np.nan
    geodata['rd4'][row]=np.nan
    geodata['rd5'][row]=np.nan
    geodata['rd6'][row]=np.nan
    geodata['rd7'][row]=np.nan
    geodata['rw1'][row]=np.nan #reports week 1
    geodata['rw2'][row]=np.nan
    geodata['rw3'][row]=np.nan
    geodata['rw4'][row]=np.nan
    geodata['rw5'][row]=np.nan
    geodata['rw6'][row]=np.nan
    geodata['sd1'][row]=np.nan #sick day 1
    geodata['sd2'][row]=np.nan
    geodata['sd3'][row]=np.nan
    geodata['sd4'][row]=np.nan
    geodata['sd5'][row]=np.nan
    geodata['sd6'][row]=np.nan
    geodata['sd7'][row]=np.nan
    geodata['sw1'][row]=np.nan #sick week 1
    geodata['sw2'][row]=np.nan
    geodata['sw3'][row]=np.nan
    geodata['sw4'][row]=np.nan
    geodata['sw5'][row]=np.nan
    geodata['sw6'][row]=np.nan
    geodata['dd1'][row]=np.nan #dead day 1
    geodata['dd2'][row]=np.nan
    geodata['dd3'][row]=np.nan
    geodata['dd4'][row]=np.nan
    geodata['dd5'][row]=np.nan
    geodata['dd6'][row]=np.nan
    geodata['dd7'][row]=np.nan #sick week 1
    geodata['dw1'][row]=np.nan
    geodata['dw2'][row]=np.nan
    geodata['dw3'][row]=np.nan
    geodata['dw4'][row]=np.nan
    geodata['dw5'][row]=np.nan
    geodata['dw6'][row]=np.nan
    geodata['TTPw1'][row]=np.nan #Top Ten Poultry week 1
    geodata['TTRw1'][row]=np.nan #Top Ten Ruminant week 1
    geodata['TTZPw1'][row]=np.nan #Top Ten Zoonotic Poultry week 1
    geodata['TTZRw1'][row]=np.nan #Top Ten Zoonotic Ruminant week 1
    geodata['TTPw6'][row]=np.nan
    geodata['TTRw6'][row]=np.nan
    geodata['TTZPw6'][row]=np.nan
    geodata['TTZRw6'][row]=np.nan
    
    print(index,'und dann', name)


ddDivlist=bahis_geodata[(bahis_geodata["loc_type"]==1)][['value', 'name']] #.str.capitalize()
ddDivlist['name']=ddDivlist['name'].str.capitalize()
ddDivlist=ddDivlist.rename(columns={'name':'Division'})
ddDivlist=ddDivlist.sort_values(by=['Division'])
ddDivlist=ddDivlist.to_dict('records')

def plot_map(path, loc, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl):
    subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]  # select (here) upazila level (results in 545 values -> comes from Dhaka and Chittagon and islands in the SW)
    reports = sub_bahis_sourcedata.value_counts().to_frame() #(results in 492 values, what about the rest, plot the rest where there is nothing)
    reports[pnumber] = reports.index
    reports.index = reports.index.astype(int)   # upazila name
    reports[pnumber] = reports[pnumber].astype(int)
    reports= reports.loc[reports[pnumber] != 'nan']    # unknown reason for now. does this have to be beore reports in sub_bahis_sourcedata?
    data = open_data(path)

    reports[pname] = reports.index
    for i in range(reports.shape[0]): # go through all upazila report values
        reports[pname].iloc[i] = subDist[subDist['value']==reports.index[i]]['name'].values[0] ###still to work with the copy , this goes with numbers and nnot names
    reports[pname]=reports[pname].str.title()  
    
    reports.set_index(pnumber)                 
        
    fig = px.choropleth_mapbox(reports, geojson=data, locations=pnumber, color=title,
                            featureidkey='properties.'+pnumber,
#                            featureidkey="Cmap",
                            color_continuous_scale="YlOrBr",
                            range_color=(0, reports[title].max()),
                            mapbox_style="carto-positron",
                            zoom=6.0, center = {"lat": 23.7, "lon": 90.3},
                            opacity=0.5,
                            labels={variab:labl}, 
                            hover_name=pname
                          )
    fig.update_layout(autosize=True, coloraxis_showscale=False, margin={"r":0,"t":0,"l":0,"b":0}, height=600) #, width=760 , height=800, ) #, coloraxis_showscale= False) #width= 1000, height=600, 
    return fig





## shape overlay of selected geotile(s)



def update_whatever(geoU2Slider, geoTile, cU2Division, cU2District, cU2Upazila, ViewU2):  
   
    ddDislist=None
    ddUpalist=None

    if cU2Division is None:
        vDistrict="", 
        vUpa="",
        #raise PreventUpdate
    else:
        ddDislist=fetchDistrictlist(cU2Division)
        vDistrict = [{'label': i['District'], 'value': i['value']} for i in ddDislist]
        if cU2District is None:
            vUpa="", 
            #raise PreventUpdate
        else:
            ddUpalist=fetchUpazilalist(cU2District)
            vUpa=[{'label': i['Upazila'], 'value': i['value']} for i in ddUpalist]  
   
    if 'ViewU2' ==ctx.triggered_id:

        
        sub_bahis_sourcedata=date_subset(start_date, end_date)
            
        # if geoTile is not None:
        #     print(geoTile['points'][0]['location'])
            
        if not cU2Upazila:
            if not cU2District:
                if not cU2Division:
                    sub_bahis_sourcedata=sub_bahis_sourcedata
    
                else:
                    sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_division']==cU2Division] #DivNo]   
     
            else:
                sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_district']==cU2District]
    
        else:
            sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_upazila']==cU2Upazila]
        #### change 1 and 2 with bad database check plot map and change value reference
        if geoU2Slider== 1:
            path=path1
            loc=1
            title='basic_info_division'
            pnumber='divnumber'
            pname='divisionname'
            splace=' Division'
            variab='division'
            labl='Incidences per division'
            bahis_sourcedata = pd.to_numeric(bahis_sdtmp['basic_info_division']).dropna().astype(int)
            # if geoTile is not None:
            #     print(geoTile['points'][0]['location'])
            #     cU2Division=geoTile['points'][0]['location']
            #     ddDislist=fetchDistrictlist(geoTile['points'][0]['location'])
            #     vDistrict = [{'label': i['District'], 'value': i['value']} for i in ddDislist]
        if geoU2Slider== 2:
            path=path2
            loc=2
            title='basic_info_district'
            pnumber='districtnumber'
            pname='districtname'
            splace=' District'
            variab='district'
            labl='Incidences per district'
            bahis_sourcedata = pd.to_numeric(bahis_sdtmp['basic_info_district']).dropna().astype(int)
        if geoU2Slider== 3:
            path=path3
            loc=3
            title='basic_info_upazila'
            pnumber='upazilanumber'
            pname='upazilaname'
            splace=' Upazila'
            variab='upazila'
            labl='Incidences per upazila'
            bahis_sourcedata = pd.to_numeric(bahis_sdtmp['basic_info_upazila']).dropna().astype(int)
        
        Rfig = plot_map(path, loc, bahis_sourcedata, title, pnumber, pname, splace, variab, labl)
    
    ###tab1
    
        tmp=sub_bahis_sourcedata['basic_info_date'].dt.date.value_counts()
        tmp=tmp.to_frame()
        tmp['counts']=tmp['basic_info_date']
    
        tmp['basic_info_date']=pd.to_datetime(tmp.index)
        tmp=tmp['counts'].groupby(tmp['basic_info_date'].dt.to_period('W-SUN')).sum().astype(int)
        tmp=tmp.to_frame()
        tmp['basic_info_date']=tmp.index
        tmp['basic_info_date']=tmp['basic_info_date'].astype('datetime64[D]')
                
        figgR= px.bar(tmp, x='basic_info_date', y='counts') 
        figgR.update_layout(height=225, margin={"r":0,"t":0,"l":0,"b":0}) 
        
        tmp=sub_bahis_sourcedata['patient_info_sick_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('W-SUN')).sum().astype(int)
        tmp=tmp.reset_index()
        tmp=tmp.rename(columns={'basic_info_date':'date'})
        tmp['date'] = tmp['date'].astype('datetime64[D]')
        figgSick= px.bar(tmp, x='date', y='patient_info_sick_number')  
        figgSick.update_layout(height=225, margin={"r":0,"t":0,"l":0,"b":0})   
    
        tmp=sub_bahis_sourcedata['patient_info_dead_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('W-SUN')).sum().astype(int)
        tmp=tmp.reset_index()
        tmp=tmp.rename(columns={'basic_info_date':'date'})
        tmp['date'] = tmp['date'].astype('datetime64[D]')
        figgDead= px.bar(tmp, x='date', y='patient_info_dead_number')  
        figgDead.update_layout(height=225, margin={"r":0,"t":0,"l":0,"b":0})   
        
    ####tab2
        poultry=['Chicken', 'Duck', 'Goose', 'Pegion', 'Quail', 'Turkey']
        sub_bahis_sourcedataP=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(poultry)]
    
        tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
        to_replace=tmpdg['name'].tolist()
        replace_with=tmpdg['Disease type'].tolist()
        sub_bahis_sourcedataP['top_diagnosis']= sub_bahis_sourcedataP.top_diagnosis.replace(to_replace, replace_with, regex=True)                                        
        sub_bahis_sourcedataP=sub_bahis_sourcedataP.drop(sub_bahis_sourcedataP[sub_bahis_sourcedataP['top_diagnosis']=='Zoonotic diseases'].index)
    
        tmp= sub_bahis_sourcedataP.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
        tmp=tmp.sort_values(by='species', ascending=False)
        tmp=tmp.rename({'species' : 'counts'}, axis=1)
        tmp=tmp.head(10)
        tmp=tmp.iloc[::-1]
        fpoul =px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases')
        fpoul.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}) 
        #figg.append_trace(px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases'), row=1, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
        
        lanimal=['Buffalo', 'Cattle', 'Goat', 'Sheep']
        sub_bahis_sourcedataLA=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(lanimal)] 
       
        tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
        to_replace=tmpdg['name'].tolist()
        replace_with=tmpdg['Disease type'].tolist()
        sub_bahis_sourcedataLA['top_diagnosis']= sub_bahis_sourcedataLA.top_diagnosis.replace(to_replace, replace_with, regex=True)  
        sub_bahis_sourcedataLA=sub_bahis_sourcedataLA.drop(sub_bahis_sourcedataLA[sub_bahis_sourcedataLA['top_diagnosis']=='Zoonotic diseases'].index)
    
        tmp= sub_bahis_sourcedataLA.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
        tmp=tmp.sort_values(by='species', ascending=False)
        tmp=tmp.rename({'species' : 'counts'}, axis=1)
        tmp=tmp.head(10)
        tmp=tmp.iloc[::-1]
        flani = px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Large Animal Diseases')
        flani.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
        #subpl.add_traces(flani, row=1, col=1)#, row=2, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
        subpl=[fpoul, flani]
        figgLiveS= make_subplots(rows=2, cols=1)
        for i, figure in enumerate(subpl):
            for trace in range(len(figure['data'])):
                figgLiveS.append_trace(figure['data'][trace], row=i+1, col=1)
        figgLiveS.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0}) 
    #    if cReport=='Zoonotic Disease Cases':   
        #subpl= make_subplots(rows=2, cols=1),
        poultry=['Chicken', 'Duck', 'Goose', 'Pegion', 'Quail', 'Turkey']
        sub_bahis_sourcedataP=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(poultry)]
    
        tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
        tmpdg=tmpdg[tmpdg['Disease type']=='Zoonotic diseases']
        tmpdg=tmpdg['name'].tolist()
        sub_bahis_sourcedataP= sub_bahis_sourcedataP[sub_bahis_sourcedataP['top_diagnosis'].isin(tmpdg)]    
        
        # to_replace=tmpdg['name'].tolist()
        # replace_with=tmpdg['Disease type'].tolist()
        # sub_bahis_sourcedataP['top_diagnosis']= sub_bahis_sourcedataP.top_diagnosis.replace(to_replace, replace_with, regex=True)                                        
        # sub_bahis_sourcedataP=sub_bahis_sourcedataP[sub_bahis_sourcedataP['top_diagnosis']=='Zoonotic diseases']
    
        tmp= sub_bahis_sourcedataP.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
        tmp=tmp.sort_values(by='species', ascending=False)
        tmp=tmp.rename({'species' : 'counts'}, axis=1)
        tmp=tmp.head(10)
        tmp=tmp.iloc[::-1]
        fpoul =px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases')
        fpoul.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
        #figg.append_trace(px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases'), row=1, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
        
        lanimal=['Buffalo', 'Cattle', 'Goat', 'Sheep']
        sub_bahis_sourcedataLA=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(lanimal)] 
      
    #        tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
        sub_bahis_sourcedataLA= sub_bahis_sourcedataLA[sub_bahis_sourcedataLA['top_diagnosis'].isin(tmpdg)]    
        
        # to_replace=tmpdg['name'].tolist()
        # replace_with=tmpdg['Disease type'].tolist()
        # sub_bahis_sourcedataLA['top_diagnosis']= sub_bahis_sourcedataLA.top_diagnosis.replace(to_replace, replace_with, regex=True)  
        # sub_bahis_sourcedataLA=sub_bahis_sourcedataLA[sub_bahis_sourcedataLA['top_diagnosis']=='Zoonotic diseases']
    
        tmp= sub_bahis_sourcedataLA.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
        tmp=tmp.sort_values(by='species', ascending=False)
        tmp=tmp.rename({'species' : 'counts'}, axis=1)
        tmp=tmp.head(10)
        tmp=tmp.iloc[::-1]
        flani = px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Ruminant Diseases')
        flani.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
        #subpl.add_traces(flani, row=1, col=1)#, row=2, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
        subpl=[fpoul, flani]
        figgZoon= make_subplots(rows=2, cols=1)
        for i, figure in enumerate(subpl):
            for trace in range(len(figure['data'])):
                figgZoon.append_trace(figure['data'][trace], row=i+1, col=1)
        figgZoon.update_layout(height=180, margin={"r":0,"t":0,"l":0,"b":0}) 
    
    return vDistrict, vUpa, Rfig, figgR, figgSick, figgDead, figgLiveS, figgZoon













