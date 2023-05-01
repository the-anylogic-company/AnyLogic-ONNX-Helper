The models in this directory are simple demonstrations of the library which are either exceedingly simple toy models or ones trained based on common test datasets.

## Guess Drawn Numbers

This is a toy model that lets you draw on a 28x28 grid by placing a series of straight lines. The provided ONNX model will attempt to guess what number it "sees".

A subset of the MNIST dataset was used to train the model. To run the Python script, you'll need the libraries: numpy, tensorflow, onnx, and tf2onnx.

## Iris Prediction

This is a toy model that randomly generates iris flowers of variable sizes. The provided ONNX model will attempt to classify which of three species it is based on the size of the flower's petal and sepal. 

For a visual of each flower type, [see here](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Machine+Learning+R/iris-machinelearning.png).

The Iris dataset was used for training. To run the Python script, you'll need the libraries: numpy, keras, sklearn, onnx, and tf2onnx.

## Simple Operations

The model demonstrates using an ONNX file with multiple inputs and outputs that use different data types. Some of the inputs/outputs also allow for variable-sized arrays.
The operations on the inputs are simple: transposing, ceiling, multiplication.

The ONNX file for this was created manually, a feature of the ONNX Python library. To run the Python script, you'll need the libraries: numpy and onnx.