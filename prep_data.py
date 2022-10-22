import pandas as pd
import datetime as dt

sourcepath = 'exported_data/'
sourcefilename =sourcepath + 'newbahis_bahis_patient_registrydyncsv_live_table.csv'
bahis_sourcedata = pd.read_csv(sourcefilename, low_memory=False)


#remove first records? Nope, we need to remove first day:
#bahis_preped_data = bahis_preped_data[~bahis_preped_data.duplicated(subset='basic_info_upazila',keep='first')]

bahis_preped_data = bahis_sourcedata[['basic_info_date',
                                      'basic_info_division',
                                      'basic_info_district',
                                      'basic_info_upazila',
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


diag_names = pd.read_csv(sourcepath + 'newbahis_bahis_diagnosis_table.csv')
diag_names2 = diag_names.set_index('diagnosisid')['diagnosisname'].drop_duplicates().astype(str)


ddict = dict(diag_names2[~diag_names2.index.duplicated(keep='first')])

ddict[-1]='Unknown'

#If there is more than one diagnosis chosen, only provide first one
bahis_preped_data['diagnosis_treatment_tentative_diagnosis'] = bahis_preped_data['diagnosis_treatment_tentative_diagnosis'].fillna('-1')
bahis_preped_data['top_diagnosis'] = bahis_preped_data.apply(lambda x: x['diagnosis_treatment_tentative_diagnosis'].split(' ')[0], axis=1)
bahis_preped_data['top_diagnosis'] = bahis_preped_data['top_diagnosis'].astype(int)
bahis_preped_data['top_diagnosis'] = bahis_preped_data['top_diagnosis'].replace(ddict)
bahis_preped_data['top_diagnosis'] = bahis_preped_data.apply(lambda x: 'Unknown' if type(x['top_diagnosis'])==int else x['top_diagnosis'],axis=1)




bahis_preped_data.to_csv(sourcepath + 'preped_data.csv')
