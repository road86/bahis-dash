import glob
import json
import os
from datetime import date, datetime, timedelta

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import callback, ctx, dash_table, dcc, html
from dash.dash import no_update
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

starttime_start = datetime.now()

pd.options.mode.chained_assignment = None

dash.register_page(__name__)  # register page to main dash app

# sourcepath='C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'    #for local debugging purposes
# path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM0_simplified.geojson"
# #1 Nation # reminder: found shapefiles from the data.humdata.org
sourcepath = "exported_data/"
geofilename = glob.glob(sourcepath + "newbahis_geo_cluster*.csv")[
    -1
]  # the available geodata from the bahis project (Masterdata)
dgfilename = os.path.join(sourcepath, "Diseaselist.csv")  # disease grouping info (Masterdata)
sourcefilename = os.path.join(
    sourcepath, "preped_data2.csv"
)  # main data resource of prepared data from old and new bahis
path1 = os.path.join(sourcepath, "processed_geodata", "divdata.geojson")  # 8 Division
path2 = os.path.join(sourcepath, "processed_geodata", "distdata.geojson")  # 64 District
path3 = os.path.join(sourcepath, "processed_geodata", "upadata.geojson")  # 495 Upazila

firstrun = True


def fetchsourcedata():  # fetch and prepare source data
    bahis_data = pd.read_csv(sourcefilename)
    bahis_data["from_static_bahis"] = bahis_data["basic_info_date"].str.contains(
        "/"
    )  # new data contains -, old data contains /
    bahis_data["basic_info_date"] = pd.to_datetime(bahis_data["basic_info_date"], errors="coerce")
    #    bahis_data = pd.to_numeric(bahis_data['basic_info_upazila']).dropna().astype(int)
    # empty upazila data can be eliminated, if therre is
    del bahis_data["Unnamed: 0"]
    bahis_data = bahis_data.rename(
        columns={
            "basic_info_date": "date",
            "basic_info_division": "division",
            "basic_info_district": "district",
            "basic_info_upazila": "upazila",
            "patient_info_species": "species_no",
            "diagnosis_treatment_tentative_diagnosis": "tentative_diagnosis",
            "patient_info_sick_number": "sick",
            "patient_info_dead_number": "dead",
        }
    )
    # assuming non negative values from division, district, upazila, speciesno, sick and dead
    bahis_data[["division", "district", "species_no"]] = bahis_data[["division", "district", "species_no"]].astype(
        np.uint16
    )
    bahis_data[["upazila", "sick", "dead"]] = bahis_data[["upazila", "sick", "dead"]].astype(
        np.int32
    )  # converting into uint makes odd values)
    #    bahis_data[['species', 'tentative_diagnosis', 'top_diagnosis']]=bahis_data[['species',
    #                                                                                'tentative_diagnosis',
    #                                                                                'top_diagnosis']].astype(str)
    # can you change object to string and does it make a memory difference`?
    bahis_data["dead"] = bahis_data["dead"].clip(lower=0)
    #    bahis_data=bahis_data[bahis_data['date']>=datetime(2019, 7, 1)]
    # limit to this year    bahis_data=bahis_data[bahis_data['date'].dt.year== max(bahis_data['date']).year]
    return bahis_data


bahis_data = fetchsourcedata()
sub_bahis_sourcedata = bahis_data
monthlydatabasis = sub_bahis_sourcedata


def sne_date(bahis_data):
    start_date = min(bahis_data["date"]).date()
    end_date = max(bahis_data["date"]).date()
    dates = [start_date, end_date]
    return dates


start_date = date(2019, 1, 1)
end_date = date(2023, 12, 31)
dates = [start_date, end_date]

ddDList = []
Divlist = []


def fetchdisgroupdata():  # fetch and prepare disease groups
    bahis_dgdata = pd.read_csv(dgfilename)
    # bahis_dgdata= bahis_dgdata[['species', 'name', 'id', 'Disease type']]
    # remark what might be helpful: reminder: memory size
    bahis_dgdata = bahis_dgdata[["name", "Disease type"]]
    bahis_dgdata = bahis_dgdata.dropna()
    # bahis_dgdata[['name', 'Disease type']] = str(bahis_dgdata[['name', 'Disease type']])
    # can you change object to string and does it make a memory difference?
    bahis_dgdata = bahis_dgdata.drop_duplicates(subset="name", keep="first")
    return bahis_dgdata


bahis_dgdata = fetchdisgroupdata()
to_replace = bahis_dgdata["name"].tolist()
replace_with = bahis_dgdata["Disease type"].tolist()


def fetchgeodata():  # fetch geodata from bahis, delete mouzas and unions
    geodata = pd.read_csv(geofilename)
    geodata = geodata.drop(
        geodata[(geodata["loc_type"] == 4) | (geodata["loc_type"] == 5)].index
    )  # drop mouzas and unions
    geodata = geodata.drop(["id", "longitude", "latitude", "updated_at"], axis=1)
    geodata["parent"] = geodata[["parent"]].astype(np.uint16)  # assuming no mouza and union is taken into
    geodata[["value"]] = geodata[["value"]].astype(np.uint32)
    geodata[["loc_type"]] = geodata[["loc_type"]].astype(np.uint8)
    return geodata


bahis_geodata = fetchgeodata()
subDist = bahis_geodata


# cache these values


def fetchDivisionlist(bahis_geodata):  # division lsit is always the same, caching possible
    Divlist = bahis_geodata[(bahis_geodata["loc_type"] == 1)][["value", "name"]]
    Divlist["name"] = Divlist["name"].str.capitalize()
    Divlist = Divlist.rename(columns={"name": "Division"})
    Divlist = Divlist.sort_values(by=["Division"])
    return Divlist.to_dict("records")


# Divlist=fetchDivisionlist()


def fetchDistrictlist(SelDiv, bahis_geodata):  # district list is dependent on selected division
    Dislist = bahis_geodata[bahis_geodata["parent"] == SelDiv][["value", "name"]]
    Dislist["name"] = Dislist["name"].str.capitalize()
    Dislist = Dislist.rename(columns={"name": "District"})
    Dislist = Dislist.sort_values(by=["District"])
    return Dislist.to_dict("records")


def fetchUpazilalist(SelDis, bahis_geodata):  # upazila list is dependent on selected district
    Upalist = bahis_geodata[bahis_geodata["parent"] == SelDis][["value", "name"]]  # .str.capitalize()
    Upalist["name"] = Upalist["name"].str.capitalize()
    Upalist = Upalist.rename(columns={"name": "Upazila"})
    Upalist = Upalist.sort_values(by=["Upazila"])
    return Upalist.to_dict("records")


def date_subset(dates, bahis_data):
    tmask = (bahis_data["date"] >= pd.to_datetime(dates[0])) & (bahis_data["date"] <= pd.to_datetime(dates[1]))
    return bahis_data.loc[tmask]


