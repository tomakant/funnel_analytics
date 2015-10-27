
# coding: utf-8

# In[359]:

import pandas as pd
import beatbox as b
import numpy as np
from pandasql import *
import datetime as dt


# In[360]:

market_source = pd.read_csv("/Volumes/public/Marketing/Growth Marketing/Analytics/Weekly Attribution/Master Attribution Files/Leads_Source_Master.csv")
# market_source = pd.read_excel("/Volumes/public/Marketing/Growth Marketing/Analytics/Weekly Attribution/Master Attribution Files/Leads_Source_Master.csv"


# In[361]:

market_source.columns = ['Application ID', 'marketing_source']


# In[362]:

market_source.head()


# In[363]:

service = b.PythonClient()


# In[364]:

service = b.PythonClient()
service.login('nhan.nguyen@fundingcircle.com', '4!SurvivordZMer7R46ySy7NgXlpTsMZUx')


# In[365]:

query_result = service.query("Select Application_ID__c,Referral_Partner_Account_Owner__c,Status,Loan_Process_Started__c, Referral_Partners_eMail__c, Referrer_Name__c,Utm_Source__c,Lead_Closed_Reason__c,CreatedDate from lead where RecordType.Name = 'loan' ")


# In[366]:

records = query_result['records']
total_records = query_result['size']
query_locator = query_result['queryLocator']


# In[367]:

while query_result.done is False and len(records) < total_records:
    query_result = service.queryMore(query_locator)
    query_locator = query_result.queryLocator
    records = records + query_result['records']


# In[368]:

leads = pd.DataFrame(records)
leads.head()


# In[369]:

leads.columns


# In[370]:

initiated = ['Awaiting Completion of Personal Section','Awaiting Completion of Review','Awaiting Financials',
            'Completed', 'Submitted', 'Awaiting Other Info (supporting docs)', 'Awaiting Completion of Prequal',
            'Awaiting Completion of Business Section', 'Closed', 'Converted']
progressed = ['Closed', 'Converted']
leads['initiated'] = np.where(leads.Status.isin(initiated) == True,'Yes','No')
leads['progressed'] = np.where(leads.Status.isin(progressed) == True,'Yes', 'No')


# In[371]:

leads.groupby(['Status', 'initiated', 'progressed']).size()


# In[372]:

leads.to_csv('/Users/nhannguyen/Google Drive/Nhan Projects/FAR Analysis/leads.csv')


# In[373]:

leads.groupby('Lead_Closed_Reason__c').size()


# In[374]:

c1 = leads.Lead_Closed_Reason__c.str.lower().str.contains('fake') == False
c2 = leads.Lead_Closed_Reason__c.str.lower().str.contains('duplicate') == False
c3 = leads.initiated == 'Yes'
c4 = leads.progressed == 'Yes'

leads = leads[c1 & c2]

leads[c3 & c4].shape


# In[375]:

c1 = leads.CreatedDate.dt.year==2015
c2 = leads.CreatedDate.dt.month==10
leads_oct = leads[c1 & c2]
leads_oct.head()


# In[376]:

print leads_oct.Status.unique()

print leads_oct.Lead_Closed_Reason__c.unique()

leads_oct.Lead_Closed_Reason__c.value_counts()


# In[377]:

# Assign a date to anyone who submitted for eligibility
b1 = leads.Status.str.lower().str.contains('converted')
b2 = leads.Status.str.lower().str.contains('closed')
b3 = leads['Lead_Closed_Reason__c'].str.len()==0
b4 = leads.Lead_Closed_Reason__c.str.lower().str.contains('ineligible')
b5 = leads.Lead_Closed_Reason__c.str.lower().str.contains('decline') == True
b6 = leads.Lead_Closed_Reason__c.isnull()

