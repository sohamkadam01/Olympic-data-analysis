import streamlit as st
import preprocessor as pd
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import  plotly.figure_factory as ff
df=pd.preprocess()
df = df.loc[:, ~df.columns.duplicated()]
st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://cdn.britannica.com/01/23901-050-33507FA4/flag-Olympic-Games.jpg')
user_menu=st.sidebar.radio('Select an Option',
('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)


# st.dataframe(df)

if user_menu =='Medal Tally':
    st.sidebar.header('Medal Tally')

    year,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",year)
    selected_country=st.sidebar.selectbox("Select Country",country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    if selected_year!='Overall' and selected_country=='Overall':
        st.title("Medal Tally in " + str(selected_year)+" olympics")
    if selected_year =='Overall' and selected_country!='Overall':
        st.title(selected_country+"  overall performance")
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country +"performance in "+ str(selected_year)+" olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 =st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3=st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    
    nations_over_time=helper.participating_nations_over_time(df)
    print(nations_over_time)
    fig=px.line(nations_over_time,x='Edition',y='No Of Countries')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')
    fig=px.line(events_over_time,x='Edition',y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athlete_over_time=helper.data_over_time(df,'Name')
    fig=px.line(athlete_over_time,x='Edition', y='Name')
    st.title("Atheletes over the years")
    st.plotly_chart(fig)



    st.title("No of events over time(Every Sport)")
    fig, ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_sucessful(df,selected_sport )
    st.table(x)

if user_menu=='Country-wise Analysis':
        st.title("Country-wise analysis")
        country_list=df['region'].unique().tolist()
        country_list = [str(item) for item in country_list]
        country_list.sort()

        selected_country=st.selectbox('Select a Country', country_list)
        country_df=helper.yearwise_medal_tally(df,selected_country)
        fig=px.line(country_df,x='Year',y='Medal')
        st.title(selected_country+" Medal tally over the year")
        st.plotly_chart(fig)

        st.title(selected_country+" excels in the following sports")
        pt=helper.country_event_heatmap(df,selected_country)
        fig, ax=plt.subplots(figsize=(20,20))
        if not pt.empty:
         ax=sns.heatmap(pt,annot=True)
         st.pyplot(fig)
        else:
            print("Heatmap data is empty for "+selected_country)
            st.header("No data available..!!")
        
        st.title("To 10 athletes of "+ selected_country)
        top10_df=helper.most_sucessful_countrywise(df,selected_country)
        st.table(top10_df)


if user_menu =='Athlete wise Analysis':
    athlete_df=df.drop_duplicates(subset=['Name','region'])

    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')   
    st.plotly_chart(fig)

    x=[]
    name=[]
    famous_sports=['Basketball','Judo','Football','Tug-Of-War','Athletics','Swimming','Badminton','Sailing','Gymnastics','Art Competitions','Handball','Weightlifting','Wrestling',
                   'Water Polo','Hockey','Rowing','Fencing','Shooting','Boxing','Taekwondo','Cycling','Diving','Canoeing','Tennis','Golf','Softball','Archery','Volleyball','Synchronized Swimming','Table Tennis','Baseball','Rhythmic Gymnastics',
                   'Rugby Sevens','Beach Volleyball','Triathlon','Rugby','Polo','Ice Hockey']
    
    for sport in famous_sports:
        temp_df=athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    print("x =", x)  
    filtered = [(data, label) for data, label in zip(x, name) if not data.empty]
    x_filtered, name_filtered = zip(*filtered) if filtered else ([], [])
    if x_filtered:
     fig=ff.create_distplot(x,name, show_hist=False,show_rug=False)
     fig.update_layout(autosize=False,width=1000,height=600)
     st.title('Distribution of Age wrt Sports')   
     st.plotly_chart(fig)
    else:
        print('No data to plot')
        st.header('No data available')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)

# Assuming helper.weight_v_height returns a DataFrame with columns:
# 'Weight', 'Height', 'Medal', and 'Sex'
    temp_df = helper.weight_v_height(df, selected_sport)

    fig, ax = plt.subplots()

# Use keyword arguments for scatterplot
    sns.scatterplot(
     data=temp_df,
     x='Weight',
     y='Height',
     hue='Medal',
     style='Sex',
     s=60,
     ax=ax
    )
    st.title('Height vs Weight')
    st.pyplot(fig)
    final=helper.men_vs_women(df)
    fig=px.line(final,x='Year',y=['Male','Female'])
    st.title('Men Vs Women')
    st.plotly_chart(fig)