def disease_subset(cDisease, sub_bahis_sourcedata):
    if "All Diseases" in cDisease:
        sub_bahis_sourcedata = sub_bahis_sourcedata
    else:
        sub_bahis_sourcedata = sub_bahis_sourcedata[sub_bahis_sourcedata["top_diagnosis"] == cDisease]
    return sub_bahis_sourcedata


ddDivision = html.Div(
    [
        dbc.Label("Select Division"),
        dcc.Dropdown(
            options=[{"label": i["Division"], "value": i["value"]} for i in Divlist],
            id="Division",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddDistrict = html.Div(
    [
        dbc.Label("Select District"),
        dcc.Dropdown(
            id="District",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddUpazila = html.Div(
    [
        dbc.Label("Select Upazila"),
        dcc.Dropdown(
            id="Upazila",
            clearable=True,
        ),
    ],
    className="mb-4",
)


def fetchdiseaselist(bahis_data):
    dislis = bahis_data["top_diagnosis"].unique()
    dislis = pd.DataFrame(dislis, columns=["Disease"])
    dislis = dislis["Disease"].sort_values().tolist()
    dislis.insert(0, "All Diseases")
    return dislis


def natNo(sub_bahis_sourcedata):
    mask = (sub_bahis_sourcedata["date"] >= datetime.now() - timedelta(days=7)) & (
        sub_bahis_sourcedata["date"] <= datetime.now()
    )
    # print(mask.value_counts(True])
    tmp_sub_data = sub_bahis_sourcedata["date"].loc[mask]
    diff = tmp_sub_data.shape[0]

    tmp_sub_data = sub_bahis_sourcedata["sick"].loc[mask]
    diffsick = int(tmp_sub_data.sum().item())

    tmp_sub_data = sub_bahis_sourcedata["dead"].loc[mask]
    diffdead = int(tmp_sub_data.sum().item())
    return [diff, diffsick, diffdead]


def fIndicator(sub_bahis_sourcedata):
    [diff, diffsick, diffdead] = natNo(sub_bahis_sourcedata)

    RfigIndic = go.Figure()

    RfigIndic.add_trace(
        go.Indicator(
            mode="number+delta",
            title="Total Reports",
            value=sub_bahis_sourcedata.shape[0],  # f"{bahis_sourcedata.shape[0]:,}"),
            delta={"reference": sub_bahis_sourcedata.shape[0] - diff},  # 'f"{diff:,}"},
            domain={"row": 0, "column": 0},
        )
    )

    RfigIndic.add_trace(
        go.Indicator(
            mode="number+delta",
            title="Sick Animals",
            value=sub_bahis_sourcedata["sick"].sum(),  # f"{int(bahis_sourcedata['sick'].sum()):,}",
            delta={"reference": sub_bahis_sourcedata["sick"].sum() - diffsick},  # f"{diffsick:,}",
            domain={"row": 0, "column": 1},
        )
    )

    RfigIndic.add_trace(
        go.Indicator(
            mode="number+delta",
            title="Dead Animals",
            value=sub_bahis_sourcedata["dead"].sum(),  # f"{int(bahis_sourcedata['dead'].sum()):,}",
            delta={"reference": sub_bahis_sourcedata["dead"].sum() - diffdead},  # f"{diffdead:,}",
            domain={"row": 0, "column": 2},
        )
    )

    RfigIndic.update_layout(
        height=100,
        grid={"rows": 1, "columns": 3},  # 'pattern': "independent"},
        # ?template=template_from_url(theme),
    )
    return RfigIndic


def open_data(path):
    with open(path) as f:
        data = json.load(f)
    return data

    # path=path3
    # loc=3
    # title='upazila'
    # pnumber='upazilanumber'
    # pname='upazilaname'
    # splace=' Upazila'
    # variab='upazila'
    # labl='Incidences per upazila'
    # incsub_bahis_sourcedata = pd.to_numeric(sub_bahis_sourcedata['upazila']).dropna().astype(int)


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
    tmp[title] = -(reports[pname].max())

    #    for i in range(tmp.shape[0]):
    #    aaa=pd.merge(tmp, reports, how="left", on=[pnumber])
    aaa = reports.combine_first(tmp)
    aaa[pname] = tmp[pname]
    del tmp
    del reports
    # aaa=aaa.drop([pname+'_y'], axis=1)
    # aaa=aaa.rename(columns={'upazilaname'+'_x': 'upazilaname'})
    reports = aaa
    for i in range(reports.shape[0]):  # go through all upazila report values
        reports[pname].iloc[i] = subDistM[subDistM["value"] == reports.index[i]]["name"].values[
            0
        ]  # still to work with the copy , this goes with numbers and nnot names
    reports[pname] = reports[pname].str.title()
    reports.set_index(pnumber)  # 1


    fig = px.choropleth_mapbox(
        reports,
        geojson=data,
        locations=pnumber,
        color=title,
        featureidkey="properties." + pnumber,
        #                            featureidkey="Cmap",
        color_continuous_scale="RdBu_r",  # "YlOrBr",
        color_continuous_midpoint=0,
        range_color=(-reports[title].max(), reports[title].max()),
        mapbox_style="carto-positron",
        zoom=5.8,
        center={"lat": 23.7, "lon": 90.3},
        opacity=0.5,
        labels={variab: labl},
        hover_name=pname,
    )
    fig.update_layout(
        autosize=True, coloraxis_showscale=False, margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550
    )  # , width=760 , height=800, ) #, coloraxis_showscale= False) #width= 1000, height=600,
    return fig

def find_weeks(start, end):
    list_of_weeks = []
    for i in range((end - start).days + 1):
        d = (start + timedelta(days=i)).isocalendar()[:2]  # e.g. (2011, 52)
        yearweek = "y{}w{:02}".format(*d)  # e.g. "201152"
        list_of_weeks.append(yearweek)
    return sorted(set(list_of_weeks))

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
    start = datetime.strptime(str(start), "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(str(end), "%Y-%m-%d %H:%M:%S")

    if division is None:  # for national numbers
        vDis = []
        filtered_bd = bahis_data
        filtered_bd = filtered_bd.sort_values("date").set_index("date").loc[start:end]

        Divlist = bahis_geodata[bahis_geodata["loc_type"] == 1][["value", "name"]]
        Divlist["name"] = Divlist["name"].str.capitalize()
        Divlist = Divlist.rename(columns={"name": "Division"})
        Divlist = Divlist.sort_values(by=["Division"])
        Divlist = Divlist.to_dict("records")

        if "All Diseases" in disease:
            filtered_bd = filtered_bd
        else:
            filtered_bd = filtered_bd[filtered_bd["top_diagnosis"]==disease] #.isin(disease)]

        #        filtered_bd=filtered_bd.sort_values('date').set_index('date').loc[start:end]

        x_axis = find_weeks(start, end)  # [1:] without first week
        x_axis = [str(x) for x in x_axis]

        # get stuff for bangaldesh total numbers with division. copy comment stuff below.
        y_axis_no = list(set([str(x)[:2] for x in filtered_bd["upazila"]]))
        y_axis = y_axis_no.copy()

        for i, value in enumerate(y_axis_no):
            tst = bahis_geodata[bahis_geodata["loc_type"] == 1].loc[
                bahis_geodata[bahis_geodata["loc_type"] == 1]["value"] == int(value), "name"
            ]
            if not tst.empty:
                y_axis[i] = tst.values[0].capitalize()

        y_axis.append("Bangladesh")  # "Σ " + tst.values[0].capitalize())
        y_axis_no.append("Bangladesh")  # int(division))
        # #            y_axis.append('No ' + str(division))

        #        y_axis=['Bangladesh']

        week = ""
        region = ""
        shapes = []  # when selected red rectangle

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
        z = pd.DataFrame(index=x_axis, columns=y_axis)
        annotations = []

        tmp = filtered_bd.index.value_counts()
        tmp = tmp.to_frame()
        tmp["counts"] = tmp["date"]
        tmp["date"] = pd.to_datetime(tmp.index)

        for ind_y, division in enumerate(y_axis):
            filtered_division = filtered_bd[
                pd.Series([str(x)[:2] == y_axis_no[ind_y] for x in filtered_bd["upazila"]]).values
            ]
            if division != "Bangladesh":
                tmp = filtered_division.index.value_counts()
                tmp = tmp.to_frame()
                tmp["counts"] = tmp["date"]
                tmp["date"] = pd.to_datetime(tmp.index)
                for ind_x, x_val in enumerate(x_axis):
                    sum_of_record = tmp.loc[
                        (
                            (tmp["date"].dt.year.astype(str) == x_val[1:5])
                            & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                        ),
                        "counts",
                    ].sum()
                    z[division][x_val] = sum_of_record

                    annotation_dict = dict(
                        showarrow=False,
                        text="<b>" + str(sum_of_record) + "<b>",
                        xref="x",
                        yref="y",
                        x=x_val,
                        y=division,
                        font=dict(family="sans-serif"),
                    )
                    annotations.append(annotation_dict)

                    if x_val == week and division == region:
                        if not reset:
                            annotation_dict.update(size=15, font=dict(color="#ff6347"))

            if division == "Bangladesh":
                tmp = filtered_bd.index.value_counts()
                tmp = tmp.to_frame()
                tmp["counts"] = tmp["date"]
                tmp["date"] = pd.to_datetime(tmp.index)
                for ind_x, x_val in enumerate(x_axis):
                    sum_of_record = tmp.loc[
                        (
                            (tmp["date"].dt.year.astype(str) == x_val[1:5])
                            & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                        ),
                        "counts",
                    ].sum()
                    z.loc[x_val, division] = sum_of_record

                    annotation_dict = dict(
                        showarrow=False,
                        text="<b>" + str(sum_of_record) + "<b>",
                        xref="x",
                        yref="y",
                        x=x_val,
                        y=division,
                        font=dict(family="sans-serif"),
                    )
                    annotations.append(annotation_dict)

                    if x_val == week and division == region:
                        if not reset:
                            annotation_dict.update(size=15, font=dict(color="#ff6347"))

    ####
    else:  # for divisional numbers
        vDis = []
        if district is None:
            tst = [str(x)[:4] for x in bahis_data["upazila"]]
            tst2 = [i for i in range(len(tst)) if tst[i][:2] == str(division)]
            filtered_bd = bahis_data.iloc[tst2]

            Dislist = bahis_geodata[bahis_geodata["parent"] == division][["value", "name"]]
            Dislist["name"] = Dislist["name"].str.capitalize()
            Dislist = Dislist.rename(columns={"name": "District"})
            Dislist = Dislist.sort_values(by=["District"])
            Dislist = Dislist.to_dict("records")
            vDis = [{"label": i["District"], "value": i["value"]} for i in Dislist]

            if "All Diseases" in disease:
                filtered_bd = filtered_bd
            else:
                filtered_bd = filtered_bd[filtered_bd["top_diagnosis"]== disease] #.isin(disease)]

            # filtered_bd=filtered_bd.sort_values('date').set_index('date').loc[start[0]:end[0]]

            filtered_bd = filtered_bd.sort_values("date").set_index("date").loc[start:end]

            x_axis = find_weeks(start, end)  # [1:] without first week
            x_axis = [str(x) for x in x_axis]

            y_axis_no = list(set([str(x)[:4] for x in filtered_bd["upazila"]]))
            y_axis = y_axis_no.copy()

            for i, value in enumerate(y_axis_no):
                tst = bahis_geodata[bahis_geodata["loc_type"] == 2].loc[
                    bahis_geodata[bahis_geodata["loc_type"] == 2]["value"] == int(value), "name"
                ]
                if not tst.empty:
                    y_axis[i] = tst.values[0].capitalize()

            #            y_axis = [('No ' + str(y)) for y in y_axis ]
            tst = bahis_geodata[bahis_geodata["loc_type"] == 1].loc[
                bahis_geodata[bahis_geodata["loc_type"] == 1]["value"] == int(division), "name"
            ]
            y_axis.append("Σ " + tst.values[0].capitalize())
            y_axis_no.append(int(division))
            #            y_axis.append('No ' + str(division))

            week = ""
            region = ""
            shapes = []  # when selected red rectangle

            if hm_click is not None:
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
            z = pd.DataFrame(index=x_axis, columns=y_axis)
            annotations = []
            for ind_y, district in enumerate(y_axis):  # go through divisions
                filtered_district = filtered_bd[
                    pd.Series([str(x)[:4] == y_axis_no[ind_y] for x in filtered_bd["upazila"]]).values
                ]

                if district[:1] != "Σ":  # for districts
                    tmp = filtered_district.index.value_counts()
                    tmp = tmp.to_frame()
                    tmp["counts"] = tmp["date"]
                    tmp["date"] = pd.to_datetime(tmp.index)
                    for ind_x, x_val in enumerate(x_axis):
                        sum_of_record = tmp.loc[
                            (
                                (tmp["date"].dt.year.astype(str) == x_val[1:5])
                                & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                            ),
                            "counts",
                        ].sum()
                        # dt.groupby([s.year, s.week]).sum()
                        z[district][x_val] = sum_of_record

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

                        # Highlight annotation text by self-click

                        if x_val == week and district == region:
                            if not reset:
                                annotation_dict.update(size=15, font=dict(color="#ff6347"))

                if district[:1] == "Σ":  # for districts
                    #                if district == 'No ' + str(division) :    # for total division
                    tmp = filtered_bd.index.value_counts()
                    tmp = tmp.to_frame()
                    tmp["counts"] = tmp["date"]
                    tmp["date"] = pd.to_datetime(tmp.index)
                    for ind_x, x_val in enumerate(x_axis):
                        sum_of_record = tmp.loc[
                            (
                                (tmp["date"].dt.year.astype(str) == x_val[1:5])
                                & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                            ),
                            "counts",
                        ].sum()
                        #                        z.loc[x_val, 'No ' + str(division)] = sum_of_record
                        z.loc[x_val, district] = sum_of_record

                        annotation_dict = dict(
                            showarrow=False,
                            text="<b>" + str(sum_of_record) + "<b>",
                            xref="x",
                            yref="y",
                            x=x_val,
                            y=district,
                            #                            y= 'No ' + str(division),
                            font=dict(family="sans-serif"),
                        )
                        annotations.append(annotation_dict)

                        if x_val == week and district == region:
                            if not reset:
                                annotation_dict.update(size=15, font=dict(color="#ff6347"))

        else:  # for district numbers
            tst = [str(x)[:6] for x in bahis_data["upazila"]]
            tst2 = [i for i in range(len(tst)) if tst[i][:4] == str(district)]
            filtered_bd = bahis_data.iloc[tst2]

            Dislist = bahis_geodata[bahis_geodata["parent"] == division][["value", "name"]]
            Dislist["name"] = Dislist["name"].str.capitalize()
            Dislist = Dislist.rename(columns={"name": "District"})
            Dislist = Dislist.sort_values(by=["District"])
            Dislist = Dislist.to_dict("records")
            vDis = [{"label": i["District"], "value": i["value"]} for i in Dislist]

            # Upalist=bahis_geodata[bahis_geodata['parent']==district][['value','name']]
            # Upalist['name']=Upalist['name'].str.capitalize()
            # Upalist=Upalist.rename(columns={'name':'Upazila'})
            # Upalist=Upalist.sort_values(by=['Upazila'])
            # Upalist=Upalist.to_dict('records')
            # vUpa = [{'label': i['Upazila'], 'value': i['value']} for i in Upalist]

            if "All Diseases" in disease:
                filtered_bd = filtered_bd
            else:
                filtered_bd = filtered_bd[filtered_bd["top_diagnosis"].isin(disease)]

            # filtered_bd=filtered_bd.sort_values('date').set_index('date').loc[start[0]:end[0]]

            filtered_bd = filtered_bd.sort_values("date").set_index("date").loc[start:end]

            x_axis = find_weeks(start, end)  # [1:] without first week
            x_axis = [str(x) for x in x_axis]

            y_axis_no = list(set([str(x)[:6] for x in filtered_bd["upazila"]]))
            y_axis = y_axis_no.copy()

            for i, value in enumerate(y_axis_no):
                tst = bahis_geodata[bahis_geodata["loc_type"] == 3].loc[
                    bahis_geodata[bahis_geodata["loc_type"] == 3]["value"] == int(value), "name"
                ]
                if not tst.empty:
                    y_axis[i] = tst.values[0].capitalize()

            tst = bahis_geodata[bahis_geodata["loc_type"] == 2].loc[
                bahis_geodata[bahis_geodata["loc_type"] == 2]["value"] == int(district), "name"
            ]
            y_axis.append("Σ " + tst.values[0].capitalize())
            y_axis_no.append(int(district))

            week = ""
            region = ""
            shapes = []  # when selected red rectangle

            if hm_click is not None:
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

            z = pd.DataFrame(index=x_axis, columns=y_axis)
            annotations = []

            for ind_y, upazila in enumerate(y_axis):  # go through divisions
                filtered_upazila = filtered_bd[
                    pd.Series([str(x)[:6] == y_axis_no[ind_y] for x in filtered_bd["upazila"]]).values
                ]

                if upazila[:1] != "Σ":  # for upazila
                    tmp = filtered_upazila.index.value_counts()
                    tmp = tmp.to_frame()
                    tmp["counts"] = tmp["date"]
                    tmp["date"] = pd.to_datetime(tmp.index)

                    for ind_x, x_val in enumerate(x_axis):
                        daysub = 0
                        # weekly defined via isocalendar (starts with Monday)
                        # so does not coincide with bengalian time counts.
                        for weekday in [1, 2, 3, 6, 7]:  # Monday to Sunday skipping Thursday and Friday
                            if pd.Timestamp(
                                date.fromisocalendar(int(x_val[1:5]), int(x_val[6:8]), weekday)
                            ) in pd.to_datetime(tmp["date"]):
                                daysub = daysub + 1

                        z[upazila][x_val] = daysub / 5

                        annotation_dict = dict(
                            showarrow=False,
                            text="<b>" + str(daysub / 5) + "<b>",
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

                if upazila[:1] == "Σ":  # for upazila
                    for ind_x, x_val in enumerate(x_axis):
                        z.loc[x_val, upazila] = sum(z.loc[x_val] == 1) / z.shape[1]  # sum_of_record
                        annotation_dict = dict(
                            showarrow=False,
                            text="<b>" + "{:.2f}".format(sum(z.loc[x_val] == 1) / (z.shape[1] - 1) * 100) + " %<b>",
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

    z = z.fillna(0)
    z = z.T
    z = z.to_numpy()
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
            colorscale=[
                [0, "white"],
                [0.2, "#eeffe3"],
                [0.4, "#ccfcae"],
                [0.6, "#adfc7c"],
                [0.8, "#77fc21"],
                [1, "#62ff00"],
            ],
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
        yaxis=dict(type="category", side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "),
        hovermode="closest",
        showlegend=False,
    )
    return {"data": data, "layout": layout} #, vDis

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row([dbc.Col(ddDivision), dbc.Col(ddDistrict), dbc.Col(ddUpazila)]),
                        dbc.Row(dcc.Graph(id="Map")),
                        dbc.Row(
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
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.DatePickerRange(
                                            id="daterange",
                                            min_date_allowed=start_date,
                                            start_date=date(2023, 1, 1),
                                            max_date_allowed=end_date,
                                            # start_date=date(end_date.year-1, end_date.month, end_date.day),
                                            # initial_visible_month=end_date,
                                            end_date=date(2023, 12, 31)
                                            # end_date=end_date
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            ddDList,
                                            "All Diseases",
                                            id="Diseaselist",
                                            multi=False,
                                            clearable=False,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Tabs(
                                    [
                                        dbc.Tab(
                                            [dbc.Card(dbc.Col([dcc.Graph(id="Completeness")]))],
                                            label="Completeness",
                                            tab_id="CompletenessTab",
                                        ),
                                        dbc.Tab(
                                            [
                                                dbc.Row(dcc.Graph(id="Reports")),
                                                dbc.Row(dcc.Graph(id="Sick")),
                                                dbc.Row(dcc.Graph(id="Dead")),
                                            ],
                                            label="Reports",
                                            tab_id="ReportsTab",
                                        ),
                                        dbc.Tab(
                                            [
                                                dbc.Row(
                                                    dbc.Col([html.Label("Top 10 Diseases"), dcc.Graph(id="Livestock")])
                                                ),
                                                dbc.Row(
                                                    dbc.Col(
                                                        [
                                                            html.Label("Top 10 Zoonotic Diseases"),
                                                            dcc.Graph(id="Zoonotic"),
                                                        ]
                                                    )
                                                ),
                                            ],
                                            label="Diseases",
                                            tab_id="DiseaseTab",
                                        ),
                                        dbc.Tab(
                                            [
                                                dbc.Card(
                                                    dbc.Col(
                                                        [
                                                            dbc.Row(dcc.Graph(id="DRindicators")),
                                                            dbc.Row(dcc.Graph(id="DRRepG1")),
                                                            dbc.Row(
                                                                [
                                                                    html.Label(
                                                                        "Non-Reporting Regions (Please handle with care as geoshape files and geolocations have issues)",
                                                                        id="NRlabel",
                                                                    ),
                                                                    html.Div(id="AlertTable"),
                                                                ]
                                                            ),
                                                        ]
                                                    )
                                                )
                                            ],
                                            label="Reports per Geolocation",
                                            tab_id="GeoRepTab",
                                        ),
                                        dbc.Tab(
                                            [dbc.Card(dbc.Col([dcc.Graph(id="figMonthly")]))],
                                            label="Monthly Comparison",
                                            tab_id="MonthCompTab",
                                        ),
                                        dbc.Tab(
                                            [
                                                dbc.Card(
                                                    dbc.Row(
                                                        [
                                                            html.Label("Export Data", id="ExportLabel"),
                                                            html.Div(id="ExportTab"),
                                                        ]
                                                    )
                                                )
                                            ],
                                            label="Export Data",
                                            tab_id="ExportTab",
                                        ),
                                    ],
                                    id="tabs",
                                )
                            ]
                        ),
                    ],
                    width=8,
                ),
            ]
        )
    ]
)


endtime_start = datetime.now()
print("initialize : " + str(endtime_start - starttime_start))


# shape overlay of selected geotile(s)


@callback(
    # dash cleintsied callback with js
    Output("Division", "value"),
    Output("District", "value"),
    Output("Upazila", "value"),
    Output("Division", "options"),
    Output("District", "options"),
    Output("Upazila", "options"),
    Output("Diseaselist", "options"),
    #    Output ('Map', 'figure'),
    Output("Reports", "figure"),
    Output("Sick", "figure"),
    Output("Dead", "figure"),
    Output("Livestock", "figure"),
    Output("Zoonotic", "figure"),
    Output("DRindicators", "figure"),
    Output("DRRepG1", "figure"),
    Output("NRlabel", "children"),
    Output("AlertTable", "children"),
    #    Output ('GeoDynTable', 'children'),
    Output("figMonthly", "figure"),
    Output("ExportLabel", "children"),
    Output("ExportTab", "children"),
    Output("Completeness", "figure"),
    Output("geoSlider", "value"),


    # Input ('cache_bahis_data', 'data'),
    # Input ('cache_bahis_dgdata', 'data'),
    # Input ('cache_bahis_geodata', 'data'),
    #    Input ('geoSlider', 'value'),
    Input("Map", "clickData"),
    Input("Reports", "clickData"),
    Input("Sick", "clickData"),
    Input("Dead", "clickData"),
    Input("Division", "value"),
    Input("District", "value"),
    Input("Upazila", "value"),
    Input("daterange", "start_date"),  # make state to prevent upate before submitting
    Input("daterange", "end_date"),  # make state to prevent upate before submitting
    Input("Diseaselist", "value"),
    Input("tabs", "active_tab"),
    Input ("Completeness", "clickData"),
    State("geoSlider", "value"),
            
    # Input ('Map', 'clickData'),
)
def update_whatever(
    geoTile, clkRep, clkSick, clkDead, SelDiv, SelDis, SelUpa, start_date, end_date, diseaselist, tabs, Completeness, geoSlider
):
    starttime_general = datetime.now()

    global firstrun, \
        vDiv, \
        vDis, \
        vUpa, \
        ddDList, \
        path, \
        variab, \
        labl, \
        splace, \
        pname, \
        pnumber, \
        loc, \
        title, \
        incsub_bahis_sourcedata, \
        sub_bahis_sourcedata, \
        monthlydatabasis, \
        subDist
    #    print(geoclick)

    # starttime=datetime.now()
    # endtime = datetime.now()
    # print(endtime-starttime)
    # print(clkRep)
    # print(clkSick)
    # print(pd.DataFrame(cbahis_data).shape)
    # print(pd.DataFrame(cbahis_dgdata).shape)
    # print(pd.DataFrame(cbahis_geodata).shape)
    # bahis_data=pd.DataFrame(cbahis_data)
    # bahis_data['date']= pd.to_datetime(bahis_data['date'])
    # bahis_dgdata=pd.DataFrame(cbahis_dgdata)
    # bahis_geodata=pd.DataFrame(cbahis_geodata)

    dates = [start_date, end_date]
    # sub_bahis_sourcedata=bahis_data
    sub_bahis_sourcedata = date_subset(dates, bahis_data)

    NRlabel = "Non-Reporting Regions (Please handle with care as geoshape files and geolocations have issues)"
    if firstrun is True:  # inital settings
        #        dates = sne_date(bahis_data)
        ddDList = fetchdiseaselist(sub_bahis_sourcedata)
        #        ddDList.insert(0, 'All Diseases')
        Divlist = fetchDivisionlist(bahis_geodata)
        vDiv = [{"label": i["Division"], "value": i["value"]} for i in Divlist]
        vDis = []
        vUpa = []
        # figgLiveS=lambda:None
        # figgZoon=[]
        # Rfigg=[]
        # Rfindic=[]
        # figMonthly=[]

        path = path3
        loc = 3
        title = "upazila"
        pnumber = "upazilanumber"
        pname = "upazilaname"
        splace = " Upazila"
        variab = "upazila"
        labl = "Reports per upazila"
        firstrun = False
        # subDist=subDist[subDist['loc_type']==loc]

    #    if ctx.triggered_id=='daterange':
    #        sub_bahis_sourcedata=date_subset(dates, bahis_data)

    if ctx.triggered_id == "Diseaselist":
        sub_bahis_sourcedata = disease_subset(diseaselist, sub_bahis_sourcedata)

    if ctx.triggered_id == "Division":
        if not SelDiv:
            sub_bahis_sourcedata = bahis_data
            subDist = bahis_geodata
            vDis = []
            Dislist = ""
            vUpa = []
            Upalist = []
            SelDis = ""
            SelUpa = ""
        else:
            sub_bahis_sourcedata = bahis_data.loc[bahis_data["division"] == SelDiv]  # DivNo]
            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelDiv))]
            Dislist = fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{"label": i["District"], "value": i["value"]} for i in Dislist]
            vUpa = []
            SelUpa = ""

    if ctx.triggered_id == "District":
        if not SelDis:
            sub_bahis_sourcedata = bahis_data.loc[bahis_data["division"] == SelDiv]  # DivNo]
            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelDiv))]
            Dislist = fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{"label": i["District"], "value": i["value"]} for i in Dislist]
            Upalist = ""
            vUpa = []
            SelUpa = ""
        else:
            sub_bahis_sourcedata = bahis_data.loc[bahis_data["district"] == SelDis]  # DivNo]
            # from basic data in case on switches districts in current way, switching leads to zero data but speed
            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelDis))]
            Upalist = fetchUpazilalist(SelDis, bahis_geodata)
            vUpa = [{"label": i["Upazila"], "value": i["value"]} for i in Upalist]

    if ctx.triggered_id == "Upazila":
        if not SelUpa:
            sub_bahis_sourcedata = bahis_data.loc[bahis_data["district"] == SelDis]  # DivNo]
            # from basic data in case on switches districts in current way, switching leads to zero data but speed
            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelDis))]
        else:
            sub_bahis_sourcedata = bahis_data.loc[bahis_data["upazila"] == SelUpa]
            subDist = bahis_geodata.loc[bahis_geodata["value"].astype("string").str.startswith(str(SelUpa))]

    #    if ctx.triggered_id=='geoSlider':
    if geoSlider == 1:
        path = path1
        loc = geoSlider
        title = "division"
        pnumber = "divnumber"
        pname = "divisionname"
        splace = " Division"
        variab = "division"
        labl = "Reports per division"
        subDistM = subDist[subDist["loc_type"] == geoSlider]
        # subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

    #        bahis_sourcedata = pd.to_numeric(bahis_data['division']).dropna().astype(int)
    # if geoTile is not None:
    #     print(geoTile['points'][0]['location'])
    #     cU2Division=geoTile['points'][0]['location']
    #     Dislist=fetchDistrictlist(geoTile['points'][0]['location'])
    #     vDistrict = [{'label': i['District'], 'value': i['value']} for i in Dislist]
    if geoSlider == 2:
        path = path2
        loc = geoSlider
        title = "district"
        pnumber = "districtnumber"
        pname = "districtname"
        splace = " District"
        variab = "district"
        labl = "Reports per district"
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
        labl = "Reports per upazila"
        subDistM = subDist[subDist["loc_type"] == 3]
        # subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

    #    Rfig = plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl)
    endtime_general = datetime.now()
    print("general callback : " + str(endtime_general - starttime_general))

