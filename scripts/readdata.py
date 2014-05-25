import sys
import os
import json

def read_house_hearing():
    all_utterances = {}
    base_path = '../../data/house_hearing_transcripts/'
    for filename in os.listdir(base_path):
        with open(base_path + filename) as f:
            data = json.load(f)
            for utterance in data['transcript']:
                speaker = utterance['speaker']['name']['first'] + ' ' + utterance['speaker']['name']['last']
                speech = utterance['speech']
                if speaker not in all_utterances:
                    all_utterances[speaker] = [speech]
                else:
                    new_speeches = all_utterances[speaker]
                    new_speeches.append(speech)
                    all_utterances[speaker] = new_speeches
    print "House hearings data read"
    return all_utterances
    #TODO figure out how this data should be stored and return it

def read_supreme_court():
    all_utterances = {}
    speaker_pairs = {}
    with open('../../data/supreme_court_dialogs_corpus_v1.01/supreme.conversations.txt', 'r') as f:
        prev_utterance_id = -1
        for line in f:
            u = {}
            splits = line.split(' +++$+++ ')
            u['case_id'] = splits[0]
            utterance_id = int(splits[1])
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
            u['utterance'] = splits[7].strip()
            all_utterances[utterance_id] = u

            if u['after_prev']:
                prev_speaker = all_utterances[prev_utterance_id]['speaker']
                speaker_pair = (prev_speaker, u['speaker'])
                speaker_pair_ids = (prev_utterance_id, utterance_id)
                if speaker_pair not in speaker_pairs:
                    speaker_pairs[speaker_pair] = [speaker_pair_ids]
                else:
                    new_ids = speaker_pairs[speaker_pair]
                    new_ids.append(speaker_pair_ids)
                    speaker_pairs[speaker_pair] = new_ids
            prev_utterance_id = utterance_id
    print "Supreme Court data read"
    return (all_utterances, speaker_pairs)

