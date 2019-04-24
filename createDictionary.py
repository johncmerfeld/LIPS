import glob, re, json

text = []
files = glob.glob('data/**/*.txt', recursive = True)
for file in files:
    with open(file, 'r') as opened:
        raw = opened.read().replace('\n', ' ')
        t1 = re.sub("Text:", "", raw)
        t2 = re.sub("Conf: .*", "", t1)
        text.append(t2)

dct = dict()
# frequency map is just for reference
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

with open('dct.json', 'w') as file:
    json.dump(dct, file, sort_keys = True, indent = 2)
    
with open('dctFreq.json', 'w') as file:
    json.dump(dctFreq, file, sort_keys = True, indent = 2)

            
"""
This leaves us with a dictionary where words map to numbers. It's sort of
backwards from how you intuitively think of a dictionary, but this way you can
encode all incoming data as numbers, and you can still use the model's 
numerical output to search for the corresponding key
"""