###tab0

    if tabs == 'CompletenessTab':
        starttime_tab0=datetime.now()
        start = start_date + " 00:00:00"
        end = end_date + " 00:00:00"

        reset = False
            # # Find which one has been triggered
            # ctx = dash.callback_context

            # if ctx.triggered:
            #     prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
            #     if prop_id == "reset-btn":
            #         reset = True
            #     if prop_id == "division-select":
        district=None
            
        a=  generate_reports_heatmap(start, end, SelDiv, SelDis, Completeness, diseaselist, reset
            )
 
        endtime_tab0 = datetime.now()
        print('tabCompleteness : ' + str(endtime_tab0-starttime_tab0))
        return SelDiv, SelDis, SelUpa, vDiv, vDis, vUpa, ddDList, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, a, geoSlider

    # tab1

    if tabs == 'ReportsTab':
        starttime_tab1=datetime.now()

        tmp = sub_bahis_sourcedata["date"].dt.date.value_counts()
        tmp = tmp.to_frame()
        tmp["counts"] = tmp["date"]
        tmp["date"] = pd.to_datetime(tmp.index)
        tmp = tmp["counts"].groupby(tmp["date"].dt.to_period("W-SAT")).sum().astype(int)
        tmp = tmp.to_frame()
        tmp["date"] = tmp.index
        tmp["date"] = tmp["date"].astype("datetime64[D]")

        figgR = px.bar(tmp, x="date", y="counts", labels={"date": "", "counts": "No. of Reports"})
        figgR.update_layout(height=200, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        figgR.update_xaxes(
            range=[
                datetime.strptime(dates[0], "%Y-%m-%d") - timedelta(days=6),
                datetime.strptime(dates[1], "%Y-%m-%d") + timedelta(days=6),
            ]
        )
        figgR.add_annotation(
            x=datetime.strptime(dates[1], "%Y-%m-%d")
            - timedelta(
                days=int(
                    ((datetime.strptime(dates[1], "%Y-%m-%d") - datetime.strptime(dates[0], "%Y-%m-%d")).days) * 0.08
                )
            ),
            y=max(tmp),
            text="total reports " + str("{:,}".format(sub_bahis_sourcedata["date"].dt.date.value_counts().sum())),
            showarrow=False,
            font=dict(family="Courier New, monospace", size=12, color="#ffffff"),
            align="center",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8,
        )

        tmp = (
            sub_bahis_sourcedata[["sick", "dead"]]
            .groupby(sub_bahis_sourcedata["date"].dt.to_period("W-SAT"))
            .sum()
            .astype(int)
        )
        tmp = tmp.reset_index()
        tmp = tmp.rename(columns={"date": "date"})
        tmp["date"] = tmp["date"].astype("datetime64[D]")
        figgSick = px.bar(tmp, x="date", y="sick", labels={"date": "", "sick": "No. of Sick Animals"})
        figgSick.update_layout(height=200, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        figgSick.update_xaxes(
            range=[
                datetime.strptime(dates[0], "%Y-%m-%d") - timedelta(days=6),
                datetime.strptime(dates[1], "%Y-%m-%d") + timedelta(days=6),
            ]
        )  # manual setting should be done better with [start_date,end_date] annotiation is invisible and bar is cut
        figgSick.add_annotation(
            x=datetime.strptime(dates[1], "%Y-%m-%d")
            - timedelta(
                days=int(
                    ((datetime.strptime(dates[1], "%Y-%m-%d") - datetime.strptime(dates[0], "%Y-%m-%d")).days) * 0.08
                )
            ),
            y=max(tmp),
            text="total sick " + str("{:,}".format(int(sub_bahis_sourcedata["sick"].sum()))),  # realy outlyer
            showarrow=False,
            font=dict(family="Courier New, monospace", size=12, color="#ffffff"),
            align="center",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8,
        )

        figgDead = px.bar(tmp, x="date", y="dead", labels={"date": "", "dead": "No. of Dead Animals"})
        figgDead.update_layout(height=200, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        figgDead.update_xaxes(
            range=[
                datetime.strptime(dates[0], "%Y-%m-%d") - timedelta(days=6),
                datetime.strptime(dates[1], "%Y-%m-%d") + timedelta(days=6),
            ]
        )
        figgDead.add_annotation(
            x=datetime.strptime(dates[1], "%Y-%m-%d")
            - timedelta(
                days=int(
                    ((datetime.strptime(dates[1], "%Y-%m-%d") - datetime.strptime(dates[0], "%Y-%m-%d")).days) * 0.08
                )
            ),
            y=max(tmp),
            text="total dead " + str("{:,}".format(int(sub_bahis_sourcedata["dead"].sum()))),  # really
            showarrow=False,
            font=dict(family="Courier New, monospace", size=12, color="#ffffff"),
            align="center",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8,
        )

        endtime_tab1 = datetime.now()
        print("tab1 : " + str(endtime_tab1 - starttime_tab1))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            figgR,
            figgSick,
            figgDead,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            geoSlider
        )

    # tab2

    if tabs == "DiseaseTab":
        starttime_tab2 = datetime.now()

        # preprocess groupdata ?

        poultry = ["Chicken", "Duck", "Goose", "Pegion", "Quail", "Turkey"]
        sub_bahis_sourcedataP = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(poultry)]

        # tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
        # to_replace=tmpdg['name'].tolist()
        # replace_with=tmpdg['Disease type'].tolist()
        sub_bahis_sourcedataP["top_diagnosis"] = sub_bahis_sourcedataP.top_diagnosis.replace(
            to_replace, replace_with, regex=True
        )

        poultryTT = sub_bahis_sourcedataP.drop(
            sub_bahis_sourcedataP[sub_bahis_sourcedataP["top_diagnosis"] == "Zoonotic diseases"].index
        )

        tmp = poultryTT.groupby(["top_diagnosis"])["species"].agg("count").reset_index()

        tmp = tmp.sort_values(by="species", ascending=False)
        tmp = tmp.rename({"species": "counts"}, axis=1)
        tmp = tmp.head(10)
        tmp = tmp.iloc[::-1]
        fpoul = px.bar(tmp, x="counts", y="top_diagnosis", title="Top10 Poultry Diseases")
        fpoul.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        # figg.append_trace(px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases'), row=1, col=1)
        # , labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')

        lanimal = ["Buffalo", "Cattle", "Goat", "Sheep"]
        sub_bahis_sourcedataLA = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(lanimal)]

        # tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
        # to_replace=tmpdg['name'].tolist()
        # replace_with=tmpdg['Disease type'].tolist()
        sub_bahis_sourcedataLA["top_diagnosis"] = sub_bahis_sourcedataLA.top_diagnosis.replace(
            to_replace, replace_with, regex=True
        )
        LATT = sub_bahis_sourcedataLA.drop(
            sub_bahis_sourcedataLA[sub_bahis_sourcedataLA["top_diagnosis"] == "Zoonotic diseases"].index
        )

        tmp = LATT.groupby(["top_diagnosis"])["species"].agg("count").reset_index()

        tmp = tmp.sort_values(by="species", ascending=False)
        tmp = tmp.rename({"species": "counts"}, axis=1)
        tmp = tmp.head(10)
        tmp = tmp.iloc[::-1]
        flani = px.bar(tmp, x="counts", y="top_diagnosis", title="Top10 Large Animal Diseases")
        flani.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        subpl = [fpoul, flani]
        figgLiveS = make_subplots(rows=2, cols=1)
        for i, figure in enumerate(subpl):
            for trace in range(len(figure["data"])):
                figgLiveS.append_trace(figure["data"][trace], row=i + 1, col=1)
        figgLiveS.update_layout(height=350, margin={"r": 0, "t": 0, "l": 0, "b": 0})

        poultry = ["Chicken", "Duck", "Goose", "Pegion", "Quail", "Turkey"]
        sub_bahis_sourcedataP = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(poultry)]

        # tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
        tmpdg = bahis_dgdata[bahis_dgdata["Disease type"] == "Zoonotic diseases"]
        tmpdg = tmpdg["name"].tolist()
        sub_bahis_sourcedataP = sub_bahis_sourcedataP[sub_bahis_sourcedataP["top_diagnosis"].isin(tmpdg)]

        tmp = sub_bahis_sourcedataP.groupby(["top_diagnosis"])["species"].agg("count").reset_index()

        tmp = tmp.sort_values(by="species", ascending=False)
        tmp = tmp.rename({"species": "counts"}, axis=1)
        tmp = tmp.head(10)
        tmp = tmp.iloc[::-1]
        fpoul = px.bar(tmp, x="counts", y="top_diagnosis", title="Top10 Poultry Diseases")
        fpoul.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        lanimal = ["Buffalo", "Cattle", "Goat", "Sheep"]
        sub_bahis_sourcedataLA = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(lanimal)]

        sub_bahis_sourcedataLA = sub_bahis_sourcedataLA[sub_bahis_sourcedataLA["top_diagnosis"].isin(tmpdg)]

        tmp = sub_bahis_sourcedataLA.groupby(["top_diagnosis"])["species"].agg("count").reset_index()

        tmp = tmp.sort_values(by="species", ascending=False)
        tmp = tmp.rename({"species": "counts"}, axis=1)
        tmp = tmp.head(10)
        tmp = tmp.iloc[::-1]
        flani = px.bar(tmp, x="counts", y="top_diagnosis", title="Top10 Ruminant Diseases")
        flani.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        subpl = [fpoul, flani]
        figgZoon = make_subplots(rows=2, cols=1)
        for i, figure in enumerate(subpl):
            for trace in range(len(figure["data"])):
                figgZoon.append_trace(figure["data"][trace], row=i + 1, col=1)
        figgZoon.update_layout(height=150, margin={"r": 0, "t": 0, "l": 0, "b": 0})

        endtime_tab2 = datetime.now()
        print("tab2 : " + str(endtime_tab2 - starttime_tab2))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            no_update,
            no_update,
            no_update,
            figgLiveS,
            figgZoon,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            geoSlider

        )

