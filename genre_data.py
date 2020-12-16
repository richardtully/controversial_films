
import pandas as pd
import numpy as np


df = pd.read_pickle('EL_IMDb_calculations.pkl')

df = df[df.scores != 'Error']



genres = ['Action','Adventure','Animation','Biography','Comedy','Crime',
'Drama','Family','Fantasy','Film-Noir','History','Horror','Music','Musical',
'Mystery','Romance','Sci-Fi','Sport','Thriller','War','Western']



genres_df = pd.DataFrame({'No. of films': [0 for i in range(len(genres))]}, index = genres)
genres_df['mean_rating'] = 0
genres_df['mean_rating'] = genres_df['mean_rating'].astype(float)
genres_df['average_variance'] = 0
genres_df['average_variance'] = genres_df['average_variance'].astype(float)
genres_df['var_of_ratings'] = 0
genres_df['var_of_ratings'] = genres_df['var_of_ratings'].astype(float)



for i in genres:
    mask = df.apply(lambda x: True if i in x['genres'] else False, axis = 1)
    specific_genre_df = df[mask]
    genres_df['No. of films'][i] = len(specific_genre_df)
    total = len(specific_genre_df)

    if total != 0:
        genres_df['mean_rating'][i] = sum([i for i in specific_genre_df['mean']])/total

        genres_df['average_variance'][i] = sum([i for i in specific_genre_df['variance']])/total

        

        total = sum([i for i in specific_genre_df['mean']])
        mean = genres_df['mean_rating'][i]
        variance = sum([(i-mean)**2 for i in specific_genre_df['mean']])/total
        genres_df['var_of_ratings'][i] = variance





print(genres_df)

genres_df.to_csv('EL_IMDb_genres.csv')
genres_df.to_pickle('EL_IMDb_genres.pkl')

