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
            
        for j in range(len(words)):
            textObject = {"word": words[j],
                          "start": starts[j],
                          "end": ends[j],
                          "asdscore": asdscores[j]}
            textData[i].append(textObject)

def timeToFrame(time, fps):
    return int(time * fps)

vidData = []
for i, vidFile in enumerate(vidFilenames):
    cap = cv2.VideoCapture(vidFile)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = timeToFrame(0.5, fps)
    cap.set(1,frame_number); # Where frame_no is the frame you want
    ret, frame = cap.read() # Read the frame
    f = np.array(frame)
    

