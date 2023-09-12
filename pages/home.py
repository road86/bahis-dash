import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path="/")

# Define the page layout
layout = dbc.Container(
    [
        # dbc.Row([
        #     html.Center(html.H1("Home: This landing page")),
        # ]),
        # # dbc.Row([
        # #     html.Center(html.H1("Alerts: Reporting status")),
        # # ]),
        # dbc.Row([
        #     html.Center(html.H1("Dls: Overview page ")),
        # ]),
        # dbc.Row([
        #     dbc.Button('Cache',id='btnCache', n_clicks=0),
        # ]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        html.Center(html.H1("Home: This landing page")),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        html.Center(html.H1("ULO: Upazila Lifestock Office")),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        html.Center(html.H1("Completeness: Reports")),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                # dbc.Col([
                #     dbc.Card([
                #         dbc.Row([
                #             html.Center(html.H1("DLO: District Lifestock Office")),
                #             ])
                #         ])
                #     ]),
                # dbc.Col([
                #     dbc.Card([
                #         dbc.Row([
                #             html.Center(html.H1("DD: Division Director ")),
                #             ])
                #         ])
                #     ]),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        html.Center(html.H1("DLS: Overview page ")),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dbc.Card([dbc.Row([dbc.Button("Home", href="/", size="lg")])])]),
                dbc.Col([dbc.Card([dbc.Row([dbc.Button("ULO", href="/ulo", size="lg")])])]),
                dbc.Col([dbc.Card([dbc.Row([dbc.Button("Completeness", href="/reports", size="lg")])])]),
                # dbc.Col([
                #     dbc.Card([
                #         dbc.Row([
                #             dbc.Button("DLO", href="/dls", size="lg")
                #             ])
                #         ])
                #     ]),
                # dbc.Col([
                #     dbc.Card([
                #         dbc.Row([
                #             dbc.Button("DD", href="/dls", size="lg")
                #             ])
                #         ])
                #     ]),
                dbc.Col([dbc.Card([dbc.Row([dbc.Button("DLS", href="/dls", size="lg")])])]),
            ]
        ),
    ]
)

# @callback(
#     Output ('cache_bahis_data', 'data'),
#     Output ('cache_bahis_dgdata', 'data'),
#     Output ('cache_bahis_geodata', 'data'),
#     Input ('btnCache', 'n_clicks'),
# )

# def incache(btn):
#     print('here')
#     sourcepath = 'exported_data/'
#     geofilename = glob.glob(sourcepath + 'newbahis_geo_cluster*.csv')[-1]
# the available geodata from the bahis project (Masterdata)
#     dgfilename = os.path.join(sourcepath, 'Diseaselist.csv')   # disease grouping info (Masterdata)
#     sourcefilename =os.path.join(sourcepath, 'preped_data2.csv')
# main data resource of prepared data from old and new bahis

#     def fetchsourcedata(): #fetch and prepare source data
#         bahis_data = pd.read_csv(sourcefilename)
#         bahis_data['from_static_bahis']=bahis_data['basic_info_date'].str.contains('/')
# new data contains -, old data contains /
#         bahis_data['basic_info_date'] = pd.to_datetime(bahis_data['basic_info_date'])
#     #    bahis_data = pd.to_numeric(bahis_data['basic_info_upazila']).dropna().astype(int)
# empty upazila data can be eliminated, if therre is
#         del bahis_data['Unnamed: 0']
#         bahis_data=bahis_data.rename(columns={'basic_info_date':'date',
#                                             'basic_info_division':'division',
#                                             'basic_info_district':'district',
#                                             'basic_info_upazila':'upazila',
#                                             'patient_info_species':'species_no',
#                                             'diagnosis_treatment_tentative_diagnosis':'tentative_diagnosis',
#                                             'patient_info_sick_number':'sick',
#                                             'patient_info_dead_number':'dead',
#                                             })
#         #assuming non negative values from division, district, upazila, speciesno, sick and dead
#         bahis_data=bahis_data[bahis_data['date']>pd.to_datetime(date(2019, 1, 1))]
#         bahis_data[['division', 'district', 'species_no']]=bahis_data[['division', 'district', 'species_no']]
#                .astype(np.uint16)
#         bahis_data[['upazila', 'sick', 'dead']]=bahis_data[['upazila',  'sick', 'dead']].astype(np.uint32)
#     #    bahis_data[['species', 'tentative_diagnosis', 'top_diagnosis']] = \
#               bahis_data[['species', 'tentative_diagnosis', 'top_diagnosis']].astype(str)
# can you change object to string and does it make a memory difference`?
#         bahis_data['dead'] = bahis_data['dead'].clip(lower=0)
#         return bahis_data
#     bahis_data=fetchsourcedata()

#     def fetchdisgroupdata(): #fetch and prepare disease groups
#         bahis_dgdata= pd.read_csv(dgfilename)
#     #    bahis_dgdata= bahis_dgdata[['species', 'name', 'id', 'Disease type']]
# remark what might be helpful: reminder: memory size
#         bahis_dgdata= bahis_dgdata[['name', 'Disease type']]
#         bahis_dgdata= bahis_dgdata.dropna()
#     #    bahis_dgdata[['name', 'Disease type']] = str(bahis_dgdata[['name', 'Disease type']])
# can you change object to string and does it make a memory difference?
#         return bahis_dgdata
#     bahis_dgdata= fetchdisgroupdata()

#     def fetchgeodata():     #fetch geodata from bahis, delete mouzas and unions
#         geodata = pd.read_csv(geofilename)
#         geodata = geodata.drop(geodata[(geodata['loc_type']==4) | (geodata['loc_type']==5)].index)
# drop mouzas and unions
#         geodata=geodata.drop(['id', 'longitude', 'latitude', 'updated_at'], axis=1)
#         geodata['parent']=geodata[['parent']].astype(np.uint16)   # assuming no mouza and union is taken into
#         geodata[['value']]=geodata[['value']].astype(np.uint32)
#         geodata[['loc_type']]=geodata[['loc_type']].astype(np.uint8)
#         return geodata
#     bahis_geodata= fetchgeodata()

#     return bahis_data.to_dict('records'), bahis_dgdata.to_dict('records'), bahis_geodata.to_dict('records')


# dbc.Row([
#     html.Center(html.H1("Dlsquick: Test environment with only essential values")),
# ]),
# dbc.Row([
#     html.Center(html.H1("Reporting: Another reporting view")),
# ]),
# dbc.Row([
#     html.Center(html.H1("Templates: Figures for reports")),
# ]),
# dbc.Row([
#     dbc.Nav([
#         dbc.NavLink(
#             [
#                 html.Div(page["name"], className="ms-2"),
#             ],
#             href=page["path"],
#             active="exact",
#             )
#     for page in dash.page_registry.values()
#         ])
# ])
