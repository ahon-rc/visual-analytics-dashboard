#Imports
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Data import
data_path = "my-app\static\DHIT.csv"
survey_2016 = pd.read_csv(data_path)


# ----------- CLEANING THE DATA -----------
# Column rename
renamed_columns = ['self_empl_flag', 'comp_no_empl', 'tech_comp_flag', 'tech_role_flag', 'mh_coverage_flag',
                'mh_coverage_awareness_flag', 'mh_employer_discussion', 'mh_resources_provided', 'mh_anonimity_flag',
                'mh_medical_leave', 'mh_discussion_neg_impact', 'ph_discussion_neg_impact', 'mh_discussion_cowork',
                'mh_discussion_supervis', 'mh_eq_ph_employer', 'mh_conseq_coworkers', 'mh_coverage_flag2', 'mh_online_res_flag',
                'mh_diagnosed&reveal_clients_flag', 'mh_diagnosed&reveal_clients_impact', 'mh_diagnosed&reveal_cowork_flag', 'mh_cowork_reveal_neg_impact',
                'mh_prod_impact', 'mh_prod_impact_perc', 'prev_employers_flag', 'prev_mh_benefits', 'prev_mh_benefits_awareness',
                'prev_mh_discussion', 'prev_mh_resources', 'prev_mh_anonimity', 'prev_mh_discuss_neg_conseq', 'prev_ph_discuss_neg_conseq',
                'prev_mh_discussion_cowork', 'prev_mh_discussion_supervisor', 'prev_mh_importance_employer', 'prev_mh_conseq_coworkers',
                'future_ph_specification', 'why/why_not', 'future_mh_specification', 'why/why_not2', 'mh_hurt_on_career', 'mh_neg_view_cowork',
                'mh_sharing_friends/fam_flag', 'mh_bad_response_workplace', 'mh_for_others_bad_response_workplace', 'mh_family_hist',
                'mh_disorder_past', 'mh_disorder_current', 'yes:what_diagnosis?', 'maybe:whats_your_diag', 'mh_diagnos_proffesional',
                'yes:condition_diagnosed', 'mh_sought_proffes_treatm', 'mh_eff_treat_impact_on_work', 'mh_not_eff_treat_impact_on_work',
                'age', 'sex', 'country_live', 'live_us_teritory', 'country_work', 'work_us_teritory', 'work_position', 'remote_flag']
survey_2016.columns = renamed_columns

# Sex column needs to be recoded (number of unique values = 70)
survey_2016['sex'].replace(to_replace = ['Male', 'male', 'Male ', 'M', 'm',
        'man', 'Cis male', 'Male.', 'male 9:1 female, roughly', 'Male (cis)', 'Man', 'Sex is male',
        'cis male', 'Malr', 'Dude', "I'm a man why didn't you make this a drop down question. You should of asked sex? And I would of answered yes please. Seriously how much text can this take? ",
        'mail', 'M|', 'male ',
        'Cis Male', 'Male (trans, FtM)',
        'cisdude', 'cis man', 'MALE'], value = "Male", inplace = True)

survey_2016['sex'].replace(to_replace = ['Female', 'female', 'I identify as female.', 'female ',
        'Female assigned at birth ', 'F', 'Woman', 'fm', 'f', 'Cis female ',
        'Female or Multi-Gender Femme', 'Female ', 'woman', 'female/woman',
        'Cisgender Female', 'fem', 'Female (props for making this a freeform field, though)',
        ' Female', 'Cis-woman', 'female-bodied; no feelings about gender',
        'AFAB'], value = "Female", inplace = True)

survey_2016['sex'].replace(to_replace = ['non-binary', 'nb masculine', 'Nonbinary', 'Enby', 
        'Queer', 'Male/genderqueer'], value = 'Non-Binary', inplace = True)

