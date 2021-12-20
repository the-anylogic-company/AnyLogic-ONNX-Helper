# Training setup copied from: https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-from-scratch-for-mnist-handwritten-digit-classification/

import numpy as np

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import SGD

import onnx
from tf2onnx.keras2onnx_api import convert_keras

#import cv2
#from imutils import build_montages

def apply_filter(images, threshold, direct=False):
    """
    Convert grayscale to B&W. Could be used to make the predictions in the simple AL demo more accurate.
    
    :param images: One or more images in numpy format
    :param threshold: Values <= will turn black, > will turn white; [0,255]
    :param direct: Whether to apply the changes to the passed images directly (vs a copy)
    :return: the new image (copy)
    """
    target = images if direct else images.copy()
    target[images<=threshold] = 0
    target[images>threshold] = 255
    return target
 

def load_dataset(source='mnist_data.npz', normalize=True, filter_threshold=None, nonblack_threshold=None):
    """
    :param normalize: Whether to normalize the data (scale the X and make Y categorical)
    :param filter_threshold: The value [0,255] to convert the grayscale image to B&W; None = no filter
    :param nonblack_threshold: The number threshold or range of counts that should be non-black; None = allow all
    """
    # load dataset
    with np.load(source) as data:
            trainX=data['x_train']
            testX=data['x_test']
            trainY=data['y_train']
            testY=data['y_test']
    # reshape dataset to have a single channel
    trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
    testX = testX.reshape((testX.shape[0], 28, 28, 1))
    
    if filter_threshold:
        # Note: 220 was found to be a good middleground for AL purposes
        # (It can be previewed by using cv2.imshow(...) with a sample image)
        trainX = apply_filter(trainX, filter_threshold, True)
        testX = apply_filter(testX, filter_threshold, True)

    if nonblack_threshold:
        nonblack_range = (nonblack_threshold,1e9) if isinstance(nonblack_threshold, int) else nonblack_threshold

        trainNon0Counts = np.count_nonzero(trainX.reshape((trainX.shape[0],28*28)), axis=1)
        trainNon0Idxs = np.where((trainNon0Counts >= nonblack_range[0]) & (trainNon0Counts <= nonblack_range[1]))
        trainX = trainX[trainNon0Idxs]
        trainY = trainY[trainNon0Idxs]
        
        testNon0Counts = np.count_nonzero(testX.reshape((testX.shape[0],28*28)), axis=1)
        testNon0Idxs = np.where((testNon0Counts >= nonblack_range[0]) & (testNon0Counts <= nonblack_range[1]))
        testX = testX[testNon0Idxs]
        testY = testY[testNon0Idxs]

    if normalize:
        # scale
        trainX = trainX.astype(float)/255
        testX = testX.astype(float)/255
        # one hot encode target values
        trainY = to_categorical(trainY)
        testY = to_categorical(testY)
    return trainX, trainY, testX, testY


def build_and_fit_model(**kwargs):
    """ Compiles and trainings a model. Keyword arguments will be passed to the dataset method. """
    model = Sequential(
        [
            Input(shape=(28,28,1)), # width, height, channels
            Conv2D(32, kernel_size=(3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(64, kernel_size=(3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dropout(0.5),
            Dense(10, activation="softmax"),
        ]
    )
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    print(model.summary())

    trainX, trainY, testX, testY = load_dataset(**kwargs)
    _ = model.fit(trainX, trainY, epochs=15, batch_size=256, validation_data=(testX, testY), verbose=1)

    return model


def save_to_onnx(model, filename):
    """ Save the keras model as an ONNX file. """
    proto = convert_keras(model)
    
    if not filename.endswith(".onnx"): filename += ".onnx"
    onnx.save(proto, filename)


if __name__ == "__main__":
    model = build_and_fit_model(source='mnist_small.npz')
    save_to_onnx(model, '..\mnist-small.onnx')
