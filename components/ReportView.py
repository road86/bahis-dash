import plotly.express as px
import pandas as pd

def Reports(sub_bahis_sourcedata, dates):

    periodClick=1
    tmp = sub_bahis_sourcedata["date"].dt.date.value_counts()
    tmp = tmp.to_frame()
    tmp["counts"] = tmp["date"]
    tmp["date"] = pd.to_datetime(tmp.index)
    if periodClick== 3:
        tmp=tmp['counts'].groupby(tmp['date']).sum().astype(int)
    if periodClick== 2:
        tmp=tmp['counts'].groupby(tmp['date'].dt.to_period('W-SAT')).sum().astype(int)
    if periodClick== 1:
        tmp=tmp['counts'].groupby(tmp['date'].dt.to_period('M')).sum().astype(int)
    tmp = tmp.to_frame()
    tmp["date"] = tmp.index
    tmp["date"] = tmp["date"].astype("datetime64[D]")

    fig1 = px.bar(tmp, x="date", y="counts", labels={"date": "", "counts": "No. of Reports"})
    
    df = px.data.gapminder()
    print(df)
    fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
            size="pop", color="continent", hover_name="country",
            log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

    fig["layout"].pop("updatemenus") # optional, drop animation buttons
#    fig.show()
    return fig1