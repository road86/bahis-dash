import plotly.express as px


def yearlyComp(bahis_data):
    monthly = bahis_data.groupby(
        [bahis_data["date"].dt.year.rename("Year"), bahis_data["date"].dt.month.rename("Month")]
    )["date"].agg({"count"})
    monthly = monthly.rename({"count": "reports"}, axis=1)
    monthly = monthly.reset_index()
    monthly['reports'] = monthly['reports'] / 1000
    monthly["Year"] = monthly["Year"].astype(str)
    figYearlyComp = px.bar(
        data_frame=monthly,
        x="Month",
        y="reports",
        labels={"Month": "Month", "reports": "Reports in Thousands"},
        color="Year",
        barmode="group",
    )
    figYearlyComp.update_xaxes(dtick="M1")  # , tickformat="%B \n%Y")
    figYearlyComp.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext=['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        )
    )
    return figYearlyComp
