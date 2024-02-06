import glob
import os


def get_pathnames(sourcepath):
    # 1 Nation # reminder: found shapefiles from the data.humdata.org

    geofilename = glob.glob(sourcepath + "newbahis_geo_cluster*.csv")[
        -1
    ]  # the available geodata from the bahis project (Masterdata)
    dgfilename = os.path.join(sourcepath, "Diseaselist.csv")  # disease grouping info (Masterdata)
    sourcefilename = os.path.join(
        sourcepath, "preped_data2.csv"
    )  # main data resource of prepared data from old and new bahis
    farmdatafilename = glob.glob(sourcepath + "bahis_farm_assessment_p2_table*.csv")[-1]

    path1 = os.path.join(sourcepath, "processed_geodata", "divdata.geojson")  # 8 Division
    path2 = os.path.join(sourcepath, "processed_geodata", "distdata.geojson")  # 64 District
    path3 = os.path.join(sourcepath, "processed_geodata", "upadata.geojson")  # 495 Upazila
    return geofilename, dgfilename, sourcefilename, farmdatafilename, path1, path2, path3
