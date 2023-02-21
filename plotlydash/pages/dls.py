# # -*- coding: utf-8 -*-
# """
# Created on Sun Jan 22 07:48:14 2023

# @author: yoshka
# """




from datetime import timedelta
import plotly.graph_objs as go
import numpy as np
from dash import dcc, html
import dash
import pandas as pd


dash.register_page(__name__)

def holidays():
    #year = dt.now().year
    
    d1 = pd.to_datetime('01.01.2022') #dt.date(2022, 8, 1)
    d2 = pd.to_datetime('01.01.2023') #dt.date(2023, 7, 15)

    delta = d2 - d1

    dates_in_year = [d1 + timedelta(i) for i in range(delta.days+1)] #gives me a list with datetimes for each day a year
    weekdays_in_year = [i.weekday() for i in dates_in_year] #gives [0,1,2,3,4,5,6,0,1,2,3,4,5,6,…] (ticktext in xaxis dict translates this to weekdays
    weeknumber_of_dates = [i.strftime("%Gww%V")[2:] for i in dates_in_year] #gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,…] name is self-explanatory
    z = np.random.randint(2, size=(len(dates_in_year)))
    text = [str(i) for i in dates_in_year] #gives something like list of strings like ‘2018-01-25’ for each date. Used in data trace to make good hovertext.
    #4cc417 green #347c17 dark green
    colorscale=[[False, '#eeeeee'], [True, '#76cf63']]

    data = [
    go.Heatmap(
    x = weeknumber_of_dates,
    y = weekdays_in_year,
    z = z,
    text=text,
    hoverinfo='text',
    xgap=3, # this
    ygap=3, # and this is used to make the grid-like apperance
    showscale=False,
    colorscale=colorscale
    )
    ]
    
    layout = go.Layout(
    title='activity chart',
    height=280,
    yaxis=dict(
    showline = False, showgrid = False, zeroline = False,
    tickmode='array',
    ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    tickvals=[0,1,2,3,4,5,6],
    ),
    xaxis=dict(
    showline = False, showgrid = False, zeroline = False,
    ),
    font={'size':10, 'color':'#9e9e9e'},
    plot_bgcolor=('#fff'),
    margin = dict(t=40),
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

#app = dash.Dash()
layout = html.Div([
dcc.Graph(id='heatmap-test', figure=holidays(), config={'displayModeBar': False})
])


# # Import necessary libraries 
# import dash
# from dash import dash_table, dcc, html, callback
# from dash.dependencies import Input, Output
# import pandas as pd
# from datetime import datetime, timedelta
# import numpy as np
# import plotly.express as px

# sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
# #geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
# sourcefilename =sourcepath + 'preped_data2.csv'   
# bahis_sd = pd.read_csv(sourcefilename)
# img_logo= 'assets/Logo.png'

# path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # found shapefiles from the data.humdata.org
# path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
# path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
# path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
# path4= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union

# def fetchsourcedata():
#     bahis_sd = pd.read_csv(sourcefilename) 
#     bahis_sd['basic_info_division'] = pd.to_numeric(bahis_sd['basic_info_division'])
#     bahis_sd['basic_info_district'] = pd.to_numeric(bahis_sd['basic_info_district'])
#     bahis_sd['basic_info_upazila'] = pd.to_numeric(bahis_sd['basic_info_upazila'])
#     bahis_sd['basic_info_date'] = pd.to_datetime(bahis_sd['basic_info_date'])
    
#     # restrict to data from 2019
#     tmask= (bahis_sd['basic_info_date']>= pd.to_datetime('01.01.2019')) & (bahis_sd['basic_info_date'] <= pd.to_datetime(bahis_sd['basic_info_date'].max()))
#     sub_data=bahis_sd.loc[tmask]
 
    
#     rep = sub_data.filter(['basic_info_district', 'basic_info_date'], axis=1)
#     rep = rep.groupby('basic_info_district').resample('W-Fri', on='basic_info_date').sum()
#     rep = rep.rename(columns={'basic_info_district': 'reports'})
#     rep = rep.reset_index()
    
#     del bahis_sd
#     #print(rep)
#     return rep
# bahis_sourcedata= fetchsourcedata()

# tmp=bahis_sourcedata['basic_info_district'].unique()
# #tmpp=pd.DataFrame([tmp]).transpose()
# #tmpp.columns=['district']
# wklst=np.arange(bahis_sourcedata['basic_info_date'].max(), bahis_sourcedata['basic_info_date'].min(), timedelta(weeks=-1)).astype(datetime)
# tmpp=pd.DataFrame(data=[], index=tmp, columns=wklst)
# for i in bahis_sourcedata.itertuples():
#     # print(int(i[1]))
#     # print(pd.to_datetime(i[2]))
#     # print(int(i[3]))
#     tmpp.loc[i[1],pd.to_datetime(i[2])]=int(i[3])
    

#                 # sub_bahis_sourcedata= sub_bahis_sourcedata

#                 # path=path2
#                 # loc=2
#                 # title='basic_info_district'
#                 # pname='districtname'
#                 # splace=' District'
#                 # variab='district'
#                 # labl='Incidences per district'
#     # subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]
#     # reports = sub_bahis_sourcedata[title].value_counts().to_frame()
#     # reports[pname] = reports.index
#     # reports= reports.loc[reports[pname] != 'nan']

#     # data = open_data(path)
#     # for i in data['features']:
#     #     i['id']= i['properties']['shapeName'].replace(" Division","")
#     # for i in range(reports.shape[0]):
#     #     reports[pname].iloc[i] = subDist.loc[subDist['value']==int(reports[pname].iloc[i]),'name'].iloc[0]
#     # reports=reports.sort_values(pname)
#     # reports[pname]=reports[pname].str.capitalize()
        
#     # Rfigg=px.bar(reports, x=pname, y=title, labels= {variab:labl})# ,color='basic_info_division')
#     # Rfigg.update_layout(autosize=True, height=500, margin={"r":0,"t":0,"l":0,"b":0}) # width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})

# bahis_sourcedata['id'] = bahis_sourcedata['basic_info_district']
# bahis_sourcedata.set_index('id', inplace=True, drop=False)


# ##df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
# # add an id column and set it as the index
# # in this case the unique ID is just the country name, so we could have just
# # renamed 'country' to 'id' (but given it the display name 'country'), but
# # here it's duplicated just to show the more general pattern.

# fig=px.imshow(tmpp)


# ##df['id'] = df['country']
# ##df.set_index('id', inplace=True, drop=False)

# #app = Dash(__name__)
# dash.register_page(__name__)

# layout = html.Div([
#     dcc.Graph(figure=fig)
# #1    dash_table.DataTable(
# #1        tmpp.to_dict('records'), [{"name": i, "id": i} for i in tmpp.columns])
# #     dash_table.DataTable(
# #         id='datatable-row-ids',
# #         columns=[
# #             {'name': i, 'id': i, 'deletable': True} for i in tmpp.columns
# # #            {'name': i, 'id': i, 'deletable': True} for i in bahis_sourcedata.columns
# # #            {'name': i, 'id': i, 'deletable': True} for i in df.columns
# #             # omit the id column
# #             if i != 'id'
# #         ],
# #         data=tmpp.to_dict('records'),
# # #        data=bahis_sourcedata.to_dict('records'),
# # #        data=df.to_dict('records'),
# #         editable=True,
# #         filter_action="native",
# #         sort_action="native",
# #         sort_mode='multi',
# #         row_selectable='multi',
# #         row_deletable=True,
# #         selected_rows=[],
# #         page_action='native',
# #         page_current= 0,
# #         page_size= 10,
# #     ),
# #     html.Div(id='datatable-row-ids-container')
# ])


# # @callback(
# #     Output('datatable-row-ids-container', 'children'),
# #     Input('datatable-row-ids', 'derived_virtual_row_ids'),
# #     Input('datatable-row-ids', 'selected_row_ids'),
# #     Input('datatable-row-ids', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])

# #     if row_ids is None:
# #         dff = tmpp
# # #        dff = bahis_sourcedata
# # #        dff = df
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = tmpp['id']
# # #        row_ids = bahis_sourcedata['id']
# # #        row_ids = df['id']
# #     else:
# #         dff = tmpp.loc[row_ids]
# # #        dff = bahis_sourcedata.loc[row_ids]
# # #        dff = df.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return [
# #         dcc.Graph(
# #             id=column + '--row-ids',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['basic_info_district'],
# # #                        'x': dff['basic_info_district'],
# # #                        'x': dff['country'],
# #                         'y': dff[column],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {'automargin': True},
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': column}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
# #         # check if column exists - user may have deleted it
# #         # If `column.deletable=False`, then you don't
# #         # need to do this check.
# #         for column in ['basic_info_date', 'reports'] if column in dff
# # #        for column in ['pop', 'lifeExp', 'gdpPercap'] if column in dff
# #     ]


# # if __name__ == '__main__':
# #     app.run_server(debug=True)
