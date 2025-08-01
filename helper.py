# def medal_tally(df):
#     medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
#     medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
#     medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
#     return medal_tally
# import numpy as np
# def country_year_list(df):
#     years=df['Year'].unique().tolist()
#     years.sort()
#     years.insert(0,'Overall')

#     country=np.unique(df['region'].dropna().values).tolist()
#     country.sort()
#     country.insert(0,'Overall')

#     return years,country

# def fetch_medal_tally(df,year,country):
#      medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

#      flag=0
#      if year=="Overall" and country=="Overall":
#         temp_df=medal_df
#      if year=="Overall" and country != "Overall":
#         flag=1
#         temp_df=medal_df[medal_df['region']==country]
#      if year!="Overall" and country=="Overall":
#         temp_df=medal_df[medal_df['Year']==int(year)]
#      if year!="Overall" and country!="Overall":
#         temp_df=medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]

#      if flag==1: 
#       x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
#      else:
#         x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

#      x['total']=x['Gold']+x['Silver']+x['Bronze']

#      x = x.loc[:, ~x.columns.duplicated()]
#      return x

import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region', as_index=False)[['Gold', 'Silver', 'Bronze']].sum(numeric_only=True)
    medal_tally = medal_tally.sort_values('Gold', ascending=False).reset_index(drop=True)
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    years = df['Year'].dropna().unique().tolist()
    years = sorted(years)
    years.insert(0, 'Overall')
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')
    return years, countries

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    elif year == "Overall":
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif country == "Overall":
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year', as_index=False)[['Gold', 'Silver', 'Bronze']].sum(numeric_only=True)
        x = x.sort_values('Year')
    else:
        x = temp_df.groupby('region', as_index=False)[['Gold', 'Silver', 'Bronze']].sum(numeric_only=True)
        x = x.sort_values('Gold', ascending=False)
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x = x.loc[:, ~x.columns.duplicated()]
    return x

def participating_nations_over_time(df):
    nations_over_time=df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Edition','count':'No Of Countries'},inplace=True)
    # print(nations_over_time)
    return nations_over_time

def data_over_time(df,col ):
    nations_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Edition','count': col},inplace=True)
    # print(nations_over_time)
    return nations_over_time

def most_sucessful(df,sport):
    temp_df=df.dropna(subset=['Medal'])

    if sport!='Overall':
        temp_df=temp_df[temp_df['Sport']==sport]

    # x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    # x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    top_athletes = temp_df['Name'].value_counts().reset_index(name='Medal_Count')
    top_athletes.rename(columns={'index': 'Name'}, inplace=True)

    x = top_athletes.head(15).merge(df, on='Name', how='left')[
    ['Name', 'Medal_Count', 'Sport', 'region']].drop_duplicates('Name')

    return x

def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']== country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']== country]
    table=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return table

def most_sucessful_countrywise(df,country):
    temp_df=df.dropna(subset=['Medal'])

    # if sport!='Overall':
    temp_df=temp_df[temp_df['region']==country]

    # x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    # x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    top_athletes = temp_df['Name'].value_counts().reset_index(name='Medal_Count')
    top_athletes.rename(columns={'index': 'Name'}, inplace=True)

    x = top_athletes.head(15).merge(df, on='Name', how='left')[
    ['Name', 'Medal_Count', 'Sport', 'region']].drop_duplicates('Name')

    return x

def weight_v_height(df,sport):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    if sport !='Overall':
     temp_df=athlete_df[athlete_df['Sport']==sport]
     return temp_df
    else:
        return athlete_df
    
def  men_vs_women(df):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    men=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    final=men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)
    return final