# leads['Date_Submitted_for_Eligibility'] = pd.to_datetime(np.where((b1|b2)&(b3|b4|b5|b6),leads.CreatedDate, None))
leads['Date_Submitted_for_Eligibility'] = pd.to_datetime(np.where((b1|b2),leads.CreatedDate, None))
leads.head(15)


# In[378]:

sp = ['Nik Milanovic', 'Brian Shields']


# In[379]:

# c1 = leads.CreatedDate.isnull()
c1 = leads.Referral_Partners_eMail__c.str.len() == 0
c2 = leads.Referral_Partner_Account_Owner__c.isin(sp)
c3 = leads.Referral_Partners_eMail__c.isnull()
c4 = leads.Referral_Partners_eMail__c.str.contains('@fundingcircle.com')
c5 = leads.Referral_Partners_eMail__c.str.contains('ramcha')


# In[380]:

leads['channel_leads'] = np.where(c5, "",np.where(c2, "Strategic Partner",np.where( c1 | c4 , "Direct", "Referral Partner")))


# In[381]:

leads[leads.Referral_Partners_eMail__c.str.contains('@fundingcircle')]


# In[382]:

leads.groupby(['channel_leads', 'Referral_Partners_eMail__c','Referral_Partner_Account_Owner__c']).size()


# In[383]:

leads.head()


# In[384]:

query_result = service.query("Select o.opp_owner__c, RP_Type__c, Referral_Partner_Name_on_Account__c,Referral_Partner_Account_Owner__c,Loan_Request_Amount__c, Account.Name, StageName, Loan_Process_Started__c, Date_Awaiting_Completion_of_Bus_Section__c, Date_Awaiting_Completion_of_Per_Section__c, Date_Awaiting_Completion_of_Review__c, Date_Awaiting_Financials__c, Date_App_Assigned_to_AM__c, Date_Awaiting_Pre_UW__c, Date_Awaiting_Underwriter_Assignment__c, Date_Awaiting_Initial_Credit_Review__c, Date_Awaiting_Credit_Diligence_Call__c, Date_Awaiting_Conditional_Approval__c, Date_Awaiting_Verification_Documents__c, Date_Awaiting_Final_Approval__c, Date_L_Fully_Verified__c, Date_Awaiting_Listing_on_Marketplace__c, Date_L_Live_on_Marketplace__c, Date_L_Loan_Purchased__c, Date_L_Funded__c , Closed_Reason__c, Withdrawn_Reason__c, Ineligible_Reason__c, Decline_Codes__c,PreScreen_Decline__c, Amount, ID, Application_ID__c, Promo_Code__c, Utm_Tag__c, Utm_Source__c, Utm_Campaign__c, Case_Worker_Credit__r.Name, Case_Worker_Pre_Underwriting__r.Name, Referral_Partner_s_eMail__c, Fico_Score__c, Referrer_Name__c, Referrer_Description__c from Opportunity as o where RecordType.Name = 'loan'")


# In[385]:

records = query_result['records']
total_records = query_result['size']
query_locator = query_result['queryLocator']


# In[386]:

while query_result.done is False and len(records) < total_records:
    query_result = service.queryMore(query_locator)
    query_locator = query_result.queryLocator
    records = records + query_result['records']


# In[387]:

opps = pd.DataFrame(records)


# In[388]:

opps.Account = [x.Account.Name for x in records]

# rec.Case_Worker_Credit = [x.Case_Worker_Credit__r.Name for x in records]


# In[389]:

c1 = opps.Closed_Reason__c.astype(str).str.lower().str.contains('duplicate')
c2 = opps.Closed_Reason__c.astype(str).str.lower().str.contains('fake')
opps=opps[~c1 & ~c2]


# In[390]:

opps['Case_Worker_Credit'] = pd.DataFrame(opps.Case_Worker_Credit__r.to_dict()).T.Name
opps['Case_Worker_Pre_Underwriting'] = pd.DataFrame(opps.Case_Worker_Pre_Underwriting__r.to_dict()).T.Name


