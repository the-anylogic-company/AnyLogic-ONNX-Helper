from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from tf2onnx.keras2onnx_api import convert_keras
import onnx
import numpy as np

def load_data():
    """ Read and transform the training, validation and test data """
    iris = load_iris()
    X = iris['data']
    y = iris['target']
    names = iris['target_names']
    feature_names = iris['feature_names']

    # One hot encoding
    enc = OneHotEncoder()
    Y = enc.fit_transform(y[:, np.newaxis]).toarray()

    # Scale data to have mean 0 and variance 1 
    # which is importance for convergence of the neural network
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split the data set into training + val and test
    X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=1)

    # Split val out of "training + val"
    X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.25, random_state=1) # 0.25*0.8=0.2

    return (X_train, Y_train), (X_val, Y_val), (X_test, Y_test)
    

def create_custom_model(input_dim, output_dim, nodes, n=1, name='model'):
    """ Build a Sequential model with the specified sepcs """
    # Create model
    model = Sequential(name=name)
    for i in range(n):
        model.add(Dense(nodes, input_dim=input_dim, activation='relu'))
    model.add(Dense(output_dim, activation='softmax'))

    # Compile model
    model.compile(loss='categorical_crossentropy', 
                  optimizer='adam', 
                  metrics=['accuracy'])
    return model

def train_pipeline(layers, nodes_per_layer):
    """ Run thru the pipeline of data loading and model building/training """
    trains, vals, tests = load_data()

    n_features = trains[0].shape[1] # x train
    n_classes = trains[1].shape[1] # y train

    model = create_custom_model(n_features, n_classes, nodes_per_layer, layers, 'model_1')
    
    print(model.summary())

    cb = EarlyStopping(monitor='loss', patience=10, min_delta=0.005)

    _ = model.fit(*trains,
                  batch_size=32,
                  epochs=500,
                  validation_data=vals,
                  callbacks=[cb],
                  verbose=1 if verbose else 0
                  )

    score = model.evaluate(*tests, verbose=0)
    return model, score


def save_to_onnx(model, filename):
    """ Save a keras model as an ONNX file """
    proto = convert_keras(model)

    if not filename.endswith(".onnx"): filename += ".onnx"
    onnx.save(proto, filename)


if __name__ == "__main__":
    model, score = train_pipeline(1, 8)
    print("Score:", score)

    save_to_onnx(model, "..\iris.onnx")
