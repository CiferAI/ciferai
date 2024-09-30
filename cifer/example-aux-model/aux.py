from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.optimizers import Adam
from keras.datasets import mnist
import numpy as np
import random

def define_model(input_shape, num_classes):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def load_mnist_byCid(cid):
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    client_data_size = len(x_train) // 5
    start_idx = cid * client_data_size
    end_idx = (cid + 1) * client_data_size
    return x_train[start_idx:end_idx], y_train[start_idx:end_idx]

def setWeightSingleList(weight_list):
    flattened_weights = []
    for layer_weights in weight_list:
        flattened_weights.extend(layer_weights.flatten())
    return flattened_weights

def reshapeWeight(flat_weights, weight_shapes):
    reshaped_weights = []
    current_position = 0
    for layer_weights in weight_shapes:
        shape_size = np.prod(layer_weights.shape)
        reshaped_weights.append(np.array(flat_weights[current_position:current_position + shape_size]).reshape(layer_weights.shape))
        current_position += shape_size
    return reshaped_weights

def createRandomClientList(clients, n_round_clients):
    return random.sample(list(clients.keys()), n_round_clients)
