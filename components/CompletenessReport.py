from datetime import date, datetime, timedelta
import pandas as pd


def find_weeks(start, end):
    list_of_weeks = []
    days_to_thursday = (3 - start.weekday()) % 7
    for i in range((end - start).days + 1):
        d = (start + timedelta(days=i)).isocalendar()[:2]  # e.g. (2011, 52)
        yearweek = "y{}w{:02}".format(*d)  # e.g. "201152"
        list_of_weeks.append(yearweek)
    return sorted(set(list_of_weeks))


def generate_reports_heatmap(bahis_data, bahis_geodata, start, end, division, district, Completeness, disease, reset):
    """
    :param: start: start date from selection.
    :param: end: end date from selection.
    :param: clinic: clinic from selection.
    :param: Completeness: clickData from heatmap.
    :param: admit_type: admission type from selection.
    :param: reset (boolean): reset heatmap graph if True.

    :return: Patient volume annotated heatmap.
    """
    start = datetime.strptime(str(start), "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(str(end), "%Y-%m-%d %H:%M:%S")
    compcols = False

    if division is None:  # for national numbers
        # vDis = []
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
            filtered_bd = filtered_bd[filtered_bd["top_diagnosis"] == disease]

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

        if Completeness is not None:
            week = Completeness["points"][0]["x"]
            region = Completeness["points"][0]["y"]
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
        # vDis = []
        if district is None:
            tst = [str(x)[:4] for x in bahis_data["upazila"]]
            tst2 = [i for i in range(len(tst)) if tst[i][:2] == str(division)]
            filtered_bd = bahis_data.iloc[tst2]

            Dislist = bahis_geodata[bahis_geodata["parent"] == division][["value", "name"]]
            Dislist["name"] = Dislist["name"].str.capitalize()
            Dislist = Dislist.rename(columns={"name": "District"})
            Dislist = Dislist.sort_values(by=["District"])
            Dislist = Dislist.to_dict("records")
            # vDis = [{"label": i["District"], "value": i["value"]} for i in Dislist]

            if "All Diseases" in disease:
                filtered_bd = filtered_bd
            else:
                filtered_bd = filtered_bd[filtered_bd["top_diagnosis"] == disease]

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

            if Completeness is not None:
                week = Completeness["points"][0]["x"]
                region = Completeness["points"][0]["y"]
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
            # vDis = [{"label": i["District"], "value": i["value"]} for i in Dislist]

            # Upalist=bahis_geodata[bahis_geodata['parent']==district][['value','name']]
            # Upalist['name']=Upalist['name'].str.capitalize()
            # Upalist=Upalist.rename(columns={'name':'Upazila'})
            # Upalist=Upalist.sort_values(by=['Upazila'])
            # Upalist=Upalist.to_dict('records')
            # vUpa = [{'label': i['Upazila'], 'value': i['value']} for i in Upalist]

            if "All Diseases" in disease:
                filtered_bd = filtered_bd
            else:
                filtered_bd = filtered_bd[filtered_bd["top_diagnosis"] == disease]

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

            if Completeness is not None:
                week = Completeness["points"][0]["x"]
                region = Completeness["points"][0]["y"]
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
                    compcols = True
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
                            # text="<b>" + "{:.0f}".format(sum(z.loc[x_val] == 1) / (z.shape[1] - 1) * 100) + " %<b>",
                            # z_text="<b>" + "{:.0f}".format(sum(z.loc[x_val] == 1) / (z.shape[1] - 1) * 100) + " %<b>",
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
                        print(z[upazila])
                        z.loc[x_val, upazila] = sum(z.loc[x_val]) / z.shape[1]  # sum_of_record
                        annotation_dict = dict(
                            showarrow=False,
                            text="<b>" + "{:.0f}".format(sum(z.loc[x_val] == 1) / (z.shape[1] - 1) * 100) + " %<b>",
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

    if compcols:
        compcol = [
            [0, "red"],
            [0.2, "#d7301f"],
            [0.4, "#fc8d59"],
            [0.6, "#fdcc8a"],
            [0.8, "#fef0d9"],
            [1, "#b8e186"]
        ]
    else:
        compcol = [
            [0, "white"],
            [0.2, "white"],
            [0.4, "white"],
            [0.6, "white"],
            [0.8, "white"],
            [1, "white"]
        ]

    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale=compcol,
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
    return {"data": data, "layout": layout}  # , vDis
