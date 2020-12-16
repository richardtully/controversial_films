import pandas as pd


df = pd.read_pickle('EL_IMDb_ratings.pkl')
df.scores = df.scores.apply(lambda x: x[::-1] if type(x) == list else x)



def calculate_variance(scores):
    '''
    Accepts a list representing the number of 1,2...,10 star ratings a film has recieved
    Returns the variance of the score distribution
    '''
    if scores == 'Error':
        return 'Error'
    total = sum(scores)
    mean = sum([scores[i]*(i+1) for i in range(10)])/total
    variance = sum([scores[i]/total * (i+1 - mean)**2 for i in range(10)])
    return variance


def calculate_mean(scores):
    '''
    Accepts a list representing the number of 1,2...,10 star ratings a film has recieved
    Returns the mean of the score distribution
    '''
    if scores == 'Error':
        return 'Error'

    total = sum(scores)

    mean = sum([scores[i]*(i+1) for i in range(10)])/total
    return mean



def calculate_median(scores):
    '''
    Accepts a list representing the number of 1,2...,10 star ratings a film has recieved
    Returns the median of the score distribution
    '''
    if scores == 'Error':
        return 'Error'
    
    total = sum(scores)
    x = round(total/2,0)
    for i in range(10):
        if x > scores[i]:
            x -= scores[i]
        else:
            median = i+1
            break
    adjusted_median = median + x/scores[median-1]
    return median, adjusted_median


def calculate_ratios(scores):
    '''
    Accepts a list representing the number of 1,2...,10 star ratings a film has recieved 
    Returns a list of the fractions (of the total number of votes) of each (star) rating 
    '''
    if scores == 'Error':
        return 'Error'
    total = sum(scores)
    ratios = [scores[i]/total for i in range(10)]
    return ratios



def get_number(numbers, x):
    '''
    Accepts a list of 10 numbers and a number x from 1 to 10
    Returns the number at index x in the list
    '''
    if numbers == 'Error': # or numbers == None:
        return 'Error'
    return numbers[x]





df['votes'] = df.scores.apply(lambda x: sum(x) if type(x) != str else 'Error')

df['variance'] = df.scores.apply(calculate_variance)

df['median'], df['adjusted_median'] = zip(*df.scores.apply(calculate_median))

df['mean'] = df.scores.apply(calculate_mean)


df['ratios'] = df.scores.apply(calculate_ratios)

for i in range(1,11):
    df[str(i) + 'ratio'] = df.ratios.apply(get_number,x = (i-1))

for i in range(1,11):
    df[str(i) + 'score'] = df.scores.apply(get_number,x = (i-1))



df.to_csv('EL_IMDb_calculations.csv')
df.to_pickle('EL_IMDb_calculations.pkl')