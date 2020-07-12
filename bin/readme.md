# Traitements et données

Ce répertoire contient les données et les traitements effectués pour l'étude 

## Récupération et nettoyage des données

- récupération des données brutes de Google Ngrams (en prenant les fichiers concernés sur le site)
- nettoyage initial en ne conservant que les lignes commençant par l'un des préfixes
- élimination des lignes commençant par sur
- élimination mots contenant des chiffres (\d)
- conservation des mots de plus de trois lettres (ou un s ou rien en cas d'emploi autonome du préfixe)

NO POS
=>
1-grams: 5381 au total
super    1400
hyper    1202
extra     985
archi     653
supra     335
ultra     316
maxi      251
méga      239

2-grams: 2672
3-grams: 3393

- élimination stoplist
=>
1-grams : 2449
hyper    876
super    445
extra    403
supra    235
ultra    190
archi    155
méga     140
maxi       5

2-grams : 2393
super    1052
extra     474
supra     424
ultra     329
hyper      71
archi      26
maxi       17

3-grams: 3393
extra    856
ultra    555
super    362
hyper    180
archi     97
méga      26
maxi       6

Total : 8243 
super    1860
extra    1734
hyper    1128
ultra    1075
supra     660
archi     279
méga      167
maxi       29


POS
1-grams:
Avant stoplist : 8713
Après stoplist: 4013
hyper	239
super	164
extra	98
méga	85
archi	81
ultra	76
supra	50
maxi	9

       count      sum
prefix                
hyper     239   247681
super     164   800862
extra      98   999827
méga       85    80663
archi      81   223565
ultra      76   679808
supra      50  1400359
maxi        9    33790


2-grams: 84696
après élimination sur : 8668
après élimination des doublons sans pos : 3177
après stoplist : 1481 puis 1114
extra    312
supra    241
ultra    231
super    229
hyper     53
maxi      27
archi     21
Puis 788 :
extra    262
ultra    194
super    146
supra    122
hyper     41
archi     13
maxi      10

        count      sum
prefix                
extra     262  36858.0
ultra     194  34652.0
super     146  23823.0
supra     122  33642.0
hyper      41   3080.0
archi      13   1056.0
maxi       10    991.0

3-grams:46627
après élimination sur : 46627
après élimination des doublons sans pos : 36705
après stoplist : 1481 puis 1114

Total:
