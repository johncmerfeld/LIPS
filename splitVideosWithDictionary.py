import json, glob, re, cv2
import numpy as np

with open('dct.json', 'r') as file:
    dct = json.load(file)

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
            
        # NOTE:
        #   so here's where we could say something like, if words[j] is not in
        #   the "approved" dictionary, don't add it
        #
        for j in range(len(words)):
            textObject = {"word" : words[j],
                          "start" : starts[j],
                          "end" : ends[j],
                          "asdscore" : asdscores[j]}
            textData[i].append(textObject)

def timeToFrame(time, fps):
    return int(time * fps)

vidData = []
for i, vidFile in enumerate(vidFilenames):
    cap = cv2.VideoCapture(vidFile)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # for each word in the text:
    for word in textData[i]:
        
        # get the frames of where it starts and ends
        startFrame = timeToFrame(float(word['start']), fps)
        endFrame = timeToFrame(float(word['end']), fps)
        
        # create a chunk of video frames for that time window
        wordVid = []
        for j in range(startFrame, endFrame):
            cap.set(1, j)
            ret, frame = cap.read() # Read the frame
            wordVid.append(np.array(frame))
        
        vidData.append({"word" : word['word'],
                        "data" : wordVid,
                        "asdscore" : word['asdscore']})
        
        
    

