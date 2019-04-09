from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2

def detect_landmarks(image,shape_predictor):
	# initialize dlib's face detector and then create
	# the facial landmark predictor
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(shape_predictor)

	# convert image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	 
	# detect a face in the grayscale image
	rect = detector(gray, 1)[0]

	# determine the facial landmarks for the face region
	shape = predictor(gray, rect)
	shape = face_utils.shape_to_np(shape)
	return shape

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


if __name__ == "__main__":
	video_path = "data/5555060020487251939/00002.mp4"
	shape_predictor = "shape_predictor_68_face_landmarks.dat"
	video = cv2.VideoCapture(video_path)

	# grab a frame of the video
	status, frame = video.read()

	# resize it
	image = imutils.resize(frame, width=500)

	# detect features 
	# shape is an array of tuples where shape[i] is a coordinate
	# (x,y) of a facial feature - the dict face_utils.FACIAL_LANDMARKS_IDXS
	# maps face part (mouth, nose, etc.) to start, end idxs in shape
	shape = detect_landmarks(image,shape_predictor)

	# draw features as overlay
	draw_mouth_detection(image,shape)
 