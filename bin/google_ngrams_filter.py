# This program parses French Google Ngrams data, extract lines containing given patterns (here prefixes denoting the high degree)
# then merge all lines into one dataframe for further processing (cleaning and so on, see 2.google_ngrams_processing.ipynb)
# You first have to download the files you are interested in (see : http://storage.googleapis.com/books/ngrams/books/datasetsv2.html)
# for example for super, download http://storage.googleapis.com/books/ngrams/books/googlebooks-fre-all-2gram-20120701-su.gz
# put then into the data_ngrams subfolder


import requests
import sys, csv,re, random, glob,os
import gzip
import pandas as pd


def read_google_ngram_to_df(filename='../data_ngrams/googlebooks-fre-all-1gram-20120701-u.gz', mindate=1899, daterange="1899-2009",query='.+'):
    ''' get google ngrams and store into df
    raw google ngrams are available here : s3://datasets.elasticmapreduce/ngrams/books/20120701/fre-all/1gram/data'
	format : ngram TAB year TAB match_count TAB volume_count NEWLINE
    '''
    data_columns = ['string', 'year', 'total_count','total_doc']   
    df= pd.read_csv(filename, compression='gzip', names = data_columns, usecols=['string', 'year', 'total_count'], header=None, sep='\t', error_bad_lines=False)
    # just keep lines without POS tag (_POS), with string corresponding to query and time span
    df2 = df[(df['string'].str.contains('^\w{3,15}(?:[\s-]+\w+){0,2}$')) & (df['string'].str.contains(query)) & (df['year'] > mindate)]
	# pivot the data so as to have years as columns and string (ngram) as row index
    df3 = df2.pivot_table(values='total_count', index='string', columns='year', fill_value=0) # index='string', aggfunc='mean'
    print(df3.head(100)) #
	# save it to csv
    #df3.to_csv(filename + daterange +'.cleaned.csv')
    return df3


# main 
# this program retrieve google 1gram, merge, clean the files and prepare the `google_ngrams_processing.ipynb` program 
mindate = 1799
maxdate = 2009
query =  '^(?:ultra|super|hyper|hypra|extra|méga|archi|maxi|supra)'
query_type='prefixes'
ngrams= [1,2,3]
lang='fre'
str_range = str(mindate) + "-" + str(maxdate)
path = '../data_ngrams'
#os.makedirs(path, exist_ok=False)

# read google ngrams files downloaded beforehand and merge them

for ngram in ngrams:
        files = glob.glob('../data_ngrams/googlebooks-' + lang + '-all-' + str(ngram) + "gram*[aehmsu].gz")
#        files2 = glob.glob('../data_ngrams/googlebooks-' + lang + '-all-' + str(ngram) + "gram*[aehmsu].gz" + str(mindate) + '-' + str(maxdate) + '.cleaned.csv')
        df = pd.DataFrame()
        print(files)
        for f in files:
            if os.path.isfile(path + '/' + f + str_range + ".cleaned.csv"):
                print("Already parsed file : " + f + str_range + ". Loading from cleaned csv file.")
                df2= pd.read_csv(path + '/' + f + str_range + '.cleaned.csv', header=0, sep=',', error_bad_lines=False)
                print("Current dataframe", df2.info())
                #print(df2.describe())
                df = df.append(df2)
                print("Global dataframe",df.info())
            else:
                print("parsing " +path + '/' +  f +  " and saving to " + f + str_range + ".cleaned.csv")
                df2 = read_google_ngram_to_df(f,mindate=1799,daterange=str_range, query=query)
                df = df.append(df2)
                print(df.info())
        # cleaning    
        df.dropna(axis=1, how='all',inplace=True)

        # remove lines with pos annotation
        df2 = df[~df.string.str.contains("_")]
        df2.set_index(['string']).to_csv( '../data/' + lang + '.' + query_type + '.' + str(ngram) + '.grams.' + str_range + '.csv') # .set_index(['string'])
        print(df.info())
print("You can now further process the dataset with google_ngram_processing.ipynb")