# In[391]:

opps.groupby(['Referral_Partner_Account_Owner__c','RP_Type__c']).size()


# In[392]:

sp = ['Nik Milanovic', 'Brian Shields']
opps_direct = [np.nan,'Internal', 'Other', 'Refinance']

#Direct
c1 = opps.RP_Type__c.isin(opps_direct)
c2 = opps.RP_Type__c.str.len()==0
c3 = opps.Application_ID__c.str.len()<>0


#Platform Partners
c4 = opps.RP_Type__c.str.contains('Platform')
c7 = opps.Referral_Partner_Account_Owner__c.isin(sp)

#Referral Partner

c6 = opps.Referral_Partner_s_eMail__c.str.contains("@fundingcircle.com")
c8 = opps.Referral_Partner_s_eMail__c.str.contains("\+broker")
c9 = opps.Referral_Partner_s_eMail__c.str.len()==0


# In[393]:

opps['channel_opps'] = np.where(c7|c4 & c3, "Strategic Partner",
                       np.where(((c1&~c8)|c2) & (c9|c6) & c3, "Direct", 
                       np.where((~c2&~c8)|(c2 & ~c6) , "Referral Partner",np.nan)))


# In[394]:

opps[c8].groupby(['channel_opps', 'RP_Type__c', 'Referral_Partner_s_eMail__c']).size()


# In[395]:

opps.groupby(['channel_opps', 'RP_Type__c']).size()


# In[396]:

opps.groupby(['channel_opps','RP_Type__c','Referral_Partner_s_eMail__c']).size()


# In[397]:

rep = pd.merge(leads,opps, how='left', left_on='Application_ID__c', right_on='Application_ID__c')
rep.shape


# In[398]:

report = pd.merge(rep, market_source, how='left', left_on='Application_ID__c', right_on='Application ID')


# In[399]:

report['channel'] = np.where(report.channel_opps.isnull(), report.channel_leads, report.channel_opps)


# In[400]:

c1 = report.Loan_Process_Started__c_x != report.Loan_Process_Started__c_y
c2 = report.Loan_Process_Started__c_y.isnull()


# In[401]:

report.columns.values


# In[402]:

c1 = report.Date_Awaiting_Financials__c.isnull()
c2 = report.FICO_Score__c < 620
c3 = report.FICO_Score__c.isnull()
c4 = report.FICO_Score__c.astype(str).str.len()==0
report['Date_App_Assigned_to_AM'] = np.where(c1|c2|c3|c4, None, report.Date_App_Assigned_to_AM__c)
report['Date_App_Assigned_to_AM'] = pd.to_datetime(report['Date_App_Assigned_to_AM'])


# In[403]:

report.info()


# In[404]:

report.head()
c1 = report.Date_L_Funded__c.notnull()
c2 = report.StageName <> 'Funded'
exclude = report[c1& c2]
report = report[report.Application_ID__c.isin(exclude.Application_ID__c) == False]


# In[405]:

conv_rate = pd.melt(report, id_vars=['Opp_Owner__c',
                                     'Referral_Partner_Account_Owner__c_y',
                                     'Referral_Partner_Name_on_Account__c',
                                     'Application_ID__c',
                                     'Account', 
                                     'CreatedDate',
                                     'Case_Worker_Credit',
                                     'Case_Worker_Pre_Underwriting',
                                     'channel',
                                    'marketing_source'],
value_vars = ['Date_App_Assigned_to_AM',
'Date_Awaiting_Completion_of_Bus_Section__c',
'Date_Awaiting_Completion_of_Per_Section__c',
'Date_Awaiting_Completion_of_PreQual__c',
'Date_Awaiting_Completion_of_Review__c',
'Date_Awaiting_Conditional_Approval__c',
'Date_Awaiting_Credit_Diligence_Call__c',
'Date_Awaiting_Final_Approval__c',
'Date_Awaiting_Financials__c',
'Date_Awaiting_Initial_Credit_Review__c',
'Date_Awaiting_Listing_on_Marketplace__c',
'Date_Awaiting_Pre_UW__c',
'Date_Awaiting_Underwriter_Assignment__c',
'Date_Awaiting_Verification_Documents__c',
'Date_L_Fully_Verified__c',
'Date_L_Funded__c',
'Date_L_Live_on_Marketplace__c',
'Date_L_Loan_Purchased__c'],
              var_name='Stage', value_name='Date')


