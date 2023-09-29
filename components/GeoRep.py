from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from dash import dash_table


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


def GeoRep(sub_bahis_sourcedata, title, subDistM, pnumber, pname, variab, labl):
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
    return Rfindic, Rfigg, NRlabel, AlertTable