survey_2016['sex'].replace(to_replace = ['Genderqueer', 'Bigender', 'Androgynous', 'Fluid',
                                        'Genderfluid', 'genderqueer', 'genderqueer woman', 'Agender',
                                        'Genderflux demi-girl', 'Genderfluid (born female)'], value='Gender Fluid', inplace = True)

survey_2016['sex'].replace(to_replace = ['Transgender woman', 'mtf', 'Transitioned, M2F',
                                        ], value='Transgender', inplace = True)

survey_2016['sex'].replace(to_replace = ['Other/Transfeminine', 'Other', 'none of your business', 'Human', 'human', 
                                        'Unicorn'], value = 'Not Answered', inplace = True)

# Recode Comp size & country columns (for ease when doing plots)
survey_2016['comp_no_empl'].replace(to_replace = ['More than 1000'], value = '>1000', inplace = True)
survey_2016['country_live'].replace(to_replace = ['United States of America'], value = 'USA', inplace = True)
survey_2016['country_live'].replace(to_replace = ['United Kingdom'], value = 'UK', inplace = True)
survey_2016['country_work'].replace(to_replace = ['United States of America'], value = 'USA', inplace = True)
survey_2016['country_work'].replace(to_replace = ['United Kingdom'], value = 'UK', inplace = True)

survey_2016['mh_coverage_flag'].replace(to_replace = ["Not eligible for coverage / N/A"], value = 'No', inplace = True)

survey_2016['work_position'].replace(to_replace = ['Dev Evangelist/Advocate|Back-end Developer',
                                                'Support|Back-end Developer|One-person shop', 'One-person shop|Back-end Developer|DevOps/SysAdmin',
                                                'DevOps/SysAdmin|Back-end Developer', 'Back-end Developer|DevOps/SysAdmin', 'One-person shop|Back-end Developer',
                                                'Back-end Developer|Supervisor/Team Lead', 'Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead',
                                                'One-person shop|Back-end Developer|Supervisor/Team Lead', 'Back-end Developer|Dev Evangelist/Advocate',
                                                'Supervisor/Team Lead|Back-end Developer|DevOps/SysAdmin', 'Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Designer',
                                                'Dev Evangelist/Advocate|Support|Back-end Developer', 'Back-end Developer|Dev Evangelist/Advocate|Supervisor/Team Lead',
                                                'Back-end Developer|One-person shop', 'DevOps/SysAdmin|Back-end Developer|One-person shop', 'Other|Back-end Developer',
                                                'Dev Evangelist/Advocate|DevOps/SysAdmin|Back-end Developer', 'DevOps/SysAdmin|Support|Back-end Developer',
                                                'Back-end Developer|Support|DevOps/SysAdmin', 'Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Support',
                                                'DevOps/SysAdmin|Support|Back-end Developer|One-person shop', 'Executive Leadership|Supervisor/Team Lead|Back-end Developer|DevOps/SysAdmin',
                                                'Supervisor/Team Lead|Back-end Developer|Support|DevOps/SysAdmin', 'Dev Evangelist/Advocate|One-person shop|Back-end Developer|Support|DevOps/SysAdmin',
                                                'One-person shop|Back-end Developer|Dev Evangelist/Advocate', 'Back-end Developer|Support|Supervisor/Team Lead',
                                                'Executive Leadership|Supervisor/Team Lead|Dev Evangelist/Advocate|Back-end Developer', 'Supervisor/Team Lead|Back-end Developer|Designer',
                                                ], 
                                                value = "Back-end Developer", inplace = True)
