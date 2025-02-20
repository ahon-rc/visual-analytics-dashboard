#Imports
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import re
import json

# Data import
data_path = "my-app\static\OSMI_2019.csv"
dp = "my-app\static\OSMI_2016.csv"
d = "my-app\static\OSMI_2014.csv"
survey_2019 = pd.read_csv(data_path)
surv_16 = pd.read_csv(dp)
surv_14 = pd.read_csv(d)

dd = [surv_14, surv_16, survey_2019]

us_state_to_abbrev = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia', 'AS': 'American Samoa', 'GU': 'Guam', 'MP': 'Northern Mariana Islands', 'PR': 'Puerto Rico', 'UM': 'United States Minor Outlying Islands', 'VI': 'Virgin Islands, U.S.'}
state_names = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
print(len(state_names))

map_col = ['If you live in the United States, which state or territory do you live in?', 'What US state or territory do you work in?', 'What US state or territory do you *work* in?']
map_dic = []
temp = {k : 0 for k in state_names}
for idx, col in enumerate(map_col):
    x = dd[idx][col].value_counts().to_dict()
    y = {}
    for j in x.keys():
        if j in us_state_to_abbrev.keys():
            y[us_state_to_abbrev[j]] = x[j]
        else:
            y[j] = x[j]
    for j in y.keys():
        if j in temp.keys():
            temp[j] += y[j]
for i in temp.keys():
    map_dic.append({"name": i, "Participants": temp[i]})
print(len(map_dic))
with open("my-app\static\map_data.json", "w") as outfile:
    outfile.write(json.dumps({"data": map_dic}, indent = 4))

# col_1 = ['Does your employer provide mental health benefits?', 'Does your employer provide mental health benefits as part of healthcare coverage?', 'Does your employer provide mental health benefits as part of healthcare coverage?']
# col_2 = ['Does your employer provide resources to learn more about mental health issues and how to seek help?', "Does your employer offer resources to learn more about mental health concerns and options for seeking help?", 'Does your employer offer resources to learn more about mental health disorders and options for seeking help?']
# col_3 = ['Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources?', 'Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources provided by your employer?', 'Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources provided by your employer?']
# col_4 = ['How easy is it for you to take medical leave for a mental health condition?', 'If a mental health issue prompted you to request a medical leave from work, asking for that leave would be:', 'If a mental health issue prompted you to request a medical leave from work, how easy or difficult would it be to ask for that leave?']
# cols = [col_1, col_2, col_3, col_4]
# output = {'2014':[
#             {
#                 "Yes": 0,
#                 "No": 0,
#                 "Didn\'t know": 0,
#                 "Not Eligible": 0,
#             },
#             {
#                 "Yes": 0,
#                 "No": 0,
#                 "Didn\'t know": 0,
#             },
#             {
#                 "Yes": 0,
#                 "No": 0,
#                 "Didn\'t know": 0,
#             },
#             {
#                 "Somewhat easy": 0,
#                 "Very easy": 0,
#                 "I don't know": 0,
#                 "Somewhat difficult": 0,
#                 "Neither easy nor difficult": 0,
#                 "Very Difficult": 0
#             }
#         ],
#         '2016': [
#             {
#                 "Yes": 0,
#                 "No": 0,
#                 "Didn\'t know": 0,
#                 "Not Eligible": 0,
#             },
#             {
#                 "Yes": 0,
#                 "No": 0,
#                 "Didn\'t know": 0,
#             },
#             {
#                 "Yes": 0,
#                 "No": 0,
#                 "Didn\'t know": 0,
#             },
#             {
#                 "Somewhat easy": 0,
#                 "Very easy": 0,
#                 "I don't know": 0,
#                 "Somewhat difficult": 0,
#                 "Neither easy nor difficult": 0,
#                 "Very Difficult": 0
#             }
#         ],
#         '2019': [
#             {
#                 "Yes": 0,
#                 "No": 0,
#                 "Didn\'t know": 0,
#                 "Not Eligible": 0,
#             },
#             {
#                 "Yes": 0,
#                 "No": 0,
#                 "Didn\'t know": 0,
#             },
#             {
#                 "Yes": 0,
#                 "No": 0,
#                 "Didn\'t know": 0,
#             },
#             {
#                 "Somewhat easy": 0,
#                 "Very easy": 0,
#                 "Didn\'t Know": 0,
#                 "Somewhat difficult": 0,
#                 "Neither easy nor difficult": 0,
#                 "Very Difficult": 0
#             }
#         ]}

