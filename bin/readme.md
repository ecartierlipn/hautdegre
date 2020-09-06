# Programs

this directory contains the main programs to parse French corpora for analyzing prefixes denoting high degree.
Three main corpora are currently under scrutiny:
- Google Ngrams : 2012 and 2020 versions,
- Néoveille corpora (2016-2020), 
- JSI Timestamped web corpus (2014-2020).


The programs in this directory enable to download, parse these respective corpora and generate visualizations for the study of high degree prefixes.


## Google Ngrams

### Google Ngrams 2012 version (Cartier et Huyghe, submitted):
- `retrieve_googlengrams.fr.2012.sh` : this shell script download the necessary raw gz files and extract the lines containing one of the prefixes; results are generated in the `../data_ngrams/googlengrams.fr.2012` directory with a cleaned.csv file for every corresponding gz gile; see shell script for details; (warning : generated files are not included here, they are too big)
- `google_ngrams_fr_2012.processing.ipynb` : this notebook parse the preceding `*.cleaned.csv` files and generate the following files :
    - `../data/fre.2012.prefixes.1.grams.1799-2009.csv`, `../data/fre.2012.prefixes.2.grams.1799-2009.csv`, `../data/fre.2012.prefixes.3.grams.1799-2009.csv`: the list of retained strings **after several filtering** (normalize strings : lowercase(), and convert \s+--?\s+ to ' -'; Check form of string (see regexp for query1gram, query2ram and query3gram) and drop string with integers; merge rows with same string values (after lowercase and normalization of -) : the csv files contain on every line the string, and for every year the count of occurrences;
    - `../data/df_prefixes_allgrams.2012.after_stoplist.csv`,`../data/df_prefixes_1grams.2012_after_stoplist.csv`, `../data/df_prefixes_2grams.2012_after_stoplist.csv`, `../data/df_prefixes_3grams.2012_after_stoplist.csv`:  the complete ngrams datafile **after stoplist removal**, and split of string into prefix, word and separator; every line contain this data and the absolute count per year; first file contains all 1, 2 and 3-grams; the others contain 1,2 and 3-grams only;
    - `../data/df_googlengrams_all_freq_abs.2012.csv` : this file contains all data **after PHD string filtering** (see `../data/stoplists/phd.csv`, which contains the list of strings)
    - **`../data/reference/df_googlengrams_all_freq_abs.pos.2012.csv`** : the same as above, but with adding the potential pos tags for every base (see `../data/dico_morph/*` for the dictionary used for this process.). This is the first reference file, with raw frequency counts; note that we also include the same file BEFORE phd filtering (`../data/reference/df_googlengrams_all_freq_with_phd_freq_abs.pos.2012.csv`);
    - **`../data/reference/df_googlengrams_all_freq_abs.pos.no_outliers.2012.csv`** : the same as above **WITHOUT outliers**; (the same without PHD filtering : , `../data/reference/df_googlengrams_all_freq_with_phd_abs.pos.no_outliers.2012.csv`);
    - **`../data/reference/df_googlengrams_all_freq_rel.2012.csv`** : the same as above but **with relative frequencies**; (`../data/reference/df_googlengrams_all_withfreq_rel.2012.csv` without PHD filtering);
    - `../data/reference/df_googlengrams_neoveille.freqrel.2012.csv`,`df_googlengrams_neoveille.freq_abs.2012`: the same as above but formatted for néoveille platform exploration (relative frequency ans absolute frequency);
    -`../visu`: contains a lot of pdf files synthesizing the data; (see `readme.md` in this directory;
    
### Google Ngrams 2020 version  :
- `retrieve_googlengrams.fr.2020.sh` : this shell script download the necessary raw gz files and extract the lines containing one of the prefixes; results are generated in the `../data_ngrams/googlengrams.fr.2020` directory with a cleaned.csv file for every corresponding gz gile; see shell script for details;
- `google_ngrams_fr_2020.processing` : this notebook parse the preceding `*.cleaned.csv` files and generate the same files as for the 2012 version but with the 2020 specification int the filenames. this work-in-progress.
    



## Néoveille (to be done)