survey_2016['work_position'].replace(to_replace = ['Front-end Developer', 'Supervisor/Team Lead|Front-end Developer', 'Front-end Developer|Designer',
                                                'Front-end Developer|Supervisor/Team Lead','One-person shop|Front-end Developer', 'One-person shop|Designer|Front-end Developer|Supervisor/Team Lead',
                                                'Designer|Front-end Developer', 'Supervisor/Team Lead|Designer|Front-end Developer|Support',
                                                'Support|Front-end Developer|Designer', 'Dev Evangelist/Advocate|DevOps/SysAdmin|Designer|Front-end Developer|Support',
                                                'Front-end Developer|One-person shop', 'Supervisor/Team Lead|DevOps/SysAdmin|Support|Front-end Developer|Designer|One-person shop',
                                                'Support|Designer|Front-end Developer', 'One-person shop|Designer|Front-end Developer', 
                                                'Front-end Developer|Executive Leadership', 'Supervisor/Team Lead|Front-end Developer|Designer', 
                                                'One-person shop|Designer|Front-end Developer|Support|Dev Evangelist/Advocate', 'Front-end Developer|Support'], 
                                                value = "Front-end Developer", inplace = True)
survey_2016['work_position'].replace(to_replace = ['Back-end Developer|Front-end Developer', 'One-person shop|Front-end Developer|Back-end Developer',
                                                'One-person shop|Front-end Developer|Back-end Developer|Dev Evangelist/Advocate|Other', 'Front-end Developer|Back-end Developer',
                                                'Front-end Developer|Back-end Developer|DevOps/SysAdmin', 'One-person shop|Front-end Developer|Back-end Developer|DevOps/SysAdmin',
                                                'DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer', 'Dev Evangelist/Advocate|Back-end Developer|Front-end Developer',
                                                'Designer|Front-end Developer|Back-end Developer', 'Front-end Developer|Back-end Developer|Sales|DevOps/SysAdmin',
                                                'Front-end Developer|Back-end Developer|Support', 'DevOps/SysAdmin|One-person shop|Front-end Developer|Back-end Developer', 
                                                'Back-end Developer|Front-end Developer|One-person shop', 'Front-end Developer|Back-end Developer|Supervisor/Team Lead',
                                                'DevOps/SysAdmin|Front-end Developer|Back-end Developer|Support', 'DevOps/SysAdmin|Back-end Developer|One-person shop|Front-end Developer', 
                                                'Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Front-end Developer', 'Dev Evangelist/Advocate|Back-end Developer|Designer|Front-end Developer',
                                                'One-person shop|Designer|Front-end Developer|Back-end Developer|Support|Dev Evangelist/Advocate', 
                                                'Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin', 'Supervisor/Team Lead|Front-end Developer|Back-end Developer',
                                                'Back-end Developer|Front-end Developer|Designer', 'Supervisor/Team Lead|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer',
                                                'DevOps/SysAdmin|Back-end Developer|Front-end Developer|Designer', 'One-person shop|Designer|Front-end Developer|Back-end Developer|Support',
                                                'Designer|Front-end Developer|Back-end Developer|DevOps/SysAdmin', 'Designer|Front-end Developer|Back-end Developer|Supervisor/Team Lead',
                                                'Front-end Developer|Back-end Developer|Support|Dev Evangelist/Advocate', 'Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin|Dev Evangelist/Advocate',
                                                'One-person shop|Front-end Developer|Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead', 
                                                'Dev Evangelist/Advocate|Support|Back-end Developer|Front-end Developer', 'Designer|Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin|Supervisor/Team Lead',
                                                'Designer|Front-end Developer|Back-end Developer|DevOps/SysAdmin|Other', 'One-person shop|Designer|Front-end Developer|Back-end Developer',
                                                'Designer|Front-end Developer|Back-end Developer|Sales|Supervisor/Team Lead', 'Front-end Developer|Back-end Developer|Dev Evangelist/Advocate',
                                                'Front-end Developer|Back-end Developer|Support|Supervisor/Team Lead','Supervisor/Team Lead|Front-end Developer|Back-end Developer|Dev Evangelist/Advocate',
                                                'Supervisor/Team Lead|DevOps/SysAdmin|Front-end Developer|Back-end Developer', 
                                                'DevOps/SysAdmin|Back-end Developer|Front-end Developer|One-person shop', 'Dev Evangelist/Advocate|Front-end Developer|Back-end Developer|DevOps/SysAdmin',
                                                'Front-end Developer|Back-end Developer|DevOps/SysAdmin|Dev Evangelist/Advocate', 'Support|Front-end Developer|Back-end Developer',
                                                'Executive Leadership|Supervisor/Team Lead|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer',
                                                'Front-end Developer|Back-end Developer|Supervisor/Team Lead|Executive Leadership', 'Executive Leadership|Supervisor/Team Lead|Back-end Developer|Front-end Developer|Designer',
                                                'Front-end Developer|Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead|Executive Leadership', 
                                                'Executive Leadership|Back-end Developer|Front-end Developer', 'DevOps/SysAdmin|Support|Front-end Developer|Back-end Developer',
                                                'Supervisor/Team Lead|Dev Evangelist/Advocate|Back-end Developer|Designer|Front-end Developer', 'Supervisor/Team Lead|Support|Front-end Developer|Back-end Developer',
                                                'Front-end Developer|Back-end Developer|Dev Evangelist/Advocate|Supervisor/Team Lead', 'Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin|Executive Leadership',
                                                'DevOps/SysAdmin|Designer|Front-end Developer|Back-end Developer', 'Front-end Developer|Back-end Developer|Other',
                                                'Supervisor/Team Lead|Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin', 'Supervisor/Team Lead|Support|Back-end Developer|Front-end Developer',
                                                'Support|Back-end Developer|Front-end Developer|One-person shop', 'DevOps/SysAdmin|Support|Back-end Developer|One-person shop|Front-end Developer',
                                                'Dev Evangelist/Advocate|DevOps/SysAdmin|Designer|Front-end Developer|Back-end Developer', 'Support|Back-end Developer|Front-end Developer|Designer',
                                                'Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|One-person shop', 'Supervisor/Team Lead|Front-end Developer|Back-end Developer|DevOps/SysAdmin|Dev Evangelist/Advocate'], 
                                                value = "Full-Stack Developer", inplace = True)
