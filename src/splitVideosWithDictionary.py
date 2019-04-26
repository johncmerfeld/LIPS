import json, glob, re, cv2, sys
import numpy as np

# how many times must a word appear for us to include it
limit = int(sys.argv[1])
wordsFile = sys.argv[2]
vidDataFile = sys.argv[3]
with open(wordsFile, 'r') as file:
    approvedWords = json.load(file)

approvedWords = approvedWords.keys()

# get parallel lists of videos and textfile names
textFilenames = glob.glob('../ainezm/mvlrs_v1/pretrain/**/*.txt')
vidFilenames = glob.glob('../ainezm/mvlrs_v1/pretrain/**/*.mp4')

textFilenames.sort()
vidFilenames.sort()

# for each video, have start and end times for each word
textData = []
for i, textFile in enumerate(textFilenames):
    if i <= limit:
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
                if words[j] in approvedWords:
                    textObject = {"word" : words[j],
                                  "start" : starts[j],
                                  "end" : ends[j],
                                  "asdscore" : asdscores[j]}
                    textData[i].append(textObject)

def timeToFrame(time, fps):
    return int(time * fps)

vidData = []
for i, vidFile in enumerate(vidFilenames):
    if i <= limit:
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

# NOTE: "JSONifying" the numpy array
for i in range(len(vidData)):
    vidData[i]['data'] = vidData[i]['data'].tolist()
     
with open(vidDataFile, 'w') as file:
    json.dump(vidData, file)
