from imutils import paths
import numpy as np
import os
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D,Flatten,Dense
from tensorflow.keras.optimizers import SGD
from keras.utils import to_categorical
import random
from tensorflow.keras.datasets import mnist

def load_test_data():
    """Load MNIST test dataset"""
    (_, _), (x_test, y_test) = mnist.load_data()
    # Resize data appropriately
    x_test = x_test.astype('float32') / 255.0
    x_test = np.expand_dims(x_test, axis=-1)  # Add dimensions to data
    y_test = np.eye(10)[y_test]  # One-hot encoding for labels
    return x_test, y_test

def load_mnist_byCid(cid):
    data = []
    labels = []

    path = f"data/client_{cid}"
    img_paths = list(paths.list_images(path))

    for imgpath in img_paths:
        img_grayscale = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)
        img_resized = cv2.resize(img_grayscale, (28, 28))
        img = np.expand_dims(img_resized, axis=-1) / 255.0
        label = imgpath.split(os.path.sep)[-2]
        data.append(img)
        labels.append(label)
    return np.array(data), np.array(labels)

def define_model(input_shape,num_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=input_shape))
    model.add(MaxPool2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(num_classes, activation='softmax'))
  
    opt = SGD(learning_rate=0.01, momentum=0.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

def setWeightSingleList(weights):
    weights_flat = [w.flatten() for w in weights]    
    weights = np.concatenate(weights_flat).tolist()
    return weights

def reshapeWeight(server_weight, client_weight):
    reshape_weight = []   
    for layer_weights in client_weight:
        n_weights = np.prod(layer_weights.shape)
        reshape_weight.append(np.array(server_weight[:n_weights]).reshape(layer_weights.shape))
        server_weight = server_weight[n_weights:]
    return reshape_weight

def createRandomClientList(clients_dictionary, n_round_clients):
    keys = list(clients_dictionary.keys())
    return random.sample(keys, n_round_clients)