survey_2016['work_position'].replace(to_replace = ['Supervisor/Team Lead', 'DevOps/SysAdmin|One-person shop', 
                                                'Supervisor/Team Lead|Dev Evangelist/Advocate|Back-end Developer|Front-end Developer', 'Supervisor/Team Lead|Support|Back-end Developer',
                                                'Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer',
                                                'Supervisor/Team Lead|Back-end Developer','Supervisor/Team Lead|DevOps/SysAdmin|Support|Back-end Developer', 'Supervisor/Team Lead|Other',
                                                'Supervisor/Team Lead|Back-end Developer|Front-end Developer', 'Supervisor/Team Lead|Back-end Developer|Front-end Developer|One-person shop',
                                                'Supervisor/Team Lead|DevOps/SysAdmin', 'DevOps/SysAdmin', 'Supervisor/Team Lead|Back-end Developer|One-person shop',
                                                'Supervisor/Team Lead|Dev Evangelist/Advocate|Back-end Developer', 'Back-end Developer|DevOps/SysAdmin|Dev Evangelist/Advocate|Supervisor/Team Lead',
                                                'Front-end Developer|Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead','Supervisor/Team Lead|Back-end Developer|DevOps/SysAdmin|Dev Evangelist/Advocate',
                                                'Supervisor/Team Lead|Front-end Developer|Back-end Developer|DevOps/SysAdmin', 'Supervisor/Team Lead|Back-end Developer|Front-end Developer|Designer',
                                                'Dev Evangelist/Advocate|DevOps/SysAdmin', 'Support|Back-end Developer|Front-end Developer',
                                                'DevOps/SysAdmin|Supervisor/Team Lead', 'Supervisor/Team Lead|DevOps/SysAdmin|Support', 'DevOps/SysAdmin|Front-end Developer|Back-end Developer',
                                                'Designer|Front-end Developer|Back-end Developer|Supervisor/Team Lead|Executive Leadership', 'Supervisor/Team Lead|Support|One-person shop|Designer|Front-end Developer|Sales',
                                                'One-person shop|DevOps/SysAdmin','One-person shop|Designer|Front-end Developer|Back-end Developer|Dev Evangelist/Advocate|Supervisor/Team Lead',
                                                'DevOps/SysAdmin|Support|Sales|Front-end Developer|Designer|One-person shop', 'One-person shop|Designer|Sales|Support|Supervisor/Team Lead',
                                                'DevOps/SysAdmin|Back-end Developer|Front-end Developer'], 
                                                value = "Team Lead", inplace = True)
