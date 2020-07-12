#!/usr/bin/env python
# coding: utf-8

# # Etude des préfixes exprimant le haut degré dans Google Ngram (1800-2010)
# 
# liste des préfixes : ultra-, super-, supra-, hyper-, hypra-, sur-, extra-, méga-, giga-, archi-, maxi-
# 
# Dans ce travail, nous étudions d'abord les unigrammes (ie formes lexicales composées de l'un des préfixes), puis les bi-grammes (formes PREF-LEXIE ou PREF LEXIE).
# 

# In[1]:


import requests
import sys, csv,re, random, glob,os
import numpy as np                               # vectors and matrices
import pandas as pd                              # tables and data manipulations
import matplotlib.pyplot as plt
import matplotlib.pylab as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6
import matplotlib
import seaborn as sns                            # more plots
from sklearn.metrics import mean_absolute_error
from matplotlib.backends.backend_pdf import PdfPages


# # Chargement des stoplists

# In[331]:


stoplist={}
files = glob.glob("./stoplists/*.txt")
for file in files:
    with open(file, mode="r",encoding="utf8") as f:
        for line in f:
            if len(line.strip())>0:
                stoplist[line.strip()]=1
            
print("Stoplist chargée : " + str(len(stoplist)) + " mots.")


# # Récupération des 1-grams (sans annotation pos)

# In[452]:



if os.path.isfile('./fre.prefixes.1.grams.1799-2009.csv'):
    print("Loading the 1 gram big file (no pos)...")
    df= pd.read_csv('./fre.prefixes.1.grams.1799-2009.csv', header=0, sep=',', error_bad_lines=False)#, index_col=0 
else:
    print("Please first launch retrieve_google_1grams.py to generate fre.prefixes.1.grams.1799-2009.csv")
    exit()

# élimination stoplist
df = df[~df.string.isin(stoplist)]
df.info()
df.head()


# ## create double column (prefix - word)

# In[453]:


# 
pref_re = '^(ultra|super|hyper|hypra|extra|méga|archi|maxi|supra)(?:.*)$'
pref_re2 = '^(?:ultra|super|hyper|hypra|extra|méga|archi|maxi|supra)(.*)$'
df['prefix'] = df.string.str.extract(pref_re, expand=True)
df['word'] = df.string.str.extract(pref_re2, expand=True)
df['sep'] = 'FUSION'
print(df.info())
#print(df.head())
df.dropna(inplace=True)
df = df[~df.word.str.contains(r"\d")]
df = df[~df.word.str.contains(r"^sur.+")]
df = df[df.word.str.contains(r"^(|s|\w{3,})$")]
print(df.info())
print(df.head(10))


# In[454]:


columns = df.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]
df['full_count'] = df.apply(lambda x: x[periods].sum(), axis=1)
df.head()
df.to_csv("df.csv")


# 
# # Récupération des 2-grams (sans annotation pos)

# In[455]:



if os.path.isfile('./fre.prefixes.2.grams.1799-2009.csv'):
    print("Loading the 2 gram big file (no pos)...")
    df2= pd.read_csv('./fre.prefixes.2.grams.1799-2009.csv', header=0, sep=',', error_bad_lines=False)#, index_col=0 
else:
    print("Please first launch retrieve_google_2grams.py to generate fre.prefixes.2.grams.1799-2009.csv")
    exit()

    
# élimination stoplist
df2 = df2[~df2.string.isin(stoplist)]
df2.info()
df2.head()


# In[456]:


# colonnes préfix et word
pref_re = '^(ultra|super|hyper|hypra|extra|méga|archi|maxi|supra)\s+(?:\w{3,})$'
pref_re2 = '^(?:ultra|super|hyper|hypra|extra|méga|archi|maxi|supra)\s+(\w{3,})$'
df2['prefix'] = df2.string.str.extract(pref_re, expand=True)
df2['word'] = df2.string.str.extract(pref_re2, expand=True)
df2['sep'] = 'ESPACE'
print(df2.info())
print(df2.head())
df2.dropna(inplace=True)
df2 = df2[~df2.word.str.contains(r"\d")]
df2 = df2[df2.word.str.contains(r"^(|s|\w{3,})$")]
print(df2.info())
print(df2.head())


# In[460]:


columns = df2.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]
df2['full_count'] = df2.apply(lambda x: x[periods].sum(), axis=1)
df2.head()
df2.to_csv("df2.csv")


# 
# # Récupération des 3-grams (sans annotation pos)

# In[461]:



if os.path.isfile('./fre.prefixes.3.grams.1799-2009.csv'):
    print("Loading the 3 gram big file (no pos)...")
    df3= pd.read_csv('./fre.prefixes.3.grams.1799-2009.csv', header=0, sep=',', error_bad_lines=False)#, index_col=0 
else:
    print("Please first launch retrieve_google_3grams.py to generate fre.prefixes.3.grams.1799-2009.csv")
    exit()

# élimination stoplist
df3 = df3[~df3.string.isin(stoplist)]
df3.info()
df3.head()


# In[462]:


# colonnes préfix et word
pref_re = '^(ultra|super|hyper|hypra|extra|méga|archi|maxi|supra)\s+-\s+(?:\w{3,})$'
pref_re2 = '^(?:ultra|super|hyper|hypra|extra|méga|archi|maxi|supra)\s+-\s+(\w{3,})$'
df3['prefix'] = df3.string.str.extract(pref_re, expand=True)
df3['word'] = df3.string.str.extract(pref_re2, expand=True)
df3['sep'] = 'TIRET'
print(df3.info())
print(df3.head())
#print(df3[df3.isnull().any(axis=1)].head())
df3.dropna(inplace=True)
df3 = df3[~df3.word.str.contains(r"\d")]
df3 = df3[df3.word.str.contains(r"^(|s|\w{3,})$")]
print(df3.info())
print(df3.head())


# In[463]:


columns = df3.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]
df3['full_count'] = df3.apply(lambda x: x[periods].sum(), axis=1)
df3.head()
df3.to_csv("df3.csv")


# # Génération dataframe commun

# In[465]:


df4 = pd.concat([df,df2,df3],ignore_index=True)
print(df4.info())
print(df4.head)
df4.to_csv("df4.csv")


# # Generate dataframes with relative frequency

# In[466]:


# load yearly corpus stats (total words)
# compare with google stats per year
def load_total_counts(corpus_id, start_year, end_year):
    '''
    This function loads the total counts for a given corpus from Google's source data.
    '''
    # map from id to url
    id_to_url= {
    15: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-totalcounts-20120701.txt',
    17: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-us-all-totalcounts-20120701.txt',
    18: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-gb-all-totalcounts-20120701.txt',
    16: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-fiction-all-totalcounts-20120701.txt',
    23: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-chi-sim-all-totalcounts-20120701.txt',
    19: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-fre-all-totalcounts-20120701.txt',
    20: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-ger-all-totalcounts-20120701.txt',
    24: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-heb-all-totalcounts-20120701.txt',
    22: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-ita-all-totalcounts-20120701.txt',
    25: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-totalcounts-20120701.txt',
    21: 'http://storage.googleapis.com/books/ngrams/books/googlebooks-spa-all-totalcounts-20120701.txt'
    }
    hdr='Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0'
    headers={'User-Agent':hdr}
    resp = requests.get(id_to_url[corpus_id],headers=headers)
    resp.raise_for_status()
    response = resp.text
    #print(response)
    #response = urllib2.urlopen(urllib2.Request(id_to_url[corpus_id]))
    #total_counts = []
    total_counts2 = {}
    data = response.split("\t")
    for row in data:
        #print (row)
        #continue
        # first and last rows are empty, so a try...except is needed
        try:
            year, word_count, _, _ = row.split(',')
            #print(start_year)
            #print(end_year)
            #print(year)
            if int(year) >= start_year and int(year) <= end_year:
                #print(year)
                #print(word_count)
                #total_counts.append(int(word_count))
                total_counts2[year]=int(word_count)
                #print(total_counts)
        except ValueError:
            pass
        
    return total_counts2

# load totals of tokens per corpus year
totals = load_total_counts(19,1800,2009)
pd.DataFrame.from_dict(totals, orient='index').plot(title="Evolution de la taille des corpus entre 1800 et 2010")
#pdf0.savefig()
#plt.close()


# # now create rel version of every dataframe (df, df2, df3, df4)

# In[468]:


df_rel = df.copy(deep=True)
# load totals of tokens per corpus year
totals = load_total_counts(19,1800,2009)

# calculate relative frequency for each column

for i in range(1800,2010):
    df_rel[str(i) + '_freqrel'] = (df_rel[str(i)] / totals[str(i)]) * 1000

# remove absolute frequency for df (relative frequency used for clustering and plotting)
df_rel = df_rel.drop([str(i) for i in range(1800,2010)], axis=1)
df_rel.columns = df_rel.columns.str.replace('_freqrel', '')

print(df_rel.info())
print(df_rel.head(10))


# In[470]:


df2_rel = df2.copy(deep=True)
# load totals of tokens per corpus year
totals = load_total_counts(19,1800,2009)

# calculate relative frequency for each column

for i in range(1800,2010):
    df2_rel[str(i) + '_freqrel'] = (df2_rel[str(i)] / totals[str(i)]) * 1000

# remove absolute frequency for df (relative frequency used for clustering and plotting)
df2_rel = df2_rel.drop([str(i) for i in range(1800,2010)], axis=1)
df2_rel.columns = df2_rel.columns.str.replace('_freqrel', '')

print(df2_rel.info())
print(df2_rel.head(10))


# In[471]:


df3_rel = df3.copy(deep=True)

# calculate relative frequency for each column

for i in range(1800,2010):
    df3_rel[str(i) + '_freqrel'] = (df3_rel[str(i)] / totals[str(i)]) * 1000

# remove absolute frequency for df (relative frequency used for clustering and plotting)
df3_rel = df3_rel.drop([str(i) for i in range(1800,2010)], axis=1)
df3_rel.columns = df3_rel.columns.str.replace('_freqrel', '')

print(df3_rel.info())
print(df3_rel.head(10))


# In[472]:


df4_rel = df4.copy(deep=True)

# calculate relative frequency for each column

for i in range(1800,2010):
    df4_rel[str(i) + '_freqrel'] = (df4_rel[str(i)] / totals[str(i)]) * 1000

# remove absolute frequency for df (relative frequency used for clustering and plotting)
df4_rel = df4_rel.drop([str(i) for i in range(1800,2010)], axis=1)
df4_rel.columns = df4_rel.columns.str.replace('_freqrel', '')

print(df4_rel.info())
print(df4_rel.head(10))
df4_rel.to_csv("df4_rel.csv")


# # Génération synthèse

# In[473]:


# for moving average
# definition of plot for all measures
def plot_rolling(df,title, window=10):
    fig, ax = plt.subplots(3,figsize=(20, 10))
    ax[0].plot(df.index, df.data, label='raw data')
    ax[0].plot(df.data.rolling(window=window).mean(), label="rolling mean (window=10)");
    ax[0].plot(df.data.rolling(window=window).std(), label="rolling std (window=10)");
    ax[0].legend()

    ax[1].plot(df.index, df.z_data, label="de-trended data")
    ax[1].plot(df.z_data.rolling(window=window).mean(), label="rolling mean (window=10)");
    ax[1].plot(df.z_data.rolling(window=window).std(), label="rolling std (window=10)");
    ax[1].legend()

    ax[2].plot(df.index, df.zp_data, label="5 lag differenced de-trended data")
    ax[2].plot(df.zp_data.rolling(window=window).mean(), label="rolling mean (window=10)");
    ax[2].plot(df.zp_data.rolling(window=window).std(), label="rolling std (window=10)");
    ax[2].legend()
    fig.suptitle(title, fontsize=13)
    plt.tight_layout()
    fig.autofmt_xdate()


