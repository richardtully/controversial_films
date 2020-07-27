import requests
from bs4 import BeautifulSoup



# This accepts an IMDb '/ratings' page and returns a list of the number of votes each rating from one to ten the film in question received
def scores_grabber(movie_code):
	print(movie_code)
	response = requests.get('https://www.imdb.com' + movie_code + 'ratings')
#Viewed 	#print(response.text)
	soup = BeautifulSoup(response.text, 'html.parser')

	table = soup.find(name = 'table', )

	scores = table.find_all('div', class_ = "leftAligned")
	scores = [int(i.string.replace(',','')) for i in scores[1:]]

	print(scores)
	return scores

# I *think* i've calculated this correctly...
def calculate_variance(scores): 
	scores.reverse()

	total = sum(scores)

	average = sum([scores[i]*(i+1) for i in range(10)])/total

	variance = sum([scores[i]/total * (i+1 - average)**2 for i in range(10)])

	print(variance)
	return variance


with open('C:\\Users\\Richard\\Desktop\\Python\\controversial_films\\5001_most_popular_films_1970_to _2020_from_IMDb.txt', 'rt') as f:
	movie_list = f.read()
movie_list = movie_list.replace('\'','').replace(' ','').split(',')

for movie_code in movie_list:
	calculate_variance(scores_grabber(movie_code))


calculate_variance(scores_grabber('/title/tt2910274/'))