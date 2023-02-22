import pandas as pd
import datetime as dt
import json, os

sourcepath = 'exported_data/'
sourcefilename = os.path.join(sourcepath, 'newbahis_bahis_patient_registrydyncsv_live_table.csv')
bahis_sourcedata = pd.read_csv(sourcefilename, low_memory=False)

oldsourcefilename = os.path.join(sourcepath, 'formdata_Patients_Registry.csv')
oldbahis_sourcedata = pd.read_csv(oldsourcefilename, low_memory=False)
###


oldbahis_preped_data = oldbahis_sourcedata[['date',
                                        'division',
                                        'district',
                                        'upazila',
                                        'species',
                                        'tentative_diagnosis',
                                        'sick_number',
                                        'dead_number']]

# add speices
anim_names=pd.read_csv(os.path.join(sourcepath, 'staticbahis_fao_species.csv'))
anim_names2 = anim_names.set_index('code')['species_name_en'].drop_duplicates().astype(str)

adict = dict(anim_names2[~anim_names2.index.duplicated(keep='first')])
adict[-1]='Unknown'

oldbahis_preped_data['species'] = oldbahis_preped_data['species'].fillna('-1')
oldbahis_preped_data['patient_info_species'] = oldbahis_preped_data['species']
oldbahis_preped_data['species'] = oldbahis_preped_data['species'].astype(int)
oldbahis_preped_data['species'] = oldbahis_preped_data['species'].replace(adict)
oldbahis_preped_data['species'] = oldbahis_preped_data.apply(lambda x: 'Unknown' if type(x['species'])==int else x['species'],axis=1)

oldbahis_preped_data['tentative_diagnosis'] = oldbahis_preped_data['tentative_diagnosis'].str.split("'", expand=True)[1]

oldbahis_preped_data.rename({'date': 'basic_info_date',
                    'division': 'basic_info_division',
                    'district': 'basic_info_district',
                    'upazila': 'basic_info_upazila',
                    'tentative_diagnosis': 'top_diagnosis',
                    'sick_number': 'patient_info_sick_number',
                    'dead_number': 'patient_info_dead_number'
                    }, axis=1, inplace=True)



diag_names = pd.read_csv(os.path.join(sourcepath, 'newbahis_bahis_diagnosis_table.csv'))
diag_names2 = diag_names.set_index('diagnosisname')['diagnosisid'].drop_duplicates().astype(str)

ddict = dict(diag_names2[~diag_names2.index.duplicated(keep='first')])
ddict[-1]='Unknown'

# reverse filling disease code
oldbahis_preped_data['diagnosis_treatment_tentative_diagnosis'] = oldbahis_preped_data['top_diagnosis'].replace(ddict)


oldbahis_preped_data= oldbahis_preped_data[['basic_info_date',
                                        'basic_info_division',
                                        'basic_info_district',
                                        'basic_info_upazila',
                                        'patient_info_species',
                                        'species',
                                        'diagnosis_treatment_tentative_diagnosis',
                                        'top_diagnosis',
                                        'patient_info_sick_number',
                                        'patient_info_dead_number']]

#remove first records? Nope, we need to remove first day:
#bahis_preped_data = bahis_preped_data[~bahis_preped_data.duplicated(subset='basic_info_upazila',keep='first')]

bahis_preped_data = bahis_sourcedata[['basic_info_date',
                                        'basic_info_division',
                                        'basic_info_district',
                                        'basic_info_upazila',
                                        'patient_info_species',
                                        'diagnosis_treatment_tentative_diagnosis',
                                        'patient_info_sick_number',
                                        'patient_info_dead_number']]

bahis_preped_data['basic_info_date'] = pd.to_datetime(bahis_preped_data['basic_info_date'])

bahis_preped_data['basic_info_date'] = bahis_preped_data['basic_info_date'].apply(lambda x: x.date())


bahis_preped_data = bahis_preped_data[bahis_preped_data['basic_info_date']>dt.date(2022,6,1)]
##remove first day of submissions of each upazila. Date of submission is UNKNOWN, but we can remove submissions with the first date assuming that during training people put today's date...
to_remove = []
for ulo in bahis_preped_data['basic_info_upazila'].unique():
    urecs = bahis_preped_data[bahis_preped_data['basic_info_upazila']==ulo]
    fdate = urecs.iloc[0]['basic_info_date']
    inds = list(bahis_preped_data[(bahis_preped_data['basic_info_upazila']==ulo) & (fdate == bahis_preped_data['basic_info_date'])].index)
    to_remove = to_remove + inds

bahis_preped_data = bahis_preped_data.drop(index=to_remove)


diag_names = pd.read_csv(os.path.join(sourcepath, 'newbahis_bahis_diagnosis_table.csv'))
diag_names2 = diag_names.set_index('diagnosisid')['diagnosisname'].drop_duplicates().astype(str)

anim_names=pd.read_csv(os.path.join(sourcepath, 'newbahis_bahis_species_table.csv'))
anim_names2 = anim_names.set_index('speciesid')['speciesname'].drop_duplicates().astype(str)


ddict = dict(diag_names2[~diag_names2.index.duplicated(keep='first')])
ddict[-1]='Unknown'

adict = dict(anim_names2[~anim_names2.index.duplicated(keep='first')])
adict[-1]='Unknown'


#If there is more than one diagnosis chosen, only provide first one
bahis_preped_data['diagnosis_treatment_tentative_diagnosis'] = bahis_preped_data['diagnosis_treatment_tentative_diagnosis'].fillna('-1')
bahis_preped_data['top_diagnosis'] = bahis_preped_data.apply(lambda x: x['diagnosis_treatment_tentative_diagnosis'].split(' ')[0], axis=1)
bahis_preped_data['top_diagnosis'] = bahis_preped_data['top_diagnosis'].astype(int)
bahis_preped_data['top_diagnosis'] = bahis_preped_data['top_diagnosis'].replace(ddict)
bahis_preped_data['top_diagnosis'] = bahis_preped_data.apply(lambda x: 'Unknown' if type(x['top_diagnosis'])==int else x['top_diagnosis'],axis=1)

bahis_preped_data['patient_info_species'] = bahis_preped_data['patient_info_species'].fillna('-1')
bahis_preped_data['species'] = bahis_preped_data['patient_info_species']  #bahis_preped_data.apply(lambda x: x['patient_info_species'].split(' ')[0], axis=1)
bahis_preped_data['species'] = bahis_preped_data['species'].astype(int)
bahis_preped_data['species'] = bahis_preped_data['species'].replace(adict)
bahis_preped_data['species'] = bahis_preped_data.apply(lambda x: 'Unknown' if type(x['species'])==int else x['species'],axis=1)

bahis_preped_data= bahis_preped_data[['basic_info_date',
                                        'basic_info_division',
                                        'basic_info_district',
                                        'basic_info_upazila',
                                        'patient_info_species',
                                        'species',
                                        'diagnosis_treatment_tentative_diagnosis',
                                        'top_diagnosis',
                                        'patient_info_sick_number',
                                        'patient_info_dead_number']]

bahis_total= pd.concat([oldbahis_preped_data, bahis_preped_data], ignore_index=True)

bahis_preped_data.to_csv(sourcepath + 'preped_ndata.csv')
oldbahis_preped_data.to_csv(sourcepath + 'preped_odata.csv')

bahis_total.to_csv(sourcepath + 'preped_data2.csv')

#bahis_preped_data.to_csv(sourcepath + 'preped_data2.csv')