# In[406]:

conv_rate.groupby(['Stage','channel']).size()


# In[407]:

# conv_rate.Stage = conv_rate.Stage.str.replace("Date_","")
# conv_rate.Stage = conv_rate.Stage.str.replace("__c","")
# conv_rate.Stage = conv_rate.Stage.str.replace("L_","")
# conv_rate.Stage = conv_rate.Stage.str.replace("_"," ")


# In[408]:

conv_rate.to_csv("/Users/nhannguyen/Google Drive/Nhan Projects/2015_02_04_Borrower_Funnel/conv_rate.csv")


# In[409]:

conv_rate.shape


# In[410]:

# df.replace({'a' : { 'Medium' : 2, 'Small' : 1, 'High' : 3 }})


# In[411]:

conv_rate.Stage = conv_rate.Stage.replace({'Date_Awaiting_Completion_of_Bus_Section__c':'03.Prequalified',
                         'Date_Awaiting_Completion_of_Per_Section__c':'04.Personal Section',
                         'Date_Awaiting_Completion_of_Review__c': '05.Completion of Review',
                         'Date_Awaiting_Financials__c': '06.Completed Online App',
                         'Date_App_Assigned_to_AM': '07.Assigned to AM',
                         'Date_Awaiting_Pre_UW__c': '08.Fully Submitted to Credit',
                         'Date_Awaiting_Underwriter_Assignment__c': '09.Submitted to UW',
                         'Date_Awaiting_Initial_Credit_Review__c': '10.Initial Credit Review',
                         'Date_Awaiting_Credit_Diligence_Call__c': '11.Credit Diligence Call',
                         'Date_Awaiting_Conditional_Approval__c': '12.Conditional Approval',
                         'Date_Awaiting_Verification_Documents__c':'13.Offered',
                         'Date_Awaiting_Final_Approval__c': '14.Final Approval',
                         'Date_L_Fully_Verified__c': '15.Fully Verified',
                         'Date_Awaiting_Listing_on_Marketplace__c': '16.Listing on Marketplace',
                         'Date_L_Live_on_Marketplace__c': '17.Listed',
                         'Date_L_Loan_Purchased__c': '18.Loan Purchased',
                         'Date_L_Funded__c': '19.Funded'})


# In[412]:

conv_rate.groupby('Stage').size()


# In[413]:

l0 = report[['Application_ID__c','Opp_Owner__c', 'Referral_Partner_Account_Owner__c_y',
             'Referral_Partner_Name_on_Account__c',
             'CreatedDate', 'channel', 'marketing_source']]
l0['Stage'] = '01.Initiated'
l0.rename(columns = {'CreatedDate': 'Date'}, inplace=True)
l0.shape


# In[414]:

c = report['Date_Submitted_for_Eligibility'].notnull()
l1 = report[['Application_ID__c','Opp_Owner__c', 'Referral_Partner_Account_Owner__c_y',
             'Referral_Partner_Name_on_Account__c',
             'Date_Submitted_for_Eligibility', 'channel', 'marketing_source']][c]
l1['Stage'] = '02.Submitted for Prequal'
l1.rename(columns = {'Date_Submitted_for_Eligibility': 'Date'}, inplace=True)
l1.shape


# In[415]:

