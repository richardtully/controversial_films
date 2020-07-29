import requests
from bs4 import BeautifulSoup
import pandas as pd
import threading
import traceback


n = 0
# This accepts an IMDb '/ratings' page and returns a list of the number of votes each rating from one to ten the film in question received
def scores_grabber(movie_code_df,results_list):
	# changed from accepting a string as the first argument to accepting a dataframe
	# the second argument was added because threading.Thread discards the returned result when it finishes calling the function
	for index, row in movie_code_df.iterrows():
		movie_code = row['URL extention']
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
			
			results_list.append(scores)
			# return scores

		except:
			print(traceback.format_exc())
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


df = pd.read_csv('movie_url_extentions.csv', names = ['URL extention'], nrows = 10000)

# split the dataframe into a list of smaller dataframes
df_list = [df[i*500:(i+1)*500] for i in range(20)]

# Create a pair of lists, one to contain all the thread objects and the other to contain the results from the threads
# We need to make a list to contain the results because threading.Thread will discard the value returned by the target function
threads_list = []
results_lists_list = []

for sub_df in df_list:
	results_lists_list.append([])

	# for each sub_df, spin up a thread which calls scores_grabber(sub_df,results_lists_list[-1])
	threads_list.append(threading.Thread(target=scores_grabber, args=(sub_df, results_lists_list[-1])))
	# We need to start the thread separately, after it has been made
	threads_list[-1].start()

for thread in threads_list:
	# for each thread, wait until that thread has completed before continuing with the rest of the code
	thread.join()
scores = [i for l in results_lists_list for i in l]
print(scores)
df['score distribution'] = scores

# df['score distribution'] = [scores_grabber(row['URL extention']) for index, row in df.iterrows()]
df['variance'] = [calculate_variance(row['score distribution']) for index, row in df.iterrows()]

# print(df.head(5))

df.to_pickle('IMDb_ratings.pkl')
df.to_csv('IMDb_ratings_csv.csv')



# for index, row in df.iterrows():
# 	print(index, row['test'])