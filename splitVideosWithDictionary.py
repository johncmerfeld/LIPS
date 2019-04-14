import json, glob, re, cv2
import numpy as np

#### GLOBAL VALUES
frequencyThreshold = 8 # how many times must a word appear for us to include it

####

with open('dct.json', 'r') as file:
    dct = json.load(file)
    
with open('dctFreq.json', 'r') as file:
    dctFreq = json.load(file)

# get parallel lists of videos and textfile names
textFilenames = glob.glob('data/**/*.txt', recursive = True)
vidFilenames = glob.glob('data/**/*.mp4', recursive = True)

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
print(numberOfClips)
#
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
  
        
    

