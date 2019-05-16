# Importing required libraries
import numpy as np
import pandas as pd

# Creating Path of data set
path = r'/home/abhishek/Data Analysis/Datasets/pandascric.csv'

# Reading Data from Data set
df = pd.read_csv(path)

# There are matches being played all around the world. Find the list of unique cities where matches are being played
# throughout the world.
cities = df['city'].unique()

# Find columns containing null values if any.
columns_null = df.isna().any()

# Matches are played throughout the world in different countries but they may or may not have multiple
# venues(stadiums where matches are played). Find the top 5 venues where the most matches are played.
top_five_venue = df['venue'].value_counts().head(5)


# Find out how the runs were scored that is the runs count frequency table( number of singles, doubles, boundaries,
# sixes etc were scored)
df2 = df[df['runs'] > 0]
run_frequency = df2['runs'].value_counts()

# IPL seasons are held every year now let's look at our data and extract how many seasons
# and which year were they played?
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['season'] = df['year'] - 2007
year = list(set(df['year']))
year.sort()
season = list(set(df['season']))
season.sort()
season_year = dict(zip(year, season))
for k, v in season_year.items():
    print("Season {} was played in year {}".format(v, k))
# Find out the total number of matches played in each season.
df3 = df.groupby('season')['match_code'].nunique()
for key, value in df3.iteritems():
    print('In Season {} {} were played'.format(key, value))


# Find the total number of runs scored in each season.
df4 = df.groupby('season')['runs'].sum()
for key, value in df4.iteritems():
    print('In Season {} {} runs were scored'.format(key, value))

# Teams who have scored more than 200+ runs. Show the top 10 results
high_scores=df.groupby(['match_code', 'inning','team1','team2'])['total'].sum().reset_index()
high_scores = high_scores[high_scores['total'] >= 200]
high_scores.nlargest(10, 'total')

# What are the chances of chasing 200+ target
high_scores1 = high_scores[high_scores['inning']==1]
high_scores2 = high_scores[high_scores['inning']==2]
high_scores1=high_scores1.merge(high_scores2[['match_code','inning', 'total']], on='match_code')
high_scores1.rename(columns={'inning_x':'inning_1','inning_y':'inning_2','total_x':'inning1_runs','total_y':'inning2_runs'},inplace=True)
high_scores1=high_scores1[high_scores1['inning1_runs']>=200]
high_scores1['is_score_chased']=1
high_scores1['is_score_chased'] = np.where(high_scores1['inning1_runs']<=high_scores1['inning2_runs'],
                                           'yes', 'no')
chances = high_scores1['is_score_chased'].value_counts()
print('The chances of chasing a target of 200+ in 1st innings are : \n' , chances[1]/14*100)

# Which team has the highest win count in their respective seasons ?
match_wise_data = df.drop_duplicates(subset = 'match_code', keep='first').reset_index(drop=True)
match_wise_data.groupby('year')['winner'].value_counts(ascending=False)