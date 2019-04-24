from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import pickle as pkl
import json

def detect_landmarks(image,shape_predictor):
	# initialize dlib's face detector and then create
	# the facial landmark predictor
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(shape_predictor)

	# convert image to grayscale
	#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	 
	# detect a face in the grayscale image
	try:
		rect = detector(image, 1)[0]

		# determine the facial landmarks for the face region
		shape = predictor(image, rect)
		shape = face_utils.shape_to_np(shape)
		return shape
	except:
		return None

def draw_mouth_detection(image,shape):

	(i, j) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
	# clone the original image so we can draw on it
	clone = image.copy()

	# draw each mouth feature as a dot over the image
	for (x, y) in shape[i:j]:
		cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)

	# extract the mouth region
	(x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
	roi = image[y:y + h, x:x + w]
	roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)

	# show the particular face part
	cv2.imshow("ROI", roi)
	cv2.waitKey(0)

	# show the mouth features as an overlay
	cv2.imshow("Image", clone)
	cv2.waitKey(0)

	# show all facial landmarks with an overlay
	output = face_utils.visualize_facial_landmarks(image, shape)
	cv2.imshow("Image", output)
	cv2.waitKey(0)

def create_x(image):
	shape_predictor = "shape_predictor_68_face_landmarks.dat"
	(i, j) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

	shape = detect_landmarks(image, shape_predictor)
	if shape is None:
		return None

	# extract the mouth region
	(x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
	# roi = image[y:y + h, x:x + w]
	#roi = imutils.resize(roi, width=250, height=150, inter=cv2.INTER_CUBIC)
	
	center_h = int((y+y+h)/2)
	center_w = int((x+x+w)/2)
	new_h = 30
	new_w = 50

	# cropped_img = img.crop((w//2 - 50//2, h//2 - 50//2, w//2 + 50//2, h//2 + 50//2))

	left = center_w-new_w/2
	top = center_h-new_h/2
	right = center_w+new_w/2
	bottom = center_h+new_h/2

	roi = image[top:bottom, left:right]
	return roi

def norm_digit(im):
    h, w = im.shape
    if h > w:
        top, left = int(h * 0.1), int((1.2 * h - w) / 2)
    else:
        top, left = int(w * 0.1), int((1.2 * w - h) / 2)

    return cv2.resize(
        cv2.copyMakeBorder(im, top, top, left, left, cv2.BORDER_CONSTANT), 
        (100, 100)
    )

def create_feature_and_label_vectors(file):
    
    vidData = pkl.load(open(file,'r'))
    
    
    with open('dct.json', 'r') as file:
        dct = json.load(file)

    # one-hot encode dictionary entries
    vocabSize = len(dct) 
    dctVector = np.zeros(len(vidData), dtype = int)
    for i in range(len(vidData)):
        dctVector[i] = dct[vidData[i]['word']]

    b = np.zeros((len(vidData), vocabSize))
    b[np.arange(len(vidData)), dctVector] = 1
    
    X = []
    Y = []
    badidx = []

    for i in range(len(5)):
        feature = []

		#iterate over frame
        for frame in vidData[i]['data']:
            frame = frame.astype(np.uint8)
            x = create_x(frame)

			#if we can't detect a face, move on
            if x is None:
                break
            x = x.flatten()
            feature += list(x)
			# print(x.shape)
			# cv2.imshow('image',x)
			# cv2.waitKey(0)

        if len(feature) == 50*30*4:
            X.append(feature)
            Y.append(b[i])
        else:
            badidx.append(i)

    print(np.array(X).shape)

    np.savetxt("X.txt", np.array(X))
    np.savetxt("badidx.txt", np.array(badidx))





if __name__ == "__main__":
	# video_path = "data/5555060020487251939/00002.mp4"
	# shape_predictor = "shape_predictor_68_face_landmarks.dat"
	# video = cv2.VideoCapture(video_path)

	# # grab a frame of the video
	# status, frame = video.read()

	# # resize it
	# image = imutils.resize(frame, width=500)

	# # detect features 
	# # shape is an array of tuples where shape[i] is a coordinate
	# # (x,y) of a facial feature - the dict face_utils.FACIAL_LANDMARKS_IDXS
	# # maps face part (mouth, nose, etc.) to start, end idxs in shape
	# shape = detect_landmarks(image,shape_predictor)

	# # draw features as overlay
	# draw_mouth_detection(image,shape)
	create_feature_vectors("vidData.pkl")
 