c = conv_rate.Date.isnull()
l2 = conv_rate[['Opp_Owner__c',
'Referral_Partner_Account_Owner__c_y',
'Referral_Partner_Name_on_Account__c',
'Application_ID__c',
'Stage',
'Date',
'channel',
'marketing_source']][~c]


# In[416]:

lead_opp_time = pd.concat([l0,l1,l2],axis=0)


# In[417]:

lead_opp_time[lead_opp_time.Stage=="07.Assigned to AM"]


# In[418]:

lead_opp_time.to_csv('/Users/nhannguyen/Google Drive/Nhan Projects/2015_02_04_Borrower_Funnel/lead_opp_time.csv')


# In[419]:

loc_0 = report[['Application_ID__c','Opp_Owner__c','Referral_Partner_Account_Owner__c_y',
                'Referral_Partner_Name_on_Account__c',
                'CreatedDate', 'channel', 'marketing_source']]
loc_0['Stage'] = '01.Initiated'
loc_0.shape


# In[420]:

report['Date_Submitted_for_Eligibility'].shape


# In[421]:

c = report['Date_Submitted_for_Eligibility'].notnull()
loc_1 = report[['Application_ID__c','Opp_Owner__c','Referral_Partner_Account_Owner__c_y',
                'Referral_Partner_Name_on_Account__c',
                'CreatedDate', 'channel', 'marketing_source']][c]
loc_1['Stage'] = '02.Submitted for Prequal'
# loc_1.rename(columns = {'CreatedDate': 'Date'}, inplace=True)
loc_1.shape


# In[422]:

c = conv_rate.Date.notnull()
loc_2 = conv_rate[['Opp_Owner__c',
'Referral_Partner_Account_Owner__c_y',
'Referral_Partner_Name_on_Account__c',
'Application_ID__c',
'Stage',
'CreatedDate',
'channel',
'marketing_source']][c]


# In[423]:

lead_opp_cohort = pd.concat([loc_0,loc_1,loc_2],axis=0)
lead_opp_cohort.head()


# In[424]:

lead_opp_cohort.to_csv('/Users/nhannguyen/Google Drive/Nhan Projects/2015_02_04_Borrower_Funnel/lead_opp_cohort.csv')


# In[425]:

amounts = pd.melt(report, id_vars=['Opp_Owner__c',
                                   'Referral_Partner_Account_Owner__c_y',
                                   'Referral_Partner_Name_on_Account__c',
                                     'Application_ID__c',
                                     'Account', 
                                     'Date_L_Funded__c',
                                     'Case_Worker_Credit',
                                     'Case_Worker_Pre_Underwriting',
                                     'channel',
                                      'marketing_source',
                                      'StageName'],
value_vars = ['Amount', 'Loan_Request_Amount__c'],
              var_name='type', value_name='value')


# In[426]:

amounts.value = amounts.value.astype(float).fillna(0)
amounts.Date_L_Funded__c = pd.to_datetime(amounts.Date_L_Funded__c).fillna('1970-01-01 00:00:00')


# In[427]:

# amounts.value.value_counts(dropna=False)
c0 = amounts.Date_L_Funded__c.dt.year==2013
c1 = amounts.Date_L_Funded__c.dt.year==2014
c2 = amounts.Date_L_Funded__c.dt.year==2015
c3 = amounts.StageName.str.lower().str.contains('funded')
amounts_2013 = amounts[c0 & c3]
amounts_2014 = amounts[c1 & c3]
amounts_2015 = amounts[c2 & c3]
amts = pd.concat([amounts_2013, amounts_2014, amounts_2015])


# In[428]:

amts.to_csv('/Users/nhannguyen/Google Drive/Nhan Projects/2015_02_04_Borrower_Funnel/amounts.csv')


# In[429]:

report.columns.values[report.columns.str.lower().str.contains('date')]


# In[430]:

report.columns[report.columns.str.lower().str.contains('opp')]


# In[431]:

