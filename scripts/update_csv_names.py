import sys
import os
import csv
import codecs
import utils

def update_csv_with_2011_12_changes(filename):
    changes = get_2011_12_changes()
    rows = []
    with open(filename) as csvfile:
        reader = utils.UnicodeReader(csvfile, delimiter = ",")
        for row in reader:
            old_name = row[1]
            if old_name in changes:
                new_row = row
                new_row[1] = changes[old_name]
                rows.append(new_row)
            else:
                rows.append(row)
    with open(filename, 'w') as csvfile:
        writer = utils.UnicodeWriter(csvfile, delimiter= ",")
        writer.writerows(rows)

def get_2011_12_changes():
    subtractions = []
    additions = []
    with codecs.open('2011-12-name-changes.csv', encoding='utf-8') as f:
        for line in f:
            splits = line.split(',')
            rank = splits[0]
            if rank == '-':
                subtractions.append(splits[2])
            elif rank == '+':
                additions.append(splits[2])
    return dict(zip(subtractions, additions))

#update_csv_with_2011_12_changes('rank/1993-103.csv')
print get_2011_12_changes()
