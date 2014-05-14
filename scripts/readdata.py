import sys
import os

def read_supreme_court():
    all_utterances = []
    with open('../data/supreme_court_dialogs_corpus_v1.01/supreme.conversations.txt', 'r') as f:
        for line in f:
            u = {}
            splits = line.split(' +++$+++ ')
            u['case_id'] = splits[0]
            u['utterance_id'] = splits[1]
            if splits[2] == 'TRUE':
                u['after_prev'] = True
            else:
                u['after_prev'] = False
            u['speaker'] = splits[3]
            if splits[4] == 'JUSTICE':
                u['is_justice'] = True
            else:
                u['is_justice'] = False
            u['justice_vote'] = splits[5]
            u['presentation_side'] = splits[6]
            u['utterance'] = splits[7]
            all_utterances.append(u)
    print "Supreme Court data read"
    return all_utterances


#utterances = read_supreme_court()

# for u in xrange(0, 9):
#     print utterances[u]

# for speaker in utterances