# c= report.Date_L_Funded__c.notnull()
delta = report[['Application_ID__c','Opp_Owner__c', 
                'Referral_Partner_Account_Owner__c_y',
             'Referral_Partner_Name_on_Account__c',
             'CreatedDate', 
            'Date_Submitted_for_Eligibility',
       'Date_App_Assigned_to_AM__c',
       'Date_Awaiting_Completion_of_Bus_Section__c',
       'Date_Awaiting_Completion_of_Per_Section__c',
       'Date_Awaiting_Completion_of_Review__c',
       'Date_Awaiting_Conditional_Approval__c',
       'Date_Awaiting_Credit_Diligence_Call__c',
       'Date_Awaiting_Final_Approval__c', 'Date_Awaiting_Financials__c',
       'Date_Awaiting_Initial_Credit_Review__c',
       'Date_Awaiting_Listing_on_Marketplace__c',
       'Date_Awaiting_Pre_UW__c',
       'Date_Awaiting_Underwriter_Assignment__c',
       'Date_Awaiting_Verification_Documents__c',
       'Date_L_Fully_Verified__c', 'Date_L_Funded__c',
       'Date_L_Live_on_Marketplace__c', 'Date_L_Loan_Purchased__c',
       'Date_App_Assigned_to_AM',
             'channel', 'marketing_source', 'StageName',
                'Case_Worker_Credit', 'Case_Worker_Pre_Underwriting']]
delta.Date_L_Funded__c = delta.Date_L_Funded__c.astype('datetime64[ns]')


# In[432]:

delta.columns


# In[433]:

delta.CreatedDate = pd.to_datetime(delta.CreatedDate)
delta.Date_Submitted_for_Eligibility = pd.to_datetime(delta.Date_Submitted_for_Eligibility)
delta.Date_App_Assigned_to_AM__c = pd.to_datetime(delta.Date_App_Assigned_to_AM__c)
delta.Date_Awaiting_Completion_of_Bus_Section__c = pd.to_datetime(delta.Date_Awaiting_Completion_of_Bus_Section__c)
delta.Date_Awaiting_Completion_of_Per_Section__c = pd.to_datetime(delta.Date_Awaiting_Completion_of_Per_Section__c)
delta.Date_Awaiting_Completion_of_Review__c = pd.to_datetime(delta.Date_Awaiting_Completion_of_Review__c)
delta.Date_Awaiting_Conditional_Approval__c = pd.to_datetime(delta.Date_Awaiting_Conditional_Approval__c)
delta.Date_Awaiting_Credit_Diligence_Call__c = pd.to_datetime(delta.Date_Awaiting_Credit_Diligence_Call__c)
delta.Date_Awaiting_Final_Approval__c = pd.to_datetime(delta.Date_Awaiting_Final_Approval__c )
delta.Date_Awaiting_Financials__c = pd.to_datetime(delta.Date_Awaiting_Financials__c)
delta.Date_Awaiting_Initial_Credit_Review__c = pd.to_datetime(delta.Date_Awaiting_Initial_Credit_Review__c)
delta.Date_Awaiting_Listing_on_Marketplace__c = pd.to_datetime(delta.Date_Awaiting_Listing_on_Marketplace__c)
delta.Date_Awaiting_Pre_UW__c = pd.to_datetime(delta.Date_Awaiting_Pre_UW__c)
delta.Date_Awaiting_Underwriter_Assignment__c = pd.to_datetime(delta.Date_Awaiting_Underwriter_Assignment__c)
delta.Date_Awaiting_Verification_Documents__c = pd.to_datetime(delta.Date_Awaiting_Verification_Documents__c)
delta.Date_L_Fully_Verified__c = pd.to_datetime(delta.Date_L_Fully_Verified__c )
delta.Date_L_Funded__c = pd.to_datetime(delta.Date_L_Funded__c)
delta.Date_L_Live_on_Marketplace__c = pd.to_datetime(delta.Date_L_Live_on_Marketplace__c )
delta.Date_L_Loan_Purchased__c = pd.to_datetime(delta.Date_L_Loan_Purchased__c)
delta.Date_App_Assigned_to_AM = pd.to_datetime(delta.Date_App_Assigned_to_AM)


