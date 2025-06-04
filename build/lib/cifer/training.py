import tensorflow as tf
from tensorflow.keras import Model

def train_custom_model(model: Model, x_train, y_train, epochs=10):
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    history = model.fit(x_train, y_train, epochs=epochs, verbose=1)
    return history
