import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Convolution2D, MaxPooling2D, GlobalAveragePooling2D
from keras.optimizers import SGD
import sys

def run_mlp(train_X,train_y,test_X, test_y):

	model = Sequential()
	model.add(Dense(64, activation='relu', input_dim=train_X.shape[1]))
	model.add(Dropout(0.5))
	model.add(Dense(64, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(train_y.shape[1], activation='softmax'))

	sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='categorical_crossentropy',
	              optimizer=sgd,
	              metrics=['accuracy'])

	model.fit(train_X, train_y,
	          epochs=100,
	          batch_size=128)
	score = model.evaluate(test_X, test_y, batch_size=128)
	print(score)

def run_cnn(train_X,train_y,test_X,test_y, y_pred_file, num_frames, h, w, epochs):
	model = Sequential()
	model.add(Convolution2D(32,(2,2),input_shape = (h,w*num_frames,1),strides=2))
	model.add(Convolution2D(64,(3,3), activation = 'relu'))
	model.add(MaxPooling2D(pool_size = (2,2)))

	model.add(Convolution2D(64,(3,3),activation = 'relu'))
	model.add(MaxPooling2D(pool_size = (2,2)))

	model.add(GlobalAveragePooling2D())
	model.add(Dropout((0.5)))
	model.add(Dense(train_y.shape[1], activation = 'softmax'))

	model.compile(optimizer = 'adadelta', loss = 'categorical_crossentropy', metrics = ['accuracy'])

	model.fit(train_X, train_y,
	          epochs=epochs,
	          batch_size=64)
	score = model.evaluate(test_X, test_y, batch_size=128)
	print(score)
	out = model.predict(test_X, batch_size=128)
    
	np.savetxt(y_pred_file, out, delimiter=",")

def unflatten_X(X, num_frames, h, w):
	out = []

	for row in X:
		new_row = None
		for i in range(num_frames):
			frame = row[i*h*w:(i+1)*h*w]
			frame = frame.reshape((h, w))
			if new_row is None:
				new_row = frame
			else:
				new_row = np.concatenate((new_row,frame),axis=1)
		out.append(np.array(new_row))
	out = np.array(out)
	print(out.shape)
	return out

if __name__ == "__main__":

    X_file = sys.argv[1]
    y_file = sys.argv[2]
    y_pred_file = sys.argv[3]
    h = int(sys.argv[4])
    w = int(sys.argv[5])
    epochs = int(sys.argv[6])

    X = np.load(X_file)
    y = np.load(y_file)

	#calculate num frames per sample
    num_frames = int(X.shape[1]/(h*w))

    X = unflatten_X(X, num_frames, h, w).reshape((len(X), h,num_frames*w,1))

    split_idx = int(X.shape[0]*.8)

    train_X = X[:split_idx]
    test_X = X[split_idx:]

    train_y = y[:split_idx]
    test_y = y[split_idx:]
    
    y_pred_base = y_pred_file.split('.')[0]
    y_pred_file = y_pred_base + "_" + sys.argv[6] + ".csv"

    run_cnn(train_X,train_y,test_X,test_y, y_pred_file, num_frames, h, w, epochs)


    np.savetxt(y_pred_base + "_" + sys.argv[6] + "_ground_truth.csv", test_y, delimiter = ",")


