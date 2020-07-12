import requests
import sys, csv,re, random, glob,os
import numpy as np                               # vectors and matrices
import pandas as pd                              # tables and data manipulations
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns                            # more plots
from pandas.io import s3
from sklearn.metrics import mean_absolute_error

import gzip
import mysql.connector
from mysql.connector import Error


def plot_distribution(df, field,bins=100):
    plt.figure(figsize=(15,5))
    df.groupby([field]).count().plot(kind='hist',log=True, legend=False)
#    plt.hist(df[field], color = 'blue', edgecolor = 'black',log=True,
             #bins = [0,100,200,300,400,500,600,700, 800,900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
#             ) # int(100/ bins)
    
    # seaborn histogram
    #sns.distplot(df[field], hist=True, kde=False, 
    #             bins=int(180/ bins), color = 'blue',
    #             hist_kws={'edgecolor':'black'})
    # Add labels
    plt.title('Histogram of distribution of : ' + field)
    plt.xlabel('Figures')
    plt.ylabel('Number of elements') 
    plt.show()

def plot_absolute_counts(token, corpus='english', smoothing=0, start_year=1800, end_year=2000, log_scale=False, save=False, show=False):
    '''
    Valid corpora names are:
    'english', 'american english', 'british english', 'english fiction'
    'chinese', 'french', 'german', 'hebrew', 'italian', 'russian', 'spanish'
    
    
    '''
    # Load absolute counts of the totken
    absolute_counts = retrieve_absolute_counts(token, corpus, smoothing, start_year, end_year)

    years = range(start_year, start_year + len(absolute_counts))

    plt.rcParams['figure.figsize'] = (15,8)
    plt.rcParams['font.size'] = 10
    ax= plt.axes()
    if log_scale:
        ax.set_yscale('log')
    plt.plot(years, absolute_counts, label = '{}'.format(token))
    title = 'Absolute Counts of "{}" in the "{}" corpus with smoothing={}.'.format(token, corpus,smoothing)
    if log_scale:
        title += ' Log Scale.'
    plt.title(title)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)

    legend_title = ax.get_legend().get_title()
    legend_title.set_fontsize(15)
    if save==True:
        plt.savefig('./'+token + '_'+ corpus + '.png')
    if show == True:
        plt.show()
    plt.close()

def print_absolute_counts(token, corpus='english', smoothing=0, start_year=1800, end_year=2000):
    '''
    Prints out the absolute counts (instead of plotting them)
    Useful to get the exact 
    '''

    absolute_counts = retrieve_absolute_counts(token, corpus, smoothing, start_year, end_year)
    print ('Absolute Counts for: {}'.format(token))
    for i in range(len(absolute_counts)):
        print ('{}: {}'.format(start_year + i, int(absolute_counts[i])))




# plotMovingAverage(ads_anomaly, 4, plot_intervals=True, plot_anomalies=True)
def plotMovingAverage(series, window, plot_intervals=False, scale=1.96, plot_anomalies=False):

    """
        series - dataframe with timeseries
        window - rolling window size 
        plot_intervals - show confidence intervals
        plot_anomalies - show anomalies 
    """
    #matplotlib.rcParams.update({'font.size': 10})
    rolling_mean = series.rolling(window=window).mean()

    plt.figure(figsize=(15,5))
    plt.title(str(list(series)) + "\nMoving average\n window size = {}".format(window))
    plt.plot(rolling_mean, "g", label="Rolling mean trend")

    # Plot confidence intervals for smoothed values
    if plot_intervals:
        mae = mean_absolute_error(series[window:], rolling_mean[window:])
        deviation = np.std(series[window:] - rolling_mean[window:])
        lower_bond = rolling_mean - (mae + scale * deviation)
        upper_bond = rolling_mean + (mae + scale * deviation)
        plt.plot(upper_bond, "r--", label="Upper Bond / Lower Bond")
        plt.plot(lower_bond, "r--")
        
        # Having the intervals, find abnormal values
        if plot_anomalies:
            anomalies = pd.DataFrame(index=series.index, columns=series.columns)
            anomalies[series<lower_bond] = series[series<lower_bond]
            anomalies[series>upper_bond] = series[series>upper_bond]
            plt.plot(anomalies, "ro", markersize=10)
        
    plt.plot(series[window:], label="Actual values")
    plt.xticks(rotation='vertical')
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.show()


