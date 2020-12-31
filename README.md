# thesaurus-graph
## find distant synonyms

This project aims to find relationships between words by representing a thesaurus as a graph. Vertices are words and edges are relationships between wrods, currently just synonyms. The program is a REPL that takes a word and a distance and returns a list of words as far as that distance. Think of it as a depth first search with limited depth.

Here is a visualization of [small-thesaurus.csv](https://github.com/1ndy/thesaurus-graph/blob/master/small-thesaurus.csv).
![small-thesaurus.csv](small-thesaurus.png)