survey_2016['work_position'].replace(to_replace = ['DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|Designer',
                                                'Support|Back-end Developer|One-person shop', 'Supervisor/Team Lead|Support|Back-end Developer', 'Support|Other',
                                                'Support', 'One-person shop|Designer|Front-end Developer|Support', 'Dev Evangelist/Advocate|Support', 
                                                'Dev Evangelist/Advocate|Back-end Developer|Support', 'Support|Back-end Developer', 'DevOps/SysAdmin|Support',
                                                'Supervisor/Team Lead|Support', 'Support|DevOps/SysAdmin', 'DevOps/SysAdmin|Support|One-person shop', 'Support|Sales|Designer'], 
                                                value = "Support Team", inplace = True)
survey_2016['work_position'].replace(to_replace = ['Executive Leadership', 'Other|Executive Leadership', 'One-person shop',
                                                'Executive Leadership|Front-end Developer|Back-end Developer|Sales|Supervisor/Team Lead',
                                                'Front-end Developer|Back-end Developer|Executive Leadership', 'Executive Leadership|Supervisor/Team Lead|Back-end Developer',
                                                'Front-end Developer|Back-end Developer|Sales|Executive Leadership', 'Executive Leadership|Supervisor/Team Lead',
                                                'Executive Leadership|DevOps/SysAdmin|Back-end Developer', 'Executive Leadership|DevOps/SysAdmin|Back-end Developer|Support',
                                                'DevOps/SysAdmin|Executive Leadership', 'Executive Leadership|Dev Evangelist/Advocate', 'Support|HR|Supervisor/Team Lead|Executive Leadership',
                                                'One-person shop|DevOps/SysAdmin|Executive Leadership', 'DevOps/SysAdmin|Dev Evangelist/Advocate|Supervisor/Team Lead|Executive Leadership',
                                                'One-person shop|Back-end Developer|Sales|DevOps/SysAdmin|Executive Leadership', 'Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead|Other',
                                                'Supervisor/Team Lead|Executive Leadership', 'One-person shop|Back-end Developer|Sales|Support|Supervisor/Team Lead|Executive Leadership',
                                                'Executive Leadership|Supervisor/Team Lead|Sales', 'Executive Leadership|Supervisor/Team Lead|Designer', 
                                                'Executive Leadership|Supervisor/Team Lead|Front-end Developer|Back-end Developer', 'Support|Sales|Back-end Developer|Front-end Developer|Designer|One-person shop',
                                                'One-person shop|Designer|Sales|Executive Leadership', 'Executive Leadership|Supervisor/Team Lead|Front-end Developer',
                                                'One-person shop|Front-end Developer|Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead|Executive Leadership',
                                                'Back-end Developer|DevOps/SysAdmin|Supervisor/Team Lead|Executive Leadership'], 
                                                value = "CXO", inplace = True)
survey_2016['work_position'].replace(to_replace = ['Designer', 'One-person shop|Designer', 'Designer|Support|Supervisor/Team Lead', 'Support|Designer',
                                                'Designer|One-person shop', 'Front-end Developer|Designer|One-person shop', 'Supervisor/Team Lead|Designer',
                                                'Designer|Supervisor/Team Lead', 'DevOps/SysAdmin|Designer'], 
                                                value = 'Designer', inplace = True)
