import plotly.express as px
from plotly.subplots import make_subplots


def TopTen(sub_bahis_sourcedata, bahis_dgdata, distype, to_replace, replace_with):

    poultry = ["Chicken", "Duck", "Goose", "Pegion", "Quail", "Turkey"]
    sub_bahis_sourcedataP = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(poultry)]
    sub_bahis_sourcedataP["top_diagnosis"] = sub_bahis_sourcedataP.top_diagnosis.replace(
        to_replace, replace_with, regex=True
        )
    tmp = sub_bahis_sourcedataP.groupby(["top_diagnosis"])["species"].agg("count").reset_index()
    tmp = tmp.sort_values(by="species", ascending=False)
    tmp = tmp.rename({"species": "counts"}, axis=1)
    tmp = tmp.head(10)
    tmp = tmp.iloc[::-1]
    fpoul = px.bar(tmp, x="counts", y="top_diagnosis", labels={"counts": "Counts", "top_diagnosis": ""}, title="")
    fpoul.update_layout(height=250, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    lanimal = ["Buffalo", "Cattle", "Goat", "Sheep"]
    sub_bahis_sourcedataLA = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(lanimal)]
    sub_bahis_sourcedataLA["top_diagnosis"] = sub_bahis_sourcedataLA.top_diagnosis.replace(
        to_replace, replace_with, regex=True
        )
    tmp = sub_bahis_sourcedataLA.groupby(["top_diagnosis"])["species"].agg("count").reset_index()
    tmp = tmp.sort_values(by="species", ascending=False)
    tmp = tmp.rename({"species": "counts"}, axis=1)
    tmp['counts'] = tmp['counts'] / 1000
    tmp = tmp.head(10)
    tmp = tmp.iloc[::-1]
    flani = px.bar(tmp, x="counts", y="top_diagnosis", labels={"counts": "Counts in Thousands", "top_diagnosis": ""}, title="")
    flani.update_layout(height=250, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    tmpdg = bahis_dgdata[bahis_dgdata["Disease type"] == distype]
    selected_diseases = tmpdg['name'].tolist()
    sub_bahis_sourcedata = sub_bahis_sourcedata[sub_bahis_sourcedata["top_diagnosis"].isin(selected_diseases)]
    tmp = sub_bahis_sourcedata.groupby(["top_diagnosis"])['species'].agg("count").reset_index()
    tmp = tmp.sort_values(by="species", ascending=False)
    tmp = tmp.rename({"species": "counts"}, axis=1)
    tmp = tmp.head(10)
    tmp = tmp.iloc[::-1]
    figDisTyp = px.bar(tmp, x="counts", y="top_diagnosis", labels={"counts": "Counts", "top_diagnosis": ""}, title="")
    figDisTyp.update_layout(height=200, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return flani, fpoul, figDisTyp
