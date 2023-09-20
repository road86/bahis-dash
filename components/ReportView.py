import plotly.express as px

def Reports(df, dates):
    tmp = sub_bahis_sourcedata["date"].dt.date.value_counts()
    tmp = tmp.to_frame()
    tmp["counts"] = tmp["date"]
    tmp["date"] = pd.to_datetime(tmp.index)
    tmp = tmp["counts"].groupby(tmp["date"].dt.to_period("W-SAT")).sum().astype(int)
    tmp = tmp.to_frame()
    tmp["date"] = tmp.index
    tmp["date"] = tmp["date"].astype("datetime64[D]")
    fig = px.bar(tmp, x="date", y="counts", labels={"date": "", "counts": "No. of Reports"})
    
    print(df)
    df = px.data.gapminder()
    fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
            size="pop", color="continent", hover_name="country",
            log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

    fig["layout"].pop("updatemenus") # optional, drop animation buttons
#    fig.show()
    return fig