# def get_dictionary(col):
#     map = {"Don\'t know": "Didn\'t know", "I don\'t know": "Didn\'t know", "Not eligible for coverage / N/A": "Not Eligible", "Not eligible for coverage / NA": "Not Eligible"}
#     z = []
#     for i in range(len(col)):
#         x = dd[i][col[i]].value_counts().to_dict()
#         y = {}
#         for j in x.keys():
#             if j in map.keys():
#                 y[map[j]] = x[j]
#             else:
#                 y[j] = x[j]
#         z.append(y)
#     return z

# for i in range(len(cols)):
#     x = get_dictionary(cols[i])
#     for idx, dic in enumerate(output.keys()):
#         for j in output[dic][i].keys():
#             if j in x[idx].keys():
#                 output[dic][i][j] = x[idx][j]
# print(output)
# with open("my-app\static\pi_data.json", "w") as outfile:
#     outfile.write(json.dumps(output, indent = 4))


# print(surv_16['mh_disorder_current'].unique())
# print(survey_2019['*If so, what disorder(s) were you diagnosed with?*'].unique())

# def split_values(text):
#     # Regular expression to match segments outside parentheses
#     pattern = r'([^(),]+(?:\([^()]*\))?)'
#     return [match.strip() for match in re.findall(pattern, text) if match.strip()]

# def get_dic(data, column_name, split=None):
#     diseases = {}
#     for i in data[column_name].unique():
#         if type(i) == str:
            
#             for j in split_values(i) if not split else i.split(split):
#                 if j in diseases.keys():
#                     diseases[j] += 1
#                 else:
#                     diseases[j] = 1

#     return({k: v for k, v in sorted(diseases.items(), key=lambda item: item[1], reverse=True)})

# dis_19 = get_dic(survey_2019, '*If so, what disorder(s) were you diagnosed with?*')
# dis_16 = get_dic(surv_16, "If so, what condition(s) were you diagnosed with?", "|")
# lst = list(set(dis_19.keys()).intersection(dis_16.keys()))[:8]
# changed = ['Anxiety Disorder', 'ADHD', 'Eating Disorder', 'OCD', 'Personality Disorder', 'Substance Use Disorder', 'Seasonal Affective Disorder', 'Addictive Disorder']

# dis_19 = {k: v for k, v in sorted({k : dis_19[k] for k in lst}.items(), key=lambda item: item[1], reverse=True)}
# dis_16 = {k : dis_16[k] for k in dis_19.keys()}

# dis_19 = {changed[i]: dis_19[lst[i]] for i in range(len(changed))}
# dis_16 = {changed[i]: dis_16[lst[i]] for i in range(len(changed))}
# print("19:\n", dis_19, "\n\n16:\n", dis_16)

# with open("my-app\static\disease_19.json", "w") as outfile:
#     outfile.write(json.dumps(dis_19, indent = 4))

# with open("my-app\static\disease_16.json", "w") as outfile:
#     outfile.write(json.dumps(dis_16, indent = 4))

# print("Survey 14:", len(surv_14), "Survey 16:", len(surv_16), "Survey 19:", len(survey_2019))
# print("Survey 14:\n",surv_14['coworkers'].unique(), surv_14['Gender'].unique(), surv_14['family_history'].unique())
# print("Survey 16:\n",surv_16["Would you feel comfortable discussing a mental health disorder with your coworkers?"].unique(), surv_16["What is your gender?"].unique(), surv_16["Do you have a family history of mental illness?"].unique())
# print("Survey 19:\n",survey_2019['Would you feel comfortable discussing a mental health issue with your coworkers?'].unique(), survey_2019['What is your gender?'].unique(), survey_2019["Do you have a family history of mental illness?"].unique())


# surv_16 = surv_16[["Do you have a family history of mental illness?", "What is your gender?", "Would you feel comfortable discussing a mental health disorder with your coworkers?"]]
# surv_16.columns = ['family_history', 'sex', 'peer_discussion']

# surv_16.to_csv("my-app\static\surv_16.csv")

# surv_14 = surv_14[["family_history", "Gender", "coworkers"]]
# surv_14.columns = ['family_history', 'sex', 'peer_discussion']

# surv_14.to_csv("my-app\static\survey_14.csv")
# print(surv_14[(surv_14['family_history']=="Yes") & (surv_14['sex']== "Male") & (surv_14['peer_discussion']=="Yes")].count())


# survey_2019 = survey_2019[["Do you have a family history of mental illness?", "What is your gender?", "Would you feel comfortable discussing a mental health issue with your coworkers?"]]
# survey_2019.columns = ['family_history', 'sex', 'peer_discussion']

# survey_2019.to_csv("my-app\static\surv_19.csv")




