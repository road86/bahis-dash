import dash
from components import fetchdata, RegionSelect, MapNResolution
from dash import html, dcc, callback, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd


dash.register_page(__name__,)  # register page to main dash app

# def plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl):
#     reports = sub_bahis_sourcedata[title].value_counts().to_frame()
#     reports[pnumber] = reports.index  # 1
#     reports.index = reports.index.astype(int)  # upazila name
#     reports[pnumber] = reports[pnumber].astype(int)
#     reports = reports.loc[
#         reports[pnumber] != "nan"
#     ]  # unknown reason for now. does this have to be beore reports in sub_bahis_sourcedata?
#     # reports, where there are no geonumbers?
#     data = open_data(path)  # 1
#     reports[pname] = reports.index
#     tmp = subDistM[["value", "name"]]
#     tmp = tmp.rename(columns={"value": pnumber, "name": pname})
#     tmp[pname] = tmp[pname].str.title()
#     tmp["Index"] = tmp[pnumber]
#     tmp = tmp.set_index("Index")
#     tmp[title] = 0

#     aaa = reports.combine_first(tmp)
#     aaa[pname] = tmp[pname]
#     del tmp
#     del reports
#     reports = aaa
#     for i in range(reports.shape[0]):  # go through all upazila report values
#         reports[pname].iloc[i] = subDistM[subDistM["value"] == reports.index[i]]["name"].values[
#             0
#         ]  # still to work with the copy , this goes with numbers and nnot names
#     reports[pname] = reports[pname].str.title()
#     reports.set_index(pnumber)  # 1

#     custolor = [[0, "white"], [1 / reports[title].max(), "lightgray"], [1, "red"]]
#     fig = px.choropleth_mapbox(
#         reports,
#         geojson=data,
#         locations=pnumber,
#         color=title,
#         featureidkey="properties." + pnumber,
#         color_continuous_scale=custolor,
#         range_color=(1, reports[title].max()),
#         mapbox_style="carto-positron",
#         zoom=5.8,
#         center={"lat": 23.7, "lon": 90.3},
#         opacity=0.7,
#         labels={variab: labl},
#         hover_name=pname,
#         hover_data={pname: False, pnumber: False}
#     )
#     fig.update_layout(
#         autosize=True, coloraxis_showscale=True, margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550
#     )  # , width=760 , height=800, ) #, coloraxis_showscale= False) #width= 1000, height=600,
#     return fig




layout = html.Div([
    # dcc.Store(id="cache_bahis_data", storage_type="memory"),
    # dcc.Store(id="cache_bahis_dgdata", storage_type="memory"),
    # dcc.Store(id="cache_bahis_distypes", storage_type="memory"),
    dcc.Store(id="cache_bahis_geodata"),
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(RegionSelect.Form),
                    ),
                    dbc.Card(
                        dbc.CardBody(MapNResolution.Form)
                    )
                ],
                width=4,
            ),
        ]
    )
]),

@callback(
    Output("District", "options"),
    Output("Upazila", "options"),
    Input("Division", "value"),
    Input("District", "value"),
    Input("Upazila", "value"),
    Input("District", "options"),
    Input("Upazila", "options"),
    Input("cache_bahis_geodata", "data"),
    prevent_initial_call=True
)

def RegionSelect(SelectedDivision, SelectedDistrict, SelectedUpazila, DistrictList, UpazilaList, geodata):
    bahis_geodata=pd.read_json(geodata, orient="split")
    if DistrictList == None: DistrictList = []
    if UpazilaList == None: UpazilaList = []

    if ctx.triggered_id == "Division":
        if not SelectedDivision:
#            subDist = bahis_geodata
            DistrictList = []
            UpazilaList = []
        else:
#            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelectedDivision))]
            List = fetchdata.fetchDistrictlist(SelectedDivision, bahis_geodata)
            DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
            UpazilaList = []
#            sub_bahis_sourcedata = bahis_data.loc[bahis_data["division"] == SelectedDivision]  # DivNo]

    if ctx.triggered_id == "District":
        if not SelectedDistrict:
#            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelectedDivision))]
            UpazilaList = []
#            sub_bahis_sourcedata = bahis_data.loc[bahis_data["division"] == SelectedDivision]  # DivNo]
        else:
#            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelectedDistrict))]
            List = fetchdata.fetchUpazilalist(SelectedDistrict, bahis_geodata)
            UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]
#            sub_bahis_sourcedata = bahis_data.loc[bahis_data["district"] == SelectedDistrict]  # DivNo]

    if ctx.triggered_id == "Upazila":
        if not SelectedUpazila:
            print("a")
#            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelectedDistrict))]
#            sub_bahis_sourcedata = bahis_data.loc[bahis_data["district"] == SelectedDistrict]  # DivNo]
        else:
            print("b")
#            subDist = bahis_geodata.loc[bahis_geodata["value"].astype("string").str.startswith(str(SelectedUpazila ))]
#            sub_bahis_sourcedata = bahis_data.loc[bahis_data["upazila"] == SelectedUpazila ]

 if geoSlider == 1:
        path = path1
        loc = geoSlider
        title = "division"
        pnumber = "divnumber"
        pname = "divisionname"
        splace = " Division"
        variab = "division"
        subDistM = subDist[subDist["loc_type"] == geoSlider]

    if geoSlider == 2:
        path = path2
        loc = geoSlider
        title = "district"
        pnumber = "districtnumber"
        pname = "districtname"
        splace = " District"
        variab = "district"
        subDistM = subDist[subDist["loc_type"] == geoSlider]
        # subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

    if geoSlider == 3:
        path = path3
        loc = geoSlider
        loc = 3
        title = "upazila"
        pnumber = "upazilanumber"
        pname = "upazilaname"
        splace = " Upazila"
        variab = "upazila"
        subDistM = subDist[subDist["loc_type"] == 3]
        # subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

    if ctx.triggered_id == 'geoSlider':
        Rfindic, Rfigg, NRlabel, AlertTable = GeoRep.GeoRep(sub_bahis_sourcedata, title,
                                                            subDistM, pnumber, pname, variab, labl)

    Rfig = plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl)



    return DistrictList, UpazilaList