# In[476]:


# base for browsing prefixes
dist1 = df4.groupby('prefix')['full_count'].agg(['count','sum']).sort_values('count', ascending=False)
print(dist1)
print(dist1.index.values)
print(dist1.loc['maxi','count'])


# In[478]:


pdf2 = PdfPages('Prefix_all_noPOS_synthesis_googlengrams.pdf')
fig, ax = plt.subplots(1, figsize=(20, 15))
fig.text(4.25/8.5, 0.5/11., "Etude globale sur les mots fusionnées\nCorpus Google Ngrams (1800-2010)", ha='center', va='center', fontsize=24, )
fig.tight_layout()
pdf2.savefig()
plt.close()

columns = df4.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]

# distribution entre les prefixes
fig, ax = plt.subplots(2, figsize=(20, 15))
df4.groupby('prefix')['full_count'].count().plot(ax=ax[0],kind="bar",title='Distribution des fréquences entre préfixes (nbre de formations distinctes)', rot=45, figsize=(20,10))  # [['full_count']]
df4.groupby('prefix')['full_count'].sum().plot(ax=ax[1],kind="bar",title="Distribution des fréquences entre préfixes (nbre total d'occurrences)", rot=45, figsize=(20,10))  # [['full_count']]
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()

pdf2.savefig()
plt.close()
# evolution globale pour chaque préfixe
fig, ax = plt.subplots(3, figsize=(20, 15))
df4.groupby('prefix')[periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
df4_rel.groupby('prefix')[periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
for k,grp in df4.groupby(['prefix']):
    grp[periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()





# distribution plots
fig, ax = plt.subplots(8,3, figsize=(20, 15))
# get 0.9 quantile
i = 0
for pref in dist1.index.values:
        dfplot = df4[df4.prefix == pref]
        sns.distplot(dfplot['full_count'], ax=ax[i][0]).set_title('{} : {} formes distinctes, {} total occurrences (100%)'.format(pref, dist1.loc[pref,'count'], dist1.loc[pref,'sum']))
        # get 0.95 quantile
        q = dfplot["full_count"].quantile(0.9)
        dfplot2 = dfplot[dfplot["full_count"] < q]['full_count']      
        sns.distplot(dfplot2, ax=ax[i][1]).set_title(pref + ' : 90% quantiles')
        #sns.distplot(np.log(dfplot), ax=ax[0])
        sns.boxplot(dfplot2,ax=ax[i][2]).set_title(pref + ' : 90% quantiles')
        i=i+1
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()         

q = df4["full_count"].quantile(0.9)
dfplot2 = df4[df4["full_count"] < q]      

sns.boxplot(x="prefix", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
pdf2.savefig()
plt.close()

fig, ax = plt.subplots(8,2, figsize=(20, 15))
# get 0.9 quantile
i = 0
for pref in dist1.index.values:
    dfplot3 = df4_rel[df4_rel.prefix == pref].set_index('word')[periods].T
    dfplot3.index = pd.to_datetime(dfplot3.index)
    dfplot4=dfplot3.resample('5AS').sum()
    dfplotdiffres = dfplot4.apply(np.ceil).diff()

    dfdiffok = dfplotdiffres.apply(lambda x : x.value_counts(), axis=1)
    dfdiffok.rename(columns={-1.0:'disparition',
                          0.0:'conservation',
                          1.0:'apparition'}, 
                 inplace=True)
    #print(dfdiffok)
    dfdiffok.plot(ax=ax[i][0], title=pref + ": vocabulaire conservé, apparaissant et disparaissant")

    dfplotdiffres['mean_diff'] = dfplot4.diff().apply(lambda x : x.mean(), axis=1)
    dfplotdiffres['mean_diff'].plot(ax=ax[i][1], title=pref + ": moyenne de l'évolution des mots construits (fréquence relative pour base)")
    i=i+1
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()    




# moving average, trends etc.
df5 = df4_rel.groupby('prefix').sum()[periods]
for pref in dist1.index.values : #df5.index.values:
    series = df5.loc[pref]
    ts = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 

    ts['z_data'] = (ts['data'] - ts.data.rolling(window=10).mean()) / ts.data.rolling(window=10).std()
    #ts['zp_data'] = ts['z_data'] - ts['z_data'].shift(10)
    plot_rolling_simple(ts,title= pref, window=10)
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
    pdf2.savefig()
    plt.close()
pdf2.close()

######### par préfixe


for pref in dist1.index.values:
    pdf2 = PdfPages(pref + '_all_noPOS_synthesis_googlengrams.pdf')

    # distribution plots
    fig, ax = plt.subplots(3, figsize=(20, 15))
    dfplot = df4[df4.prefix == pref]
    sns.distplot(dfplot['full_count'], ax=ax[0]).set_title('{} : {} formes distinctes, {} total occurrences (100%)'.format(pref, dist1.loc[pref,'count'], dist1.loc[pref,'sum']))
    # get 0.95 quantile
    q = dfplot["full_count"].quantile(0.9)
    dfplot2 = dfplot[dfplot["full_count"] < q]['full_count']      
    sns.distplot(dfplot2, ax=ax[1]).set_title(pref + ' : 90% quantiles')
    #sns.distplot(np.log(dfplot), ax=ax[0])
    sns.boxplot(dfplot2,ax=ax[2]).set_title(pref + ' : 90% quantiles')
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    fig.tight_layout()
    pdf2.savefig()
    plt.close() 
    
    
    q = df4["full_count"].quantile(0.9)
    dfplot2 = dfplot[dfplot["full_count"] < q]      
    sns.boxplot(x="sep", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
    pdf2.savefig()
    plt.close()

    # evolution globale 
    fig, ax = plt.subplots(4, figsize=(20, 15))
    df4[df4.prefix == pref][periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
    df4_rel[df4_rel.prefix == pref][periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
    df4_rel[df4_rel.prefix == pref][periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
    # vocabulaire stable, appariassant, dispariassant
    dfplot3 = df4_rel[df4_rel.prefix == pref].set_index('word')[periods].T
    dfplot3.index = pd.to_datetime(dfplot3.index)
    dfplot4=dfplot3.resample('5AS').sum()
    dfplotdiffres = dfplot4.apply(np.ceil).diff()

    dfdiffok = dfplotdiffres.apply(lambda x : x.value_counts(), axis=1)
    dfdiffok.rename(columns={-1.0:'disparition',
                          0.0:'conservation',
                          1.0:'apparition'}, 
                 inplace=True)
    #print(dfdiffok)
    dfdiffok.plot(ax=ax[3], title=pref + ": vocabulaire conservé, apparaissant et disparaissant")
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    fig.tight_layout()
    pdf2.savefig()
    plt.close()
    
    
    # moving average, trends etc.
    df5 = df4_rel.groupby('prefix').sum()[periods]
    series = df5.loc[pref]
    ts = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 
    ts['z_data'] = (ts['data'] - ts.data.rolling(window=10).mean()) / ts.data.rolling(window=10).std()
    plot_rolling_simple(ts,title= pref, window=10)
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()

    
    # nbre de formations différentes par an
    fig, ax = plt.subplots(2, figsize=(20, 15))
    df4[df4.prefix == pref][periods].astype(bool).sum(axis=0).T.plot(ax=ax[0],kind="line", title=pref + " : nombre de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
    df4[df4.prefix == pref][periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : nombre d'occurrences par année", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # global distribution
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 15))
    df4[df4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('sep')['full_count'].count().plot(ax=ax[0],kind="barh", title=pref + ' : distribution par séparateur (formes distinctes)', figsize=(20,10))  # [['full_count']]
    df4[df4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('sep')['full_count'].sum().plot(ax=ax[1],kind="barh", title=pref + ' : distribution par séparateur (total de formes)', figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # timeline ()
    fig, ax = plt.subplots(2, figsize=(20, 15))
    df4[df4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('sep')[periods].apply(lambda column: (column != 0).sum()).T.plot(ax=ax[0],kind="line", title=pref + " : évolution des distributions des séparateurs(formes distinctes)", rot=45, figsize=(20,10))  # [['full_count']]
    df4[df4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('sep')[periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : évolution des distributions des séparateurs (total de formes)", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # timeline (word)
    df4[df4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('word')[periods].sum().head(20).T.plot(kind="line", title=pref + " : évolution des distributions des mots", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
#    for k2, grp2 in grp[~grp.word_pos.str.contains('_')].groupby('word_pos'):
    for k2, grp2 in df4[df4.prefix == pref].groupby('sep'):
        grp2.sort_values(['full_count'],ascending=False).groupby(['word'])[periods].sum().head(20).T.plot(kind="line", title=pref + "+x - " + k2, figsize=(20,10) )
        fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

        pdf2.savefig()
        plt.close()
    pdf2.close()




# In[479]:


# save dataframe df4
# save to excel
def save_report(report, key, outfile):
    """
    Take a report and save it to a single Excel file
    """
    cols = sorted(list(report.columns.values),reverse=True)
    #print(cols)
    writer = pd.ExcelWriter(outfile)
    for k, grp in report.groupby(key):
        grp[cols].sort_values('full_count', ascending=False).set_index('word').to_excel(writer,k)
    writer.save()
    return True

#print(df4.head())
save_report(df4, 'prefix','prefixes_googlengrams1800-2010_nopos.xls')


# ## With Plotly

# In[480]:


# with plotly
import plotly.plotly as py
import plotly.tools as pytools
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=False)
#pytools.set_credentials_file(username='ecartierdijon', api_key='3msHhM6RjRcAvIpAgcz6')
#help(py.plot) max 25 public graphs

    
    
filename = "./plotly_graphs/Distribution_mots-distincts_prefixes_nopos_googlengram.html"
group_data = df4.groupby('prefix')['full_count'].count()
#print(group_data)
data = [go.Bar(
            x=group_data.index.values,# 
            y=group_data
    )]

plot(data, filename = filename)

filename = "./plotly_graphs/Distribution_nb_total_prefixes_nopos_googlengram.html"
group_data = df4.groupby('prefix')['full_count'].sum()
#print(group_data)
data = [go.Bar(
            x=group_data.index.values,# 
            y=group_data
    )]

plot(data, filename = filename) 

# evolution globale pour chaque préfixe
#fig, ax = plt.subplots(3, figsize=(20, 15))
#df4.groupby('prefix')[periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
#df4_rel.groupby('prefix')[periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
#for k,grp in df4.groupby(['prefix']):
#    grp[periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
#plt.show()


# fréquence par nb de formes générées
filename = "./plotly_graphs/Evolution_nb_lexie-prefixes_nopos_googlengram.html"

data = []
for k,grp in df4.groupby(['prefix']):
        dfpref = grp[periods].astype(bool).sum(axis=0).T
        #print(dfpref)
        linegraph = go.Scatter(x=dfpref.index.values, y=dfpref, name=k, opacity = 0.8)
        data.append(linegraph)

layout = dict(
    title='Evolution des nombres de formes différentes par année',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 


# fréquence absolue
filename = "./plotly_graphs/Evolution_absolue-prefixes_nopos_googlengram.html"
group_data = df4.groupby('prefix').sum()
df6 = group_data[periods].T
#print(df6.head())
data = []
for pref in df6.columns.values:
    linegraph = go.Scatter(
        x=df6.index,
        y=df6[pref],
        name = pref,
        opacity = 0.8)
    data.append(linegraph)

layout = dict(
    title='Evolution des fréquences absolues de 1800 à 2010',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 

# frequence relative
filename = "./plotly_graphs/Evolution_relative-prefixes_nopos_googlengram.html"
group_data = df4_rel.groupby('prefix').sum()
df6 = group_data[periods].T
#print(df6.head())
data = []
for pref in df6.columns.values:
    linegraph = go.Scatter(
        x=df6.index,
        y=df6[pref],
        name = pref,
        #line = dict(color = '#17BECF'),
        opacity = 0.8)
    data.append(linegraph)

layout = dict(
    title='Evolution des fréquences relatives de 1800 à 2010',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 



# ## get boxplot of frequency for each prefix
# To be done : evolution of distribution (boxplot) + for every word

# In[ ]:





# ## Stationarity assessment

# In[26]:





# In[27]:


# composante saisonnière
from statsmodels.tsa.seasonal import seasonal_decompose



for pref in df5.index.values:
    series = df5.loc[pref]
    data = pd.DataFrame({pref:series.values}, index=series.index) # 'year':seriesrel.index, 
    #print(data)

    res = seasonal_decompose(data[pref].as_matrix().ravel(), freq=7, two_sided=False)
    data["season"] = res.seasonal
    data["trendsea"] = res.trend
    data.plot(y=[pref, "season", "trendsea"], figsize=(20,10), title=pref + " : saisonnalité")
    pdf0.savefig()
    plt.close()
    data[-30:].plot(y=[pref, "season", "trendsea"], figsize=(20,10), title=pref + " : saisonnalité (30 dernières années)")
    pdf0.savefig()
    plt.close()
#pdf0.close()


# In[28]:


# autocorrelation
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import periodogram
for pref in df5.index.values:
    series = df5.loc[pref]
    data = pd.DataFrame({pref:series.values}, index=series.index) # 'year':seriesrel.index, 
    #print(data)

    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = plot_acf(data[pref], lags=40, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = plot_pacf(data[pref], lags=40, ax=ax2)
    fig.suptitle(pref + " : autocorrelation")
    pdf0.savefig()
    plt.close()
    p = periodogram(data[pref])
    plt.plot(p)
    pdf0.savefig()
    plt.close()

#pdf0.close()


# ## Decompose in trend, seasonality and residual

# In[29]:


from random import randrange
from pandas import Series
from matplotlib import pyplot
#fig, ax = plt.subplots(1,1,figsize = (20,20))
from statsmodels.tsa.seasonal import seasonal_decompose


for pref in df5.index.values:
    series = df5.loc[pref]
    df2 = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 

    #series = [i+randrange(10) for i in range(1,100)]
    res = seasonal_decompose(df2, model='additive', freq=1)
    res.plot()
    pdf0.savefig()
    plt.close()
    pyplot.show()
    #res = seasonal_decompose(df2, model='multiplicative', freq=1)
    #res.plot()
    #pdf0.savefig()
    #plt.close()
    #pyplot.show()
    #print(result.trend)
    #print(result.seasonal)
    #print(result.resid)
    #print(result.observed)
pdf0.close()


# # Load pos data

# # 1 grams pos data : fre.prefixes.1.grams.pos.1799-2009.csv

# In[332]:


# 1-grams 

if os.path.isfile('./fre.prefixes.1.grams.pos.1799-2009.csv'):
    print("Loading the 1 gram big file (no pos)...")
    dfpos= pd.read_csv('./fre.prefixes.1.grams.pos.1799-2009.csv', header=0, sep=',', error_bad_lines=False)#, index_col=0 
else:
    print("Please first launch retrieve_google_1grams.py to generate fre.prefixes.1.grams.1799-2009.csv")
    exit()


dfpos.info()
dfpos.head()



# In[333]:



# ## create triple column (prefix - word - POS)
# élimination stoplist
#df = df[~df.string.isin(stoplist)]
# In[4]:


# 
pref_re = '^(ultra|super|hyper|hypra|extra|méga|archi|maxi|supra)(?:.*)_(?:.+)$'
pref_re2 = '^(?:ultra|super|hyper|hypra|extra|méga|archi|maxi|supra)(.*)_(?:.+)$'
pref_re3 = '^(?:ultra|super|hyper|hypra|extra|méga|archi|maxi|supra)(?:.*)_(.+)$'
pref_re4 = '^(.+)_(?:.+)$'
dfpos['prefix'] = dfpos.string.str.extract(pref_re, expand=True)
dfpos['word'] = dfpos.string.str.extract(pref_re2, expand=True)
dfpos['pos'] = dfpos.string.str.extract(pref_re3, expand=True)
dfpos['string'] = dfpos.string.str.extract(pref_re4, expand=True)
dfpos['sep'] = ""
print(dfpos.info())
print(dfpos[['string','pos','prefix','word','sep']].head(20))
dfpos = dfpos[~dfpos.string.isin(stoplist)]
#dfpos.dropna(inplace=True)
dfpos = dfpos[~dfpos.word.str.contains(r"[0-9]", na=False)]
dfpos = dfpos[dfpos.word.str.contains(r"^(|s|\w{3,})$", na=True)]
print(dfpos.info())
print(dfpos[['string','pos','prefix','word','sep']].head(20))
dfpos.to_csv("dfpos.csv")


# In[334]:


columns = dfpos.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]
dfpos['full_count'] = dfpos.apply(lambda x: x[periods].sum(), axis=1)
dfpos.head()


# # dfpos_rel

# In[335]:


dfpos_rel = dfpos.copy(deep=True)
# load totals of tokens per corpus year
totals = load_total_counts(19,1800,2009)

# calculate relative frequency for each column

for i in range(1800,2010):
    dfpos_rel[str(i) + '_freqrel'] = (dfpos_rel[str(i)] / totals[str(i)]) * 1000

# remove absolute frequency for df (relative frequency used for clustering and plotting)
dfpos_rel = dfpos_rel.drop([str(i) for i in range(1800,2010)], axis=1)
dfpos_rel.columns = dfpos_rel.columns.str.replace('_freqrel', '')

print(dfpos_rel.info())
print(dfpos_rel.head(10))


# ## data synthesis

# In[336]:


# save dataframe dfpos
# save to excel
def save_report(report, key, outfile):
    """
    Take a report and save it to a single Excel file
    """
    cols = sorted(list(report.columns.values),reverse=True)
    #print(cols)
    writer = pd.ExcelWriter(outfile)
    for k, grp in report.groupby(key):
        grp[cols].sort_values('full_count', ascending=False).groupby('string').sum().to_excel(writer,k)
#        grp[cols].sort_values('full_count', ascending=False).set_index('word').to_excel(writer,k)
    writer.save()
    return True

#print(df4.head())
save_report(dfpos, 'prefix','prefixes_1gram_googlengrams1800-2010.xls')


# In[337]:


# base for browsing prefixes
dist1 = dfpos.groupby('prefix')['full_count'].agg(['count','sum']).sort_values('count', ascending=False)
print(dist1)
print(dist1.index.values)
print(dist1.loc['maxi','count'])


# In[338]:


# simple moving average function
def plot_rolling_simple(df,title, window=10):
    fig, ax = plt.subplots(2,figsize=(20, 10))
    ax[0].plot(df.index, df.data, label='raw data')
    ax[0].plot(df.data.rolling(window=window).mean(), label="rolling mean (window=10)");
    ax[0].plot(df.data.rolling(window=window).std(), label="rolling std (window=10)");
    ax[0].legend()

    ax[1].plot(df.index, df.z_data, label="de-trended data")
    ax[1].plot(df.z_data.rolling(window=window).mean(), label="rolling mean (window=10)");
    ax[1].plot(df.z_data.rolling(window=window).std(), label="rolling std (window=10)");
    ax[1].legend()

    fig.suptitle(title, fontsize=13)
    plt.tight_layout()
    fig.autofmt_xdate()


# # synthèse pdf

# In[339]:


pdf2 = PdfPages('Prefix-X_POS_synthesis_googlengrams.pdf')
fig, ax = plt.subplots(1, figsize=(20, 15))
fig.text(4.25/8.5, 0.5/11., "Etude globale sur les mots fusionnées\nCorpus Google Ngrams (1800-2010)", ha='center', va='center', fontsize=24, )
fig.tight_layout()
pdf2.savefig()
plt.close()

columns = dfpos.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]

# distribution entre les prefixes
fig, ax = plt.subplots(2, figsize=(20, 15))
dfpos.groupby('prefix')['full_count'].count().plot(ax=ax[0],kind="bar",title='Distribution des fréquences entre préfixes (nbre de formations distinctes)', rot=45, figsize=(20,10))  # [['full_count']]
dfpos.groupby('prefix')['full_count'].sum().plot(ax=ax[1],kind="bar",title="Distribution des fréquences entre préfixes (nbre total d'occurrences)", rot=45, figsize=(20,10))  # [['full_count']]
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()

pdf2.savefig()
plt.close()
# evolution globale pour chaque préfixe
fig, ax = plt.subplots(3, figsize=(20, 15))
dfpos.groupby('prefix')[periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
dfpos_rel.groupby('prefix')[periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
for k,grp in dfpos.groupby(['prefix']):
    grp[periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()





# distribution plots
fig, ax = plt.subplots(8,3, figsize=(20, 15))
# get 0.9 quantile
i = 0
for pref in dist1.index.values:
        dfplot = dfpos[dfpos.prefix == pref]
        sns.distplot(dfplot['full_count'], ax=ax[i][0]).set_title('{} : {:d} formes distinctes, {:d} total occurrences (100%)'.format(pref, dist1.loc[pref,'count'], dist1.loc[pref,'sum']))
        # get 0.95 quantile
        q = dfplot["full_count"].quantile(0.9)
        dfplot2 = dfplot[dfplot["full_count"] < q]['full_count']      
        sns.distplot(dfplot2, ax=ax[i][1]).set_title(pref + ' : 90% quantiles')
        #sns.distplot(np.log(dfplot), ax=ax[0])
        sns.boxplot(dfplot2,ax=ax[i][2]).set_title(pref + ' : 90% quantiles')
        i=i+1
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()         

q = dfpos["full_count"].quantile(0.9)
dfplot2 = dfpos[dfpos["full_count"] < q]      

sns.boxplot(x="prefix", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
pdf2.savefig()
plt.close()

fig, ax = plt.subplots(8,2, figsize=(20, 15))
# get 0.9 quantile
i = 0
for pref in dist1.index.values:
    dfplot3 = dfpos_rel[dfpos_rel.prefix == pref].set_index('word')[periods].T
    dfplot3.index = pd.to_datetime(dfplot3.index)
    dfplot4=dfplot3.resample('5AS').sum()
    dfplotdiffres = dfplot4.apply(np.ceil).diff()

    dfdiffok = dfplotdiffres.apply(lambda x : x.value_counts(), axis=1)
    dfdiffok.rename(columns={-1.0:'disparition',
                          0.0:'conservation',
                          1.0:'apparition'}, 
                 inplace=True)
    #print(dfdiffok)
    dfdiffok.plot(ax=ax[i][0], title=pref + ": vocabulaire conservé, apparaissant et disparaissant")

    dfplotdiffres['mean_diff'] = dfplot4.diff().apply(lambda x : x.mean(), axis=1)
    dfplotdiffres['mean_diff'].plot(ax=ax[i][1], title=pref + ": moyenne de l'évolution des mots construits (fréquence relative pour base)")
    i=i+1
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()    




# moving average, trends etc.
df5 = dfpos_rel.groupby('prefix').sum()[periods]
for pref in dist1.index.values : #df5.index.values:
    series = df5.loc[pref]
    ts = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 

    ts['z_data'] = (ts['data'] - ts.data.rolling(window=10).mean()) / ts.data.rolling(window=10).std()
    #ts['zp_data'] = ts['z_data'] - ts['z_data'].shift(10)
    plot_rolling_simple(ts,title= pref, window=10)
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
    pdf2.savefig()
    plt.close()
pdf2.close()

######### par préfixe


for pref in dist1.index.values:
    pdf2 = PdfPages(pref + '-X_POS_synthesis_googlengrams.pdf')

    # distribution plots
    fig, ax = plt.subplots(3, figsize=(20, 15))
    dfplot = dfpos[dfpos.prefix == pref]
    sns.distplot(dfplot['full_count'], ax=ax[0]).set_title('{} : {:d} formes distinctes, {:d} total occurrences (100%)'.format(pref, dist1.loc[pref,'count'], dist1.loc[pref,'sum']))
    # get 0.95 quantile
    q = dfplot["full_count"].quantile(0.9)
    dfplot2 = dfplot[dfplot["full_count"] < q]['full_count']      
    sns.distplot(dfplot2, ax=ax[1]).set_title(pref + ' : 90% quantiles')
    #sns.distplot(np.log(dfplot), ax=ax[0])
    sns.boxplot(dfplot2,ax=ax[2]).set_title(pref + ' : 90% quantiles')
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    fig.tight_layout()
    pdf2.savefig()
    plt.close() 
    
    
    q = dfpos["full_count"].quantile(0.9)
    dfplot2 = dfplot[dfplot["full_count"] < q]      
    sns.boxplot(x="pos", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
    pdf2.savefig()
    plt.close()

    # evolution globale 
    fig, ax = plt.subplots(4, figsize=(20, 15))
    dfpos[dfpos.prefix == pref][periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
    dfpos_rel[dfpos_rel.prefix == pref][periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
    dfpos_rel[dfpos_rel.prefix == pref][periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
    # vocabulaire stable, appariassant, dispariassant
    dfplot3 = dfpos_rel[dfpos_rel.prefix == pref].set_index('word')[periods].T
    dfplot3.index = pd.to_datetime(dfplot3.index)
    dfplot4=dfplot3.resample('5AS').sum()
    dfplotdiffres = dfplot4.apply(np.ceil).diff()

    dfdiffok = dfplotdiffres.apply(lambda x : x.value_counts(), axis=1)
    dfdiffok.rename(columns={-1.0:'disparition',
                          0.0:'conservation',
                          1.0:'apparition'}, 
                 inplace=True)
    #print(dfdiffok)
    dfdiffok.plot(ax=ax[3], title=pref + ": vocabulaire conservé, apparaissant et disparaissant")
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    fig.tight_layout()
    pdf2.savefig()
    plt.close()
    
    
    # moving average, trends etc.
    df5 = dfpos_rel.groupby('prefix').sum()[periods]
    series = df5.loc[pref]
    ts = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 
    ts['z_data'] = (ts['data'] - ts.data.rolling(window=10).mean()) / ts.data.rolling(window=10).std()
    plot_rolling_simple(ts,title= pref, window=10)
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()

    
    # nbre de formations différentes par an
    fig, ax = plt.subplots(2, figsize=(20, 15))
    dfpos[dfpos.prefix == pref][periods].astype(bool).sum(axis=0).T.plot(ax=ax[0],kind="line", title=pref + " : nombre de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
    dfpos[dfpos.prefix == pref][periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : nombre d'occurrences par année", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # global distribution
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 15))
    dfpos[dfpos.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')['full_count'].count().plot(ax=ax[0],kind="barh", title=pref + ' : distribution des parties du discours (formes distinctes)', figsize=(20,10))  # [['full_count']]
    dfpos[dfpos.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')['full_count'].sum().plot(ax=ax[1],kind="barh", title=pref + ' : distribution des parties du discours (total de formes)', figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # timeline (pos)
    fig, ax = plt.subplots(2, figsize=(20, 15))
    dfpos[dfpos.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')[periods].apply(lambda column: (column != 0).sum()).T.plot(ax=ax[0],kind="line", title=pref + " : évolution des distributions des parties du discours(formes distinctes)", rot=45, figsize=(20,10))  # [['full_count']]
    dfpos[dfpos.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')[periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : évolution des distributions des parties du discours (total de formes)", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # timeline (word)
    dfpos[dfpos.prefix == pref].sort_values(['full_count'],ascending=False).groupby('word')[periods].sum().head(20).T.plot(kind="line", title=pref + " : évolution des distributions des mots", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
#    for k2, grp2 in grp[~grp.word_pos.str.contains('_')].groupby('word_pos'):
    for k2, grp2 in dfpos[dfpos.prefix == pref][dfpos[dfpos.prefix == pref].pos.isin(['ADJ','ADV','NOUN','VERB'])].groupby('pos'):
        grp2.sort_values(['full_count'],ascending=False).groupby(['word'])[periods].sum().head(20).T.plot(kind="line", title=pref + "+x - " + k2, figsize=(20,10) )
        fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

        pdf2.savefig()
        plt.close()
    pdf2.close()




# ## Plotly from matplotlib : check https://plot.ly/matplotlib/
# ## Note do not use it s not yet stable!!!!

# ## Plotly interactif

# In[340]:


# with plotly
import plotly.plotly as py
import plotly.tools as pytools
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=False)
#pytools.set_credentials_file(username='ecartierdijon', api_key='3msHhM6RjRcAvIpAgcz6')
#help(py.plot) max 25 public graphs

    
    
filename = "./plotly_graphs/Distribution_mots-distincts_prefixes_POS1_googlengram.html"
group_data = dfpos.groupby('prefix')['full_count'].count()
#print(group_data)
data = [go.Bar(
            x=group_data.index.values,# 
            y=group_data
    )]

plot(data, filename = filename)

filename = "./plotly_graphs/Distribution_nb_total_prefixes_POS1_googlengram.html"
group_data = dfpos.groupby('prefix')['full_count'].sum()
#print(group_data)
data = [go.Bar(
            x=group_data.index.values,# 
            y=group_data
    )]

plot(data, filename = filename) 

# evolution globale pour chaque préfixe
#fig, ax = plt.subplots(3, figsize=(20, 15))
#dfpos.groupby('prefix')[periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
#dfpos_rel.groupby('prefix')[periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
#for k,grp in dfpos.groupby(['prefix']):
#    grp[periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
#plt.show()


# fréquence par nb de formes générées
filename = "./plotly_graphs/Evolution_nb_lexie-prefixes_POS1_googlengram.html"

data = []
for k,grp in dfpos.groupby(['prefix']):
        dfpref = grp[periods].astype(bool).sum(axis=0).T
        #print(dfpref)
        linegraph = go.Scatter(x=dfpref.index.values, y=dfpref, name=k, opacity = 0.8)
        data.append(linegraph)

layout = dict(
    title='Evolution des nombres de formes différentes par année',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 


# fréquence absolue
filename = "./plotly_graphs/Evolution_absolue-prefixes_POS1_googlengram.html"
group_data = dfpos.groupby('prefix').sum()
df6 = group_data[periods].T
#print(df6.head())
data = []
for pref in df6.columns.values:
    linegraph = go.Scatter(
        x=df6.index,
        y=df6[pref],
        name = pref,
        opacity = 0.8)
    data.append(linegraph)

layout = dict(
    title='Evolution des fréquences absolues de 1800 à 2010',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 

# frequence relative
filename = "./plotly_graphs/Evolution_relative-prefixes_POS1_googlengram.html"
group_data = dfpos_rel.groupby('prefix').sum()
df6 = group_data[periods].T
#print(df6.head())
data = []
for pref in df6.columns.values:
    linegraph = go.Scatter(
        x=df6.index,
        y=df6[pref],
        name = pref,
        #line = dict(color = '#17BECF'),
        opacity = 0.8)
    data.append(linegraph)

layout = dict(
    title='Evolution des fréquences relatives de 1800 à 2010',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 



# # 2 bigrams (pref word)

# In[353]:


if os.path.isfile('./fre.prefixes.2.grams.pos.1799-2009.csv'):
    print("Loading the 2 gram big file (pos)...")
    dfpos2= pd.read_csv('./fre.prefixes.2.grams.pos.1799-2009.csv', header=0, sep=',', error_bad_lines=False)#, index_col=0 
else:
    print("Please first launch retrieve_google_1grams.py to generate fre.prefixes.2.pos.grams.1799-2009.csv")
    exit()


dfpos2.info()
dfpos2.head()



# In[359]:


# ## create triple column (prefix - word - POS)
# remove sur...
dfpos2 = dfpos2[~dfpos2.string.str.contains("^sur")]
print(dfpos2.info())
# remove where there are less than two _
dfpos2 = dfpos2[dfpos2.string.str.contains("_.+_")]
print(dfpos2.info())
# split two words
string_re = '^(.+) (?:.+)$'
string_re2 = '^(?:.+) (.+)$'
dfpos2['string1'] = dfpos2.string.str.extract(string_re, expand=True)
dfpos2['string2'] = dfpos2.string.str.extract(string_re2, expand=True)
#print(dfpos2.string1.unique(), len(dfpos2.string1.unique()))
#print(dfpos2.string2.unique(), len(dfpos2.string2.unique()))
#print(dfpos2[~dfpos2.string1.str.contains("_")])
#print(dfpos2[dfpos2.string.str.contains("archi.+_ADV")])
#print(dfpos2.head())
#print(dfpos2.string.describe())
print(dfpos2.string1.describe())
print(dfpos2.string2.describe())


# In[361]:


# get word1 pos1

word_pos = '^(.+)_(?:.+)$'
word_pos1 = '^(?:.+)_(.+)$'
word_pos2 = '^(.+)?_(?_.+)_$'
word_pos3 = '^_(.+)_$'

# general case for string1
dfpos2['prefix'] = dfpos2.string1.str.extract(word_pos, expand=True)
#dfpos2['pos1'] = dfpos2.string1.str.extract(word_pos1, expand=True)

# case of archi
#dfpos2.prefix.fillna(dfpos2.string1, inplace=True)
#dfpos2.pos1.fillna('', inplace=True)

# general case for string1
dfpos2['word'] = dfpos2.string2.str.extract(word_pos, expand=True)
dfpos2['pos'] = dfpos2.string2.str.extract(word_pos1, expand=True)
# case of _NOUN_
#dfpos2.pos2.fillna(dfpos2.string2, inplace=True)
#dfpos2.word.fillna('', inplace=True)

dfpos2['sep'] = " "
dfpos2.prefix = dfpos2.prefix.str.replace('_','')
#dfpos2[dfpos2.pos1.isnull()].prefix.unique()

print(dfpos2.info())
dfpos2.dropna(inplace=True)
print(dfpos2.info())

dfpos2[['string','string1','prefix','string2','word','pos','sep']].head(20)


# In[362]:



dfpos2 = dfpos2[~dfpos2.word.str.contains(r"[0-9]", na=False)]
dfpos2 = dfpos2[dfpos2.word.str.contains(r"^(|s|\w{3,})$", na=True)]
print(dfpos2.info())
print(dfpos2[['string','string1','prefix','string2','word','pos','sep']].head(20))
dfpos.to_csv("dfpos2.csv")


# # colonne full_count

# In[363]:



columns = dfpos2.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]
dfpos2['full_count'] = dfpos2.apply(lambda x: x[periods].sum(), axis=1)
dfpos2.head()


# # dfpos2_rel (fréquence relative)

# In[364]:



dfpos2_rel = dfpos2.copy(deep=True)
# load totals of tokens per corpus year
totals = load_total_counts(19,1800,2009)

# calculate relative frequency for each column

for i in range(1800,2010):
    dfpos2_rel[str(i) + '_freqrel'] = (dfpos2_rel[str(i)] / totals[str(i)]) * 1000

# remove absolute frequency for df (relative frequency used for clustering and plotting)
dfpos2_rel = dfpos2_rel.drop([str(i) for i in range(1800,2010)], axis=1)
dfpos2_rel.columns = dfpos2_rel.columns.str.replace('_freqrel', '')

print(dfpos2_rel.info())
print(dfpos2_rel.head(10))


# In[366]:


# save to excel
def save_report(report, key, outfile):
    """
    Take a report and save it to a single Excel file
    """
    cols = sorted(list(report.columns.values),reverse=True)
    #print(cols)
    writer = pd.ExcelWriter(outfile)
    for k, grp in report.groupby(key):
        grp[cols].sort_values('full_count', ascending=False).groupby('word').sum().to_excel(writer,k)
#        grp[cols].sort_values('full_count', ascending=False).set_index('word').to_excel(writer,k)
    writer.save()
    return True

#print(df4.head())
save_report(dfpos2, 'prefix','prefixes_2gram_googlengrams1800-2010.xls')


# In[377]:


# base for browsing prefixes
dist1 = dfpos2.groupby('prefix')['full_count'].agg(['count','sum']).sort_values('count', ascending=False)
print(dist1)
print(dist1.index.values)
print(dist1.loc['maxi','count'])


# # Synthèse

# In[379]:


pdf2 = PdfPages('Prefix_SPACE_X_POS_synthesis_googlengrams.pdf')
fig, ax = plt.subplots(1, figsize=(20, 15))
fig.text(4.25/8.5, 0.5/11., "Etude globale sur les mots construits liés par espace \nCorpus Google Ngrams (1800-2010)", ha='center', va='center', fontsize=24, )
fig.tight_layout()
pdf2.savefig()
plt.close()

columns = dfpos2.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]

# distribution entre les prefixes
fig, ax = plt.subplots(2, figsize=(20, 15))
dfpos2.groupby('prefix')['full_count'].count().plot(ax=ax[0],kind="bar",title='Distribution des fréquences entre préfixes (nbre de formations distinctes)', rot=45, figsize=(20,10))  # [['full_count']]
dfpos2.groupby('prefix')['full_count'].sum().plot(ax=ax[1],kind="bar",title="Distribution des fréquences entre préfixes (nbre total d'occurrences)", rot=45, figsize=(20,10))  # [['full_count']]
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()

pdf2.savefig()
plt.close()
# evolution globale pour chaque préfixe
fig, ax = plt.subplots(3, figsize=(20, 15))
dfpos2.groupby('prefix')[periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
dfpos2_rel.groupby('prefix')[periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
for k,grp in dfpos2.groupby(['prefix']):
    grp[periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()





# distribution plots
fig, ax = plt.subplots(8,3, figsize=(20, 15))
# get 0.9 quantile
i = 0
for pref in dist1.index.values:
        dfplot = dfpos2[dfpos2.prefix == pref]
        sns.distplot(dfplot['full_count'], ax=ax[i][0]).set_title('{} : {} formes distinctes, {} total occurrences (100%)'.format(pref, dist1.loc[pref,'count'], dist1.loc[pref,'sum']))
        # get 0.95 quantile
        q = dfplot["full_count"].quantile(0.9)
        dfplot2 = dfplot[dfplot["full_count"] < q]['full_count']      
        sns.distplot(dfplot2, ax=ax[i][1]).set_title(pref + ' : 90% quantiles')
        #sns.distplot(np.log(dfplot), ax=ax[0])
        sns.boxplot(dfplot2,ax=ax[i][2]).set_title(pref + ' : 90% quantiles')
        i=i+1
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()         

q = dfpos2["full_count"].quantile(0.9)
dfplot2 = dfpos2[dfpos2["full_count"] < q]      

sns.boxplot(x="prefix", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
pdf2.savefig()
plt.close()

fig, ax = plt.subplots(8,2, figsize=(20, 15))
# get 0.9 quantile
i = 0
for pref in dist1.index.values:
        dfplot3 = dfpos2_rel[dfpos2_rel.prefix == pref].set_index('word')[periods].T
        #print(dfplot3.info())
        dfplot3.index = pd.to_datetime(dfplot3.index)
        dfplot4=dfplot3.resample('5AS').sum()
        #print(dfplot4.info())
        dfplotdiffres = dfplot4.apply(np.ceil).diff()

        dfdiffok = dfplotdiffres.apply(lambda x : x.value_counts(), axis=1)
        dfdiffok.rename(columns={-1.0:'disparition',
                          0.0:'conservation',
                          1.0:'apparition'}, 
                 inplace=True)
        #print(dfdiffok)
        dfdiffok.plot(ax=ax[i][0], title=pref + ": vocabulaire conservé, apparaissant et disparaissant")

        dfplotdiffres['mean_diff'] = dfplot4.diff().apply(lambda x : x.mean(), axis=1)
        dfplotdiffres['mean_diff'].plot(ax=ax[i][1], title=pref + ": moyenne de l'évolution des mots construits (fréquence relative pour base)")
        i=i+1
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()    




# moving average, trends etc.
df5 = dfpos2_rel.groupby('prefix').sum()[periods]
for pref in dist1.index.values : #df5.index.values:
    series = df5.loc[pref]
    ts = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 

    ts['z_data'] = (ts['data'] - ts.data.rolling(window=10).mean()) / ts.data.rolling(window=10).std()
    #ts['zp_data'] = ts['z_data'] - ts['z_data'].shift(10)
    plot_rolling_simple(ts,title= pref, window=10)
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
    pdf2.savefig()
    plt.close()
pdf2.close()

######### par préfixe


for pref in dist1.index.values:
    pdf2 = PdfPages(pref + '_SPACE_X_POS_synthesis_googlengrams.pdf')

    # distribution plots
    fig, ax = plt.subplots(3, figsize=(20, 15))
    dfplot = dfpos2[dfpos2.prefix == pref]
    sns.distplot(dfplot['full_count'], ax=ax[0]).set_title('{} : {} formes distinctes, {} total occurrences (100%)'.format(pref, dist1.loc[pref,'count'], dist1.loc[pref,'sum']))
    # get 0.95 quantile
    q = dfplot["full_count"].quantile(0.9)
    dfplot2 = dfplot[dfplot["full_count"] < q]['full_count']      
    sns.distplot(dfplot2, ax=ax[1]).set_title(pref + ' : 90% quantiles')
    #sns.distplot(np.log(dfplot), ax=ax[0])
    sns.boxplot(dfplot2,ax=ax[2]).set_title(pref + ' : 90% quantiles')
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    fig.tight_layout()
    pdf2.savefig()
    plt.close() 
    
    
    q = dfpos2["full_count"].quantile(0.9)
    dfplot2 = dfplot[dfplot["full_count"] < q]      
    sns.boxplot(x="pos", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
    pdf2.savefig()
    plt.close()

    # evolution globale 
    fig, ax = plt.subplots(4, figsize=(20, 15))
    dfpos2[dfpos2.prefix == pref][periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
    dfpos2_rel[dfpos2_rel.prefix == pref][periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
    dfpos2_rel[dfpos2_rel.prefix == pref][periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
    # vocabulaire stable, appariassant, dispariassant
    dfplot3 = dfpos2_rel[dfpos2_rel.prefix == pref].set_index('word')[periods].T
    dfplot3.index = pd.to_datetime(dfplot3.index)
    dfplot4=dfplot3.resample('5AS').sum()
    dfplotdiffres = dfplot4.apply(np.ceil).diff()

    dfdiffok = dfplotdiffres.apply(lambda x : x.value_counts(), axis=1)
    print(dfdiffok)
    dfdiffok.rename(columns={-1.0:'disparition',
                          0.0:'conservation',
                          1.0:'apparition'}, 
                 inplace=True)
    #print(dfdiffok)
    dfdiffok.plot(ax=ax[3], title=pref + ": vocabulaire conservé, apparaissant et disparaissant")
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    fig.tight_layout()
    pdf2.savefig()
    plt.close()
    
    
    # moving average, trends etc.
    df5 = dfpos2_rel.groupby('prefix').sum()[periods]
    series = df5.loc[pref]
    ts = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 
    ts['z_data'] = (ts['data'] - ts.data.rolling(window=10).mean()) / ts.data.rolling(window=10).std()
    plot_rolling_simple(ts,title= pref, window=10)
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()

    
    # nbre de formations différentes par an
    fig, ax = plt.subplots(2, figsize=(20, 15))
    dfpos2[dfpos2.prefix == pref][periods].astype(bool).sum(axis=0).T.plot(ax=ax[0],kind="line", title=pref + " : nombre de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
    dfpos2[dfpos2.prefix == pref][periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : nombre d'occurrences par année", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # global distribution
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 15))
    dfpos2[dfpos2.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')['full_count'].count().plot(ax=ax[0],kind="barh", title=pref + ' : distribution des parties du discours (formes distinctes)', figsize=(20,10))  # [['full_count']]
    dfpos2[dfpos2.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')['full_count'].sum().plot(ax=ax[1],kind="barh", title=pref + ' : distribution des parties du discours (total de formes)', figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # timeline (pos)
    fig, ax = plt.subplots(2, figsize=(20, 15))
    dfpos2[dfpos2.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')[periods].apply(lambda column: (column != 0).sum()).T.plot(ax=ax[0],kind="line", title=pref + " : évolution des distributions des parties du discours(formes distinctes)", rot=45, figsize=(20,10))  # [['full_count']]
    dfpos2[dfpos2.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')[periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : évolution des distributions des parties du discours (total de formes)", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # timeline (word)
    dfpos2[dfpos2.prefix == pref].sort_values(['full_count'],ascending=False).groupby('word')[periods].sum().head(20).T.plot(kind="line", title=pref + " : évolution des distributions des mots", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
#    for k2, grp2 in grp[~grp.word_pos.str.contains('_')].groupby('word_pos'):
    for k2, grp2 in dfpos2[dfpos2.prefix == pref][dfpos2[dfpos2.prefix == pref].pos.isin(['ADJ','ADV','NOUN','VERB'])].groupby('pos'):
        grp2.sort_values(['full_count'],ascending=False).groupby(['word'])[periods].sum().head(20).T.plot(kind="line", title=pref + "+x - " + k2, figsize=(20,10) )
        fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

        pdf2.savefig()
        plt.close()
    pdf2.close()




# # Plotly

# In[380]:



# with plotly
import plotly.plotly as py
import plotly.tools as pytools
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=False)
#pytools.set_credentials_file(username='ecartierdijon', api_key='3msHhM6RjRcAvIpAgcz6')
#help(py.plot) max 25 public graphs

    
    
filename = "./plotly_graphs/Distribution_mots-distincts_prefixes_POS2_googlengram.html"
group_data = dfpos2.groupby('prefix')['full_count'].count()
#print(group_data)
data = [go.Bar(
            x=group_data.index.values,# 
            y=group_data
    )]

plot(data, filename = filename)

filename = "./plotly_graphs/Distribution_nb_total_prefixes_POS2_googlengram.html"
group_data = dfpos2.groupby('prefix')['full_count'].sum()
#print(group_data)
data = [go.Bar(
            x=group_data.index.values,# 
            y=group_data
    )]

plot(data, filename = filename) 


# In[341]:


# evolution globale pour chaque préfixe
#fig, ax = plt.subplots(3, figsize=(20, 15))
#dfpos2.groupby('prefix')[periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
#dfpos2_rel.groupby('prefix')[periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
#for k,grp in dfpos2.groupby(['prefix']):
#    grp[periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
#plt.show()


# fréquence par nb de formes générées
filename = "./plotly_graphs/Evolution_nb_lexie-prefixes_POS2_googlengram.html"

data = []
for k,grp in dfpos2.groupby(['prefix']):
        dfpref = grp[periods].astype(bool).sum(axis=0).T
        #print(dfpref)
        linegraph = go.Scatter(x=dfpref.index.values, y=dfpref, name=k, opacity = 0.8)
        data.append(linegraph)

layout = dict(
    title='Evolution des nombres de formes différentes par année',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 


# fréquence absolue
filename = "./plotly_graphs/Evolution_absolue-prefixes_POS2_googlengram.html"
group_data = dfpos2.groupby('prefix').sum()
df6 = group_data[periods].T
#print(df6.head())
data = []
for pref in df6.columns.values:
    linegraph = go.Scatter(
        x=df6.index,
        y=df6[pref],
        name = pref,
        opacity = 0.8)
    data.append(linegraph)

layout = dict(
    title='Evolution des fréquences absolues de 1800 à 2010',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 

# frequence relative
filename = "./plotly_graphs/Evolution_relative-prefixes_POS2_googlengram.html"
group_data = dfpos2_rel.groupby('prefix').sum()
df6 = group_data[periods].T
#print(df6.head())
data = []
for pref in df6.columns.values:
    linegraph = go.Scatter(
        x=df6.index,
        y=df6[pref],
        name = pref,
        #line = dict(color = '#17BECF'),
        opacity = 0.8)
    data.append(linegraph)

layout = dict(
    title='Evolution des fréquences relatives de 1800 à 2010',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 


# # 3 grams

# In[396]:




if os.path.isfile('./fre.prefixes.3.grams.pos.1799-2009.csv'):
    print("Loading the 3 gram big file (pos)...")
    dfpos3= pd.read_csv('./fre.prefixes.3.grams.pos.1799-2009.csv', header=0, sep=',', error_bad_lines=False)#, index_col=0 
else:
    print("Please first launch retrieve_google_1grams.py to generate fre.prefixes.3.pos.grams.1799-2009.csv")
    exit()


dfpos3.info()
dfpos3.head()


# ## create triple column (prefix - word - POS)

# In[398]:



# remove sur...
dfpos3 = dfpos3[~dfpos3.string.str.contains("^sur")]
print(dfpos3.info())
# remove where there are less than two _
dfpos3 = dfpos3[dfpos3.string.str.contains("_.+_")]
print(dfpos3.info())
# split two words
string_re = '^(.+) (?:-.*) (?:.+)$'
string_re2 = '^(?:.+) (-.*) (?:.+)$'
string_re3 = '^(?:.+) (?:-.*) (.+)$'
dfpos3['string1'] = dfpos3.string.str.extract(string_re, expand=True)
dfpos3['sep'] = dfpos3.string.str.extract(string_re2, expand=True)
dfpos3['string3'] = dfpos3.string.str.extract(string_re3, expand=True)
print(dfpos3.info())
# on élimine ceux qui ne matche pas (pas de séparateur -)
dfpos3.dropna(inplace=True)
print(dfpos3.info())
# on unifie les séparateurs de -- à -
dfpos3.sep.replace(to_replace ='--', value = '-', regex = True, inplace=True) 
# on ne conserve que ceux avec pos (sinon doublons) puis on élimine
dfpos3 = dfpos3[~dfpos3.sep.isin(['-'])]
dfpos3.sep.replace(to_replace ='_.+$', value = '', regex = True, inplace=True)
print(dfpos3.info())
# on ne conserve que le string1 avec pos (sinon doublons) puis on l'elimine et on renomme en prefix
dfpos3 = dfpos3[dfpos3.string1.str.contains('_')]
dfpos3.string1.replace(to_replace ='_.+$', value = '', regex = True, inplace=True)
dfpos3.rename(columns={'string1':'prefix'}, inplace=True)
print(dfpos3.info())
# enfin on sépare string2 en word et pos, puis on elimine les nan (pas de match donc doublon)
dfpos3['word'] = dfpos3.string3.str.extract("^(.+)_(?:.+)$", expand=True)
dfpos3['pos'] = dfpos3.string3.str.extract("^(?:.+)_(.+)$", expand=True)
dfpos3.dropna(inplace=True)
print(dfpos3.info())
print(dfpos3[['string','prefix','sep','word','pos']])


# In[399]:


dfpos3 = dfpos3[~dfpos3.word.str.contains(r"[0-9]", na=False)]
dfpos3 = dfpos3[dfpos3.word.str.contains(r"^(|s|\w{3,})$", na=True)]
print(dfpos3.info())
print(dfpos3[['string','prefix','word','pos','sep']].head(20))

columns = dfpos3.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]
dfpos3['full_count'] = dfpos3.apply(lambda x: x[periods].sum(), axis=1)
dfpos3.head()
dfpos3.to_csv("dfpos3.csv")


# ## dfpos3_rel (fréquence relative)

# In[400]:


dfpos3_rel = dfpos3.copy(deep=True)
# load totals of tokens per corpus year
totals = load_total_counts(19,1800,2009)

# calculate relative frequency for each column

for i in range(1800,2010):
    dfpos3_rel[str(i) + '_freqrel'] = (dfpos3_rel[str(i)] / totals[str(i)]) * 1000

# remove absolute frequency for df (relative frequency used for clustering and plotting)
dfpos3_rel = dfpos3_rel.drop([str(i) for i in range(1800,2010)], axis=1)
dfpos3_rel.columns = dfpos3_rel.columns.str.replace('_freqrel', '')

print(dfpos3_rel.info())
print(dfpos3_rel.head(10))


# # save to excel

# In[401]:



def save_report(report, key, outfile):
    """
    Take a report and save it to a single Excel file
    """
    cols = sorted(list(report.columns.values),reverse=True)
    #print(cols)
    writer = pd.ExcelWriter(outfile)
    for k, grp in report.groupby(key):
        grp[cols].sort_values('full_count', ascending=False).groupby('word').sum().to_excel(writer,k)
#        grp[cols].sort_values('full_count', ascending=False).set_index('word').to_excel(writer,k)
    writer.save()
    return True

#print(df4.head())
save_report(dfpos3, 'prefix','prefixes_3gram_googlengrams1800-2010.xls')


# In[402]:


# base for browsing prefixes
dist1 = dfpos3.groupby('prefix')['full_count'].agg(['count','sum']).sort_values('count', ascending=False)
print(dist1)
print(dist1.index.values)
print(dist1.loc['maxi','count'])


# ## Synthèse

# In[403]:




pdf2 = PdfPages('Prefix_-_X_POS_synthesis_googlengrams.pdf')
fig, ax = plt.subplots(1, figsize=(20, 15))
fig.text(4.25/8.5, 0.5/11., "Etude globale sur les mots construits liés par espace \nCorpus Google Ngrams (1800-2010)", ha='center', va='center', fontsize=24, )
fig.tight_layout()
pdf2.savefig()
plt.close()

columns = dfpos3.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]

# distribution entre les prefixes
fig, ax = plt.subplots(2, figsize=(20, 15))
dfpos3.groupby('prefix')['full_count'].count().plot(ax=ax[0],kind="bar",title='Distribution des fréquences entre préfixes (nbre de formations distinctes)', rot=45, figsize=(20,10))  # [['full_count']]
dfpos3.groupby('prefix')['full_count'].sum().plot(ax=ax[1],kind="bar",title="Distribution des fréquences entre préfixes (nbre total d'occurrences)", rot=45, figsize=(20,10))  # [['full_count']]
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()

pdf2.savefig()
plt.close()
# evolution globale pour chaque préfixe
fig, ax = plt.subplots(3, figsize=(20, 15))
dfpos3.groupby('prefix')[periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
dfpos3_rel.groupby('prefix')[periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
for k,grp in dfpos3.groupby(['prefix']):
    grp[periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()





# distribution plots
fig, ax = plt.subplots(8,3, figsize=(20, 15))
# get 0.9 quantile
i = 0
for pref in dist1.index.values:
        dfplot = dfpos3[dfpos3.prefix == pref]
        sns.distplot(dfplot['full_count'], ax=ax[i][0]).set_title('{} : {} formes distinctes, {} total occurrences (100%)'.format(pref, dist1.loc[pref,'count'], dist1.loc[pref,'sum']))
        # get 0.95 quantile
        q = dfplot["full_count"].quantile(0.9)
        dfplot2 = dfplot[dfplot["full_count"] < q]['full_count']      
        sns.distplot(dfplot2, ax=ax[i][1]).set_title(pref + ' : 90% quantiles')
        #sns.distplot(np.log(dfplot), ax=ax[0])
        sns.boxplot(dfplot2,ax=ax[i][2]).set_title(pref + ' : 90% quantiles')
        i=i+1
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()         

q = dfpos3["full_count"].quantile(0.9)
dfplot2 = dfpos3[dfpos3["full_count"] < q]      

sns.boxplot(x="prefix", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
pdf2.savefig()
plt.close()

fig, ax = plt.subplots(8,2, figsize=(20, 15))
# get 0.9 quantile
i = 0
for pref in dist1.index.values:
        dfplot3 = dfpos3_rel[dfpos3_rel.prefix == pref].set_index('word')[periods].T
        #print(dfplot3.info())
        dfplot3.index = pd.to_datetime(dfplot3.index)
        dfplot4=dfplot3.resample('5AS').sum()
        #print(dfplot4.info())
        dfplotdiffres = dfplot4.apply(np.ceil).diff()

        dfdiffok = dfplotdiffres.apply(lambda x : x.value_counts(), axis=1)
        dfdiffok.rename(columns={-1.0:'disparition',
                          0.0:'conservation',
                          1.0:'apparition'}, 
                 inplace=True)
        #print(dfdiffok)
        dfdiffok.plot(ax=ax[i][0], title=pref + ": vocabulaire conservé, apparaissant et disparaissant")

        dfplotdiffres['mean_diff'] = dfplot4.diff().apply(lambda x : x.mean(), axis=1)
        dfplotdiffres['mean_diff'].plot(ax=ax[i][1], title=pref + ": moyenne de l'évolution des mots construits (fréquence relative pour base)")
        i=i+1
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()    




# moving average, trends etc.
df5 = dfpos3_rel.groupby('prefix').sum()[periods]
for pref in dist1.index.values : #df5.index.values:
    series = df5.loc[pref]
    ts = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 

    ts['z_data'] = (ts['data'] - ts.data.rolling(window=10).mean()) / ts.data.rolling(window=10).std()
    #ts['zp_data'] = ts['z_data'] - ts['z_data'].shift(10)
    plot_rolling_simple(ts,title= pref, window=10)
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
    pdf2.savefig()
    plt.close()
pdf2.close()

######### par préfixe


for pref in dist1.index.values:
    pdf2 = PdfPages(pref + '-_X_POS_synthesis_googlengrams.pdf')

    # distribution plots
    fig, ax = plt.subplots(3, figsize=(20, 15))
    dfplot = dfpos3[dfpos3.prefix == pref]
    sns.distplot(dfplot['full_count'], ax=ax[0]).set_title('{} : {} formes distinctes, {} total occurrences (100%)'.format(pref, dist1.loc[pref,'count'], dist1.loc[pref,'sum']))
    # get 0.95 quantile
    q = dfplot["full_count"].quantile(0.9)
    dfplot2 = dfplot[dfplot["full_count"] < q]['full_count']      
    sns.distplot(dfplot2, ax=ax[1]).set_title(pref + ' : 90% quantiles')
    #sns.distplot(np.log(dfplot), ax=ax[0])
    sns.boxplot(dfplot2,ax=ax[2]).set_title(pref + ' : 90% quantiles')
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    fig.tight_layout()
    pdf2.savefig()
    plt.close() 
    
    
    q = dfpos3["full_count"].quantile(0.9)
    dfplot2 = dfplot[dfplot["full_count"] < q]      
    sns.boxplot(x="pos", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
    pdf2.savefig()
    plt.close()

    # evolution globale 
    fig, ax = plt.subplots(4, figsize=(20, 15))
    dfpos3[dfpos3.prefix == pref][periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
    dfpos3_rel[dfpos3_rel.prefix == pref][periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
    dfpos3_rel[dfpos3_rel.prefix == pref][periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
    # vocabulaire stable, appariassant, dispariassant
    dfplot3 = dfpos3_rel[dfpos3_rel.prefix == pref].set_index('word')[periods].T
    dfplot3.index = pd.to_datetime(dfplot3.index)
    dfplot4=dfplot3.resample('5AS').sum()
    dfplotdiffres = dfplot4.apply(np.ceil).diff()

    dfdiffok = dfplotdiffres.apply(lambda x : x.value_counts(), axis=1)
    print(dfdiffok)
    dfdiffok.rename(columns={-1.0:'disparition',
                          0.0:'conservation',
                          1.0:'apparition'}, 
                 inplace=True)
    #print(dfdiffok)
    dfdiffok.plot(ax=ax[3], title=pref + ": vocabulaire conservé, apparaissant et disparaissant")
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    fig.tight_layout()
    pdf2.savefig()
    plt.close()
    
    
    # moving average, trends etc.
    df5 = dfpos3_rel.groupby('prefix').sum()[periods]
    series = df5.loc[pref]
    ts = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 
    ts['z_data'] = (ts['data'] - ts.data.rolling(window=10).mean()) / ts.data.rolling(window=10).std()
    plot_rolling_simple(ts,title= pref, window=10)
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()

    
    # nbre de formations différentes par an
    fig, ax = plt.subplots(2, figsize=(20, 15))
    dfpos3[dfpos3.prefix == pref][periods].astype(bool).sum(axis=0).T.plot(ax=ax[0],kind="line", title=pref + " : nombre de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
    dfpos3[dfpos3.prefix == pref][periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : nombre d'occurrences par année", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # global distribution
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 15))
    dfpos3[dfpos3.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')['full_count'].count().plot(ax=ax[0],kind="barh", title=pref + ' : distribution des parties du discours (formes distinctes)', figsize=(20,10))  # [['full_count']]
    dfpos3[dfpos3.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')['full_count'].sum().plot(ax=ax[1],kind="barh", title=pref + ' : distribution des parties du discours (total de formes)', figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # timeline (pos)
    fig, ax = plt.subplots(2, figsize=(20, 15))
    dfpos3[dfpos3.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')[periods].apply(lambda column: (column != 0).sum()).T.plot(ax=ax[0],kind="line", title=pref + " : évolution des distributions des parties du discours(formes distinctes)", rot=45, figsize=(20,10))  # [['full_count']]
    dfpos3[dfpos3.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')[periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : évolution des distributions des parties du discours (total de formes)", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # timeline (word)
    dfpos3[dfpos3.prefix == pref].sort_values(['full_count'],ascending=False).groupby('word')[periods].sum().head(20).T.plot(kind="line", title=pref + " : évolution des distributions des mots", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
#    for k2, grp2 in grp[~grp.word_pos.str.contains('_')].groupby('word_pos'):
    for k2, grp2 in dfpos3[dfpos3.prefix == pref][dfpos3[dfpos3.prefix == pref].pos.isin(['ADJ','ADV','NOUN','VERB'])].groupby('pos'):
        grp2.sort_values(['full_count'],ascending=False).groupby(['word'])[periods].sum().head(20).T.plot(kind="line", title=pref + "+x - " + k2, figsize=(20,10) )
        fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

        pdf2.savefig()
        plt.close()
    pdf2.close()


# ## Plotly

# In[404]:



# with plotly
import plotly.plotly as py
import plotly.tools as pytools
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=False)
#pytools.set_credentials_file(username='ecartierdijon', api_key='3msHhM6RjRcAvIpAgcz6')
#help(py.plot) max 25 public graphs

    
    
filename = "./plotly_graphs/Distribution_mots-distincts_prefixes_POS3_googlengram.html"
group_data = dfpos3.groupby('prefix')['full_count'].count()
#print(group_data)
data = [go.Bar(
            x=group_data.index.values,# 
            y=group_data
    )]

plot(data, filename = filename)

filename = "./plotly_graphs/Distribution_nb_total_prefixes_POS3_googlengram.html"
group_data = dfpos3.groupby('prefix')['full_count'].sum()
#print(group_data)
data = [go.Bar(
            x=group_data.index.values,# 
            y=group_data
    )]

plot(data, filename = filename) 


# In[341]:


# evolution globale pour chaque préfixe
#fig, ax = plt.subplots(3, figsize=(20, 15))
#dfpos3.groupby('prefix')[periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
#dfpos3_rel.groupby('prefix')[periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
#for k,grp in dfpos3.groupby(['prefix']):
#    grp[periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
#plt.show()


# fréquence par nb de formes générées
filename = "./plotly_graphs/Evolution_nb_lexie-prefixes_POS3_googlengram.html"

data = []
for k,grp in dfpos3.groupby(['prefix']):
        dfpref = grp[periods].astype(bool).sum(axis=0).T
        #print(dfpref)
        linegraph = go.Scatter(x=dfpref.index.values, y=dfpref, name=k, opacity = 0.8)
        data.append(linegraph)

layout = dict(
    title='Evolution des nombres de formes différentes par année',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 


# fréquence absolue
filename = "./plotly_graphs/Evolution_absolue-prefixes_POS3_googlengram.html"
group_data = dfpos3.groupby('prefix').sum()
df6 = group_data[periods].T
#print(df6.head())
data = []
for pref in df6.columns.values:
    linegraph = go.Scatter(
        x=df6.index,
        y=df6[pref],
        name = pref,
        opacity = 0.8)
    data.append(linegraph)

layout = dict(
    title='Evolution des fréquences absolues de 1800 à 2010',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 

# frequence relative
filename = "./plotly_graphs/Evolution_relative-prefixes_POS3_googlengram.html"
group_data = dfpos3_rel.groupby('prefix').sum()
df6 = group_data[periods].T
#print(df6.head())
data = []
for pref in df6.columns.values:
    linegraph = go.Scatter(
        x=df6.index,
        y=df6[pref],
        name = pref,
        #line = dict(color = '#17BECF'),
        opacity = 0.8)
    data.append(linegraph)

layout = dict(
    title='Evolution des fréquences relatives de 1800 à 2010',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 


# # now all the cases ...

# In[442]:


dfpos.sep = 'FUSION'
dfpos2.sep = 'ESPACE'
dfpos3.sep = 'TIRET'

dfpos4 = pd.concat([dfpos, dfpos2, dfpos3])
print(dfpos4.info())
print(dfpos4.head())
print(dfpos4.sep.unique())


# In[443]:


dfpos_rel.sep = 'FUSION'
dfpos2_rel.sep = 'ESPACE'
dfpos3_rel.sep = 'TIRET'
dfpos4_rel = pd.concat([dfpos_rel, dfpos2_rel, dfpos3_rel])
print(dfpos4_rel.info())
print(dfpos4_rel.head())

print(dfpos4_rel.sep.unique())


# # save...

# In[444]:


# save to excel
def save_report(report, key, outfile):
    """
    Take a report and save it to a single Excel file
    """
    cols = sorted(list(report.columns.values),reverse=True)
    #print(cols)
    writer = pd.ExcelWriter(outfile)
    for k, grp in report.groupby(key):
        grp[cols].sort_values('full_count', ascending=False).groupby('word').sum().to_excel(writer,k)
#        grp[cols].sort_values('full_count', ascending=False).set_index('word').to_excel(writer,k)
    writer.save()
    return True

#print(df4.head())
save_report(dfpos4, 'prefix','prefixes_allgram_googlengrams1800-2010_freq_abs.xls')
#print(df4.head())
save_report(dfpos4_rel, 'prefix','prefixes_allgram_googlengrams1800-2010_freq_rel.xls')


# In[445]:


# base for browsing prefixes


# In[446]:


dist1 = dfpos4.groupby('prefix')['full_count'].agg(['count','sum']).sort_values('count', ascending=False)
print(dist1)
print(dist1.index.values)
#print(dist1.loc['maxi','count'])


# # synthèse

# In[447]:



pdf2 = PdfPages('Prefix_all_POS_synthesis_googlengrams.pdf')
fig, ax = plt.subplots(1, figsize=(20, 15))
fig.text(4.25/8.5, 0.5/11., "Etude globale sur les mots construits liés par espace \nCorpus Google Ngrams (1800-2010)", ha='center', va='center', fontsize=24, )
fig.tight_layout()
pdf2.savefig()
plt.close()

columns = dfpos4.columns
periods = [elt for elt in columns if re.match("[0-9]{4}", elt)]

# distribution entre les prefixes
fig, ax = plt.subplots(2, figsize=(20, 15))
dfpos4.groupby('prefix')['full_count'].count().plot(ax=ax[0],kind="bar",title='Distribution des fréquences entre préfixes (nbre de formations distinctes)', rot=45, figsize=(20,10))  # [['full_count']]
dfpos4.groupby('prefix')['full_count'].sum().plot(ax=ax[1],kind="bar",title="Distribution des fréquences entre préfixes (nbre total d'occurrences)", rot=45, figsize=(20,10))  # [['full_count']]
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()

pdf2.savefig()
plt.close()
# evolution globale pour chaque préfixe
fig, ax = plt.subplots(3, figsize=(20, 15))
dfpos4.groupby('prefix')[periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
dfpos4_rel.groupby('prefix')[periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
for k,grp in dfpos4.groupby(['prefix']):
    grp[periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()





# distribution plots
fig, ax = plt.subplots(8,3, figsize=(20, 15))
# get 0.9 quantile
i = 0
for pref in dist1.index.values:
        dfplot = dfpos4[dfpos4.prefix == pref]
        sns.distplot(dfplot['full_count'], ax=ax[i][0]).set_title('{} : {} formes distinctes, {} total occurrences (100%)'.format(pref, dist1.loc[pref,'count'], dist1.loc[pref,'sum']))
        # get 0.95 quantile
        q = dfplot["full_count"].quantile(0.9)
        dfplot2 = dfplot[dfplot["full_count"] < q]['full_count']      
        sns.distplot(dfplot2, ax=ax[i][1]).set_title(pref + ' : 90% quantiles')
        #sns.distplot(np.log(dfplot), ax=ax[0])
        sns.boxplot(dfplot2,ax=ax[i][2]).set_title(pref + ' : 90% quantiles')
        i=i+1
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()         

q = dfpos4["full_count"].quantile(0.9)
dfplot2 = dfpos4[dfpos4["full_count"] < q]      

sns.boxplot(x="prefix", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
pdf2.savefig()
plt.close()

fig, ax = plt.subplots(8,2, figsize=(20, 15))
# get 0.9 quantile
i = 0
for pref in dist1.index.values:
        dfplot3 = dfpos4_rel[dfpos4_rel.prefix == pref].set_index('word')[periods].T
        #print(dfplot3.info())
        dfplot3.index = pd.to_datetime(dfplot3.index)
        dfplot4=dfplot3.resample('5AS').sum()
        #print(dfplot4.info())
        dfplotdiffres = dfplot4.apply(np.ceil).diff()

        dfdiffok = dfplotdiffres.apply(lambda x : x.value_counts(), axis=1)
        dfdiffok.rename(columns={-1.0:'disparition',
                          0.0:'conservation',
                          1.0:'apparition'}, 
                 inplace=True)
        #print(dfdiffok)
        dfdiffok.plot(ax=ax[i][0], title=pref + ": vocabulaire conservé, apparaissant et disparaissant")

        dfplotdiffres['mean_diff'] = dfplot4.diff().apply(lambda x : x.mean(), axis=1)
        dfplotdiffres['mean_diff'].plot(ax=ax[i][1], title=pref + ": moyenne de l'évolution des mots construits (fréquence relative pour base)")
        i=i+1
fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
fig.tight_layout()
pdf2.savefig()
plt.close()    




# moving average, trends etc.
df5 = dfpos4_rel.groupby('prefix').sum()[periods]
for pref in dist1.index.values : #df5.index.values:
    series = df5.loc[pref]
    ts = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 

    ts['z_data'] = (ts['data'] - ts.data.rolling(window=10).mean()) / ts.data.rolling(window=10).std()
    #ts['zp_data'] = ts['z_data'] - ts['z_data'].shift(10)
    plot_rolling_simple(ts,title= pref, window=10)
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
    pdf2.savefig()
    plt.close()
pdf2.close()

######### par préfixe


for pref in dist1.index.values:
    pdf2 = PdfPages(pref + '_all_POS_synthesis_googlengrams.pdf')

    # distribution plots
    fig, ax = plt.subplots(3, figsize=(20, 15))
    dfplot = dfpos4[dfpos4.prefix == pref]
    sns.distplot(dfplot['full_count'], ax=ax[0]).set_title('{} : {} formes distinctes, {} total occurrences (100%)'.format(pref, dist1.loc[pref,'count'], dist1.loc[pref,'sum']))
    # get 0.95 quantile
    q = dfplot["full_count"].quantile(0.9)
    dfplot2 = dfplot[dfplot["full_count"] < q]['full_count']      
    sns.distplot(dfplot2, ax=ax[1]).set_title(pref + ' : 90% quantiles')
    #sns.distplot(np.log(dfplot), ax=ax[0])
    sns.boxplot(dfplot2,ax=ax[2]).set_title(pref + ' : 90% quantiles')
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    fig.tight_layout()
    pdf2.savefig()
    plt.close() 
    
    
    q = dfpos4["full_count"].quantile(0.9)
    dfplot2 = dfplot[dfplot["full_count"] < q]      
    sns.boxplot(x="pos", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
    pdf2.savefig()
    plt.close()
    sns.boxplot(x="sep", y="full_count", data=dfplot2) # +  (TBD) kind= violin, box, boxen...
    pdf2.savefig()
    plt.close()
    
    
    # evolution globale 
    fig, ax = plt.subplots(4, figsize=(20, 15))
    dfpos4[dfpos4.prefix == pref][periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
    dfpos4_rel[dfpos4_rel.prefix == pref][periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
    dfpos4_rel[dfpos4_rel.prefix == pref][periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
    # vocabulaire stable, appariassant, dispariassant
    dfplot3 = dfpos4_rel[dfpos4_rel.prefix == pref].set_index('word')[periods].T
    dfplot3.index = pd.to_datetime(dfplot3.index)
    dfplot4=dfplot3.resample('5AS').sum()
    dfplotdiffres = dfplot4.apply(np.ceil).diff()

    dfdiffok = dfplotdiffres.apply(lambda x : x.value_counts(), axis=1)
    #print(dfdiffok)
    dfdiffok.rename(columns={-1.0:'disparition',
                          0.0:'conservation',
                          1.0:'apparition'}, 
                 inplace=True)
    #print(dfdiffok)
    dfdiffok.plot(ax=ax[3], title=pref + ": vocabulaire conservé, apparaissant et disparaissant")
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    fig.tight_layout()
    pdf2.savefig()
    plt.close()
    
    
    # moving average, trends etc.
    df5 = dfpos4_rel.groupby('prefix').sum()[periods]
    series = df5.loc[pref]
    ts = pd.DataFrame({'data':series.values}, index=series.index) # 'year':seriesrel.index, 
    ts['z_data'] = (ts['data'] - ts.data.rolling(window=10).mean()) / ts.data.rolling(window=10).std()
    plot_rolling_simple(ts,title= pref, window=10)
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()

    
    # nbre de formations différentes par an
    fig, ax = plt.subplots(2, figsize=(20, 15))
    dfpos4[dfpos4.prefix == pref][periods].astype(bool).sum(axis=0).T.plot(ax=ax[0],kind="line", title=pref + " : nombre de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
    dfpos4[dfpos4.prefix == pref][periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : nombre d'occurrences par année", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
    # global distribution (pos)
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 15))
    dfpos4[dfpos4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')['full_count'].count().plot(ax=ax[0],kind="barh", title=pref + ' : distribution des parties du discours (formes distinctes)', figsize=(20,10))  # [['full_count']]
    dfpos4[dfpos4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')['full_count'].sum().plot(ax=ax[1],kind="barh", title=pref + ' : distribution des parties du discours (total de formes)', figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
    pdf2.savefig()
    plt.close()

    # global distribution (sep)
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 15))
    dfpos4[dfpos4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('sep')['full_count'].count().plot(ax=ax[0],kind="barh", title=pref + ' : distribution des séparateurs (formes distinctes)', figsize=(20,10))  # [['full_count']]
    dfpos4[dfpos4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('sep')['full_count'].sum().plot(ax=ax[1],kind="barh", title=pref + ' : distribution des séparateurs (total de formes)', figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
    pdf2.savefig()
    plt.close()

    
    # timeline (pos)
    fig, ax = plt.subplots(2, figsize=(20, 15))
    dfpos4[dfpos4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')[periods].apply(lambda column: (column != 0).sum()).T.plot(ax=ax[0],kind="line", title=pref + " : évolution des distributions des parties du discours(formes distinctes)", rot=45, figsize=(20,10))  # [['full_count']]
    dfpos4[dfpos4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('pos')[periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : évolution des distributions des parties du discours (total de formes)", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()

    # timeline (sep)
    fig, ax = plt.subplots(2, figsize=(20, 15))
    dfpos4[dfpos4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('sep')[periods].apply(lambda column: (column != 0).sum()).T.plot(ax=ax[0],kind="line", title=pref + " : évolution des distributions des séparateurs(formes distinctes)", rot=45, figsize=(20,10))  # [['full_count']]
    dfpos4[dfpos4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('sep')[periods].sum().T.plot(ax=ax[1],kind="line", title=pref + " : évolution des distributions des séparateurs (total de formes)", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()

    
    # timeline (word)
    dfpos4[dfpos4.prefix == pref].sort_values(['full_count'],ascending=False).groupby('word')[periods].sum().head(20).T.plot(kind="line", title=pref + " : évolution des distributions des mots", rot=45, figsize=(20,10))  # [['full_count']]
    fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)

    pdf2.savefig()
    plt.close()
#    for k2, grp2 in grp[~grp.word_pos.str.contains('_')].groupby('word_pos'):
    for k2, grp2 in dfpos4[dfpos4.prefix == pref][dfpos4[dfpos4.prefix == pref].pos.isin(['ADJ','ADV','NOUN','VERB'])].groupby('pos'):
        grp2.sort_values(['full_count'],ascending=False).groupby(['word'])[periods].sum().head(20).T.plot(kind="line", title=pref + "+x - " + k2, figsize=(20,10) )
        fig.text(4.25/8.5, 0.5/11., pdf2.get_pagecount(), ha='center', va='center', fontsize=8)
        pdf2.savefig()
        plt.close()
        
    pdf2.close()



# In[ ]:


# plotly


# In[418]:



# with plotly
import plotly.plotly as py
import plotly.tools as pytools
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=False)
#pytools.set_credentials_file(username='ecartierdijon', api_key='3msHhM6RjRcAvIpAgcz6')
#help(py.plot) max 25 public graphs

    
    
filename = "./plotly_graphs/Distribution_mots-distincts_prefixes_POS_all_googlengram.html"
group_data = dfpos4.groupby('prefix')['full_count'].count()
#print(group_data)
data = [go.Bar(
            x=group_data.index.values,# 
            y=group_data
    )]

plot(data, filename = filename)

filename = "./plotly_graphs/Distribution_nb_total_prefixes_POS_all_googlengram.html"
group_data = dfpos4.groupby('prefix')['full_count'].sum()
#print(group_data)
data = [go.Bar(
            x=group_data.index.values,# 
            y=group_data
    )]

plot(data, filename = filename) 


# In[341]:


# evolution globale pour chaque préfixe
#fig, ax = plt.subplots(3, figsize=(20, 15))
#dfpos4.groupby('prefix')[periods].sum().T.plot(ax=ax[0],kind="line", title="Evolution des distributions des préfixes (fréquence absolue)", rot=45, figsize=(20,10))  # [['full_count']]    
#dfpos4_rel.groupby('prefix')[periods].sum().T.plot(ax=ax[1],kind="line", title="Evolution des distributions des préfixes (fréquence relative)", rot=45, figsize=(20,10))  # [['full_count']]    
#for k,grp in dfpos4.groupby(['prefix']):
#    grp[periods].astype(bool).sum(axis=0).T.plot(ax=ax[2],kind="line", title="Evolution des nombres de formes différentes par année", rot=45, figsize=(20,10))  # [['full_count']]
#plt.show()


# fréquence par nb de formes générées
filename = "./plotly_graphs/Evolution_nb_lexie-prefixes_POS_all_googlengram.html"

data = []
for k,grp in dfpos4.groupby(['prefix']):
        dfpref = grp[periods].astype(bool).sum(axis=0).T
        #print(dfpref)
        linegraph = go.Scatter(x=dfpref.index.values, y=dfpref, name=k, opacity = 0.8)
        data.append(linegraph)

layout = dict(
    title='Evolution des nombres de formes différentes par année',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 


# fréquence absolue
filename = "./plotly_graphs/Evolution_absolue-prefixes_POS_all_googlengram.html"
group_data = dfpos4.groupby('prefix').sum()
df6 = group_data[periods].T
#print(df6.head())
data = []
for pref in df6.columns.values:
    linegraph = go.Scatter(
        x=df6.index,
        y=df6[pref],
        name = pref,
        opacity = 0.8)
    data.append(linegraph)

layout = dict(
    title='Evolution des fréquences absolues de 1800 à 2010',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 

# frequence relative
filename = "./plotly_graphs/Evolution_relative-prefixes_POS_all_googlengram.html"
group_data = dfpos4_rel.groupby('prefix').sum()
df6 = group_data[periods].T
#print(df6.head())
data = []
for pref in df6.columns.values:
    linegraph = go.Scatter(
        x=df6.index,
        y=df6[pref],
        name = pref,
        #line = dict(color = '#17BECF'),
        opacity = 0.8)
    data.append(linegraph)

layout = dict(
    title='Evolution des fréquences relatives de 1800 à 2010',
    xaxis=dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plot(fig, filename = filename) 


# In[ ]:




