# Programmes

Ce répertoire contient les traitements effectués pour l'étude (pour l'instant à partir des données Google Ngrams et Néoveille 2016-2020).

## Google Ngrams

Deux programmes permettent de récupérer et nettoyer les données brutes de Google Ngrams :
- `google_ngrams_filter.py` : récupération des données Google Ngrams, filtrage des lignes contenant les préfixes étudiés, et élimination des lignes contenant l'étiquette morphosyntaxique. Ce programme génère trois fichiers pour le filtrage suivant, dans le répertoire `data`: `fre.prefixes.1.grams.1799-2009.csv`, 'fre.prefixes.2.grams.1799-2009.csv', `fre.prefixes.3.grams.1799-2009.csv`. Voir le fichier Python pour plus de détails.
- `google_ngrams_processing.ipynb` : ce programme filtre et fusionne les fichiers générés par le programme précédent, et produit plusieurs fichiers dans le sous-répertoire `data`: `df_googlengrams_all.csv` (chaque ligne contient une forme lexicale retenue, et pour chaque année, sa fréquence absolue, la première ligne contient les en-têtes, séparateur `\t`), et fréquence absolue par année , `df_googlengrams_all_freqrel.csv` (chaque ligne contient une forme lexicale retenue, et pour chaque année, sa fréquence relative, la première ligne contient les en-têtes, séparateur `\t`), `df_googlengrams_neoveille_visu.csv` (fichier csv avec sur chaque ligne la forme lexicale complète, le préfixe, le mot lié, le séparateur, l'année et la fréquence relative; ce fichier est utilisé pour la visualisation interactive Néoveille), `prefixes_googlengrams_synthesis.xls` (fichier excel reprennant pour chaque préfixe les formes liées et la fréquence absolue).


### Résultats synthétiques des filtrages successifs

1. Après programme `google_ngrams_filter.py`
* 1-grams: 10358 lexies
* 2-grams: 26763 lexies
* 3-grams: 3393 lexies

2. Après programme `google_ngrams_processing.ipynb`:
* après élimination lexies commençant par `sur`:

* après élimination stoplist


## Néoveille (to be done)