# print(set(survey_2016.columns).intersection(set(surv_19.columns)))
# print(len(set(survey_2016.columns).intersection(set(surv_19.columns))))

# print((set(surv_19.columns))-set(survey_2016.columns))
# print(len((set(surv_19.columns))-set(survey_2016.columns)))

# # ----------- CLEANING THE DATA -----------
# # Column rename
# renamed_columns = ['self_empl_flag', 'comp_no_empl', 'tech_comp_flag', 'tech_role_flag', 'mh_coverage_flag',
#                 'mh_coverage_awareness_flag', 'mh_employer_discussion', 'mh_resources_provided', 'mh_anonimity_flag',
#                 'mh_medical_leave', 'mh_discussion_neg_impact', 'ph_discussion_neg_impact', 'mh_discussion_cowork',
#                 'mh_discussion_supervis', 'mh_eq_ph_employer', 'mh_conseq_coworkers', 'mh_coverage_flag2', 'mh_online_res_flag',
#                 'mh_diagnosed&reveal_clients_flag', 'mh_diagnosed&reveal_clients_impact', 'mh_diagnosed&reveal_cowork_flag', 'mh_cowork_reveal_neg_impact',
#                 'mh_prod_impact', 'mh_prod_impact_perc', 'prev_employers_flag', 'prev_mh_benefits', 'prev_mh_benefits_awareness',
#                 'prev_mh_discussion', 'prev_mh_resources', 'prev_mh_anonimity', 'prev_mh_discuss_neg_conseq', 'prev_ph_discuss_neg_conseq',
#                 'prev_mh_discussion_cowork', 'prev_mh_discussion_supervisor', 'prev_mh_importance_employer', 'prev_mh_conseq_coworkers',
#                 'future_ph_specification', 'why/why_not', 'future_mh_specification', 'why/why_not2', 'mh_hurt_on_career', 'mh_neg_view_cowork',
#                 'mh_sharing_friends/fam_flag', 'mh_bad_response_workplace', 'mh_for_others_bad_response_workplace', 'mh_family_hist',
#                 'mh_disorder_past', 'mh_disorder_current', 'yes:what_diagnosis?', 'maybe:whats_your_diag', 'mh_diagnos_proffesional',
#                 'yes:condition_diagnosed', 'mh_sought_proffes_treatm', 'mh_eff_treat_impact_on_work', 'mh_not_eff_treat_impact_on_work',
#                 'age', 'sex', 'country_live', 'live_us_teritory', 'country_work', 'work_us_teritory', 'work_position', 'remote_flag']
# survey_2016.columns = renamed_columns

# # Sex column needs to be recoded (number of unique values = 70)
# survey_2016['sex'].replace(to_replace = ['Male', 'male', 'Male ', 'M', 'm',
#         'man', 'Cis male', 'Male.', 'male 9:1 female, roughly', 'Male (cis)', 'Man', 'Sex is male',
#         'cis male', 'Malr', 'Dude', "I'm a man why didn't you make this a drop down question. You should of asked sex? And I would of answered yes please. Seriously how much text can this take? ",
#         'mail', 'M|', 'male ',
#         'Cis Male', 'Male (trans, FtM)',
#         'cisdude', 'cis man', 'MALE'], value = "Male", inplace = True)

# survey_2016['sex'].replace(to_replace = ['Female', 'female', 'I identify as female.', 'female ',
#         'Female assigned at birth ', 'F', 'Woman', 'fm', 'f', 'Cis female ',
#         'Female or Multi-Gender Femme', 'Female ', 'woman', 'female/woman',
#         'Cisgender Female', 'fem', 'Female (props for making this a freeform field, though)',
#         ' Female', 'Cis-woman', 'female-bodied; no feelings about gender',
#         'AFAB'], value = "Female", inplace = True)

# survey_2016['sex'].replace(to_replace = ['non-binary', 'nb masculine', 'Nonbinary', 'Enby', 
#         'Queer', 'Male/genderqueer'], value = 'Non-Binary', inplace = True)

# survey_2016['sex'].replace(to_replace = ['Genderqueer', 'Bigender', 'Androgynous', 'Fluid',
#                                         'Genderfluid', 'genderqueer', 'genderqueer woman', 'Agender',
#                                         'Genderflux demi-girl', 'Genderfluid (born female)'], value='Gender Fluid', inplace = True)

# survey_2016['sex'].replace(to_replace = ['Transgender woman', 'mtf', 'Transitioned, M2F',
#                                         ], value='Transgender', inplace = True)

# survey_2016['sex'].replace(to_replace = ['Other/Transfeminine', 'Other', 'none of your business', 'Human', 'human', 
#                                         'Unicorn'], value = 'Not Answered', inplace = True)

