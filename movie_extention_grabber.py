import requests
from bs4 import BeautifulSoup
import numpy as np

'''
This script builds a list of IMDb url extensions (and can also save them as a CSV file).
The extension lead to the 10,000 most voted for movies with English listed as one of the languages.
These extensions are used elsewhere for webscraping.
'''

links_to_ratings = []
for i in range(1,9951,50):
	try:
		print(i)
		response = requests.get('https://www.imdb.com/search/title/?title_type=feature&primary_language=en&sort=num_votes,desc&start=' + str(i))
		soup = BeautifulSoup(response.text, 'html.parser')
		links = soup.find_all(class_ ='lister-item-header')
		links_to_ratings += [i.contents[3]['href'] for i in links]
	except:
		print('This version of i didnt work: '+str(i))

# Un-comment the text underneath to overwrite the current csv file of url extensions
# np.savetxt('English_language_movie_url_extentions.csv',links_to_ratings, delimiter = ',',fmt = '%s')

print(links_to_ratings)

