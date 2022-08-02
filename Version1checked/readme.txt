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

- download and copy into output folder: 
	STATICBAHIS_geo_cluster_202204301723.csv
	AWaReclass.csv
	Antibiotics.csv		Done with repo


#########
known problems, 
	
-	path to pngs somehow without C:/ (ine 81 (working) vs 86-88 (non-working)
-	graphs of measures not nice