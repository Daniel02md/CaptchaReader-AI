import cv2 as cv
import os
import numpy as np
import pickle
from imutils import paths
from helpers import resize_to_fit
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense


aupha_num_folder = "captcha/aupha_num_letters"
datas = []
labels = []

images = paths.list_images(aupha_num_folder)

for img in images:
    label = img.split(os.path.sep)[-2]
    image = cv.imread(img)
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = resize_to_fit(image, 20, 20)
    
    image3d = np.expand_dims(image, axis=-1)
    
    labels.append(label)
    datas.append(image3d)

datas = np.array(datas, "float") / 255
labels = np.array(labels)


X_train, X_test, Y_train, Y_test = train_test_split(datas, labels, test_size=0.25, random_state=0)

lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)

with open('labelbinarizer_to_letter.dat', 'wb') as arquivo_pickle:
    pickle.dump(lb, arquivo_pickle)


model = Sequential()

model.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Flatten())
model.add(Dense(500, activation="relu"))

model.add(Dense(16, activation="softmax"))


model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])


model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=16, epochs=10, verbose=1, )
model.save("AI.hdf5", overwrite=True)