# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 20:31:28 2023

@author: Adeel
"""

import streamlit as st
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")
st.title('Olympic History Dashboard')


#st.header("Olympic History Dashboard")
st.subheader("Muhammad Adeel")

athlete = pd.read_csv("athlete_events.csv")
print(athlete)


athlete.info()

athlete.isnull().sum()

athlete['Age']=athlete['Age'].interpolate()

athlete['Weight'].fillna(athlete['Weight'].mean(),inplace=True)

athlete['Height'].fillna(athlete['Height'].median(),inplace=True)

athlete.isnull().sum()

athlete['Medal'].fillna("No Medal")#,inplace=True)

col6,col7,col8,col9=st.columns(4)
s=athlete['Name'].nunique()
col6.metric("Total:",s)



#subset gold
Gold=athlete[athlete['Medal']=='Gold']

q=Gold['Medal'].count()
col7.metric("gold",q)

#subset silver
Silver=athlete[athlete['Medal']=='Silver']

f=Silver['Medal'].count()
col8.metric("silver",f)

#subset bronze
Bronze=athlete[athlete['Medal']=='Bronze']

e=Bronze['Medal'].count()
col9.metric("bronze",e)








all_country = sorted(athlete['City'].unique())
selected_country = st.selectbox('Select Your Country', all_country)
subset_country = athlete[athlete['City']==selected_country]
st.dataframe(subset_country)



curr_count = athlete[athlete['City']==selected_country]['Name'].count()

participants= subset_country['Name'].nunique()
subset_gold = athlete[(athlete['City']== selected_country) & (athlete['Medal']=='Gold')]
gold=subset_gold['Medal'].count()
subset_silver = athlete[(athlete['City']== selected_country) & (athlete['Medal']=='Silver')]
silver=subset_silver['Medal'].count()
subset_bronze = athlete[(athlete['City']== selected_country) & (athlete['Medal']=='Bronze')]
bronze=subset_bronze['Medal'].count()
medal_won= athlete[(athlete['City']==selected_country) & (athlete['Medal']!='No Medal')]
medal_name= medal_won.groupby('Name')['Name'].count().sort_values(ascending=False).head()
Table= medal_won.groupby('Name')[['Medal']].count().sort_values(by='Medal', ascending= False).head(5)
season_medal=medal_won.groupby('Season')['Medal'].count().head(5)
Bar=medal_won.groupby('Name').agg(Total_Medals_Won=('Medal','count')).head(5)
Hist= medal_won['Age'].value_counts()



 
st.header('Olympics')

col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Participants', participants)
col2.metric('Gold Medals', gold)
col3.metric('Silver Medals',silver)
col4.metric('Bronze Medals', bronze)



with st.container():
    col10,col11,col12= st.columns(3)



#Line Chart


g=subset_gold.groupby('Year').agg(Gold=('Medal','count'))
s=subset_silver.groupby('Year').agg(Silver=('Medal','count'))
b=subset_bronze.groupby('Year').agg(Bronze=('Medal','count'))
line= pd.concat([g,s,b],1)
col10.header('Medals Win')
col10.line_chart(line)


#Bar chart

fig, ax=plt.subplots(figsize=(20,15))
ax= plt.barh(medal_name.index,medal_name.values, color='blue')
plt.xlabel('No of Medals')
col11.header('Top 5 Medal Winners')
col11.pyplot(fig)

# Table
col12.header('Hall of Fame')
col12.table(Table) 


with st.container():
    col13,col14,col15 = st.columns(3)
    fig=plt.figure(figsize=(20,15))
    sns.histplot(medal_won, x='Age',bins=10)
    col13.header('Medal vs Age')
    col13.pyplot(fig)
    
    gender= medal_won.groupby(['Medal','Sex'])['Sex'].count()
    fig1, ax1 = plt.subplots()
    ax1.pie(gender, labels = gender.index, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal') 
    col14.header('Gender-Wise Winners')
    col14.pyplot(fig1)
    
    figb = plt.figure(figsize=(15,10))
    sns.barplot(x=season_medal.index, y=season_medal.values, alpha=0.8)
    col15.header('Season Wins')
    col15.pyplot(figb)
