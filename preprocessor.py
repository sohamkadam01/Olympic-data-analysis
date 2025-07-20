import pandas as pd

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

def preprocess():
    global df, region_df

    df = df[df['Season'] == 'Summer']

    # Drop existing 'region' and 'notes' if they exist to prevent merge conflicts
    df = df.drop(columns=['region', 'notes'], errors='ignore')

    df = df.merge(region_df, on='NOC', how='left')
    df.drop_duplicates(inplace=True)

    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df
