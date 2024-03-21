import os
from datetime import datetime

import numpy as np
import pandas as pd


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
    bahis_data = bahis_data[bahis_data["date"] >= datetime(2019, 7, 1)]
    # limit to static bahis start
    return bahis_data


def fetchfarmdata(farmfilename):
    tmp = pd.read_csv(farmfilename)
    farm_data = tmp[
        [
            "id",
            "basic_info_date",
            "basic_info_division",
            "basic_info_district",
            "basic_info_upazila",
            "biosecurity_practices_outsider_vehicles_entry",
            "biosecurity_practices_workers_approve_visitor_entry",
            "biosecurity_practices_manure_collector_entry",
            "biosecurity_practices_fenced_and_duck_chicken_proof",
            "biosecurity_practices_dead_birds_disposed_safely",
            "biosecurity_practices_sign_posted_1st",
            "biosecurity_practices_vehical_movement_production_area",
            "biosecurity_practices_workers_entry_production_area",
            "biosecurity_practices_visitors_approved_production_area",
            "biosecurity_practices_sign_posted_2nd",
            "biosecurity_practices_footwear_left_outside",
            "biosecurity_practices_change_clothes_upon_entering_farm",
            "biosecurity_practices_use_dedicated_footwear",
            "biosecurity_practices_shower_before_enter_farm",
            "biosecurity_practices_materials_cleaned",
            "biosecurity_practices_materials_disinfect",
            "g1_product1",
            "g2_product2",
            "g3_product3",
            "g4_product4",
            "g5_product5",
            "g1_product1_generic1",
            "g1_product1_generic2",
            "g1_product1_generic3",
            "g1_product1_generic4",
            "g2_product2_generic1",
            "g2_product2_generic2",
            "g2_product2_generic3",
            "g2_product2_generic4",
            "g3_product3_generic1",
            "g3_product3_generic2",
            "g3_product3_generic3",
            "g3_product3_generic4",
            "g4_product4_generic1",
            "g4_product4_generic2",
            "g4_product4_generic3",
            "g4_product4_generic4",
            "g5_product5_generic1",
            "g5_product5_generic2",
            "g5_product5_generic3",
            "g5_product5_generic4",
        ]
    ]
    farm_data = farm_data.rename(
        columns={
            "basic_info_date": "date",
            "basic_info_division": "division",
            "basic_info_district": "district",
            "basic_info_upazila": "upazila",
            "biosecurity_practices_outsider_vehicles_entry": "outsider_vehicles_entry",
            "biosecurity_practices_workers_approve_visitor_entry": "workers_approve_visitor_entry",
            "biosecurity_practices_manure_collector_entry": "manure_collector_entry",
            "biosecurity_practices_fenced_and_duck_chicken_proof": "fenced_and_duck_chicken_proof",
            "biosecurity_practices_dead_birds_disposed_safely": "dead_birds_disposed_safely",
            "biosecurity_practices_sign_posted_1st": "sign_posted_1st",
            "biosecurity_practices_vehical_movement_production_area": "vehical_movement_production_area",
            "biosecurity_practices_workers_entry_production_area": "workers_entry_production_area",
            "biosecurity_practices_visitors_approved_production_area": "visitors_approved_production_area",
            "biosecurity_practices_sign_posted_2nd": "sign_posted_2nd",
            "biosecurity_practices_footwear_left_outside": "footwear_left_outside",
            "biosecurity_practices_change_clothes_upon_entering_farm": "change_clothes_upon_entering_farm",
            "biosecurity_practices_use_dedicated_footwear": "use_dedicated_footwear",
            "biosecurity_practices_shower_before_enter_farm": "shower_before_enter_farm",
            "biosecurity_practices_materials_cleaned": "materials_cleaned",
            "biosecurity_practices_materials_disinfect": "materials_disinfect",
            "g1_product1": "g1",
            "g2_product2": "g2",
            "g3_product3": "g3",
            "g4_product4": "g4",
            "g5_product5": "g5",
            "g1_product1_generic1": "g1g1",
            "g1_product1_generic2": "g1g2",
            "g1_product1_generic3": "g1g3",
            "g1_product1_generic4": "g1g4",
            "g2_product2_generic1": "g2g1",
            "g2_product2_generic2": "g2g2",
            "g2_product2_generic3": "g2g3",
            "g2_product2_generic4": "g2g4",
            "g3_product3_generic1": "g3g1",
            "g3_product3_generic2": "g3g2",
            "g3_product3_generic3": "g3g3",
            "g3_product3_generic4": "g3g4",
            "g4_product4_generic1": "g4g1",
            "g4_product4_generic2": "g4g2",
            "g4_product4_generic3": "g4g3",
            "g4_product4_generic4": "g4g4",
            "g5_product5_generic1": "g5g1",
            "g5_product5_generic2": "g5g2",
            "g5_product5_generic3": "g5g3",
            "g5_product5_generic4": "g5g4",
        }
    )
    farm_data["date"] = pd.to_datetime(farm_data["date"], errors="coerce")
    farm_data["date"] = pd.to_datetime(farm_data.date).dt.tz_localize(None)
    return farm_data


