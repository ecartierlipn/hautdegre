import json
import requests
import sys, csv,re, random, glob,os
import numpy as np                               # vectors and matrices
import pandas as pd                              # tables and data manipulations
import matplotlib.pyplot as plt
import matplotlib.pylab as plt
#%matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6
import matplotlib
import seaborn as sns                            # more plots
from sklearn.metrics import mean_absolute_error
from matplotlib.backends.backend_pdf import PdfPages

files = glob.glob("/Users/emmanuelcartier/Desktop/GitHub/neoveille/diachronic_analysis/neoveille/*.json")
#print(files)
dfglob = pd.DataFrame()
try:
    for file in files:
        elt = re.sub("/Users/emmanuelcartier/Desktop/GitHub/neoveille/diachronic_analysis/neoveille/|.json","",file)
        print("parsing file : " + file + " for elt : [" + elt + ']')
        with open(file) as json_file:
            data = json.load(json_file)
            #print(type(data['response']['docs']))
            #print(data['response']['docs'][0])
            df = pd.DataFrame.from_records(data['response']['docs'])
            df['prefix'] = elt
            #df['contents'] = df['contents'].apply(','.join)
            df['list_occurences'] = df['contents'].apply(','.join).str.findall(elt + "[ -]?\w{0,10}", flags=re.I)
            df.to_csv(file + ".csv")
            dfglob.append(df)
            print(data['response']['numFound'])
except Exception as e:
    print(str(e))

dfglob.to_csv("/Users/emmanuelcartier/Desktop/GitHub/neoveille/diachronic_analysis/neoveille/neoveille_glob.csv")	