import requests
from bs4 import BeautifulSoup
import pandas as pd
import threading
import traceback
import concurrent.futures


# This counter (referenced in the grab_scores function below) lets us keep track of how far through 
# the list of movie url's we are. 
n=0


def grab_scores(movie_code):
    '''
    Accepts: A URL extension leading to an imdb movie page
    Returns: A list representing the distribution of user ratings given to the film.
    '''
    global n
    n+=1
    print(n)
    try:
        response = requests.get('https://www.imdb.com' + movie_code + 'ratings')
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find(name = 'table', )
        scores = table.find_all('div', class_ = "leftAligned")
        scores = [int(i.string.replace(',','')) for i in scores[1:]]
        return scores
    except:
        print(traceback.format_exc())
        print('Couldnt grab the scores for this movie: ' + movie_code)
        return 'Error'


def grab_genres(movie_code):
    '''
    Accepts: A URL extension leading to an imdb movie page
    Returns: A list of genres assosiated with that film by IMDb
    '''
    response = requests.get('https://www.imdb.com' + movie_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    genres = soup.find('h4', string = 'Genres:')
    genres = genres.parent.text
    genres = genres.split('\n')[2:-1]
    result = []
    for i in genres:
        i = i.strip()
        i = i.split('\xa0')
        result.append(i[0])
    print(result)
    return result



def add_data_to_df(df_from_list):
    '''
    Accepts a part of a dataframe
    Returns a part of a dataframe with the scores and genres included
    '''
    df_from_list['scores'] = df_from_list['URL_extention'].apply(grab_scores)
    df_from_list['genres'] = df_from_list['URL_extention'].apply(grab_genres)
    return df_from_list
    #print(df_from_list)


# Create a dataframe from a csv that we created using another script
df = pd.read_csv('English_language_movie_url_extentions.csv', names = ['URL_extention'], nrows = 9950)


# Split the dataframe into a list of smaller dataframes
df_list = [df[i*995:(i+1)*995] for i in range(10)]


# Create an iterable of df parts. These parts include the scores that have been grabbed form IMDb.com
with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
    df_iterator = executor.map(add_data_to_df, df_list)

# Create a new dataframe composed of all the parts that have had the scores added
df = pd.DataFrame()
for df_part in df_iterator:
    df = df.append(df_part)

print(df)


# Un-comment the text underneath to overwrite the current saved files
# df.to_pickle('EL_IMDb_ratings.pkl') #EL = English Language
# df.to_csv('EL_IMDb_ratings_csv.csv')

