import numpy as np
import tflearn
import cv2
import os

from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression


class NeuralModel:

    TRAIN = "data/train/"
    TEST = "data/test1/"
    SIZE = 50
    LR = 0.001
    MODEL_NAME = 'models/dogsvscats-0.001.model'
    DETECTOR = ('cat', 'dog')

    def __init__(self):
        self.model = None
        self.files = None

    @classmethod
    def load_image_grayscale(cls, filename):
        return cv2.resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE), (cls.SIZE, cls.SIZE))

    @classmethod
    def convert_images(cls, images):
        images = list(map(lambda i: 'images/' + i, images))
        images = list(map(lambda i: cls.load_image_grayscale(i), images))
        images = list(map(lambda i: i.reshape(-1, cls.SIZE, cls.SIZE, 1), images))
        return images

    def load_model(self):
        cnn = input_data(shape=[None, self.SIZE, self.SIZE, 1], name='input')

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
        cnn = regression(cnn, optimizer='adam', learning_rate=self.LR, loss='categorical_crossentropy', name='targets')

        model = tflearn.DNN(cnn, tensorboard_dir='log')

        if os.path.exists(f'{self.MODEL_NAME}.meta'):
            model.load(self.MODEL_NAME)

        self.model = model

    def predict(self, image, file):
        ans = self.model.predict(image)[0]
        response = {
            'predictions': ans,
            'answer': {
                'answer': self.DETECTOR[np.argmax(ans)],
                'likelihood': max(ans),
            },
        }
        print(f'With {response["answer"]["likelihood"]} % it is a {response["answer"]["answer"]}')
        _remove_file(file)
        return response


def _remove_file(file):
    if os.path.exists(f"images/{file}"):
        os.remove(f"images/{file}")
