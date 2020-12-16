'''

READ ME

I wanted to know which films are the most divisive. I decided a good way to measure the divisiveness of a film 
would be by the variance in it's IMDb user ratings. 

I've used threading to avoid the script bottlenecking when it sends requests to IMDb's website. Instead of waiting
for IMDb to return information about a particular film before requesting info on the next one, the script
now sends many requests at the same time from seperate threads. This sped things up a great deal. 


'''