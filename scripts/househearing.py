import readdata

#just testing with one transcript to see how the data should be stored
#base_path = '../../data/house_hearing_transcripts/'
#with open(base_path + 'house_hearing_transcript0.json') as f:
#    data = json.load(f)
#    pprint(data)

#transcript = data['transcript']
#utterances = {}
#for utterance in transcript:
#    speaker_name = utterance['speaker']['name']['first'] + ' ' + utterance['speaker']['name']['last']
#    speech = utterance['speech']
#    if speaker_name not in utterances:
#        utterances[speaker_name] = [speech]
#    else:
#        new_utterances = utterances[speaker_name]
#        new_utterances.append(speech)
#        utterances[speaker_name] = new_utterances


utterances = readdata.read_house_hearing()
print len(utterances)
