import urllib.request
import numpy as np
import tflearn
import cv2
import os

from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression

import command_system

TRAIN = "data/train/"
TEST = "data/test1/"
SIZE = 50
LR = 0.001
MODEL_NAME = 'models/dogsvscats-0.001.model'
DETECTOR = ('cat', 'dog')


def load_image_grayscale(filename, shape):
    return cv2.resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE), shape)


def convert_images(images):
    images = list(map(lambda i: 'images/' + i, images))
    images = list(map(lambda i: load_image_grayscale(i, (SIZE, SIZE)), images))
    images = list(map(lambda i: i.reshape(-1, SIZE, SIZE, 1), images))
    return images


def load_model(path):
    cnn = input_data(shape=[None, SIZE, SIZE, 1], name='input')

    cnn = conv_2d(cnn, 32, 5, activation='relu')
    cnn = max_pool_2d(cnn, 5)

    cnn = conv_2d(cnn, 64, 5, activation='relu')
    cnn = max_pool_2d(cnn, 5)

    cnn = conv_2d(cnn, 32, 5, activation='relu')
    cnn = max_pool_2d(cnn, 5)

    cnn = conv_2d(cnn, 64, 5, activation='relu')
    cnn = max_pool_2d(cnn, 5)

    cnn = conv_2d(cnn, 32, 5, activation='relu')
    cnn = max_pool_2d(cnn, 5)

    cnn = conv_2d(cnn, 32, 5, activation='relu')
    cnn = max_pool_2d(cnn, 5)

    cnn = fully_connected(cnn, 1024, activation='relu')
    cnn = dropout(cnn, 0.8)

    cnn = fully_connected(cnn, 2, activation='softmax')
    cnn = regression(cnn, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(cnn, tensorboard_dir='log')

    if os.path.exists(f'{path}.meta'):
        model.load(MODEL_NAME)

    return model


def detect(attachments):
    n_files = len(attachments)
    message = ""
    for i in range(n_files):
        urllib.request.urlretrieve(attachments[i], f"images/detect-{i}.jpg")
    files = list(filter(lambda i: 'detect' in i, os.listdir('images/')))
    files = sorted(files, key=lambda x: x.split('-')[1])
    images = convert_images(files)
    model = load_model(MODEL_NAME)
    for i in range(n_files):
        ans = model.predict(images[i])[0]
        print(f'With {max(ans)} % it is a {DETECTOR[np.argmax(ans)]}')
        message += f"на картинке {i+1}/{n_files}. {DETECTOR[np.argmax(ans)]}\n"
        if os.path.exists(f"images/{files[i]}"):
            os.remove(f"images/{files[i]}")
    return message, ""


detect_command = command_system.Command()

detect_command.keys = ["$"]
detect_command.get_content = True
detect_command.description = "Отправь фото и я распознаю на нем я распознаю на нем кота или собаку"
detect_command.process = detect
