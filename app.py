#Import packages
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

sns.set_theme(style='whitegrid')

#Load in dataset
df = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_Microcourse_Visualization/main/Data/Georgia_COVID/Georgia_COVID-19_Case_Data.csv')
df
len(df)
df.shape

#Describe the variables
df.info()
list(df)
df['COUNTY'].value_counts()

df_counties = df['COUNTY'].value_counts()
df_counties.head(10)

#Transforming columns
df['DATESTAMP']

df['DATESTAMP_MOD'] = df['DATESTAMP']
print(df['DATESTAMP_MOD'].head(10))
print(df['DATESTAMP_MOD'].dtypes)

df['DATESTAMP_MOD'] = pd.to_datetime(df['DATESTAMP_MOD'])
df['DATESTAMP_MOD'].dtypes

df[['DATESTAMP', 'DATESTAMP_MOD']]

df['DATESTAMP_MOD_DAY'] = df['DATESTAMP_MOD'].dt.date
df['DATESTAMP_MOD_DAY']

df['DATESTAMP_MOD_YEAR'] = df['DATESTAMP_MOD'].dt.year
df['DATESTAMP_MOD_MONTH'] = df['DATESTAMP_MOD'].dt.month

df['DATESTAMP_MOD_YEAR']
df['DATESTAMP_MOD_MONTH'] 
df

df['DATESTAMP_MOD_MONTH_YEAR'] = df['DATESTAMP_MOD'].dt.to_period('M')
df['DATESTAMP_MOD_MONTH_YEAR'].sort_values()

df['DATESTAMP_MOD_WEEK'] = df['DATESTAMP_MOD'].dt.week
df['DATESTAMP_MOD_WEEK']

df['DATESTAMP_MOD_QUARTER'] = df['DATESTAMP_MOD'].dt.to_period('Q')
df['DATESTAMP_MOD_QUARTER'].sort_values()

df['DATESTAMP_MOD_DAY_STRING'] = df['DATESTAMP_MOD_DAY'].astype(str)
df['DATESTAMP_MOD_WEEK_STRING'] = df['DATESTAMP_MOD_WEEK'].astype(str)
df['DATETIME_STRING'] = df['DATESTAMP_MOD_MONTH_YEAR'].astype(str)

#Getting the counties required for analysis: Cobb, DeKalb, Fulton, Gwinnett, Hall
df['COUNTY']

countList = ['COBB', 'DEKALB', 'FULTON', 'GWINNETT', 'HALL']
countList

selectCounties = df['COUNTY'].isin(countList)
len(selectCounties)

#Getting the specific date/timestamp you want
#df = length ~90,000
#selectCounties = length 2,830
#selectCountytime= TBD

selectcountytime = selectCounties

selectcountytime['DATESTAMP_MOD_MONTH_YEAR']


selectCountTime_april2020 = selectcountytime[selectcountytime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04']
len(selectCountTime_april2020)

selectCountTime_may2020 = selectcountytime[selectcountytime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-05']
len(selectCountTime_may2020)

selectCountTime_aprilmay2020 = selectcountytime[(selectcountytime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-05')|(selectcountytime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04')]
len(selectCountTime_may2020)

selectCountTime_aprilmay2020.head(50)


#Creating the final df

finalDF = selectCountTime_aprilmay2020[[
    'COUNTY',
    'DATESTAMP_MOD',
    'DATESTAMP_MOD_DAY',
    'DATESTAMP_MOD_DAY_STRING',
    'DATETIME_STRING',
    'DATESTAMP_MOD_MONTH_YEAR',
    'C_New', 
    'C-Cum', 
    'H_New', 
    'H-Cum', 
    'D-New', 
    'D-Cum' 
]]
finalDF

#Looking at total COVID cases by month

finalDF_dropdups = finalDF.drop_duplicates(subset=['COUNTY', 'DATETIME_STRING'], keep='last')
finalDF_dropdups

pd.pivot_table(finalDF_dropdups, values='C_Cum', index=['COUNTY'], columns=['DATESTAMP_MOD_MONTH_YEAR'], aggfunc=np.sum)

vis1 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR',y='C_Cum', data=finalDF_dropdups)

vis2 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', hue='COUNTY', data=finalDF_dropdups)

plotly1 = px.bar(finalDF_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='group')
plotly1.show()

plotly2 = px.bar(finalDF_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='stack')
plotly2.show()

#Looking at total covid cases by day

daily = finalDF
daily
len(daily)

pd.pivot_table(daily, values='C_Cum', index=['COUNTY'], columns=['DATESTAMP_MOD_DAY'], aggfunc=np.sum)

pd.pivot_table(daily, values='C_Cum', index=['DATESTAMP_MOD_DAY'], columns=['COUNTY'], aggfunc=np.sum)

startdate = pd.to_datetime('2020-04-26').date()
enddate = pd.to_datetime('2020-05-09').date()

maskFilter = (daily['DATESTAMP_MOD_DAY'] >= startdate) & (daily['DATESTAMP_MOD_DAY'] <= enddate)
dailySpecific = daily.loc[maskFilter]
dailySpecific

dailySpecific[dailySpecific['COUNTY'] == 'FULTON']

vis3 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum')

vis4 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum', hue='COUNTY')

plotly3 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum', color='COUNTY')
plotly3.show()

plotly4 = px.bar(dailySpecific,
                 x='DATESTAMP_MOD_DAY',
                 y='H_New',
                 color='COUNTY',
                 barmode='group')
plotly4.show()

plotly4 = px.bar(dailySpecific,
                 x='DATESTAMP_MOD_DAY',
                 y='H_Cum',
                 color='COUNTY',
                 barmode='group')
plotly4.show()

dailySpecific['newHospandDeathCovid'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int) + dailySpecific['C_New'].astype(int)
dailySpecific['newHospandDeathCovid']

dailySpecific['newHospandDeath'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int)
dailySpecific['newHospandDeath']

plotly8 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='newHospandDeathCovid', color='COUNTY', title='Georgia 2020 COVID Data: Total New Hospitalizations, Deaths, and COVID cases by County', barmode='group', labels={'DATESTAMP_MOD_DAY': "Time (Month, Day, Year)", 'newHospandDeathCovid': "Total Count"})
plotly8.update_layout(xaxis=dict(tickmode='linear',type='category'))
plotly8.show()