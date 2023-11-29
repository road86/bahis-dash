from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd
import json
import plotly.express as px

def open_data(path):
    with open(path) as f:
        data = json.load(f)
    return data

def plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl):
    reports = sub_bahis_sourcedata[title].value_counts().to_frame()
    reports[pnumber] = reports.index  # 1
    reports.index = reports.index.astype(int)  # upazila name
    reports[pnumber] = reports[pnumber].astype(int)
    reports = reports.loc[
        reports[pnumber] != "nan"
    ]  # unknown reason for now. does this have to be beore reports in sub_bahis_sourcedata?
    # reports, where there are no geonumbers?
    data = open_data(path)  # 1
    reports[pname] = reports.index
    tmp = subDistM[["value", "name"]]
    tmp = tmp.rename(columns={"value": pnumber, "name": pname})
    tmp[pname] = tmp[pname].str.title()
    tmp["Index"] = tmp[pnumber]
    tmp = tmp.set_index("Index")
    tmp[title] = 0

    aaa = reports.combine_first(tmp)
    aaa[pname] = tmp[pname]
    del tmp
    del reports
    reports = aaa
    for i in range(reports.shape[0]):  # go through all upazila report values
        reports[pname].iloc[i] = subDistM[subDistM["value"] == reports.index[i]]["name"].values[
            0
        ]  # still to work with the copy , this goes with numbers and nnot names
    reports[pname] = reports[pname].str.title()
    reports.set_index(pnumber)  # 1

    custolor = [[0, "white"], [1 / reports[title].max(), "lightgray"], [1, "red"]]
    fig = px.choropleth_mapbox(
        reports,
        geojson=data,
        locations=pnumber,
        color=title,
        featureidkey="properties." + pnumber,
        color_continuous_scale=custolor,
        range_color=(1, reports[title].max()),
        mapbox_style="carto-positron",
        zoom=5.8,
        center={"lat": 23.7, "lon": 90.3},
        opacity=0.7,
        labels={variab: labl},
        hover_name=pname,
        hover_data={pname: False, pnumber: False}
    )
    fig.update_layout(
        autosize=True, coloraxis_showscale=True, margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550
    )  # , width=760 , height=800, ) #, coloraxis_showscale= False) #width= 1000, height=600,
    return fig


Form = html.Div([
    dcc.Store(id="cache_bahis_data", storage_type="memory"),
    dcc.Store(id="cache_bahis_geodata", storage_type="memory"),
    dcc.Graph(id="Map"),
        dcc.Slider(
            min=1,
            max=3,
            step=1,
            marks={
                1: "Division",
                2: "District",
                3: "Upazila",
            },
            value=3,
            id="geoSlider",
        )
    ])


@callback(
    Output("Map", "figure"),
    Input("cache_bahis_data", "data"),
    Input("cache_bahis_geodata", "data"),
)

def plotMap(sourcedata, geodata):

    sub_bahis_sourcedata=pd.read_json(sourcedata, orient="split")
    subDist=pd.read_json(geodata, orient="split")
    path = "exported_data/processed_geodata/upadata.geojson"
    loc = 3
    title = "upazila"
    pnumber = "upazilanumber"
    pname = "upazilaname"
    splace = " Upazila"
    variab = "upazila"
    subDistM = subDist[subDist["loc_type"] == 3]
    labl = "Reports"
    # subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

#    if ctx.triggered_id == 'geoSlider':
#        Rfindic, Rfigg, NRlabel, AlertTable = GeoRep.GeoRep(sub_bahis_sourcedata, title,
#                                                            subDistM, pnumber, pname, variab, labl)

    Rfig = plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl)
    return Rfig