def vocabulary_growth(df):
    '''Plot vocabulary growth ie : volume of unique lexical units, new words, disappearing words and common words'''
    #df2 = df.filter(regex=("^....$"))
    #print(df2.head(3))
    print(df.T.head())
    df2 = df.filter(regex=("^[0-9]{4}$")).T
    df2['sum'] = df2.sum(axis=1)
    df2['cnt'] = df2.astype(bool).count(axis=1)
    #df2[]
    print(df2.head(10))
    df2['sum'].plot(kind='bar',grid=True)
    plt.show()
    df2['cnt'].plot(kind='bar',grid=True)
    plt.show()





# main 
# this program retrieve google 1gram, merge, clean the files and prepare the google_1gram_analysis.py program 
if os.path.isfile('fre-all_1gram.csv'):
    print("Loading the 1 gram big file...")
    df= pd.read_csv('fre-all_1gram.csv', header=0, sep=',', error_bad_lines=False, index_col=0)
else:
    print("Please first launch retrieve_google_1grams.py to generate fre-all_1gram.csv")
    exit()

print(df.info())
print("You can now analyze the dataset with google_1gram_analysis.py")
exit()

# vocabulary evolution
vocabulary_growth(df)

# load totals of tokens per corpus year
totals = load_total_counts(19,1900,2009)

# calculate relative frequency for each column

for i in range(1900,2009):
    df[str(i) + '_freqrel'] = (df[str(i)] / totals[str(i)]) * 1000
    df[str(i) + '_freqrel'] = (df[str(i)] / totals[str(i)]) * 1000

print(df.info())
print(df.head(5))


# remove absolute frequency for df (relative frequency used for clustering and plotting)
#df = df.drop([str(i) for i in range(1900,2010)], axis=1)
#df.columns = df.columns.str.replace('_freqrel', '')
#df.to_csv('./fre-all_1gram_relfreq.csv')
#exit()

# total counts for years and years_freqrel
# df3['full_count'] = df3.apply(lambda x: x.sum(), axis=1)
#standard variation, mean, median,
df['total_count'] = df.filter(regex=("^....$")).apply(lambda x: x.sum(), axis=1)
df['total_rel_count'] = df.filter(regex=("_freqrel")).apply(lambda x: x.sum(), axis=1)
df['average'] = df.filter(regex=("_freqrel")).apply(lambda x: x.mean(), axis=1)
df['standard_dev'] = df.filter(regex=("_freqrel")).apply(lambda x: x.std(), axis=1)
#print(df2.sort_values('total_count', ascending=False )['total_count'].head(100))
print(df.sort_values('total_rel_count', ascending=False )['total_rel_count'].head(10))
print(df.sort_values('average', ascending=False )['average'].head(10))
print(df.sort_values('standard_dev', ascending=False )['standard_dev'].head(10))
#df2.to_csv('fre-all-statistics.csv')
print(df.describe())
df['standard_dev'].plot(kind='hist') # , bins=50
plt.show()
df['average'].plot(kind='hist')
plt.show()
#exit()

# plotting specific evolution for a given lexical unit
for i in range(1,10):
    plotMovingAverage(df.iloc[[random.randint(1,10000)]].T, 5, plot_intervals=True, plot_anomalies=True)

exit()
'''
        A note on python syntax
        
        The following three commands achieve exactly the same result:
        
        plot_absolute_counts('addicted to smoking')
        plot_absolute_counts('addicted to smoking', 'english', 0, 1800, 2000, True)
        plot_absolute_counts(token='addicted_to_smoking', corpus='english', smoothing=0, start_year=1800, end_year=2000, 
                             log_scale=True)
        
        The first one only passes the one necessary parameter (token) and uses defaults for everything else.
        The second one passes all parameters explicitly (token, corpus, smoothing, start/end year, log_scale). 
        For this to work, they need to be passed in the same order as they are declared in plot_absolute_counts
        The third command explicitly instantiates each parameter. It is the least ambiguous but also the most verbose version.
        
'''


#print(words)
#exit()
for w in words:
    plot_absolute_counts(w, 'french', smoothing=0, start_year=1900, end_year=2010, log_scale=True,save=True, show=False)