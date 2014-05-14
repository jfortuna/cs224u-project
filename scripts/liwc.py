import sys
import os

#articles, auxiliary verbs, conjunctions, high-frequency adverbs, impersonal pronouns, personal pronouns, prepositions, and quantifiers

articles = set()
with open('../liwc/articles.txt', 'r') as f:
    for line in f:
        articles.add(line.strip())

aux_verbs = set()
with open('../liwc/aux_verbs.txt', 'r') as f:
    for line in f:
        aux_verbs.add(line.strip())

conjunctions = set()
with open('../liwc/conjunctions.txt', 'r') as f:
    for line in f:
        conjunctions.add(line.strip())

adverbs = set()
with open('../liwc/adverbs.txt', 'r') as f:
    for line in f:
        adverbs.add(line.strip())

ipronouns = set()
with open('../liwc/ipronouns.txt', 'r') as f:
    for line in f:
        ipronouns.add(line.strip())

ppronouns = set()
with open('../liwc/ppronouns.txt', 'r') as f:
    for line in f:
        ppronouns.add(line.strip())

prepositions = set()
with open('../liwc/prepositions.txt', 'r') as f:
    for line in f:
        prepositions.add(line.strip())

quantifiers = set()
with open('../liwc/quantifiers.txt', 'r') as f:
    for line in f:
        quantifiers.add(line.strip())

