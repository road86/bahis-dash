# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:51:59 2023

@author: yoshka
"""

# Import necessary libraries 
import pandas as pd 
from datetime import date, timedelta

#sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
#path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/divdata.geojson" #8 Division
#path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/distdata.geojson" #64 District
#path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/upadata.geojson" #495 Upazila

sourcepath = 'exported_data/'
path1= "geodata/divdata.geojson" #8 Division
path2= "geodata/distdata.geojson" #64 District
path3= "geodata/upadata.geojson" #495 Upazila

geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
dgfilename = sourcepath + 'Diseaselist.csv'   # disease grouping info
sourcefilename =sourcepath + 'preped_data2.csv'   

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
week=[today- timedelta(days=6), today]
sixw=[today- timedelta(weeks=6)+timedelta(days=1), today]

sixwmask= (bahis_sdtmp['basic_info_date']>= pd.to_datetime(sixw[0])) & (bahis_sdtmp['basic_info_date'] <= pd.to_datetime(sixw[1]))
sixwdata= bahis_sdtmp.loc[sixwmask]
del bahis_sdtmp
weekmask= (sixwdata['basic_info_date']>= pd.to_datetime(week[0])) & (sixwdata['basic_info_date'] <= pd.to_datetime(week[1]))
weekdata= sixwdata.loc[weekmask]

# geodata['rd1']=np.nan #reports day 1
# geodata['rd2']=np.nan
# geodata['rd3']=np.nan
# geodata['rd4']=np.nan
# geodata['rd5']=np.nan#5
# geodata['rd6']=np.nan
# geodata['rd7']=np.nan
# geodata['rw1']=np.nan #reports week 1
# geodata['rw2']=np.nan
# geodata['rw3']=np.nan#10
# geodata['rw4']=np.nan
# geodata['rw5']=np.nan
# geodata['rw6']=np.nan #13
# geodata['sd1']=np.nan #sick day 1
# geodata['sd2']=np.nan#15
# geodata['sd3']=np.nan
# geodata['sd4']=np.nan
# geodata['sd5']=np.nan
# geodata['sd6']=np.nan
# geodata['sd7']=np.nan#20
# geodata['sw1']=np.nan #sick week 1
# geodata['sw2']=np.nan
# geodata['sw3']=np.nan
# geodata['sw4']=np.nan
# geodata['sw5']=np.nan#25
# geodata['sw6']=np.nan
# geodata['dd1']=np.nan #dead day 1
# geodata['dd2']=np.nan
# geodata['dd3']=np.nan
# geodata['dd4']=np.nan#30
# geodata['dd5']=np.nan
# geodata['dd6']=np.nan
# geodata['dd7']=np.nan #sick week 1
# geodata['dw1']=np.nan
# geodata['dw2']=np.nan#35
# geodata['dw3']=np.nan
# geodata['dw4']=np.nan
# geodata['dw5']=np.nan
# geodata['dw6']=np.nan
# geodata['TTPw1']=np.nan #Top Ten Poultry week 1
# geodata['TTRw1']=np.nan #Top Ten Ruminant week 1
# geodata['TTZPw1']=np.nan #Top Ten Zoonotic Poultry week 1
# geodata['TTZRw1']=np.nan #Top Ten Zoonotic Ruminant week 1
# geodata['TTPw6']=np.nan
# geodata['TTRw6']=np.nan
# geodata['TTZPw6']=np.nan
# geodata['TTZRw6']=np.nan

# TOP10 still to be done

result=geodata
result.loc[1]=['BANGLADESH']
result=result.sort_index()

 # df.loc[-1] = [2, 3, 4]  # adding a row
 # df.index = df.index + 1  # shifting index
 # df = df.sort_index() 
 
for i in range (1,8):
    tmpdiv=weekdata[weekdata['basic_info_date']==pd.to_datetime(today-pd.Timedelta(i-1,unit='D'))]['basic_info_division'].value_counts().to_frame()
    tmpdiv.index=tmpdiv.index.astype(int)
    tmpdiv=tmpdiv.rename(columns={'basic_info_division': 'rd'+str(i)})
    tmpdis=weekdata[weekdata['basic_info_date']==pd.to_datetime(today-pd.Timedelta(i-1,unit='D'))]['basic_info_district'].value_counts().to_frame()
    tmpdis.index=tmpdis.index.astype(int)
    tmpdis=tmpdis.rename(columns={'basic_info_district': 'rd'+str(i)})
    tmpupa=weekdata[weekdata['basic_info_date']==pd.to_datetime(today-pd.Timedelta(i-1,unit='D'))]['basic_info_upazila'].value_counts().to_frame()
    tmpupa.index=tmpupa.index.astype(int)
    tmpupa=tmpupa.rename(columns={'basic_info_upazila': 'rd'+str(i)})
    tmptot=[tmpdiv, tmpdis, tmpupa]
    result = result.merge(tmpdiv, left_index=True, right_index=True, how='outer').merge(tmpdis, left_index=True, right_index=True, how='outer').merge(tmpupa, left_index=True, right_index=True, how='outer')
    result['rd'+str(i)]=result['rd'+str(i)].fillna(result['rd'+str(i)+'_x'])
    result['rd'+str(i)]=result['rd'+str(i)].fillna(result['rd'+str(i)+'_y'])
    result=result.drop(columns={'rd'+str(i)+'_x', 'rd'+str(i)+'_y'})
    result['rd'+str(i)][1]=int(tmpdiv['rd'+str(i)].sum())

    tmpdiv=weekdata[weekdata['basic_info_date']==pd.to_datetime(today-pd.Timedelta(i-1,unit='D'))]['patient_info_sick_number'].groupby(weekdata['basic_info_division']).sum().to_frame()
    tmpdiv.index=tmpdiv.index.astype(int)
    tmpdiv=tmpdiv.rename(columns={'patient_info_sick_number': 'sd'+str(i)})
    tmpdis=weekdata[weekdata['basic_info_date']==pd.to_datetime(today-pd.Timedelta(i-1,unit='D'))]['patient_info_sick_number'].groupby(weekdata['basic_info_district']).sum().to_frame()
    tmpdis.index=tmpdis.index.astype(int)
    tmpdis=tmpdis.rename(columns={'patient_info_sick_number': 'sd'+str(i)})
    tmpupa=weekdata[weekdata['basic_info_date']==pd.to_datetime(today-pd.Timedelta(i-1,unit='D'))]['patient_info_sick_number'].groupby(weekdata['basic_info_upazila']).sum().to_frame()
    tmpupa.index=tmpupa.index.astype(int)
    tmpupa=tmpupa.rename(columns={'patient_info_sick_number': 'sd'+str(i)})
    result = result.merge(tmpdiv, left_index=True, right_index=True, how='outer').merge(tmpdis, left_index=True, right_index=True, how='outer').merge(tmpupa, left_index=True, right_index=True, how='outer')
    result['sd'+str(i)]=result['sd'+str(i)].fillna(result['sd'+str(i)+'_x'])
    result['sd'+str(i)]=result['sd'+str(i)].fillna(result['sd'+str(i)+'_y'])
    result=result.drop(columns={'sd'+str(i)+'_x', 'sd'+str(i)+'_y'})
    result['sd'+str(i)][1]=tmpdiv['sd'+str(i)].sum()
    
    tmpdiv=weekdata[weekdata['basic_info_date']==pd.to_datetime(today-pd.Timedelta(i-1,unit='D'))]['patient_info_dead_number'].groupby(weekdata['basic_info_division']).sum().to_frame()
    tmpdiv.index=tmpdiv.index.astype(int)
    tmpdiv=tmpdiv.rename(columns={'patient_info_dead_number': 'dd'+str(i)})
    tmpdis=weekdata[weekdata['basic_info_date']==pd.to_datetime(today-pd.Timedelta(i-1,unit='D'))]['patient_info_dead_number'].groupby(weekdata['basic_info_district']).sum().to_frame()
    tmpdis.index=tmpdis.index.astype(int)
    tmpdis=tmpdis.rename(columns={'patient_info_dead_number': 'dd'+str(i)})
    tmpupa=weekdata[weekdata['basic_info_date']==pd.to_datetime(today-pd.Timedelta(i-1,unit='D'))]['patient_info_dead_number'].groupby(weekdata['basic_info_upazila']).sum().to_frame()
    tmpupa.index=tmpupa.index.astype(int)
    tmpupa=tmpupa.rename(columns={'patient_info_dead_number': 'dd'+str(i)})
    result = result.merge(tmpdiv, left_index=True, right_index=True, how='outer').merge(tmpdis, left_index=True, right_index=True, how='outer').merge(tmpupa, left_index=True, right_index=True, how='outer')
    result['dd'+str(i)]=result['dd'+str(i)].fillna(result['dd'+str(i)+'_x'])
    result['dd'+str(i)]=result['dd'+str(i)].fillna(result['dd'+str(i)+'_y'])
    result=result.drop(columns={'dd'+str(i)+'_x', 'dd'+str(i)+'_y'})
    result['dd'+str(i)][1]=tmpdiv['dd'+str(i)].sum()

# code snipped to check, if other calc leads to the same result for sanity check
# tmpdiv=weekdata['basic_info_division'].value_counts().to_frame()
# tmpdiv.index=tmpdiv.index.astype(int)
# tmpdiv=tmpdiv.rename(columns={'basic_info_division': 'rw1'})
# tmpdis=weekdata['basic_info_district'].value_counts().to_frame()
# tmpdis.index=tmpdis.index.astype(int)
# tmpdis=tmpdis.rename(columns={'basic_info_district': 'rw1'})
# tmpupa=weekdata['basic_info_upazila'].value_counts().to_frame()
# tmpupa.index=tmpupa.index.astype(int)
# tmpupa=tmpupa.rename(columns={'basic_info_upazila': 'rw1'})
# tmptot=[tmpdiv, tmpdis, tmpupa]
# result = result.merge(tmpdiv, left_index=True, right_index=True, how='outer').merge(tmpdis, left_index=True, right_index=True, how='outer').merge(tmpupa, left_index=True, right_index=True, how='outer')
# result['rw1']=result['rw1'].fillna(result['rw1_x'])
# result['rw1']=result['rw1'].fillna(result['rw1_y'])
# result=result.drop(columns={'rw1_x', 'rw1_y'})

for i in range (1,7):
    tmpdiv=sixwdata[(sixwdata['basic_info_date']<=pd.to_datetime(today-pd.Timedelta(i-1,unit='W'))) & (sixwdata['basic_info_date']>pd.to_datetime(today-pd.Timedelta(i,unit='W')))]['basic_info_division'].value_counts().to_frame()
    tmpdiv.index=tmpdiv.index.astype(int)
    tmpdiv=tmpdiv.rename(columns={'basic_info_division': 'rw'+str(i)})
    tmpdis=sixwdata[(sixwdata['basic_info_date']<=pd.to_datetime(today-pd.Timedelta(i-1,unit='W'))) & (sixwdata['basic_info_date']>pd.to_datetime(today-pd.Timedelta(i,unit='W')))]['basic_info_district'].value_counts().to_frame()
    tmpdis.index=tmpdis.index.astype(int)
    tmpdis=tmpdis.rename(columns={'basic_info_district': 'rw'+str(i)})
    tmpupa=sixwdata[(sixwdata['basic_info_date']<=pd.to_datetime(today-pd.Timedelta(i-1,unit='W'))) & (sixwdata['basic_info_date']>pd.to_datetime(today-pd.Timedelta(i,unit='W')))]['basic_info_upazila'].value_counts().to_frame()
    tmpupa.index=tmpupa.index.astype(int)
    tmpupa=tmpupa.rename(columns={'basic_info_upazila': 'rw'+str(i)})
    tmptot=[tmpdiv, tmpdis, tmpupa]
    result = result.merge(tmpdiv, left_index=True, right_index=True, how='outer').merge(tmpdis, left_index=True, right_index=True, how='outer').merge(tmpupa, left_index=True, right_index=True, how='outer')
    result['rw'+str(i)]=result['rw'+str(i)].fillna(result['rw'+str(i)+'_x'])
    result['rw'+str(i)]=result['rw'+str(i)].fillna(result['rw'+str(i)+'_y'])
    result=result.drop(columns={'rw'+str(i)+'_x', 'rw'+str(i)+'_y'})
    result['rw'+str(i)][1]=tmpdiv['rw'+str(i)].sum()
    
    tmpdiv=sixwdata[(sixwdata['basic_info_date']<=pd.to_datetime(today-pd.Timedelta(i-1,unit='W'))) & (sixwdata['basic_info_date']>pd.to_datetime(today-pd.Timedelta(i,unit='W')))]['patient_info_sick_number'].groupby(sixwdata['basic_info_division']).sum().to_frame()
    tmpdiv.index=tmpdiv.index.astype(int)
    tmpdiv=tmpdiv.rename(columns={'patient_info_sick_number': 'sw'+str(i)})
    tmpdis=sixwdata[(sixwdata['basic_info_date']<=pd.to_datetime(today-pd.Timedelta(i-1,unit='W'))) & (sixwdata['basic_info_date']>pd.to_datetime(today-pd.Timedelta(i,unit='W')))]['patient_info_sick_number'].groupby(sixwdata['basic_info_district']).sum().to_frame()
    tmpdis.index=tmpdis.index.astype(int)
    tmpdis=tmpdis.rename(columns={'patient_info_sick_number': 'sw'+str(i)})
    tmpupa=sixwdata[(sixwdata['basic_info_date']<=pd.to_datetime(today-pd.Timedelta(i-1,unit='W'))) & (sixwdata['basic_info_date']>pd.to_datetime(today-pd.Timedelta(i,unit='W')))]['patient_info_sick_number'].groupby(sixwdata['basic_info_upazila']).sum().to_frame()
    tmpupa.index=tmpupa.index.astype(int)
    tmpupa=tmpupa.rename(columns={'patient_info_sick_number': 'sw'+str(i)})
    result = result.merge(tmpdiv, left_index=True, right_index=True, how='outer').merge(tmpdis, left_index=True, right_index=True, how='outer').merge(tmpupa, left_index=True, right_index=True, how='outer')
    result['sw'+str(i)]=result['sw'+str(i)].fillna(result['sw'+str(i)+'_x'])
    result['sw'+str(i)]=result['sw'+str(i)].fillna(result['sw'+str(i)+'_y'])
    result=result.drop(columns={'sw'+str(i)+'_x', 'sw'+str(i)+'_y'})
    result['sw'+str(i)][1]=tmpdiv['sw'+str(i)].sum()
    
    tmpdiv=sixwdata[(sixwdata['basic_info_date']<=pd.to_datetime(today-pd.Timedelta(i-1,unit='W'))) & (sixwdata['basic_info_date']>pd.to_datetime(today-pd.Timedelta(i,unit='W')))]['patient_info_dead_number'].groupby(sixwdata['basic_info_division']).sum().to_frame()
    tmpdiv.index=tmpdiv.index.astype(int)
    tmpdiv=tmpdiv.rename(columns={'patient_info_dead_number': 'dw'+str(i)})
    tmpdis=sixwdata[(sixwdata['basic_info_date']<=pd.to_datetime(today-pd.Timedelta(i-1,unit='W'))) & (sixwdata['basic_info_date']>pd.to_datetime(today-pd.Timedelta(i,unit='W')))]['patient_info_dead_number'].groupby(sixwdata['basic_info_district']).sum().to_frame()
    tmpdis.index=tmpdis.index.astype(int)
    tmpdis=tmpdis.rename(columns={'patient_info_dead_number': 'dw'+str(i)})
    tmpupa=sixwdata[(sixwdata['basic_info_date']<=pd.to_datetime(today-pd.Timedelta(i-1,unit='W'))) & (sixwdata['basic_info_date']>pd.to_datetime(today-pd.Timedelta(i,unit='W')))]['patient_info_dead_number'].groupby(sixwdata['basic_info_upazila']).sum().to_frame()
    tmpupa.index=tmpupa.index.astype(int)
    tmpupa=tmpupa.rename(columns={'patient_info_dead_number': 'dw'+str(i)})
    result = result.merge(tmpdiv, left_index=True, right_index=True, how='outer').merge(tmpdis, left_index=True, right_index=True, how='outer').merge(tmpupa, left_index=True, right_index=True, how='outer')
    result['dw'+str(i)]=result['dw'+str(i)].fillna(result['dw'+str(i)+'_x'])
    result['dw'+str(i)]=result['dw'+str(i)].fillna(result['dw'+str(i)+'_y'])
    result=result.drop(columns={'dw'+str(i)+'_x', 'dw'+str(i)+'_y'})
    result['dw'+str(i)][1]=tmpdiv['dw'+str(i)].sum()
    
result.index.names=['geonumber']
result.to_csv(sourcepath + 'preped_quickdata.csv')










