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

Except explicited, all files are generated :
- step 1 to 3 : in the `../data` subdirectory,
- step 4 and 5 : in the `../data/reference` subdirectory.

Step | Generated files | Contents Explanation
------------ | ------------- | -------------
**1 : generic filtering from raw data** | `fre.2012.prefixes.1.grams.1799-2009.csv`<br/> `fre.2012.prefixes.2.grams.1799-2009.csv`<br/> `fre.2012.prefixes.3.grams.1799-2009.csv` | the list of retained strings after several low-level filtering. Format : string, and for every year (as columns) the absolute count of occurrences
**2a : stoplist removal** | `df_prefixes_allgrams.2012.after_stoplist.csv`<br/>`df_prefixes_1grams.2012_after_stoplist.csv`<br/> `df_prefixes_2grams.2012_after_stoplist.csv`<br/> `df_prefixes_3grams.2012_after_stoplist.csv`|  the complete ngrams datafile after stoplist removal, and split of string into prefix, word and separator; same format as preceding + word, sep and prefix columns added
**2b : PHD filtering** | `df_prefixes_allgrams.2012.after_phd_filtering.csv` | this file contains all data after PHD string filtering (see `../data/stoplists/phd.csv`, which contains the list of strings); same format as preceding
**3 : potential POS tags** | `df_prefixes_allgrams.2012.after_pos_tagging.csv` | the same as above, but with adding the potential pos tags for every base (see `../data/dico_morph/*` for the dictionary used for this process.). Same format as preceding + pos column. 
**4 : outliers removal (absolute frequencies)** | `df_prefixes_allgrams.2012.freq_abs.no_outliers.csv` (copy of the preceding)<br/>`df_prefixes_allgrams.2012.freq_abs.no_outliers.csv` | the same as above WITHOUT outliers; 
**4 : outliers removal (relative frequencies)** |  `df_prefixes_allgrams.2012.freq_rel.csv`<br/>`df_prefixes_allgrams.2012.freq_rel.no_outliers.csv` | the same as above but with relative frequencies;
**5 : Néoveille versions of reference data** |  `df_prefixes_allgrams.2012.freq_abs.neoveille.csv`<br/>`df_prefixes_allgrams.2012.freq_abs.no_outliers.neoveille.csv` <br/> `df_prefixes_allgrams.2012.freq_rel.neoveille.csv`<br/>`df_prefixes_allgrams.2012.freq_rel.no_outliers.neoveille.csv` | the same as above but in the Néoveille platform adequate format (string, prefix, sep, pos, freq, year);

> **_NOTE:_** those just interested in the final data should consider these couple of files (the first one in this project format , the second one in the néoveille format) : 

- `google_ngrams_fr_2012.exploratory_analysis.ipynb` : this notebook parse the reference data generated above, and generate pdf or xls synthesis in the `../visu/` subdirectory. Notably you will find :

File |  Contents
------------ | ------------- | -------------

**`../data/reference/df_googlengrams_all_freq_rel.2012.csv`**.
Several statistics and visualizations synthesis from the above file are generated in the`../visu` subdirectory (see `readme.md` in this directory;


### Google Ngrams 2020 version  :
- `retrieve_googlengrams.fr.2020.sh` : this shell script download the necessary raw gz files and extract the lines containing one of the prefixes; results are generated in the `../data_ngrams/googlengrams.fr.2020` directory with a cleaned.csv file for every corresponding gz gile; see shell script for details;
- `google_ngrams_fr_2020.processing` : this notebook parse the preceding `*.cleaned.csv` files and generate the same files as for the 2012 version but with the 2020 specification int the filenames. this work-in-progress.
    



## Néoveille (to be done)