### tab3 geolocation    # tab3 geolocation
    if tabs == "GeoRepTab":
        starttime_tab3 = datetime.now()

        # geoSlider "if" can be included to accumulate over different resolution

        reports = sub_bahis_sourcedata[title].value_counts().to_frame()

        reports["cases"] = reports[title]
        reports[title] = reports.index
        reports = reports.loc[reports[title] != "nan"]

        for i in range(reports.shape[0]):
            reports[title].iloc[i] = subDistM.loc[subDistM["value"] == int(reports[title].iloc[i]), "name"].iloc[0]

        reports = reports.sort_values(title)
        reports[title] = reports[title].str.capitalize()

        tmp = subDistM[["value", "name"]]
        tmp = tmp.rename(columns={"value": pnumber, "name": pname})
        tmp[pname] = tmp[pname].str.title()
        tmp["Index"] = tmp[pnumber]
        tmp = tmp.set_index("Index")
        aaa = reports.combine_first(tmp)
        aaa[pname] = tmp[pname]
        alerts = aaa[aaa.isna().any(axis=1)]
        alerts = alerts[[pname, pnumber]]
        del tmp
        del aaa

        Rfindic = fIndicator(sub_bahis_sourcedata)
        Rfindic.update_layout(height=100, margin={"r": 0, "t": 30, "l": 0, "b": 0})

        Rfigg = px.bar(reports, x=title, y="cases", labels={variab: labl, "cases": "Reports"})  # ,color='division')
        Rfigg.update_layout(autosize=True, height=200, margin={"r": 0, "t": 0, "l": 0, "b": 0})

        NRlabel = f"Regions with no data in the current database: {len(alerts)} \
            (Please handle with care as geoshape files and geolocations have issues)"

        AlertTable = (
            dash_table.DataTable(
                # columns=[{'upazilaname': i, 'upazilanumber': i} for i in alerts.loc[:,:]], #['Upazila','total']]],
                style_header={
                    "overflow": "hidden",
                    "maxWidth": 0,
                    "fontWeight": "bold",
                },
                style_cell={"textAlign": "left"},
                export_format="csv",
                style_table={"height": "220px", "overflowY": "auto"},
                style_as_list_view=True,
                fixed_rows={"headers": True},
                data=alerts.to_dict("records"),
            ),
        )

        endtime_tab3 = datetime.now()
        print("tab3 : " + str(endtime_tab3 - starttime_tab3))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            Rfindic,
            Rfigg,
            NRlabel,
            AlertTable,
            no_update,
            no_update,
            no_update,
            no_update,
            geoSlider
        )

    # tab 4 geodyn tab per current year

    # removed since Completeness is replacing this tab

    # tab 5 monthly currently not geo resolved and disease, because of bahis_data, either ata is time restricted or

    if tabs == "MonthCompTab":
        starttime_tab5 = datetime.now()

        monthly = bahis_data.groupby(
            [bahis_data["date"].dt.year.rename("year"), bahis_data["date"].dt.month.rename("month")]
        )["date"].agg({"count"})
        monthly = monthly.rename({"count": "reports"}, axis=1)
        monthly = monthly.reset_index()
        monthly["year"] = monthly["year"].astype(str)
        figMonthly = px.bar(
            data_frame=monthly,
            x="month",
            y="reports",
            labels={"month": "Month", "reports": "Reports"},
            color="year",
            barmode="group",
        )
        figMonthly.update_xaxes(dtick="M1", tickformat="%B")

        endtime_tab5 = datetime.now()
        print("tab5 : " + str(endtime_tab5 - starttime_tab5))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            figMonthly,
            no_update,
            no_update,
            no_update,
            geoSlider
        )

    # tab 6 export tab

    if tabs == "ExportTab":
        starttime_tab6 = datetime.now()

        ExportTable = sub_bahis_sourcedata.copy()
        ExportTable["date"] = ExportTable["date"].dt.strftime("%Y-%m-%d")
        del ExportTable["Unnamed: 0.1"]
        ExportTable.drop("species_no", inplace=True, axis=1)
        ExportTable.drop("tentative_diagnosis", inplace=True, axis=1)
        ExportTable.rename(columns={"top_diagnosis": "Diagnosis"}, inplace=True)
        ExportTable = ExportTable.merge(bahis_geodata[["value", "name"]], left_on="division", right_on="value")
        ExportTable["division"] = ExportTable["name"].str.capitalize()
        ExportTable.drop(["name", "value"], inplace=True, axis=1)

        ExportTable = ExportTable.merge(bahis_geodata[["value", "name"]], left_on="district", right_on="value")
        ExportTable["district"] = ExportTable["name"].str.capitalize()
        ExportTable.drop(["name", "value"], inplace=True, axis=1)

        ExportTable = ExportTable.merge(bahis_geodata[["value", "name"]], left_on="upazila", right_on="value")
        ExportTable["upazila"] = ExportTable["name"].str.capitalize()
        ExportTable.drop(["name", "value"], inplace=True, axis=1)

        ExportLabel = "Export Data Size: " + str(ExportTable.shape)

        ExportTab = (
            dash_table.DataTable(
                style_header={
                    #                                        'overflow': 'hidden',
                    #                                        'maxWidth': 0,
                    "fontWeight": "bold",
                },
                style_cell={"textAlign": "left"},
                export_format="csv",
                style_table={"height": "500px", "overflowY": "auto"},
                #                                style_as_list_view=True,
                #                                fixed_rows={'headers': True},
                data=ExportTable.to_dict("records"),
                columns=[{"name": i, "id": i} for i in ExportTable.columns],
            ),
        )

        endtime_tab6 = datetime.now()
        print("tab6 : " + str(endtime_tab6 - starttime_tab6))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            ExportLabel,
            ExportTab,
            no_update,
            geoSlider
        )