# # Recode Comp size & country columns (for ease when doing plots)
# survey_2016['comp_no_empl'].replace(to_replace = ['More than 1000'], value = '>1000', inplace = True)
# survey_2016['country_live'].replace(to_replace = ['United States of America'], value = 'USA', inplace = True)
# survey_2016['country_live'].replace(to_replace = ['United Kingdom'], value = 'UK', inplace = True)
# survey_2016['country_work'].replace(to_replace = ['United States of America'], value = 'USA', inplace = True)
# survey_2016['country_work'].replace(to_replace = ['United Kingdom'], value = 'UK', inplace = True)

# survey_2016['mh_coverage_flag'].replace(to_replace = ["Not eligible for coverage / N/A"], value = 'No', inplace = True)

# survey_2016['work_position'].replace(to_replace = ['Dev Evangelist/Advocate|Back-end Developer',
#                                                 'Support|Back-end Developer|One-person shop', 'One-person shop|Back-end Developer|DevOps/SysAdmin',
#                                                 'DevOps/SysAdmin|Back-end Developer', 'Back-end Developer|DevOps/SysAdmin', 'One-person shop|Back-end Developer',
#                                                 'Back-end Developer|Supervisor/Team Lead', 'Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead',
#                                                 'One-person shop|Back-end Developer|Supervisor/Team Lead', 'Back-end Developer|Dev Evangelist/Advocate',
#                                                 'Supervisor/Team Lead|Back-end Developer|DevOps/SysAdmin', 'Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Designer',
#                                                 'Dev Evangelist/Advocate|Support|Back-end Developer', 'Back-end Developer|Dev Evangelist/Advocate|Supervisor/Team Lead',
#                                                 'Back-end Developer|One-person shop', 'DevOps/SysAdmin|Back-end Developer|One-person shop', 'Other|Back-end Developer',
#                                                 'Dev Evangelist/Advocate|DevOps/SysAdmin|Back-end Developer', 'DevOps/SysAdmin|Support|Back-end Developer',
#                                                 'Back-end Developer|Support|DevOps/SysAdmin', 'Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Support',
#                                                 'DevOps/SysAdmin|Support|Back-end Developer|One-person shop', 'Executive Leadership|Supervisor/Team Lead|Back-end Developer|DevOps/SysAdmin',
#                                                 'Supervisor/Team Lead|Back-end Developer|Support|DevOps/SysAdmin', 'Dev Evangelist/Advocate|One-person shop|Back-end Developer|Support|DevOps/SysAdmin',
#                                                 'One-person shop|Back-end Developer|Dev Evangelist/Advocate', 'Back-end Developer|Support|Supervisor/Team Lead',
#                                                 'Executive Leadership|Supervisor/Team Lead|Dev Evangelist/Advocate|Back-end Developer', 'Supervisor/Team Lead|Back-end Developer|Designer',
#                                                 ], 
#                                                 value = "Back-end Developer", inplace = True)
# survey_2016['work_position'].replace(to_replace = ['Front-end Developer', 'Supervisor/Team Lead|Front-end Developer', 'Front-end Developer|Designer',
#                                                 'Front-end Developer|Supervisor/Team Lead','One-person shop|Front-end Developer', 'One-person shop|Designer|Front-end Developer|Supervisor/Team Lead',
#                                                 'Designer|Front-end Developer', 'Supervisor/Team Lead|Designer|Front-end Developer|Support',
#                                                 'Support|Front-end Developer|Designer', 'Dev Evangelist/Advocate|DevOps/SysAdmin|Designer|Front-end Developer|Support',
#                                                 'Front-end Developer|One-person shop', 'Supervisor/Team Lead|DevOps/SysAdmin|Support|Front-end Developer|Designer|One-person shop',
#                                                 'Support|Designer|Front-end Developer', 'One-person shop|Designer|Front-end Developer', 
#                                                 'Front-end Developer|Executive Leadership', 'Supervisor/Team Lead|Front-end Developer|Designer', 
#                                                 'One-person shop|Designer|Front-end Developer|Support|Dev Evangelist/Advocate', 'Front-end Developer|Support'], 
#                                                 value = "Front-end Developer", inplace = True)
# survey_2016['work_position'].replace(to_replace = ['Back-end Developer|Front-end Developer', 'One-person shop|Front-end Developer|Back-end Developer',
#                                                 'One-person shop|Front-end Developer|Back-end Developer|Dev Evangelist/Advocate|Other', 'Front-end Developer|Back-end Developer',
#                                                 'Front-end Developer|Back-end Developer|DevOps/SysAdmin', 'One-person shop|Front-end Developer|Back-end Developer|DevOps/SysAdmin',
#                                                 'DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer', 'Dev Evangelist/Advocate|Back-end Developer|Front-end Developer',
#                                                 'Designer|Front-end Developer|Back-end Developer', 'Front-end Developer|Back-end Developer|Sales|DevOps/SysAdmin',
#                                                 'Front-end Developer|Back-end Developer|Support', 'DevOps/SysAdmin|One-person shop|Front-end Developer|Back-end Developer', 
#                                                 'Back-end Developer|Front-end Developer|One-person shop', 'Front-end Developer|Back-end Developer|Supervisor/Team Lead',
#                                                 'DevOps/SysAdmin|Front-end Developer|Back-end Developer|Support', 'DevOps/SysAdmin|Back-end Developer|One-person shop|Front-end Developer', 
#                                                 'Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Front-end Developer', 'Dev Evangelist/Advocate|Back-end Developer|Designer|Front-end Developer',
#                                                 'One-person shop|Designer|Front-end Developer|Back-end Developer|Support|Dev Evangelist/Advocate', 
#                                                 'Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin', 'Supervisor/Team Lead|Front-end Developer|Back-end Developer',
#                                                 'Back-end Developer|Front-end Developer|Designer', 'Supervisor/Team Lead|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer',
#                                                 'DevOps/SysAdmin|Back-end Developer|Front-end Developer|Designer', 'One-person shop|Designer|Front-end Developer|Back-end Developer|Support',
#                                                 'Designer|Front-end Developer|Back-end Developer|DevOps/SysAdmin', 'Designer|Front-end Developer|Back-end Developer|Supervisor/Team Lead',
#                                                 'Front-end Developer|Back-end Developer|Support|Dev Evangelist/Advocate', 'Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin|Dev Evangelist/Advocate',
#                                                 'One-person shop|Front-end Developer|Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead', 
#                                                 'Dev Evangelist/Advocate|Support|Back-end Developer|Front-end Developer', 'Designer|Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin|Supervisor/Team Lead',
#                                                 'Designer|Front-end Developer|Back-end Developer|DevOps/SysAdmin|Other', 'One-person shop|Designer|Front-end Developer|Back-end Developer',
#                                                 'Designer|Front-end Developer|Back-end Developer|Sales|Supervisor/Team Lead', 'Front-end Developer|Back-end Developer|Dev Evangelist/Advocate',
#                                                 'Front-end Developer|Back-end Developer|Support|Supervisor/Team Lead','Supervisor/Team Lead|Front-end Developer|Back-end Developer|Dev Evangelist/Advocate',
#                                                 'Supervisor/Team Lead|DevOps/SysAdmin|Front-end Developer|Back-end Developer', 
#                                                 'DevOps/SysAdmin|Back-end Developer|Front-end Developer|One-person shop', 'Dev Evangelist/Advocate|Front-end Developer|Back-end Developer|DevOps/SysAdmin',
#                                                 'Front-end Developer|Back-end Developer|DevOps/SysAdmin|Dev Evangelist/Advocate', 'Support|Front-end Developer|Back-end Developer',
#                                                 'Executive Leadership|Supervisor/Team Lead|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer',
#                                                 'Front-end Developer|Back-end Developer|Supervisor/Team Lead|Executive Leadership', 'Executive Leadership|Supervisor/Team Lead|Back-end Developer|Front-end Developer|Designer',
#                                                 'Front-end Developer|Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead|Executive Leadership', 
#                                                 'Executive Leadership|Back-end Developer|Front-end Developer', 'DevOps/SysAdmin|Support|Front-end Developer|Back-end Developer',
#                                                 'Supervisor/Team Lead|Dev Evangelist/Advocate|Back-end Developer|Designer|Front-end Developer', 'Supervisor/Team Lead|Support|Front-end Developer|Back-end Developer',
#                                                 'Front-end Developer|Back-end Developer|Dev Evangelist/Advocate|Supervisor/Team Lead', 'Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin|Executive Leadership',
#                                                 'DevOps/SysAdmin|Designer|Front-end Developer|Back-end Developer', 'Front-end Developer|Back-end Developer|Other',
#                                                 'Supervisor/Team Lead|Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin', 'Supervisor/Team Lead|Support|Back-end Developer|Front-end Developer',
#                                                 'Support|Back-end Developer|Front-end Developer|One-person shop', 'DevOps/SysAdmin|Support|Back-end Developer|One-person shop|Front-end Developer',
#                                                 'Dev Evangelist/Advocate|DevOps/SysAdmin|Designer|Front-end Developer|Back-end Developer', 'Support|Back-end Developer|Front-end Developer|Designer',
#                                                 'Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|One-person shop', 'Supervisor/Team Lead|Front-end Developer|Back-end Developer|DevOps/SysAdmin|Dev Evangelist/Advocate'], 
#                                                 value = "Full-Stack Developer", inplace = True)
# survey_2016['work_position'].replace(to_replace = ['Supervisor/Team Lead', 'DevOps/SysAdmin|One-person shop', 
#                                                 'Supervisor/Team Lead|Dev Evangelist/Advocate|Back-end Developer|Front-end Developer', 'Supervisor/Team Lead|Support|Back-end Developer',
#                                                 'Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer',
#                                                 'Supervisor/Team Lead|Back-end Developer','Supervisor/Team Lead|DevOps/SysAdmin|Support|Back-end Developer', 'Supervisor/Team Lead|Other',
#                                                 'Supervisor/Team Lead|Back-end Developer|Front-end Developer', 'Supervisor/Team Lead|Back-end Developer|Front-end Developer|One-person shop',
#                                                 'Supervisor/Team Lead|DevOps/SysAdmin', 'DevOps/SysAdmin', 'Supervisor/Team Lead|Back-end Developer|One-person shop',
#                                                 'Supervisor/Team Lead|Dev Evangelist/Advocate|Back-end Developer', 'Back-end Developer|DevOps/SysAdmin|Dev Evangelist/Advocate|Supervisor/Team Lead',
#                                                 'Front-end Developer|Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead','Supervisor/Team Lead|Back-end Developer|DevOps/SysAdmin|Dev Evangelist/Advocate',
#                                                 'Supervisor/Team Lead|Front-end Developer|Back-end Developer|DevOps/SysAdmin', 'Supervisor/Team Lead|Back-end Developer|Front-end Developer|Designer',
#                                                 'Dev Evangelist/Advocate|DevOps/SysAdmin', 'Support|Back-end Developer|Front-end Developer',
#                                                 'DevOps/SysAdmin|Supervisor/Team Lead', 'Supervisor/Team Lead|DevOps/SysAdmin|Support', 'DevOps/SysAdmin|Front-end Developer|Back-end Developer',
#                                                 'Designer|Front-end Developer|Back-end Developer|Supervisor/Team Lead|Executive Leadership', 'Supervisor/Team Lead|Support|One-person shop|Designer|Front-end Developer|Sales',
#                                                 'One-person shop|DevOps/SysAdmin','One-person shop|Designer|Front-end Developer|Back-end Developer|Dev Evangelist/Advocate|Supervisor/Team Lead',
#                                                 'DevOps/SysAdmin|Support|Sales|Front-end Developer|Designer|One-person shop', 'One-person shop|Designer|Sales|Support|Supervisor/Team Lead',
#                                                 'DevOps/SysAdmin|Back-end Developer|Front-end Developer'], 
#                                                 value = "Team Lead", inplace = True)
# survey_2016['work_position'].replace(to_replace = ['DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|Designer',
#                                                 'Support|Back-end Developer|One-person shop', 'Supervisor/Team Lead|Support|Back-end Developer', 'Support|Other',
#                                                 'Support', 'One-person shop|Designer|Front-end Developer|Support', 'Dev Evangelist/Advocate|Support', 
#                                                 'Dev Evangelist/Advocate|Back-end Developer|Support', 'Support|Back-end Developer', 'DevOps/SysAdmin|Support',
#                                                 'Supervisor/Team Lead|Support', 'Support|DevOps/SysAdmin', 'DevOps/SysAdmin|Support|One-person shop', 'Support|Sales|Designer'], 
#                                                 value = "Support Team", inplace = True)
# survey_2016['work_position'].replace(to_replace = ['Executive Leadership', 'Other|Executive Leadership', 'One-person shop',
#                                                 'Executive Leadership|Front-end Developer|Back-end Developer|Sales|Supervisor/Team Lead',
#                                                 'Front-end Developer|Back-end Developer|Executive Leadership', 'Executive Leadership|Supervisor/Team Lead|Back-end Developer',
#                                                 'Front-end Developer|Back-end Developer|Sales|Executive Leadership', 'Executive Leadership|Supervisor/Team Lead',
#                                                 'Executive Leadership|DevOps/SysAdmin|Back-end Developer', 'Executive Leadership|DevOps/SysAdmin|Back-end Developer|Support',
#                                                 'DevOps/SysAdmin|Executive Leadership', 'Executive Leadership|Dev Evangelist/Advocate', 'Support|HR|Supervisor/Team Lead|Executive Leadership',
#                                                 'One-person shop|DevOps/SysAdmin|Executive Leadership', 'DevOps/SysAdmin|Dev Evangelist/Advocate|Supervisor/Team Lead|Executive Leadership',
#                                                 'One-person shop|Back-end Developer|Sales|DevOps/SysAdmin|Executive Leadership', 'Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead|Other',
#                                                 'Supervisor/Team Lead|Executive Leadership', 'One-person shop|Back-end Developer|Sales|Support|Supervisor/Team Lead|Executive Leadership',
#                                                 'Executive Leadership|Supervisor/Team Lead|Sales', 'Executive Leadership|Supervisor/Team Lead|Designer', 
#                                                 'Executive Leadership|Supervisor/Team Lead|Front-end Developer|Back-end Developer', 'Support|Sales|Back-end Developer|Front-end Developer|Designer|One-person shop',
#                                                 'One-person shop|Designer|Sales|Executive Leadership', 'Executive Leadership|Supervisor/Team Lead|Front-end Developer',
#                                                 'One-person shop|Front-end Developer|Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead|Executive Leadership',
#                                                 'Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead|Executive Leadership'], 
#                                                 value = "CXO", inplace = True)
# survey_2016['work_position'].replace(to_replace = ['Designer', 'One-person shop|Designer', 'Designer|Support|Supervisor/Team Lead', 'Support|Designer',
#                                                 'Designer|One-person shop', 'Front-end Developer|Designer|One-person shop', 'Supervisor/Team Lead|Designer',
#                                                 'Designer|Supervisor/Team Lead', 'DevOps/SysAdmin|Designer'], 
#                                                 value = 'Designer', inplace = True)
# survey_2016['work_position'].replace(to_replace = ['Sales', 'Supervisor/Team Lead|Sales', 'Sales|Support|DevOps/SysAdmin|Executive Leadership', 
#                                                 'One-person shop|Designer|Support', ], 
#                                                 value = 'Sales Team', inplace = True)
# survey_2016['work_position'].replace(to_replace = ['HR', 'Other|HR', 'HR|Supervisor/Team Lead|Executive Leadership', 'HR|Dev Evangelist/Advocate|Sales', 'Supervisor/Team Lead|DevOps/SysAdmin|HR',
#                                                 ], 
#                                                 value = 'HR Team', inplace = True)
# survey_2016['work_position'].replace(to_replace = ['Other', 'One-person shop|Back-end Developer|Sales|Support|DevOps/SysAdmin|Dev Evangelist/Advocate|Supervisor/Team Lead|Executive Leadership|Other',
#                                                 'Executive Leadership|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer',
#                                                 'Other|Supervisor/Team Lead|Support|Back-end Developer|Designer', 'Other|Executive Leadership|Supervisor/Team Lead|Back-end Developer',
#                                                 'Executive Leadership|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Back-end Developer|Front-end Developer',
#                                                 'Other|Back-end Developer|Front-end Developer|Designer','Other|Back-end Developer|Front-end Developer|Designer', 
#                                                 'Other|Supervisor/Team Lead|Back-end Developer|One-person shop', 'Dev Evangelist/Advocate',
#                                                 'Other|Back-end Developer|Front-end Developer', 'Other|Support', 'Supervisor/Team Lead|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|Designer',
#                                                 'Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Designer|Front-end Developer', 
#                                                 'One-person shop|Front-end Developer|Back-end Developer|Supervisor/Team Lead|Executive Leadership', 
#                                                 'Other|Dev Evangelist/Advocate|Sales|Back-end Developer|Front-end Developer', 'Other|Front-end Developer|Back-end Developer|Sales|DevOps/SysAdmin|Dev Evangelist/Advocate',
#                                                 'One-person shop|Back-end Developer|Other', 'Other|Executive Leadership|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Back-end Developer|One-person shop',
#                                                 'One-person shop|Back-end Developer|DevOps/SysAdmin|Dev Evangelist/Advocate|Other', 'Other|Supervisor/Team Lead|Back-end Developer|Front-end Developer', 
#                                                 'Other|Dev Evangelist/Advocate|One-person shop', 'Other|Back-end Developer|Front-end Developer|One-person shop', 
#                                                 'Other|One-person shop|Back-end Developer|Sales|Support|DevOps/SysAdmin|Dev Evangelist/Advocate|Supervisor/Team Lead',
#                                                 'One-person shop|Front-end Developer|Back-end Developer|Sales|Support|DevOps/SysAdmin',
#                                                 'DevOps/SysAdmin|Support|Sales|One-person shop|Designer|Front-end Developer|Back-end Developer',
#                                                 'Executive Leadership|Supervisor/Team Lead|HR|DevOps/SysAdmin|Support|Sales|Back-end Developer|One-person shop|Designer|Front-end Developer',
#                                                 'Other|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|One-person shop',
#                                                 'Other|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer', 'Other|Front-end Developer|Designer',
#                                                 'Other|Dev Evangelist/Advocate|Back-end Developer|Front-end Developer', 'DevOps/SysAdmin|Other',
#                                                 'Other|Executive Leadership|Supervisor/Team Lead|HR|Support|Sales|Designer|One-person shop',
#                                                 'Executive Leadership|One-person shop|Front-end Developer|Back-end Developer|Support|Supervisor/Team Lead',
#                                                 'Other|Support|Back-end Developer|Front-end Developer|Designer', 'Other|Designer|Front-end Developer', 
#                                                 'Other|Front-end Developer', 'Other|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|Designer|One-person shop',
#                                                 'One-person shop|Other', 'Designer|Front-end Developer|Back-end Developer|Executive Leadership|Other',
#                                                 'Front-end Developer|Back-end Developer|Sales|Support|DevOps/SysAdmin|Supervisor/Team Lead|Executive Leadership', 
#                                                 'One-person shop|Front-end Developer|Back-end Developer|Support|Other', 'One-person shop|Designer|Front-end Developer|Back-end Developer|Sales|Support',
#                                                 'Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Designer|Front-end Developer',
#                                                 'Other|DevOps/SysAdmin|Support|Back-end Developer', 'Other|One-person shop', 'Executive Leadership|Other',
#                                                 'One-person shop|Designer|Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin|Other', 
#                                                 'Other|Dev Evangelist/Advocate|Support', 'Executive Leadership|Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Front-end Developer|One-person shop',
#                                                 'Other|DevOps/SysAdmin|Back-end Developer', 'Other|Back-end Developer|Supervisor/Team Lead', 'Other|Dev Evangelist/Advocate',
#                                                 'Back-end Developer|Supervisor/Team Lead|Other', 'Other|Supervisor/Team Lead|Front-end Developer', 'Other|Supervisor/Team Lead' 'DevOps/SysAdmin|Designer',
#                                                 'Front-end Developer|Back-end Developer|Support|Other', 'Executive Leadership|Supervisor/Team Lead|Support|Sales|Designer|Front-end Developer|Back-end Developer',
#                                                 'Other|Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Support', 'Other|Front-end Developer|Designer|One-person shop'
#                                                 'DevOps/SysAdmin|Support|Sales|Front-end Developer|Designer|One-person shop', 'Other|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|One-person shop',
#                                                 'Other|One-person shop|Designer|Front-end Developer|Back-end Developer|Support|Supervisor/Team Lead', 
#                                                 'Other|Supervisor/Team Lead|DevOps/SysAdmin|Support|Front-end Developer|Back-end Developer', 'Other|One-person shop|Designer|Front-end Developer',
#                                                 'Other|One-person shop|Designer|Front-end Developer', 'Designer|Front-end Developer|Back-end Developer|Other', 'Other|Supervisor/Team Lead|Dev Evangelist/Advocate',
#                                                 'Other|Supervisor/Team Lead', 'Other|Front-end Developer|Designer|One-person shop', ], 
#                                                 value = 'Other', inplace = True)

