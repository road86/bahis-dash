import pandas as pd

sourcepath = 'exported_data/'
sourcefilename =sourcepath + 'newbahis_bahis_patient_registrydyncsv_live_table.csv'
bahis_sourcedata = pd.read_csv(sourcefilename, low_memory=False)

bahis_preped_data = bahis_sourcedata[['basic_info_date',
                                      'basic_info_division',
                                      'basic_info_district',
                                      'basic_info_upazila',
                                      'diagnosis_treatment_tentative_diagnosis',
                                      'patient_info_sick_number',
                                      'patient_info_dead_number']]

bahis_preped_data.to_csv(sourcepath + 'preped_data.csv')

