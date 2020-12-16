import matplotlib.pyplot as plt
import pandas as pd

# Uncomment one of the following:
df = pd.read_pickle('EL_IMDb_genres.pkl')

# df.loc[1245]['scores'] = 'Error'

# df = df[df.scores != 'Error']


plt.scatter(df['average_variance'], df['var_of_ratings'], marker = '.', s = 50)
plt.xlabel('1ratio')
plt.ylabel('variance')
plt.suptitle('Data from the 10,000 most voted for IMDb movies')

plt.show()


