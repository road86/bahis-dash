# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:43:44 2023

@author: yoshka
"""

import dash
from dash import callback, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc 


import numpy as np
import pandas as pd
import datetime 
from datetime import datetime as dt
import os, glob

dash.register_page(__name__) 

sourcepath = 'exported_data/'
sourcefilename =os.path.join(sourcepath, 'preped_data2.csv')
geofilename = glob.glob(sourcepath + 'newbahis_geo_cluster*.csv')[-1]

def fetchsourcedata(): #fetch and prepare source data
    bahis_data = pd.read_csv(sourcefilename)
    bahis_data['from_static_bahis']=bahis_data['basic_info_date'].str.contains('/') # new data contains -, old data contains /
    bahis_data['basic_info_date'] = pd.to_datetime(bahis_data['basic_info_date'])
    del bahis_data['Unnamed: 0']
    bahis_data=bahis_data.rename(columns={'basic_info_date':'date',
                                        'basic_info_division':'division',
                                        'basic_info_district':'district',
                                        'basic_info_upazila':'upazila',
                                        'patient_info_species':'species_no',
                                        'diagnosis_treatment_tentative_diagnosis':'tentative_diagnosis',
                                        'patient_info_sick_number':'sick',
                                        'patient_info_dead_number':'dead',
                                        })
    bahis_data[['division', 'district', 'species_no']]=bahis_data[['division', 'district', 'species_no']].astype(np.uint16)
    bahis_data[['upazila', 'sick', 'dead']]=bahis_data[['upazila',  'sick', 'dead']].astype(np.int32) #converting into uint makes odd values)
    bahis_data['dead'] = bahis_data['dead'].clip(lower=0)
    bahis_data=bahis_data[bahis_data['date'].dt.year== max(bahis_data['date']).year]
    return bahis_data
bahis_data=fetchsourcedata()
sub_bahis_sourcedata=bahis_data
monthlydatabasis=sub_bahis_sourcedata

def fetchgeodata():     #fetch geodata from bahis, delete mouzas and unions
    geodata = pd.read_csv(geofilename)
    geodata = geodata.drop(geodata[(geodata['loc_type']==4) | (geodata['loc_type']==5)].index)  #drop mouzas and unions
    geodata=geodata.drop(['id', 'longitude', 'latitude', 'updated_at'], axis=1)
    geodata['parent']=geodata[['parent']].astype(np.uint16)   # assuming no mouza and union is taken into
    geodata[['value']]=geodata[['value']].astype(np.uint32)
    geodata[['loc_type']]=geodata[['loc_type']].astype(np.uint8)
    return geodata
bahis_geodata= fetchgeodata()


def fetchDivisionlist(bahis_geodata):   # division list is always the same, caching possible
    Divlist=bahis_geodata[(bahis_geodata["loc_type"]==1)][['value', 'name']]
    Divlist['name']=Divlist['name'].str.capitalize()
    Divlist=Divlist.rename(columns={'name':'Division'})
    Divlist=Divlist.sort_values(by=['Division'])
    return Divlist.to_dict('records')
Divlist=fetchDivisionlist(bahis_geodata)

def fetchdiseaselist(bahis_data):
    dislis= bahis_data['top_diagnosis'].unique()
    dislis= pd.DataFrame(dislis, columns=['Disease'])
    dislis= dislis['Disease'].sort_values().tolist()
    dislis.insert(0, 'All Diseases')
    return dislis
dislis=fetchdiseaselist(bahis_data)


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Division"),
            dcc.Dropdown(
                id="division-select",
                options=[{'label': i['Division'], 'value': i['value']} for i in Divlist],
#                value=Divlist[0]['value'],
            ),
            html.Br(),
            html.P("Select District"),
            dcc.Dropdown(
                id="district-select",
            ),
            html.Br(),
            html.P("Select Check-In Time"),
            dcc.DatePickerRange(
                id="date-picker-select",
                start_date="2022-12-31",
                end_date="2023-07-16",
                min_date_allowed=dt(2022, 1, 1),
                max_date_allowed=dt(2023, 12, 31),
                initial_visible_month=dt(2023, 1, 1),
            ),
            html.Br(),
            html.Br(),
            html.P("Select Disease"),
            dcc.Dropdown(
                id="disease-select",
                options=[{"label": i, "value": i} for i in dislis],
                value=dislis[0],
                multi=True,
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )


def find_weeks(start,end):
    l = []
    for i in range((end-start).days + 1):
        d = (start+datetime.timedelta(days=i)).isocalendar()[:2] # e.g. (2011, 52)
        yearweek = 'y{}w{:02}'.format(*d) # e.g. "201152"
        l.append(yearweek)
    return sorted(set(l))


def generate_reports_heatmap(start, end, division, district, hm_click, disease, reset):
    """
    :param: start: start date from selection.
    :param: end: end date from selection.
    :param: clinic: clinic from selection.
    :param: hm_click: clickData from heatmap.
    :param: admit_type: admission type from selection.
    :param: reset (boolean): reset heatmap graph if True.

    :return: Patient volume annotated heatmap.
    """
    start=dt.strptime(str(start),'%Y-%m-%d %H:%M:%S')
    end=dt.strptime(str(end),'%Y-%m-%d %H:%M:%S')

    if division is None:  # for national numbers
        vDis=[]
        filtered_bd=bahis_data
        filtered_bd=filtered_bd.sort_values('date').set_index('date').loc[start:end]
    
        if 'All Diseases' in disease:
            filtered_bd=filtered_bd
        else:
            filtered_bd=filtered_bd[filtered_bd['top_diagnosis'].isin(disease)]
        
        x_axis = find_weeks(start,end) #[1:] without first week
        x_axis = [str(x) for x in x_axis]
        y_axis=['Bangladesh']

        week = ""
        region = ""
        shapes = []  #when selected red rectangle

        if hm_click is not None:
            week = hm_click["points"][0]["x"]
            region = hm_click["points"][0]["y"]
            if region in y_axis:
    
                # Add shapes
                x0 = x_axis.index(week) / len(x_axis)
                x1 = x0 + 1 / len(x_axis)
                y0 = y_axis.index(region) / len(y_axis)
                y1 = y0 + 1 / len(y_axis)
        
                shapes = [
                    dict(
                        type="rect",
                        xref="paper",
                        yref="paper",
                        x0=x0,
                        x1=x1,
                        y0=y0,
                        y1=y1,
                        line=dict(color="#ff6347"),
                    )
                ]
        z= pd.DataFrame(index=x_axis, columns=y_axis)
        annotations = []

        tmp=filtered_bd.index.value_counts()
        tmp=tmp.to_frame()
        tmp['counts']=tmp['date']
        tmp['date']=pd.to_datetime(tmp.index)
        
        for ind_x, x_val in enumerate(x_axis):
            sum_of_record=tmp.loc[((tmp['date'].dt.year.astype(str)== x_val[1:5]) & (tmp['date'].dt.isocalendar().week.astype(str).str.zfill(2)== x_val[6:8])), 'counts'].sum()
            z.loc[x_val, 'Bangladesh'] = sum_of_record
    
            annotation_dict = dict(
                showarrow=False,
                text="<b>" + str(sum_of_record) + "<b>",
                xref="x",
                yref="y",
                x=x_val,
                y= 'Bangladesh',
                font=dict(family="sans-serif"),
            )
            annotations.append(annotation_dict) 

    else:   # for divisional numbers
        vDis=[]
        if district is None:
            tst=[str(x)[:4] for x in bahis_data['upazila']]
            tst2 = [i for i in range(len(tst)) if tst[i][:2]== str(division)]
            filtered_bd=bahis_data.iloc[tst2]
    
    
            Dislist=bahis_geodata[bahis_geodata['parent']==division][['value','name']]
            Dislist['name']=Dislist['name'].str.capitalize()
            Dislist=Dislist.rename(columns={'name':'District'})
            Dislist=Dislist.sort_values(by=['District'])
            Dislist=Dislist.to_dict('records')    
            vDis = [{'label': i['District'], 'value': i['value']} for i in Dislist]
        
            if 'All Diseases' in disease:
                filtered_bd=filtered_bd
            else:
                filtered_bd=filtered_bd[filtered_bd['top_diagnosis'].isin(disease)]
        
            #filtered_bd=filtered_bd.sort_values('date').set_index('date').loc[start[0]:end[0]]
        
            filtered_bd=filtered_bd.sort_values('date').set_index('date').loc[start:end]
        
            x_axis = find_weeks(start,end) #[1:] without first week
            x_axis = [str(x) for x in x_axis]
        ##    x_axis = find_weeks(dt.strptime(str(start[0]),'%Y-%m-%d %H:%M:%S'),dt.strptime(str(end[0]),'%Y-%m-%d %H:%M:%S')) #[1:] without first week#    x_axis = find_weeks(dt.strptime(str(start),'%Y-%m-%dT%H:%M:%S'),dt.strptime(str(end),'%Y-%m-%dT%H:%M:%S')) #[1:] without first week
            
            y_axis_no = list(set([str(x)[:4] for x in filtered_bd['upazila']]))
            y_axis=y_axis_no.copy()
                        
            for i, value in enumerate(y_axis_no):
                tst= bahis_geodata[bahis_geodata['loc_type']==2].loc[bahis_geodata[bahis_geodata['loc_type']==2]['value']== int(value), 'name']
                if not tst.empty:
                    y_axis[i] = tst.values[0].capitalize()
            
#            y_axis = [('No ' + str(y)) for y in y_axis ]
            tst= bahis_geodata[bahis_geodata['loc_type']==1].loc[bahis_geodata[bahis_geodata['loc_type']==1]['value']== int(division), 'name']
            y_axis.append("Σ " + tst.values[0].capitalize())
            y_axis_no.append(int(division))
#            y_axis.append('No ' + str(division))
            
            week = ""
            region = ""
            shapes = []  #when selected red rectangle
        
            if hm_click is not None  :
                week = hm_click["points"][0]["x"]
                region = hm_click["points"][0]["y"]
                if region in y_axis:
                    # Add shapes
                    if y_axis.index(region):
                        x0 = x_axis.index(week) / len(x_axis)
                        x1 = x0 + 1 / len(x_axis)
                        y0 = y_axis.index(region) / len(y_axis)
                        y1 = y0 + 1 / len(y_axis)
                
                        shapes = [
                            dict(
                                type="rect",
                                xref="paper",
                                yref="paper",
                                x0=x0,
                                x1=x1,
                                y0=y0,
                                y1=y1,
                                line=dict(color="#ff6347"),
                            )
                        ]
        
            # Get z value : sum(number of records) based on x, y,
        
           # z = np.zeros((len(y_axis), len(x_axis)))
            z= pd.DataFrame(index=x_axis, columns=y_axis)
            annotations = []
         #   tmp=filtered_bd.index.value_counts()
         #   z[division]=filtered_bd.groupby([filtered_bd['date'].dt.isocalendar().year, filtered_bd['date'].dt.isocalendar().week]).sum()
            for ind_y, district in enumerate(y_axis):       # go through divisions
                filtered_district = filtered_bd[pd.Series([str(x)[:4]==y_axis_no[ind_y] for x in filtered_bd['upazila']]).values]
#                filtered_district = filtered_bd[pd.Series([str(x)[:4]==district[3:7] for x in filtered_bd['upazila']]).values]
                #tmp['date']=tmp.index
#                if district != 'No ' + str(division) :  #for districts
                if district[:1] != 'Σ': #for districts
                    tmp=filtered_district.index.value_counts()
                    tmp=tmp.to_frame()
                    tmp['counts']=tmp['date']
                    tmp['date']=pd.to_datetime(tmp.index)
                    for ind_x, x_val in enumerate(x_axis):
            #            tmp=filtered_division['date'].dt.date.value_counts()
            #            sum_of_record = tmp['y'+tmp['date'].isocalendar().year+'w'+tmp['date'].isocalendar().week==x_val].sum()
            #            sum_of_record = len([x for x in tmp['date'] if (str(x.isocalendar().year) ==x_val[1:5] and str(x.isocalendar().week).zfill(2) ==x_val[6:8])])
                        # test [x for x in tmp['date'] if (str(tmp['date'].isocalendar().year) ==x_val[1:5] and str(tmp['date'].isocalendar().week) ==x_val[6:8])]
                        #sum_of_record = filtered_district['y'+filtered_district.index[ind_x].date().isocalendar().year+'w'+filtered_district.index[ind_x].date().isocalendar().week == x_val]["Number of Records"].sum()
                        
                        #sum_of_record = tmp['counts'].groupby([tmp['date'].dt.isocalendar().year, tmp['date'].dt.isocalendar().week]).sum()
                        #sum_of_record.index=['y'+str(col[0])+'w'+str("{:02d}".format(col[1])) for col in sum_of_record.index]     
            
                        sum_of_record= tmp.loc[((tmp['date'].dt.year.astype(str)== x_val[1:5]) & (tmp['date'].dt.isocalendar().week.astype(str).str.zfill(2)== x_val[6:8])), 'counts'].sum()
                        #dt.groupby([s.year, s.week]).sum()
                        z[district][x_val]=sum_of_record
            
                        annotation_dict = dict(
                            showarrow=False,
                            text="<b>" + str(sum_of_record) + "<b>",
                            xref="x",
                            yref="y",
                            x=x_val,
                            y=district,
                            font=dict(family="sans-serif"),
                        )
                        annotations.append(annotation_dict)    
                    
                    #Highlight annotation text by self-click
        
                        if x_val == week and district == region:
                            if not reset:
                                annotation_dict.update(size=15, font=dict(color="#ff6347"))
        
                if district[:1] == 'Σ': #for districts
#                if district == 'No ' + str(division) :    # for total division
                    tmp=filtered_bd.index.value_counts()
                    tmp=tmp.to_frame()
                    tmp['counts']=tmp['date']
                    tmp['date']=pd.to_datetime(tmp.index)
                    for ind_x, x_val in enumerate(x_axis):
                        sum_of_record=tmp.loc[((tmp['date'].dt.year.astype(str)== x_val[1:5]) & (tmp['date'].dt.isocalendar().week.astype(str).str.zfill(2)== x_val[6:8])), 'counts'].sum()
#                        z.loc[x_val, 'No ' + str(division)] = sum_of_record
                        z.loc[x_val, district] = sum_of_record
                
                        annotation_dict = dict(
                            showarrow=False,
                            text="<b>" + str(sum_of_record) + "<b>",
                            xref="x",
                            yref="y",
                            x=x_val,
                            y= district,
#                            y= 'No ' + str(division),
                            font=dict(family="sans-serif"),
                        )
                        annotations.append(annotation_dict)    
    
                        if x_val == week and district == region:
                            if not reset:
                                annotation_dict.update(size=15, font=dict(color="#ff6347"))

        else: #for district numbers
            tst=[str(x)[:6] for x in bahis_data['upazila']]
            tst2 = [i for i in range(len(tst)) if tst[i][:4]== str(district)]
            filtered_bd=bahis_data.iloc[tst2]
            
            Dislist=bahis_geodata[bahis_geodata['parent']==division][['value','name']]
            Dislist['name']=Dislist['name'].str.capitalize()
            Dislist=Dislist.rename(columns={'name':'District'})
            Dislist=Dislist.sort_values(by=['District'])
            Dislist=Dislist.to_dict('records')    
            vDis = [{'label': i['District'], 'value': i['value']} for i in Dislist]
    
            # Upalist=bahis_geodata[bahis_geodata['parent']==district][['value','name']]
            # Upalist['name']=Upalist['name'].str.capitalize()
            # Upalist=Upalist.rename(columns={'name':'Upazila'})
            # Upalist=Upalist.sort_values(by=['Upazila'])
            # Upalist=Upalist.to_dict('records')    
            # vUpa = [{'label': i['Upazila'], 'value': i['value']} for i in Upalist]
        
            if 'All Diseases' in disease:
                filtered_bd=filtered_bd
            else:
                filtered_bd=filtered_bd[filtered_bd['top_diagnosis'].isin(disease)]
        
            #filtered_bd=filtered_bd.sort_values('date').set_index('date').loc[start[0]:end[0]]
        
            filtered_bd=filtered_bd.sort_values('date').set_index('date').loc[start:end]
        
            x_axis = find_weeks(start,end) #[1:] without first week
            x_axis = [str(x) for x in x_axis]
        ##    x_axis = find_weeks(dt.strptime(str(start[0]),'%Y-%m-%d %H:%M:%S'),dt.strptime(str(end[0]),'%Y-%m-%d %H:%M:%S')) #[1:] without first week#    x_axis = find_weeks(dt.strptime(str(start),'%Y-%m-%dT%H:%M:%S'),dt.strptime(str(end),'%Y-%m-%dT%H:%M:%S')) #[1:] without first week
        
            y_axis_no = list(set([str(x)[:6] for x in filtered_bd['upazila']]))
            y_axis=y_axis_no.copy()
                        
            for i, value in enumerate(y_axis_no):
                tst= bahis_geodata[bahis_geodata['loc_type']==3].loc[bahis_geodata[bahis_geodata['loc_type']==3]['value']== int(value), 'name']
                if not tst.empty:
                    y_axis[i] = tst.values[0].capitalize()
            
            tst= bahis_geodata[bahis_geodata['loc_type']==2].loc[bahis_geodata[bahis_geodata['loc_type']==2]['value']== int(district), 'name']
            y_axis.append("Σ " + tst.values[0].capitalize())
            y_axis_no.append(int(district))
        
        
            week = ""
            region = ""
            shapes = []  #when selected red rectangle
        
            if hm_click is not None  :
                week = hm_click["points"][0]["x"]
                region = hm_click["points"][0]["y"]
                if region in y_axis:
                    # Add shapes
                    if y_axis.index(region):
                        x0 = x_axis.index(week) / len(x_axis)
                        x1 = x0 + 1 / len(x_axis)
                        y0 = y_axis.index(region) / len(y_axis)
                        y1 = y0 + 1 / len(y_axis)
                
                        shapes = [
                            dict(
                                type="rect",
                                xref="paper",
                                yref="paper",
                                x0=x0,
                                x1=x1,
                                y0=y0,
                                y1=y1,
                                line=dict(color="#ff6347"),
                            )
                        ]
        
            z= pd.DataFrame(index=x_axis, columns=y_axis)
            annotations = []
               
            for ind_y, upazila in enumerate(y_axis):       # go through divisions
                filtered_upazila = filtered_bd[pd.Series([str(x)[:6]==y_axis_no[ind_y] for x in filtered_bd['upazila']]).values]
        
                if upazila[:1] != 'Σ':  #for upazila
                    tmp=filtered_upazila.index.value_counts()
                    tmp=tmp.to_frame()
                    tmp['counts']=tmp['date']
                    tmp['date']=pd.to_datetime(tmp.index)            

                    for ind_x, x_val in enumerate(x_axis):
                        daysub=0
###########weekly defined via isocalendar (starts with Monday). so does not coincide with bengalian time counts.
                        for weekday in [1,2,3,6,7]: #Monday to Sunday skipping Thursday and Friday
                            if pd.Timestamp(datetime.date.fromisocalendar(int(x_val[1:5]), int(x_val[6:8]), weekday)) in pd.to_datetime(tmp['date']):
                                daysub=daysub + 1
                            
                                                    
                        ###sum_of_record= tmp.loc[((tmp['date'].dt.year.astype(str)== x_val[1:5]) & (tmp['date'].dt.isocalendar().week.astype(str).str.zfill(2)== x_val[6:8])), 'counts'].sum()

################ !!bug with year transition!!! 1.1.23 counts to wk52 from 2022

#                        ######
# code snipped to see reports per weekday 
# cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# bahis_data.groupby(pd.to_datetime(bahis_data['date'].astype(str), format = '%Y-%m-%d').dt.day_name()).count().reindex(cats) 
                        ###z[upazila][x_val]=sum_of_record
                        z[upazila][x_val]=daysub/5
            
                        annotation_dict = dict(
                            showarrow=False,
                            ###text="<b>" + str(sum_of_record) + "<b>",
                            text="<b>" + str(daysub/5) + "<b>",
                            xref="x",
                            yref="y",
                            x=x_val,
                            y=upazila,
                            font=dict(family="sans-serif"),
                        )
                        annotations.append(annotation_dict)    
        
                        if x_val == week and upazila == region:
                            if not reset:
                                annotation_dict.update(size=15, font=dict(color="#ff6347"))
        
                if upazila[:1] == 'Σ':  #for upazila
                    ### tmp=filtered_bd.index.value_counts()
                    ### tmp=tmp.to_frame()
                    ### tmp['counts']=tmp['date']
                    ### tmp['date']=pd.to_datetime(tmp.index)
                    for ind_x, x_val in enumerate(x_axis):
                        #for entries in range(z.shape[1]):
                    ###     sum_of_record=tmp.loc[((tmp['date'].dt.year.astype(str)== x_val[1:5]) & (tmp['date'].dt.isocalendar().week.astype(str).str.zfill(2)== x_val[6:8])), 'counts'].sum()
                    ###     z.loc[x_val, upazila] = sum_of_record
                            z.loc[x_val, upazila] = sum(z.loc[x_val] ==1)/z.shape[1]#sum_of_record
                            annotation_dict = dict(
                                showarrow=False,
                                ###text="<b>" + str(sum_of_record) + "<b>",
                                text="<b>" + "{:.2f}".format(sum(z.loc[x_val] ==1)/(z.shape[1]-1)*100) + " %<b>",
                                xref="x",
                                yref="y",
                                x=x_val,
                                y=upazila, 
                                font=dict(family="sans-serif"),
                            )
                            annotations.append(annotation_dict)    
        
                            if x_val == week and upazila == region:
                                if not reset:
                                    annotation_dict.update(size=15, font=dict(color="#ff6347"))
        
    z=z.fillna(0)
    z=z.T
    z=z.to_numpy()
    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} Records"
    
    
    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            ###colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
            colorscale=[[0, "white" ], [0.2, "#eeffe3" ], [0.4, "#ccfcae" ], [0.6, "#adfc7c" ], [0.8, "#77fc21" ], [1, "#62ff00" ],],
        )
    ]
    
    layout = dict(
        margin=dict(l=100, b=50, t=50, r=50),
        modebar={"orientation": "v"},
        font=dict(family="Open Sans"),
        annotations=annotations,
        shapes=shapes,
        xaxis=dict(
            type="category",
            side="top",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
        ),
        yaxis=dict(
            type="category", 
            side="left", 
            ticks="", 
            tickfont=dict(family="sans-serif"), 
            ticksuffix=" "
        ),
        hovermode="closest",
        showlegend=False,
    )
    return {"data": data, "layout": layout}, vDis


layout = html.Div([
    dbc.Row([
        dbc.Col([
                html.Div(
                    id="left-column",
                    className="four columns",
                    children=[generate_control_card()]
                    + [
                        html.Div(
                            ["initial child"], id="output-clientside", style={"display": "none"}
                        )
                    ],
                ),
        ], width= 3),
        dbc.Col([
        
            # Right column
            html.Div(
                id="right-column",
                className="eight columns",
                children=[
                    # Reports Heatmap
                    html.Div(
                        id="reports_card",
                        children=[
                            html.B("Reports"),
                            html.Hr(),
                            dcc.Graph(id="reports_hm"),
                        ],
                    ),
                ],
            ),
        ], width= 9)
    ])
    ],
)

# code snipped to see reports per weekday 
# cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# bahis_data.groupby(pd.to_datetime(bahis_data['date'].astype(str), format = '%Y-%m-%d').dt.day_name()).count().reindex(cats) 

@callback(
    Output("reports_hm", "figure"),
    Output("district-select", "options"),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("division-select", "value"),
        Input("district-select", "value"),
        Input("reports_hm", "clickData"),
        Input("disease-select", "value"),
        Input("reset-btn", "n_clicks"),
    ],
)
def update_heatmap(start, end, division, district, hm_click, disease, reset_click):
    start = start + " 00:00:00"
    end = end + " 00:00:00"

    reset = False
    # Find which one has been triggered
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "reset-btn":
            reset = True
        if prop_id == "division-select":
            district=None
    
    return generate_reports_heatmap(
        start, end, division, district, hm_click, disease, reset
    )





