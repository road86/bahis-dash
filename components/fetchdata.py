import numpy as np
import pandas as pd
import os
from datetime import datetime


def fetchsourcedata(sourcefilename):  # fetch and prepare source data
    bahis_data = pd.read_csv(sourcefilename)
    bahis_data["from_static_bahis"] = bahis_data["basic_info_date"].str.contains(
        "/"
    )  # new data contains -, old data contains /
    bahis_data["basic_info_date"] = pd.to_datetime(bahis_data["basic_info_date"], errors="coerce")
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
    bahis_data = bahis_data[bahis_data['date'] >= datetime(2019, 7, 1)]
    # limit to static bahis start
    return bahis_data


def fetchgeodata(geofilename):  # fetch geodata from bahis, delete mouzas and unions
    geodata = pd.read_csv(geofilename)
    geodata = geodata.drop(
        geodata[(geodata["loc_type"] == 4) | (geodata["loc_type"] == 5)].index
    )  # drop mouzas and unions
    geodata = geodata.drop(["id", "longitude", "latitude", "updated_at"], axis=1)
    geodata["parent"] = geodata[["parent"]].astype(np.uint16)  # assuming no mouza and union is taken into
    geodata[["value"]] = geodata[["value"]].astype(np.uint32)
    geodata[["loc_type"]] = geodata[["loc_type"]].astype(np.uint8)
    return geodata


def sne_date(bahis_data):
    start_date = min(bahis_data["date"]).date()
    end_date = max(bahis_data["date"]).date()
    dates = [start_date, end_date]
    return dates


def create_date(sourcefilename):
    create_time = os.path.getmtime(sourcefilename)
    create_date = datetime.fromtimestamp(create_time).date()
    return create_date


def fetchdisgroupdata(dgfilename):  # fetch and prepare disease groups
    bahis_dgdata = pd.read_csv(dgfilename)
    # bahis_dgdata= bahis_dgdata[['species', 'name', 'id', 'Disease type']]
    # remark what might be helpful: reminder: memory size
    bahis_dgdata = bahis_dgdata[["name", "Disease type"]]
    bahis_dgdata = bahis_dgdata.dropna()
    # bahis_dgdata[['name', 'Disease type']] = str(bahis_dgdata[['name', 'Disease type']])
    # can you change object to string and does it make a memory difference?
    bahis_dgdata = bahis_dgdata.drop_duplicates(subset="name", keep="first")
    bahis_distype = bahis_dgdata.drop_duplicates(subset="Disease type", keep="first")
    return bahis_dgdata, bahis_distype


def fetchGeoName(bahis_geodata, geonumber):  #  #######to be done
    geoname=""
    if len(str(geonumber)) == 2:
        geoname = bahis_geodata[(bahis_geodata["loc_type"] == 1) & (bahis_geodata["division"] == geonumber)][["value", "name"]]
        print(geonumber)
        print(geoname)
    if len(str(geonumber)) == 4:
        geoname = bahis_geodata[(bahis_geodata["loc_type"] == 2) & (bahis_geodata["district"] == geonumber)][["value", "name"]]
    if len(str(geonumber)) == 6:
        geoname = bahis_geodata[(bahis_geodata["loc_type"] == 3) & (bahis_geodata["upazila"] == geonumber)][["value", "name"]]

    return geoname


def fetchDivisionlist(bahis_geodata):  # division list is always the same, caching possible
    Divlist = bahis_geodata[(bahis_geodata["loc_type"] == 1)][["value", "name"]]
    Divlist["name"] = Divlist["name"].str.capitalize()
    Divlist = Divlist.rename(columns={"name": "Division"})
    Divlist = Divlist.sort_values(by=["Division"])
    return Divlist.to_dict("records")


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


def fetchDiseaselist(bahis_data):
    dislis = bahis_data["top_diagnosis"].unique()
    dislis = pd.DataFrame(dislis, columns=["Disease"])
    dislis = dislis["Disease"].sort_values().tolist()
    dislis.insert(0, "All Diseases")
    return dislis


def date_subset(dates, bahis_data):
    tmask = (bahis_data["date"] >= pd.to_datetime(dates[0])) & (bahis_data["date"] <= pd.to_datetime(dates[1]))
    return bahis_data.loc[tmask]


def disease_subset(cDisease, sub_bahis_sourcedata):
    if "All Diseases" in cDisease:
        sub_bahis_sourcedata = sub_bahis_sourcedata
    else:
        sub_bahis_sourcedata = sub_bahis_sourcedata[sub_bahis_sourcedata["top_diagnosis"] == cDisease]
    return sub_bahis_sourcedata
