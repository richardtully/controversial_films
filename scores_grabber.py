import requests
from bs4 import BeautifulSoup
import pandas as pd
from ast import literal_eval
import matplotlib.pyplot as plt


n = 0
# This accepts an IMDb '/ratings' page and returns a list of the number of votes each rating from one to ten the film in question received
def scores_grabber(movie_code):
	global n
	n+=1
	print(n)
	try:
		response = requests.get('https://www.imdb.com' + movie_code + 'ratings')
	#Viewed 	#print(response.text)
		soup = BeautifulSoup(response.text, 'html.parser')

		table = soup.find(name = 'table', )

		scores = table.find_all('div', class_ = "leftAligned")
		scores = [int(i.string.replace(',','')) for i in scores[1:]]
		return scores

	except:
		print('Couldnt grab the scores for this movie: ' + movie_code)
		return None

	# print(scores)
	
# I *think* i've calculated this correctly...
def calculate_variance(scores): 
	if scores == None:
		return 'Error'
	scores.reverse()

	total = sum(scores)

	average = sum([scores[i]*(i+1) for i in range(10)])/total

	variance = sum([scores[i]/total * (i+1 - average)**2 for i in range(10)])

	# print(variance)
	return variance

def calculate_average(scores):
	total = sum(scores)
	return sum([(scores[i]/total)*(i+1) for i in range(10)])
		




df = pd.read_csv('IMDb_ratings_csv.csv', nrows = 10000)

# df['score distribution'] = [scores_grabber(row['URL extention']) for index, row in df.iterrows()]
# df['variance'] = [calculate_variance(literal_eval(row['score distribution'])) for index, row in df.iterrows()]
df['total_votes'] = [sum(literal_eval(row['score distribution'])) for index, row in df.iterrows()]
df['mean_vote'] = [calculate_average(literal_eval(row['score distribution'])) for index, row in df.iterrows()]

print(df.head(5))

df.to_pickle('IMDb_ratings.pkl')
df.to_csv('IMDb_ratings_csv.csv')
plt.scatter(df['mean_vote'], df['variance'], marker = '.')
plt.xlabel('mean_vote')
plt.ylabel('variance')
plt.suptitle('Data from the 10,000 most voted for IMDb movies')

plt.show()


# for index, row in df.iterrows():
# 	print(index, row['test'])