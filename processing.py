import pandas as pd
import numpy as np

df = pd.read_csv('athlete_events.csv')
regions_df = pd.read_csv('noc_regions.csv')


df = df[df['Season'] == 'Summer']


df = df.merge(regions_df, on='NOC', how='left')


df.drop_duplicates(inplace=True)


medal_dummies = pd.get_dummies(df['Medal'])
df = pd.concat([df, medal_dummies], axis=1)

 
df[['Gold', 'Silver', 'Bronze']] = df[['Gold', 'Silver', 'Bronze']].fillna(0).astype(int)

medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
medal_tally=medal_tally.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
# print(medal_tally)


temp_df=df.dropna(subset=['Medal'])
temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
new_df=temp_df[temp_df['region']=='india']
final_df=new_df.groupby('Year').count()['Medal'].reset_index()

