# -*- coding: utf-8 -*-
"""Dicoding_ML_Beginner_SWP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VAlMd6TiyLf8XxVuNiKVHlKyBlMWf9mQ
"""

!wget --no-check-certificate \
  https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip

import numpy as np
import matplotlib.pyplot as plt
import zipfile
import os
import shutil
import math
from tqdm import tqdm

import tensorflow as tf

loc_zip = 'rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(loc_zip, 'r')
zip_ref.extractall('Dataset/')
zip_ref.close()

dataset_dir = 'Dataset/rockpaperscissors/rps-cv-images'
rock_dir = 'Dataset/rockpaperscissors/rps-cv-images/rock'
paper_dir ='Dataset/rockpaperscissors/rps-cv-images/paper'
scissors_dir ='Dataset/rockpaperscissors/rps-cv-images/scissors'

file_txt = 'Dataset/rockpaperscissors/rps-cv-images/README_rpc-cv-images.txt'
os.remove(file_txt)

kelas = os.listdir(dataset_dir)
print(kelas)
data_kelas = np.array(kelas)
print(data_kelas)

import cv2
X=[]
Z=[]
lebar_gambar = 300
tinggi_gambar = 200

def label_gambar(img, gaya_suit):
  return gaya_suit

def data_training(gaya_suit, DIR):
  for img in tqdm(os.listdir(DIR)):
    label=label_gambar(img,gaya_suit)
    path = os.path.join(DIR,img)
    img = cv2.imread(path,cv2.IMREAD_COLOR)
    img = cv2.resize(img, (lebar_gambar, tinggi_gambar))
        
    X.append(np.array(img))
    Z.append(str(label))

data_training('rock',rock_dir)
print(len(X))

data_training('paper',paper_dir)
print(len(X))

data_training('scissors',scissors_dir)
print(len(X))

from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical

le=LabelEncoder()
Y=le.fit_transform(Z)
Y=to_categorical(Y,3)
X=np.array(X)
X=X/255

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,random_state=42)

from keras.callbacks import ReduceLROnPlateau

red_lr= ReduceLROnPlateau(monitor='val_accuracy',patience=3,verbose=1,factor=0.1)

early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    min_delta=0.05,
    patience=3,
    verbose=1,
    mode="auto",
    baseline=None,
    restore_best_weights=False,
)

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout

model = Sequential()
model.add(Conv2D(64, (3,3), input_shape=(200,300,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(32, (3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(32, (3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    zoom_range = 0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip = True)

datagen.fit(x_train)

history = model.fit(datagen.flow(x_train, y_train, batch_size=32), 
                    steps_per_epoch=len(x_train)/32, validation_data=(x_test,y_test),epochs=5,
                    verbose=1,callbacks=[red_lr, early_stop])

model.save("model_fix-rmsprop.h5")
print("Model Berhasil Disimpan")

plt.figure(figsize=(8,6))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Test Accuracy')
plt.title(" Evaluasi Model CNN ")
plt.legend()
plt.show()

plt.figure(figsize=(8,6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Test Lost')
plt.title(" Evaluasi Model CNN ")
plt.legend()
plt.show()

from google.colab import files
from keras.preprocessing import image
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

uploaded = files.upload()
for path in uploaded.keys():
  img = image.load_img(path, target_size=(200,300))
  imgplot = plt.imshow(img)
  test_image = image.img_to_array(img)
  test_image = test_image[np.newaxis,:,:,:]
  hasil = model.predict(test_image)

print(hasil)
if hasil[0][0]==1:
  print("Hasil Prediksi : PAPER")
if hasil[0][1]==1:
  print("Hasil Prediksi : ROCK")
if hasil[0][2]==1:
  print("Hasil Prediksi : SCISSOR")