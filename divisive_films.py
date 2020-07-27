
#What are the most divisive films according to the user score on IMDb?
#Find the movies with the highest variance in user rating
#		Which actors star in divisive films?
#		Which genres are divisive?


import requests
from bs4 import BeautifulSoup
import numpy as np

#start with the url of the main page of the movie we are analysing
links_to_ratings = []
for i in range(1,9951,50):
	try:
		response = requests.get('https://www.imdb.com/search/title/?title_type=feature&year=1970-01-01,2020-07-10&sort=num_votes,desc&start=' + str(i))
		soup = BeautifulSoup(response.text, 'html.parser')
		links = soup.find_all(class_ ='lister-item-header')
		links_to_ratings += [i.contents[3]['href'] for i in links]
	except:
		print(i)

np.savetxt('movie_url_extentions.csv',links_to_ratings, delimiter = ',',fmt = '%s')

print(links_to_ratings)

