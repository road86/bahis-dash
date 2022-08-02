Status 220802:
Win11, python 3.9.7 64-bit

-	Download data from:
	EPI integration > old BAHIS data (form 30 April) > output
	https://drive.google.com/drive/folders/14oJ1L9fffLYVFuzRH4VI0A-IMNOPr3uN

-	Extract zip to main path

- conda env create -f bahisDashEnv.yml

- (if you are using spyder, there is an error message, which can be ignored: https://github.com/spyder-ide/spyder/issues/15387)

- download and copy into output folder: 
	STATICBAHIS_geo_cluster_202204301723.csv
	AWaReclass.csv
	Antibiotics.csv


- known problems, 
	path to pngs somehow without C:/ (ine 81 (working) vs 86-88 (non-working)
	loading times very long, smaller geojson to be implemented
	graphs of measures not nice