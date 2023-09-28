import plotly.express as px
from plotly.subplots import make_subplots


def TopTen(sub_bahis_sourcedata, bahis_dgdata, to_replace, replace_with):
    poultry = ["Chicken", "Duck", "Goose", "Pegion", "Quail", "Turkey"]
    sub_bahis_sourcedataP = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(poultry)]

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

    return flani, fpoul, figgZoon
