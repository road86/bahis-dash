# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 18:07:34 2023

@author: yoshka
"""


# Import necessary libraries 
import dash
from dash import dcc, html, callback, dash_table #, ctx #Dash, #dash_table, dbc 
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc #dbc deprecationwarning
import pandas as pd
from dash.dependencies import Input, Output
import json  
import datetime
# from datetime import date
# from dateutil.relativedelta import relativedelta


pd.options.mode.chained_assignment = None

dash.register_page(__name__) #, path='/') for entry point probably

lpath='C:/Users/yoshka/Documents/GitHub/bahis-dash/'
npath=''
sourcepath = lpath+'exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
sourcefilename =sourcepath + 'resp_data.csv'   
reportsfilename =sourcepath + 'resp_rep_data.csv'  
path1= "geodata/divdata.geojson" #8 Division
path2= "geodata/distdata.geojson" #64 District
path3= "geodata/upadata.geojson" #495 Upazila

resp_data = pd.read_csv(sourcefilename) 
resp_data['date'] = pd.to_datetime(resp_data['date'])

resp_rep_data = pd.read_csv(reportsfilename) 
resp_rep_data['date'] = pd.to_datetime(resp_rep_data['date'])
    
def fetchgeodata():  
    geodata = pd.read_csv(geofilename)
    geodata = geodata.drop(geodata[(geodata['loc_type']==4) | (geodata['loc_type']==5)].index)
    return geodata
geodata= fetchgeodata()


def fetchDivisionlist():   #### fetched names; make detour via numbers for all div, dis and upa,
    ddDivlist=geodata[(geodata["loc_type"]==1)][['value', 'name']] #.str.capitalize()
    ddDivlist['name']=ddDivlist['name'].str.capitalize()
    ddDivlist=ddDivlist.rename(columns={'name':'Division'})
    ddDivlist=ddDivlist.sort_values(by=['Division'])
    diccc=ddDivlist.to_dict('records')
    return diccc
ddDivlist=fetchDivisionlist()

def fetchDistrictlist(SelDiv):   
    DivNo=SelDiv
    ddDislist=geodata[geodata['parent']==DivNo][['value','name']] #.str.capitalize()
    ddDislist['name']=ddDislist['name'].str.capitalize()
    ddDislist=ddDislist.rename(columns={'name':'District'})   
    ddDislist=ddDislist.sort_values(by=['District'])
    diccc=ddDislist.to_dict('records')
    return diccc

def fetchUpazilalist(SelDis):   
    DisNo=SelDis
    ddUpalist=geodata[geodata['parent']==DisNo][['value','name']] #.str.capitalize()
    ddUpalist['name']=ddUpalist['name'].str.capitalize()
    ddUpalist=ddUpalist.rename(columns={'name':'Upazila'})     
    ddUpalist=ddUpalist.sort_values(by=['Upazila'])
    diccc=ddUpalist.to_dict('records')
    return diccc 

start_date=min(resp_data['date']).date()
end_date=max(resp_data['date']).date()
start_dater=min(resp_rep_data['date']).date()
end_dater=max(resp_rep_data['date']).date()
#start_date=date(2023, 1, 1)


def date_subset(sdate, edate, sdater, edater):
    dates=[sdate, edate]
    datesr=[sdater, edater]
    tmask = (resp_data['date']>= pd.to_datetime(dates[0])) & (resp_data['date'] <= pd.to_datetime(dates[1]))
    tmaskr = (resp_rep_data['date']>= pd.to_datetime(datesr[0])) & (resp_rep_data['date'] <= pd.to_datetime(datesr[1]))
    return resp_data.loc[tmask], resp_rep_data.loc[tmaskr]

def disease_subset(cDisease, dis_sub_data):
    if 'All Diseases' in cDisease:
        dis_sub_data=dis_sub_data 
    else:
        dis_sub_data=dis_sub_data[dis_sub_data['disease'].isin(cDisease)] 
    return dis_sub_data

ddDivision = html.Div(
    [
        dbc.Label("Select Division"),
        dcc.Dropdown(
            options=[{'label': i['Division'], 'value': i['value']} for i in ddDivlist],
            id="rDivision",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddDistrict = html.Div(
    [
        dbc.Label("Select District"),
        dcc.Dropdown(
            id="rDistrict",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddUpazila = html.Div(
    [
        dbc.Label("Select Upazila"),
        dcc.Dropdown(
            id="rUpazila",
            clearable=True,
        ),
    ],
    className="mb-4",
)

def fetchdiseaselist():
    dislis= resp_data['disease'].unique()
    dislis= pd.DataFrame(dislis, columns=['disease'])
    ddDList= dislis['disease'].sort_values()
    return ddDList.tolist()
ddDList= fetchdiseaselist()
ddDList.insert(0, 'All Diseases')


def open_data(path):
    with open(path) as f:
        data = json.load(f)             
    return data

def plot_map(path, loc, sub_data, title, pnumber, pname, splace, variab, labl):
    subDist=geodata[(geodata["loc_type"]==loc)]  # select (here) upazila level (results in 545 values -> comes from Dhaka and Chittagon and islands in the SW)
#    reports = sub_data.value_counts().to_frame() #(results in 492 values, what about the rest, plot the rest where there is nothing)
    reports = sub_data.groupby([title])['cases'].sum().to_frame()#(results in 492 values, what about the rest, plot the rest where there is nothing)
    reports= reports.rename(columns={'cases' : title}, index={title: 'Index'})
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
                            color_continuous_scale="YlOrBr",
                            range_color=(0, reports[title].max()),
                            mapbox_style="carto-positron",
                            zoom=5.8, center = {"lat": 23.7, "lon": 90.3},
                            opacity=0.5,
                            labels={variab:labl}, 
                            hover_name=pname
                          )
    fig.update_layout(autosize=True, coloraxis_showscale=False, margin={"r":0,"t":0,"l":0,"b":0}, height=550) #, width=760 , height=800, ) #, coloraxis_showscale= False) #width= 1000, height=600, 
    return fig


layout =  html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(ddDivision), dbc.Col(ddDistrict), dbc.Col(ddUpazila)
                        ]),
#                    dbc.Row(dcc.RangeSlider(min=1, max=104, marks={1:'1', 104:'104'}, step=1, value=[1,104], id="test")),
                    dbc.Row(dcc.Graph(id="rMap")),
                    dbc.Row(dcc.Slider(min=1, max=3, step=1,
                                       marks={1:'Division', 
                                              2:'District', 
                                              3:'Upazila',}, 
                            value=3,
                            id="rgeoSlider")
                            )
                ], width= 4),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dcc.DatePickerRange(
                                    id='rdaterange',
                                    min_date_allowed=start_date,
                                    start_date=start_date,
#                                    start_date=date(end_date.year-1, end_date.month, end_date.day),
                                    max_date_allowed=end_date,
                                    initial_visible_month=end_date,
                                    end_date=end_date
                                ),
                            ]),
                        dbc.Col([
                            dcc.Dropdown(
                                ddDList,
                                "All Diseases",
                                id="rDiseaselist",
                                multi=True,
                                clearable=False,
                                ),
                            ])                        
                        ]),
                    dbc.Row([
                        dbc.Tabs([
                            dbc.Tab([
                                dbc.Row(dcc.Graph(id='figRep')),
                                dbc.Row([ 
                                    dbc.Col([
                                        dcc.Graph(id='RepStat')]),
                                    dbc.Col([
                                        dcc.Graph(id='LabStat')]),
                                    dbc.Col([
                                        dcc.Graph(id='figSig')]),
                                    ]),
                                dbc.Row(dcc.Graph(id='figSignal')),
                                ], label='Reports'),                     
                            dbc.Tab([
                                dbc.Row(dcc.Graph(id='rSick')),
                                dbc.Row(dcc.Graph(id='rDead'))
                                ], label='Disease Cases over Time'),
                            dbc.Tab([
                                dbc.Row(html.Div(id='casetable')),
                                dbc.Row(dcc.Graph(id='rRegion')),
                                ], label='Region List')
                            ])                                
                        ])
                        #label='rReports'),
                    ], width=8)
            ])
])


## shape overlay of selected geotile(s)

@callback(
    Output ('rDistrict', 'options'),
    Output ('rUpazila', 'options'),

    Output ('rMap', 'figure'),
    Output ('figRep', 'figure'),
    Output ('figSignal', 'figure'),
    
    Output ('rSick', 'figure'),
    Output ('rDead', 'figure'),
    Output ('casetable', 'children'),
    Output ('rRegion', 'figure'),

    Input ('rgeoSlider', 'value'),
    Input ('rMap', 'clickData'),  
#    Input ('rReports', 'clickData'),  
    Input ('rSick', 'clickData'),  
    Input ('rDead', 'clickData'),  
    
    Input ('rDivision', 'value'),
    Input ('rDistrict', 'value'),
    Input ("rUpazila",'value'),
    Input ("rdaterange",'start_date'),
    Input ("rdaterange",'end_date'),
    Input ("rDiseaselist",'value'),
)
def update_whatever(rgeoSlider, geoTile, clkSick, clkDead, rDivision, rDistrict, rUpazila, start_date, end_date, diseaselist):       #clkRep, 
    date_sub, data_resp=date_subset(start_date, end_date, start_dater, end_dater)
    sub_data=disease_subset(diseaselist, date_sub)

    # tmp1as= pd.to_datetime(start_date)-relativedelta(years=1)   
    # tmp1ae= pd.to_datetime(start_date)-relativedelta(days=1)
    # sub1a_data=date_subset(tmp1as, tmp1ae)
    # sub1a_data=disease_subset(diseaselist, sub1a_data)

    # tmp2as= pd.to_datetime(start_date)-relativedelta(years=2)   
    # tmp2ae= pd.to_datetime(start_date)-relativedelta(years=1)-relativedelta(days=1)
    # sub2a_data=date_subset(tmp2as, tmp2ae)
    # sub2a_data=disease_subset(diseaselist, sub2a_data)


    ddDislist=None
    ddUpalist=None
    

    if rDivision is None:
        vDistrict="", 
        vUpa="",
    else:
        ddDislist=fetchDistrictlist(rDivision)
        vDistrict = [{'label': i['District'], 'value': i['value']} for i in ddDislist]
        if rDistrict is None:
            vUpa="", 
            #raise PreventUpdate
        else:
            ddUpalist=fetchUpazilalist(rDistrict)
            vUpa=[{'label': i['Upazila'], 'value': i['value']} for i in ddUpalist]        
    if not rUpazila:
        if not rDistrict:
            if not rDivision:
                sub_data=sub_data
                #sub1a_data=sub1a_data
            else:
                sub_data= sub_data.loc[sub_data['division']==rDivision] #DivNo]   
                #sub1a_data= sub1a_data.loc[sub1a_data['division']==rDivision] #DivNo]   
        else:
            sub_data= sub_data.loc[sub_data['district']==rDistrict]
            #sub1a_data= sub1a_data.loc[sub1a_data['district']==rDistrict]
    else:
        sub_data= sub_data.loc[sub_data['upazila']==rUpazila]
        #sub1a_data= sub1a_data.loc[sub_data['upazila']==rUpazila]
    #### change 1 and 2 with bad database check plot map and change value reference
    if rgeoSlider== 1:
        path=path1
        loc=1
        title='division'
        pnumber='divnumber'
        pname='divisionname'
        splace=' Division'
        variab='division'
        labl='Incidences per division'
#        incsub_data = pd.to_numeric(sub_data['division']).dropna().astype(int)
        incsub_data = sub_data
    if rgeoSlider== 2:
        path=path2
        loc=2
        title='district'
        pnumber='districtnumber'
        pname='districtname'
        splace=' District'
        variab='district'
        labl='Incidences per district'
#        incsub_data = pd.to_numeric(sub_data['district']).dropna().astype(int)
        incsub_data = sub_data

    if rgeoSlider== 3:
        path=path3
        loc=3
        title='upazila'
        pnumber='upazilanumber'
        pname='upazilaname'
        splace=' Upazila'
        variab='upazila'
        labl='Incidences per upazila'
#        incsub_data = pd.to_numeric(sub_data['upazila']).dropna().astype(int)
        incsub_data = sub_data
    
    Rfig = plot_map(path, loc, incsub_data, title, pnumber, pname, splace, variab, labl)

###tab1

    reps = data_resp.groupby([data_resp['date'].dt.to_period('W-SAT')])[['Reported', 'Verified', 'Signal', 'LabSent', 'LabResult'] ].sum()     # in two steps
    reps['year']=reps.index.start_time.year
    tmprep= reps.loc[reps['year']==max(reps['year'])]
    
    color=['red', 'blue', 'orange', 'green', 'black', 'brown']
    figRep=px.bar(tmprep, x=tmprep.index.week, y='Reported')    
    i=0
    for year in reps['year'].unique(): 
        if year != max(reps['year']):
            tmprep = reps.loc[reps['year']==year]
            Reportss= px.line(tmprep, x=tmprep.index.week, y='Reported') #, labels={'date':'Date', 'cases':'No. of Sick Animals'})  
            Reportss['data'][0]['line']['color']=color[i] #'rgb(204, 0, 0)'  # make color
            Reportss['data'][0]['line']['width']=1
            figRep = go.Figure(data=figRep.data + Reportss.data)
            i=i+1
    figRep.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}) 
     
    
    
    
    
    
    tmp=data_resp[pd.DatetimeIndex(data_resp['date']).year==2023]
    repss=tmp.groupby([tmp['date'].dt.to_period('W-SAT')])[['Reported']].sum() 
    #color=['red', 'blue', 'orange', 'green', 'black', 'brown']
    figSignal=px.bar(repss, x=repss.index.week, y='Reported')    
#    figSig=px.bar(tmprep, x=tmprep.index.week, y='Reported')    
    i=0
    for sig in tmp['Signal'].unique():
        repss[sig]=tmp[tmp['Signal']==sig].groupby([tmp['date'].dt.to_period('W-SAT')])[['Reported']].sum() 
        repss=repss.fillna(0)
        RepSig= px.line(repss, x=repss.index.week, y=sig) #, labels={'date':'Date', 'cases':'No. of Sick Animals'})  
        RepSig['data'][0]['line']['color']=color[i] #'rgb(204, 0, 0)'  # make color
        RepSig['data'][0]['line']['width']=1
        figSignal = go.Figure(data=figSignal.data + RepSig.data)
        i=i+1
    figSignal.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}) 
    
###tab2
    
#    tmp = sub_data.groupby([(pd.DatetimeIndex(sub_data['date']).year), (pd.DatetimeIndex(sub_data['date']).month)])[['cases', 'deaths']].sum()
#    dynrep = sub_data.groupby([(pd.DatetimeIndex(sub_data['date']).year), (sub_data['date'].dt.to_period('W-SAT'))])[['cases', 'deaths']].sum() #creates overlap in weeks between years
#    dynrep = sub_data.groupby([(sub_data['date'].dt.to_period('W-SAT')), (pd.DatetimeIndex(sub_data['date']).year)])[['cases', 'deaths'] ].sum() #same
#    dynrep = sub_data.groupby([(sub_data['date'].dt.to_period('W-SAT')), ((sub_data['date'].dt.to_period('W-SAT')).index.start_time.year)])[['cases', 'deaths'] ].sum()     # in two steps
    dynrep = sub_data.groupby([sub_data['date'].dt.to_period('W-SAT')])[['cases', 'deaths'] ].sum()     # in two steps
    dynrep['year']=dynrep.index.start_time.year
    tmpp= dynrep.loc[dynrep['year']==max(dynrep['year'])]
    
    color=['red', 'blue', 'orange', 'green']
    figgSick=px.bar(tmpp, x=tmpp.index.week, y='cases')     
    figgDead=px.bar(tmpp, x=tmpp.index.week, y='deaths')    
    i=0
    #potentially make a specific dataframe for the plot instead
    for year in dynrep['year'].unique():  # withing the month plot each year
        if year != max(dynrep['year']):
            tmpp = dynrep.loc[dynrep['year']==year]
            figgSickk = px.line(tmpp, x=tmpp.index.week, y='cases') #, labels={'date':'Date', 'cases':'No. of Sick Animals'})  
            figgSickk['data'][0]['line']['color']=color[i] #'rgb(204, 0, 0)'  # make color
            figgSickk['data'][0]['line']['width']=1
            figgSick = go.Figure(data=figgSick.data + figgSickk.data) #
            
            figgDeadd = px.line(tmpp, x=tmpp.index.week, y='deaths') #, labels={'date':'Date', 'cases':'No. of Sick Animals'})  
            figgDeadd['data'][0]['line']['color']=color[i] #'rgb(204, 0, 0)'
            figgDeadd['data'][0]['line']['width']=1
            figgDead = go.Figure(data=figgDead.data + figgDeadd.data)
            
            i=i+1

    figgSick.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})   
    figgDead.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})        

 
#################discrepancy international bangladesh weeks. 1.1.23 is sunday and would be week one. internationally it is week 52
   
    subDist=geodata[(geodata["loc_type"]==rgeoSlider)]
    tmp=sub_data[pd.DatetimeIndex(sub_data['date']).year==2023]
    total=tmp.groupby([tmp['date'].dt.to_period('W-SAT')])['cases'].sum()
    
    reports=pd.DataFrame({title.capitalize():[]})
    for i in range(len(total)):
      reports[i+1]=''
    reports['total']=''
    
    
    #summary weeks
    # if len(total)>2:
    #     for i in range(len(total)):
    #       reports[str('1-'+str(len(total)-1))]=''
    #       reports[str(len(total))]=''
          
    # if len(total)==2:
    #     reports['1']=''
    #     reports['2']=''
        
    # if len(total)==1:
    #     reports['1']=''
 
    for upano in tmp[title].unique():
        reports.at[upano,title.capitalize()]=str(subDist[subDist['value']==upano]['name'].reset_index(drop=True)[0]).title()
#################discrepancy international bangladesh weeks. 1.1.23 is sunday and would be week one. internationally it is week 52
        tmpp=tmp[tmp[title]==upano].groupby([tmp['date'].dt.to_period('W-SAT')])['cases'].sum()
        for entry in range(len(tmpp)):
#################discrepancy international bangladesh weeks. 1.1.23 is sunday and would be week one. internationally it is week 52
                reports.loc[upano][tmpp.index[entry].end_time.date().isocalendar()[1]]=tmpp[entry]
                
      
    reports['total']= reports.iloc[:,1:len(total)+1].sum(axis=1)
    reports[len(total)-1]=reports.iloc[:, 1:len(total)-2].sum(axis=1)
    reports.drop(reports.iloc[:, 1:len(total)-1], inplace=True, axis=1)
    reports=reports.rename(columns={len(total)-1:'week 1-'+ str(len(total)-1), len(total):'week ' + str(len(total))})
    reports=reports.fillna(0)
    # last=tmp['date'].dt.to_period('W-SAT')
    # lastwk=last.iloc[-1]
    # total=tmp.groupby([tmp['date'].dt.to_period('W-SAT')])['cases'].sum()
    # total.reset_index
    
    # tmp[tmp['upazila']==upano].groupby([tmp['date'].dt.to_period('W-SAT')])['cases'].sum()
    
    # reps= tmp.groupby([tmp['upazila']]).agg([tmp['date'].dt.to_period('W-SAT')])
    # reps = tmp.groupby([tmp['date'].dt.to_period('W-SAT')])[['cases'] ].sum()     
    # records = tmp.groupby([tmp['date'].dt.to_period('W-SAT')])[['cases'] ].sum() 
    # records = data_resp.groupby([title])['cases'].sum().to_frame()#(results in 492 values, what about the rest, plot the rest where there is nothing)

    #    casetable= dash_table.DataTable(resp_rep_data.to_dict('records'),
    casetable= dash_table.DataTable(reports.to_dict('records'), 
                                  columns=[{'name': i, 'id': i} for i in reports.loc[:,:]], #['Upazila','total']]],
                                  style_header={
                                        'overflow': 'hidden',
                                        'maxWidth': 0,
                                        },
                                  style_table={'height': '300px', 'overflowY': 'auto'},
                                  fixed_rows={'headers': True}),
    
    
    subDist=geodata[(geodata["loc_type"]==rgeoSlider)]
#    reports = sub_data[title].value_counts().to_frame()
#    reports = sub_data.value_counts().to_frame() #(results in 492 values, what about the rest, plot the rest where there is nothing)
    reports = sub_data.groupby([title])['cases'].sum().to_frame()#(results in 492 values, what about the rest, plot the rest where there is nothing)
    reports= reports.rename(columns={'cases' : title}, index={title: 'Index'})
    reports[pnumber] = reports.index
    reports[pname] = reports.index
    reports= reports.loc[reports[pname] != 'nan']

    data = open_data(path)
    for i in data['features']:
        i['id']= i['properties']['shapeName'].replace(" Division","")
    for i in range(reports.shape[0]):
        reports[pname].iloc[i] = subDist.loc[subDist['value']==int(reports[pname].iloc[i]),'name'].iloc[0]
    reports=reports.sort_values(pname)
    reports[pname]=reports[pname].str.capitalize()

    figRegion=px.bar(reports, x=pname, y=title, labels= {variab:labl})# ,color='basic_info_division')
    figRegion.update_layout(autosize=True, height=600, margin={"r":0,"t":0,"l":0,"b":0}) # width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})
    



    return vDistrict, vUpa, Rfig, figRep, figSignal, figgSick, figgDead, casetable, figRegion #figgR, 