# In[434]:

delta.dtypes
print delta.shape


# In[435]:

c1 = delta.Date_L_Funded__c.isnull()==True
c2 = delta.Date_L_Funded__c.dt.year<2013
c3 = delta.Date_Awaiting_Financials__c.notnull()

delta.Date_Awaiting_Financials__c.isnull()
delta.CreatedDate
delta.Date_App_Assigned_to_AM
delta['d_init_fund'] =  (delta.Date_L_Funded__c - delta.CreatedDate).astype('timedelta64[m]')/1440
delta['d_init_COA'] = (delta.Date_Awaiting_Financials__c - delta.CreatedDate).astype('timedelta64[m]')
delta['d_COA_AM'] = (delta.Date_App_Assigned_to_AM - delta.Date_Awaiting_Financials__c).astype('timedelta64[m]')
delta['d_AM_UWA'] = (delta.Date_Awaiting_Pre_UW__c - delta.Date_App_Assigned_to_AM).astype('timedelta64[m]')/1440
delta['d_UWA_UW'] = (delta.Date_Awaiting_Underwriter_Assignment__c - delta.Date_Awaiting_Pre_UW__c).astype('timedelta64[m]')/60
delta['d_UW_Offered'] = (delta.Date_Awaiting_Verification_Documents__c - delta.Date_Awaiting_Underwriter_Assignment__c).astype('timedelta64[m]')/1440
delta['d_Offered_Listed'] = (delta.Date_L_Live_on_Marketplace__c - delta.Date_Awaiting_Verification_Documents__c).astype('timedelta64[m]')/1440


# In[436]:

delta_2 = pd.melt(delta, 
                      id_vars=['Application_ID__c',
                                  'Opp_Owner__c', 
                                  'Referral_Partner_Account_Owner__c_y',
                                  'Referral_Partner_Name_on_Account__c',
                                  'channel', 
                                  'marketing_source',
                              'CreatedDate', 'StageName',
                               'Case_Worker_Credit', 
                               'Case_Worker_Pre_Underwriting'],
                      value_vars=['d_init_fund',
                                      'd_init_COA',
                                      'd_COA_AM', 
                                      'd_AM_UWA',
                                      'd_UWA_UW',
                                      'd_UW_Offered',
                                      'd_Offered_Listed'],
                         var_name = 'stage_delta', value_name = 'value_delta')


# In[437]:

delta_2.to_csv('/Users/nhannguyen/Google Drive/Nhan Projects/2015_02_04_Borrower_Funnel/delta.csv')


# In[438]:

delta.info()


# In[439]:

delta.describe()


# In[440]:

# df[['channel', 'time_delta']].groupby(lambda x: x.month)
# np.median(df.time_delta)


# In[441]:

report.Referral_Partner_s_eMail__c=report.Referral_Partner_s_eMail__c.fillna('blank')
report.Referral_Partner_s_eMail__c.value_counts(dropna=False)


# In[442]:

ref_1 = report[['Referral_Partner_Account_Owner__c_y','Decline_Codes__c']]


# In[443]:

from pandas import Series
ref_1.Decline_Codes__c.str.split(',').apply(Series,1).stack()


# In[444]:

dec = ref_1.Decline_Codes__c.apply(Series,1).stack()


# In[445]:

ref_1.index


# In[446]:

dec = dec.reset_index


# In[447]:

print '\uFFFFD'


# In[448]:

l = [
'658ccffb-fcee-44eb-a57a-479c5040d0de',
'c8a0909f-ecba-414f-bc0c-ed7291363a32'
]
report[report.Application_ID__c.isin(l)].T


# In[ ]:



