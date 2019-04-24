import json, glob, re, cv2
import numpy as np
import pickle as pkl

#### GLOBAL VALUES
frequencyThreshold = 4# how many times must a word appear for us to include it

####

with open('dct.json', 'r') as file:
    dct = json.load(file)
    
with open('dctFreq.json', 'r') as file:
    dctFreq = json.load(file)

# get parallel lists of videos and textfile names
textFilenames = glob.glob('data/**/*.txt')
vidFilenames = glob.glob('data/**/*.mp4')

textFilenames.sort()
vidFilenames.sort()

# for each video, have start and end times for each word
textData = []
for i, textFile in enumerate(textFilenames):
    textData.append([])
    with open(textFile, 'r') as opened:
        raw = opened.read().replace('\n', ' ')
        t1 = re.sub(".*ASDSCORE ", "", raw)
        # get the word and its start and end time
        words = []
        starts = []
        ends = []
        asdscores = []
        
        # exploit repeating pattern to get objects from text
        for j, text in enumerate(t1.split()):
            if j % 4 == 0:
                words.append(text)
            elif j % 4 == 1:
                starts.append(text)
            elif j % 4 == 2:
                ends.append(text)
            elif j % 4 == 3:
                asdscores.append(text)
            
        # Currently using frequency threshold but can also search for words
        # manually to keep or remove
        for j in range(len(words)):
            if dctFreq[words[j]] >= frequencyThreshold:
                textObject = {"word" : words[j],
                              "start" : starts[j],
                              "end" : ends[j],
                              "asdscore" : asdscores[j]}
                textData[i].append(textObject)

# for record keeping
numberOfClips = 0
for data in textData:
    numberOfClips += len(data)

def timeToFrame(time, fps):
    return int(time * fps)

vidData = []
for i, vidFile in enumerate(vidFilenames):
    cap = cv2.VideoCapture(vidFile)
    fps = cap.get(cv2.CAP_PROP_FPS)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # for each word in the text:
    for word in textData[i]:
        
        # get the frames of where it starts and ends
        startFrame = timeToFrame(float(word['start']), fps)
        endFrame = timeToFrame(float(word['end']), fps)
        
        # for super short clips!
        if startFrame == endFrame:
            endFrame += 1
        
        # create a chunk of video frames for that time window
        wordVid = np.zeros((endFrame - startFrame, height, width), dtype = int)
        for j in range(startFrame, endFrame):
            cap.set(1, j)
            ret, frame = cap.read() # Read the frame
            grayFrame = np.array(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            wordVid[j - startFrame] = grayFrame
        
        vidData.append({"word" : word['word'],
                        "data" : wordVid,
                        "asdscore" : word['asdscore']})

## median frames per word clip (should be between 3 and 5)
lengths = np.zeros((len(vidData)), int)
for i in range(len(vidData)):
    lengths[i] = len(vidData[i]['data'])
medianFrames = int(np.median(lengths))

for i in range(len(vidData)):
    
    vid = vidData[i]['data']
    frames = len(vid)

    # Downsample or upsample depending on the clip
    # if it is already the desired number of frames, do nothing
    if frames != medianFrames: 
        sampleRate = frames / medianFrames
        #print(str(medianFrames - frames) + " frames")
        
        # sample the median number of frames, repeating for shorter clips
        samples = []
        for j in range(medianFrames):
            samples.append(int((sampleRate) * j))

        # create new data object
        wordVid = np.zeros((medianFrames, height, width), dtype = int)
        for j in range(len(wordVid)):
            wordVid[j] = vid[samples[j]]
        
        # replace video with sampled copy
        vidData[i]['data'] = wordVid
        
#import operator
#rev_x = sorted(dctFreq.items(), key=operator.itemgetter(1), reverse=True)

pkl.dump(vidData, open("vidData.pkl",'w'))
# with open('vidData.txt', 'w') as f:
#     for item in vidData:
#         f.write("%s\n" % item)
    
"""
Number of clips by threshold:
    
    1: 3,789
    2: 3,005
    4: 2,462
    8: 1,958
    16: 1,505
    32: 957
    64: 713 (just a lot of instances of very common words)

"""