# # Max age is 323, min age is 3.
# # There are only 5 people that have weird ages (3yo, 15yo, or 99yo or 323 yo.) 
# # These people will take the average age of the dataset (the correct calculated one, w/out outliers)
# mean_age = survey_2016[(survey_2016['age'] >= 18) | (survey_2016['age'] <= 75)]['age'].mean()
# survey_2016['age'].replace(to_replace = survey_2016[(survey_2016['age'] < 18) | (survey_2016['age'] > 75)]['age'].tolist(),
#                         value = mean_age, inplace = True)

# # The survey has 1433 rows, so first we will drop all columns where more than half of the observations have missing values
# cols = (survey_2016.isna().sum() >= survey_2016.shape[0]/2).tolist()
# to_drop = survey_2016.columns[cols]
# survey_2016.drop(labels = to_drop, axis = 1, inplace = True)

# # Dealing with other missing values
# from sklearn.impute import SimpleImputer

# # Impute nan with the most frequent value (mode) on every row
# imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
# imp.fit(survey_2016)
# imp_data = pd.DataFrame(data = imp.transform(survey_2016), columns = survey_2016.columns)

# # for i in imp_data.columns:
# #     print(i,':')
# #     print(imp_data[i].nunique())
# #     print(imp_data[i].unique())


# imp_data.to_csv(data_path)