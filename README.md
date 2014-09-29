delta-cliques
=============

Algorithm for computing Delta-cliques in link streams

Usage:
```
cat <data_file> | python main.py <int:delta>
```

Where <data_file> is a sequence of triplets:
```
1 2 3
1 1 3
...
```
 Meaning that at time 1, nodes 2 and 3 interacted.

The code can be run on 10 test cases by using
```
python TestClique.py
```
