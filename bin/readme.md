# Programs

this directory contains the main programs to parse French corpora for analyzing prefixes denoting high degree.
Three main corpora are currently under scrutiny:
- Google Ngrams : 2012 and 2020 versions,
- Néoveille corpora, 
- JSI Timestamped web corpus.





## Google Ngrams

### Google Ngrams 2012 version :
- `retrieve_googlengrams.fr.2012.sh` : this shell script download the necessary raw gz files and extract the lines containing one of the prefixes; results are generated in the `../data_ngrams/googlengrams.fr.2012` directory with a cleaned.csv file for every corresponding gz gile; see shell script for details;
- `google_ngrams_fr_2012.processing` : this notebook parse the preceding `*.cleaned.csv` files and generate the following files :
    - `../data/fre.prefixes.1.grams.1799-2009.2012.csv`, `../data/fre.prefixes.2.grams.1799-2009.2012.csv`, `../data/fre.prefixes.3.grams.1799-2009.2012.csv`: the list of retained strings after several filtering (normalize strings : lowercase(), and convert \s+--?\s+ to ' -'; Check form of string (see regexp for query1gram, query2ram and query3gram) and drop string with integers; merge rows with same string values (after lowercase and normalization of -) : the tsv files contain on every line the string, ans for every year the count of occurrences;
    - `../data/df_googlengrams_all.2012.csv`, `../data/df_googlengrams_all_freqrel.2012.csv`,`../data/df_googlengrams_all_freqrel.2012.no_outliers.csv`,``: the complete ngrams datafile after stoplist removal, and split of string into prefix, word and separator; every line contain this data and the absolute count per year (first file), relative count per year (second file), and data without outliers (90% quertile, third file); 
    - `../data/df_googlengrams_neoveille.2012.csv`,`../data/df_googlengrams_neoveille.2012.no_outliers.csv`: the same data for the Néoveille interactive exploration, in a different format (string, prefix, word, separator, year, relative count). First file with outiliers, second one without.
    -`../visu`: contains a lot of pdf files synthesizing the data;
    
### Google Ngrams 2012 version :
- `retrieve_googlengrams.fr.2020.sh` : this shell script download the necessary raw gz files and extract the lines containing one of the prefixes; results are generated in the `../data_ngrams/googlengrams.fr.2020` directory with a cleaned.csv file for every corresponding gz gile; see shell script for details;
- `google_ngrams_fr_2020.processing` : this notebook parse the preceding `*.cleaned.csv` files and generate the following files :
    - `../data/fre.prefixes.1.grams.1799-2009.2020.csv`, `../data/fre.prefixes.2.grams.1799-2009.2020.csv`, `../data/fre.prefixes.3.grams.1799-2009.2020.csv`: the list of retained strings after several filtering (normalize strings : lowercase(), and convert \s+--?\s+ to ' -'; Check form of string (see regexp for query1gram, query2ram and query3gram) and drop string with integers; merge rows with same string values (after lowercase and normalization of -) : the tsv files contain on every line the string, ans for every year the count of occurrences;
    - `../data/df_googlengrams_all.2020.csv`, `../data/df_googlengrams_all_freqrel.2020.csv`,`../data/df_googlengrams_all_freqrel.2020.no_outliers.csv`,``: the complete ngrams datafile after stoplist removal, and split of string into prefix, word and separator; every line contain this data and the absolute count per year (first file), relative count per year (second file), and data without outliers (90% quertile, third file); 
    - `../data/df_googlengrams_neoveille.2020.csv`,`../data/df_googlengrams_neoveille.2020.no_outliers.csv`: the same data for the Néoveille interactive exploration, in a different format (string, prefix, word, separator, year, relative count). First file with outiliers, second one without.
    -`../visu`: contains a lot of pdf files synthesizing the data;
    



## Néoveille (to be done)
