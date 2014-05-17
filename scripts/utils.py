import sys
import os
import liwc

from nltk import tokenize

def get_liwc_counts_from_utterance(utterance):
    tokens = tokenize_utterance(utterance)
    num_articles, num_aux_verbs, num_conjunctions, num_adverbs, num_ipronouns, num_ppronouns, num_prepositions, num_quantifiers = [0 for x in range(8)] 
    #initializing 8 different variables all to zero
    for token in tokens:
        if token in liwc.articles:
            num_articles += 1
        if token in liwc.aux_verbs:
            num_aux_verbs += 1
        if token in liwc.conjunctions:
            num_conjunctions += 1
        if token in liwc.adverbs:
            num_adverbs += 1
        if token in liwc.ipronouns:
            num_ipronouns += 1
        if token in liwc.ppronouns:
            num_ppronouns += 1
        if token in liwc.prepositions:
            num_prepositions += 1
        if token in liwc.quantifiers:
            num_quantifiers += 1
    return (num_articles, num_aux_verbs, num_conjunctions, num_adverbs, num_ipronouns, num_ppronouns, num_prepositions, num_quantifiers)

def tokenize_utterance(utterance):
    token_list = []
    sent_tokens = tokenize.sent_tokenize(utterance)
    for sent_token in sent_tokens:
        words = tokenize.word_tokenize(sent_token)
        token_list.append(words)
    return [item for sublist in token_list for item in sublist]
