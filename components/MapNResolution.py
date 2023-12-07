from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd
import json
import plotly.express as px


def open_data(path):
    with open(path) as f:
        data = json.load(f)
    return data


def plotMap(geoResolution, geoResolutionNo, reportsdata, geoNameNNumber, shapePath):

    reports = reportsdata[geoResolution].value_counts().to_frame()
    reports[geoResolution + "number"] = reports.index       #print(reports.loc[reports[geoResolution + "number"] == "nan"])  reports, with no geonumbers?
    reports = reports.rename(columns={geoResolution: "Reports"})

    geoNameNNumber = geoNameNNumber[geoNameNNumber["loc_type"] == geoResolutionNo]
    geoNameNNumber = geoNameNNumber.rename(columns={"value": geoResolution + "number", "name": geoResolution + "name"})[[geoResolution + "number", geoResolution + "name"]]
    geoNameNNumber = geoNameNNumber.set_index(geoResolution + "number")
    geoNameNNumber[geoResolution + "name"] = geoNameNNumber[geoResolution + "name"].str.title()

    reports = reports.combine_first(geoNameNNumber)
    reports[geoResolution + "number"] = reports.index
    shapedata = open_data(shapePath)  
    geoResolutionDiv = geoResolution    # exception of shapefile names in division resolution
    if geoResolutionNo == 1:
        geoResolutionDiv = "div"


    if pd.notna(reports['Reports']).any():
       custolor = [[0, "white"], [1 / reports["Reports"].max(), "lightgray"], [1, "red"]]
    else:
       custolor = [[0, "white"]]

    fig = px.choropleth_mapbox(
        reports,
        geojson=shapedata,
        locations=geoResolution + "number",
        color="Reports",
        featureidkey="properties." + geoResolutionDiv + "number",
        color_continuous_scale=custolor,
        range_color=(1, reports["Reports"].max()),
        mapbox_style="carto-positron",
        zoom=5.8,
        center={"lat": 23.7, "lon": 90.3},
        opacity=0.7,
        labels={"Reports": "Reports"},
        hover_name=geoResolution + "name",
        hover_data={geoResolution + "name": False, geoResolution + "number": False}
    )
    fig.update_layout(
        autosize=True, coloraxis_showscale=True, margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550)
    
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
    Output("Map", "figure", allow_duplicate=True),
    Input("cache_bahis_data", "data"),
    Input("cache_bahis_geodata", "data"),
    prevent_initial_call=True
)

def mapPrep(sourcedata, geodata):

    geoResolution = "upazila"
    geoResolutionNo = 3
    reportsdata = pd.read_json(sourcedata, orient="split")
    geoNameNNumber = pd.read_json(geodata, orient="split")
    shapePath = "exported_data/processed_geodata/upadata.geojson"
    fig = plotMap(geoResolution, geoResolutionNo, reportsdata, geoNameNNumber, shapePath)
    return fig

#     # subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

# #    if ctx.triggered_id == 'geoSlider':
# #        Rfindic, Rfigg, NRlabel, AlertTable = GeoRep.GeoRep(sub_bahis_sourcedata, title,
# #                                                            subDistM, pnumber, pname, variab, labl)

# #    Rfig = plot_map(path, subDistM, sub_bahis_sourcedata, title, pnumber, pname, variab, labl)
#     Rfig = plot_map(path, subDistM, reportsdata, title, pnumber, pname, variab, labl)
#     return Rfig

