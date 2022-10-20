Update 221020_ Version 4:
- clone repo:
https://github.com/road86/bahis-dash/tree/main/Version1checked

++++++++++++ list of necessary files +++++++++
bahis_dash_V4.py
bahisDashEnv2.yml
readme.txt
/logos/Logo.png
/geodata/*
++++++++ further data see next topic ++++++++++

- Download data from server(?) 
	https://drive.google.com/drive/folders/1YI7q_OAlvSp-vWaBuwQUWWX-0HO6yNwj?usp=sharing
- Extract data to following folder
	/exported data/

+++++++++ list of necessary files from this folder +++++++++
newbahis_geo_cluster.csv
newbahis_bahis_patient_registrydyncsv_live_table.csv
++++++++ end of list in "exported data" folder +++++++++++++

- "conda env create -f bahisDashEnv.yml", does not work on linux yet

- adjust "basepath=" variable on line 22 in bahis_dash_V4.py to project folder

- change to folder where bahis_dash_V4.py is stored

- "streamlit run bahis_dash_V4.py"



Status 221018:
same environment, new Version 3
- environment same
- the exported new data from the new server needs to be put into a folder named "exported data"



Status 220802: Win11, python 3.9.7 64-bit


- "conda env create -f bahisDashEnv.yml"

- "conda activate bahisDash1"

- clone repo:
https://github.com/road86/bahis-dash/tree/main/Version1checked

-	Download data from:
	EPI integration > old BAHIS data (form 30 April) > output
	https://drive.google.com/drive/folders/14oJ1L9fffLYVFuzRH4VI0A-IMNOPr3uN

-	Extract zip to main path (there is an output folder, where these files need to be added)

- adjust "basepath = " on line 17 in bahis_dash_V1.py

- neglect or comment out or adjust logo paths on line 73 (would apply for line 78-80 too, but they are left in a way one can see the comparison.

- change to folder where bahis_dash_V1.py is stored

- "streamlit run bahis_dash_V1.py"



#########
comments:
- if you are using spyder, there is an error message, which can be ignored: https://github.com/spyder-ide/spyder/issues/15387

- for newest files, download and copy into output folder: 
	STATICBAHIS_geo_cluster_202204301723.csv
	AWaReclass.csv
	Antibiotics.csv		Done with repo


#########
known problems, 
	
-	path to pngs somehow without C:/ (ine 81 (working) vs 86-88 (non-working)
-	graphs of measures not nice
