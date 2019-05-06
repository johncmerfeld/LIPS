import glob, re, json, sys

# how many files to look at, supplied by script

text = []
files = glob.glob('../ainezm/mvlrs_v1/pretrain/**/*.txt', recursive = True)

files.sort()

for file in files:
    with open(file, 'r') as opened:
        raw = opened.read().replace('\n', ' ')
        t1 = re.sub("Text:", "", raw)
        t2 = re.sub("Conf: .*", "", t1)
        text.append(t2)

# create a mapping from words to unique numbers
dct = dict()
# create a mapping from words to frequencies
dctFreq = dict()
did = 0
for line in text:      
    for word in line.split():
        if word not in dct:
            dct[word] = did
            did += 1
            dctFreq[word] = 1
        else:
            dctFreq[word] += 1

# write out json files
with open('dct.json', 'w') as file:
    json.dump(dct, file, sort_keys = True, indent = 2)
    
with open('dctFreq.json', 'w') as file:
    json.dump(dctFreq, file, sort_keys = True, indent = 2)