survey_2016['work_position'].replace(to_replace = ['Sales', 'Supervisor/Team Lead|Sales', 'Sales|Support|DevOps/SysAdmin|Executive Leadership', 
                                                'One-person shop|Designer|Support', ], 
                                                value = 'Sales Team', inplace = True)
survey_2016['work_position'].replace(to_replace = ['HR', 'Other|HR', 'HR|Supervisor/Team Lead|Executive Leadership', 'HR|Dev Evangelist/Advocate|Sales', 'Supervisor/Team Lead|DevOps/SysAdmin|HR',
                                                ], 
                                                value = 'HR Team', inplace = True)
survey_2016['work_position'].replace(to_replace = ['Other', 'One-person shop|Back-end Developer|Sales|Support|DevOps/SysAdmin|Dev Evangelist/Advocate|Supervisor/Team Lead|Executive Leadership|Other',
                                                'Executive Leadership|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer',
                                                'Other|Supervisor/Team Lead|Support|Back-end Developer|Designer', 'Other|Executive Leadership|Supervisor/Team Lead|Back-end Developer',
                                                'Executive Leadership|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Back-end Developer|Front-end Developer',
                                                'Other|Back-end Developer|Front-end Developer|Designer','Other|Back-end Developer|Front-end Developer|Designer', 
                                                'Other|Supervisor/Team Lead|Back-end Developer|One-person shop', 'Dev Evangelist/Advocate',
                                                'Other|Back-end Developer|Front-end Developer', 'Other|Support', 'Supervisor/Team Lead|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|Designer',
                                                'Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Designer|Front-end Developer', 
                                                'One-person shop|Front-end Developer|Back-end Developer|Supervisor/Team Lead|Executive Leadership', 
                                                'Other|Dev Evangelist/Advocate|Sales|Back-end Developer|Front-end Developer', 'Other|Front-end Developer|Back-end Developer|Sales|DevOps/SysAdmin|Dev Evangelist/Advocate',
                                                'One-person shop|Back-end Developer|Other', 'Other|Executive Leadership|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Back-end Developer|One-person shop',
                                                'One-person shop|Back-end Developer|DevOps/SysAdmin|Dev Evangelist/Advocate|Other', 'Other|Supervisor/Team Lead|Back-end Developer|Front-end Developer', 
                                                'Other|Dev Evangelist/Advocate|One-person shop', 'Other|Back-end Developer|Front-end Developer|One-person shop', 
                                                'Other|One-person shop|Back-end Developer|Sales|Support|DevOps/SysAdmin|Dev Evangelist/Advocate|Supervisor/Team Lead',
                                                'One-person shop|Front-end Developer|Back-end Developer|Sales|Support|DevOps/SysAdmin',
                                                'DevOps/SysAdmin|Support|Sales|One-person shop|Designer|Front-end Developer|Back-end Developer',
                                                'Executive Leadership|Supervisor/Team Lead|HR|DevOps/SysAdmin|Support|Sales|Back-end Developer|One-person shop|Designer|Front-end Developer',
                                                'Other|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|One-person shop',
                                                'Other|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer', 'Other|Front-end Developer|Designer',
                                                'Other|Dev Evangelist/Advocate|Back-end Developer|Front-end Developer', 'DevOps/SysAdmin|Other',
                                                'Other|Executive Leadership|Supervisor/Team Lead|HR|Support|Sales|Designer|One-person shop',
                                                'Executive Leadership|One-person shop|Front-end Developer|Back-end Developer|Support|Supervisor/Team Lead',
                                                'Other|Support|Back-end Developer|Front-end Developer|Designer', 'Other|Designer|Front-end Developer', 
                                                'Other|Front-end Developer', 'Other|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|Designer|One-person shop',
                                                'One-person shop|Other', 'Designer|Front-end Developer|Back-end Developer|Executive Leadership|Other',
                                                'Front-end Developer|Back-end Developer|Sales|Support|DevOps/SysAdmin|Supervisor/Team Lead|Executive Leadership', 
                                                'One-person shop|Front-end Developer|Back-end Developer|Support|Other', 'One-person shop|Designer|Front-end Developer|Back-end Developer|Sales|Support',
                                                'Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Designer|Front-end Developer',
                                                'Other|DevOps/SysAdmin|Support|Back-end Developer', 'Other|One-person shop', 'Executive Leadership|Other',
                                                'One-person shop|Designer|Front-end Developer|Back-end Developer|Support|DevOps/SysAdmin|Other', 
                                                'Other|Dev Evangelist/Advocate|Support', 'Executive Leadership|Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Front-end Developer|One-person shop',
                                                'Other|DevOps/SysAdmin|Back-end Developer', 'Other|Back-end Developer|Supervisor/Team Lead', 'Other|Dev Evangelist/Advocate',
                                                'Back-end Developer|Supervisor/Team Lead|Other', 'Other|Supervisor/Team Lead|Front-end Developer', 'Other|Supervisor/Team Lead' 'DevOps/SysAdmin|Designer',
                                                'Front-end Developer|Back-end Developer|Support|Other', 'Executive Leadership|Supervisor/Team Lead|Support|Sales|Designer|Front-end Developer|Back-end Developer',
                                                'Other|Supervisor/Team Lead|DevOps/SysAdmin|Back-end Developer|Support', 'Other|Front-end Developer|Designer|One-person shop'
                                                'DevOps/SysAdmin|Support|Sales|Front-end Developer|Designer|One-person shop', 'Other|Supervisor/Team Lead|Dev Evangelist/Advocate|DevOps/SysAdmin|Support|Back-end Developer|Front-end Developer|One-person shop',
                                                'Other|One-person shop|Designer|Front-end Developer|Back-end Developer|Support|Supervisor/Team Lead', 
                                                'Other|Supervisor/Team Lead|DevOps/SysAdmin|Support|Front-end Developer|Back-end Developer', 'Other|One-person shop|Designer|Front-end Developer',
                                                'Other|One-person shop|Designer|Front-end Developer', 'Designer|Front-end Developer|Back-end Developer|Other', 'Other|Supervisor/Team Lead|Dev Evangelist/Advocate',
                                                'Other|Supervisor/Team Lead', 'Other|Front-end Developer|Designer|One-person shop', ], 
                                                value = 'Other', inplace = True)

# Max age is 323, min age is 3.
# There are only 5 people that have weird ages (3yo, 15yo, or 99yo or 323 yo.) 
# These people will take the average age of the dataset (the correct calculated one, w/out outliers)
mean_age = survey_2016[(survey_2016['age'] >= 18) | (survey_2016['age'] <= 75)]['age'].mean()
survey_2016['age'].replace(to_replace = survey_2016[(survey_2016['age'] < 18) | (survey_2016['age'] > 75)]['age'].tolist(),
                        value = mean_age, inplace = True)

# The survey has 1433 rows, so first we will drop all columns where more than half of the observations have missing values
cols = (survey_2016.isna().sum() >= survey_2016.shape[0]/2).tolist()
to_drop = survey_2016.columns[cols]
survey_2016.drop(labels = to_drop, axis = 1, inplace = True)

# Dealing with other missing values
from sklearn.impute import SimpleImputer

# Impute nan with the most frequent value (mode) on every row
imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
imp.fit(survey_2016)
imp_data = pd.DataFrame(data = imp.transform(survey_2016), columns = survey_2016.columns)

# for i in imp_data.columns:
#     print(i,':')
#     print(imp_data[i].nunique())
#     print(imp_data[i].unique())


imp_data.to_csv(data_path)