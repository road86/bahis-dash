import plotly.express as px


def yearlyComp(bahis_data):
    monthly = bahis_data.groupby(
        [bahis_data["date"].dt.year.rename("year"), bahis_data["date"].dt.month.rename("month")])["date"].agg({"count"})
    monthly = monthly.rename({"count": "reports"}, axis=1)
    monthly = monthly.reset_index()
    monthly["year"] = monthly["year"].astype(str)
    figYearlyComp = px.bar(
        data_frame=monthly,
        x="month",
        y="reports",
        labels={"month": "", "reports": "Reports"},
        color="year",
        barmode="group",
    )
    figYearlyComp.update_xaxes(dtick="M1", tickformat="%b\n%Y")
    return figYearlyComp
