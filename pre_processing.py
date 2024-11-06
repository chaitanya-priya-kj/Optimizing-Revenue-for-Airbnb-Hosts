import pandas as pd
import numpy as np

def pre_process_data(path):

    raw_data = pd.read_csv(path)

    raw_data.drop(columns=['Unnamed: 0','host_location'], inplace=True)
    raw_data['num_bookings'] = raw_data.groupby('listing_id')['listing_id'].transform('count')

    df_agg = raw_data.groupby('listing_id')['month'].agg(list).reset_index()
    df = pd.merge(raw_data, df_agg, on='listing_id', suffixes=('', '_booked'))
    df.drop(columns=['month'], inplace = True)

    df = df[df['zipcode'] != 0]
    df = df.loc[df.astype(str).drop_duplicates().index]

    df['num_amenities'] = df['amenities'].apply(lambda x: len(x.split(',')))

    return df