def fetchAIinvestdata(AIinvestdatafilename):
    tmp = pd.read_csv(AIinvestdatafilename)
    AIinvestdata = tmp[
        [
            "id",
            "basic_info_date",
            "basic_info_division",
            "basic_info_district",
            "basic_info_upazila",
        ]
    ]
    AIinvestdata = AIinvestdata.rename(
        columns={
            "basic_info_date": "date",
            "basic_info_division": "division",
            "basic_info_district": "district",
            "basic_info_upazila": "upazila",
        }
    )
    AIinvestdata["date"] = pd.to_datetime(AIinvestdata["date"], errors="coerce")
    AIinvestdata["date"] = pd.to_datetime(AIinvestdata.date).dt.tz_localize(None)
    AIinvestdata["date"] = pd.to_datetime(AIinvestdata["date"])
    AIinvestdata["date"] = AIinvestdata["date"].dt.strftime("%Y-%m-%d")
    AIinvestdata["date"] = pd.to_datetime(AIinvestdata["date"])
    return AIinvestdata


def fetchDiseaseInvestdata(DiseaseInvestdatafilename):
    tmp = pd.read_csv(DiseaseInvestdatafilename)
    DiseaseInvestdata = tmp[
        [
            "id",
            "basic_info_date",
            "basic_info_division",
            "basic_info_district",
            "basic_info_upazila",
        ]
    ]
    DiseaseInvestdata = DiseaseInvestdata.rename(
        columns={
            "basic_info_date": "date",
            "basic_info_division": "division",
            "basic_info_district": "district",
            "basic_info_upazila": "upazila",
        }
    )
    DiseaseInvestdata["date"] = pd.to_datetime(DiseaseInvestdata["date"], errors="coerce")
    DiseaseInvestdata["date"] = pd.to_datetime(DiseaseInvestdata.date).dt.tz_localize(None)
    return DiseaseInvestdata


def fetchPartLSAssdata(PartLSAssisdatafilename):
    tmp = pd.read_csv(PartLSAssisdatafilename)
    LSAssisdata = tmp[
        [
            "id",
            "basic_info_date",
            "basic_info_division",
            "basic_info_district",
            "basic_info_upazila",
        ]
    ]
    LSAssisdata = LSAssisdata.rename(
        columns={
            "basic_info_date": "date",
            "basic_info_division": "division",
            "basic_info_district": "district",
            "basic_info_upazila": "upazila",
        }
    )
    LSAssisdata["date"] = pd.to_datetime(LSAssisdata["date"], errors="coerce")
    LSAssisdata["date"] = pd.to_datetime(LSAssisdata.date).dt.tz_localize(None)
    return LSAssisdata


def fetchmedsdata(medsfilename):
    tmp = pd.read_csv(medsfilename)
    tmp = tmp.drop_duplicates(subset=["product_id"]).sort_values(by=["product_id"])
    medsdata = tmp[
        [
            "product_id",
            "product_label",
            "generic1",
            "generic1_label",
            "generic2",
            "generic2_label",
            "generic3",
            "generic3_label",
            "generic4",
            "generic4_label",
            "treatment_type",
            "generic1_importance_category",
            "generic1_importance_generic",
            "generic1_aware_category",
            "generic1_aware_class",
        ]
    ]
    medsdata = medsdata.rename(
        columns={
            "product_id": "id",
            "product_label": "label",
            "generic1": "g1",
            "generic1_label": "g1label",
            "generic2": "g2",
            "generic2_label": "g2label",
            "generic3": "g3",
            "generic3_label": "g3label",
            "generic4": "g4",
            "generic4_label": "g4label",
            "treatment_type": "treattype",
            "generic1_importance_category": "importance_category",
            "generic1_importance_generic": "importance_gen",
            "generic1_aware_category": "aware",
            "generic1_aware_class": "aware_class",
        }
    )
    return medsdata


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


def fetchGeoName(bahis_geodata, geonumber):  # to be done
    geoname = ""
    if len(str(geonumber)) == 2:
        geoname = bahis_geodata[(bahis_geodata["loc_type"] == 1) & (bahis_geodata["division"] == geonumber)]
        [["value", "name"]]
        print(geonumber)
        print(geoname)
    if len(str(geonumber)) == 4:
        geoname = bahis_geodata[(bahis_geodata["loc_type"] == 2) & (bahis_geodata["district"] == geonumber)]
        [["value", "name"]]
    if len(str(geonumber)) == 6:
        geoname = bahis_geodata[(bahis_geodata["loc_type"] == 3) & (bahis_geodata["upazila"] == geonumber)]
        [["value", "name"]]

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