@callback(
    Output("Map", "figure"),
    #    Output ('geoSlider', 'value'),
    Input("geoSlider", "value"),
    State("Division", "value"),
    State("District", "value"),
    State("Upazila", "value"),
    prevent_initial_call=True,
)
def export(geoSlider, Division, District, Upazila):
    #    if ctx.triggered_id=='geoSlider':
    if geoSlider == 1:
        if not Division:
            path = path1
            loc = geoSlider
            title = "division"
            pnumber = "divnumber"
            pname = "divisionname"
            splace = " Division"
            variab = "division"
            labl = "Reports per division"
            subDistM = subDist[subDist["loc_type"] == geoSlider]
        else:
            path = path1
            loc = geoSlider
            title = "division"
            pnumber = "divnumber"
            pname = "divisionname"
            splace = " Division"
            variab = "division"
            labl = "Reports per division"
            subDistM = subDist[subDist["loc_type"] == geoSlider]
    if geoSlider == 2:
        if not District:
            path = path2
            loc = geoSlider
            title = "district"
            pnumber = "districtnumber"
            pname = "districtname"
            splace = " District"
            variab = "district"
            labl = "Reports per district"
            subDistM = subDist[subDist["loc_type"] == geoSlider]
        else:
            geoSlider = 3

    if geoSlider == 3:
        path = path3
        loc = geoSlider
        title = "upazila"
        pnumber = "upazilanumber"
        pname = "upazilaname"
        splace = " Upazila"
        variab = "upazila"
        labl = "Reports per upazila"
        subDistM = subDist[subDist["loc_type"] == geoSlider]

    Rfig = plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl)
    return Rfig  # , geoSlider


# make callback for tabs

