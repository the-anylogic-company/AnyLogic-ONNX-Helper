# Examples

This folder contains some simple examples that utilize the ONNX Helper Library for AnyLogic. They all require you to have the latest version of AnyLogic installed and the library included in your development environment.

The models prefixed with "Demo" are simple demonstrations of the library which are either exceedingly simple toy models or ones trained based on common datasets. Any other models are more practical examples which expect you to be familiar with the basics of navigating an AnyLogic model.

Many examples also include a "python" directory which has the code that was used to generate the ONNX files (provided purely as reference). The descriptions below explain further about the provided scripts and their individual requirements.

If you would like to visualize any of the ONNX files provided, check out: https://netron.app/. 

## Demo - Guess Drawn Numbers

This is a toy model that lets you draw on a 28x28 grid by placing a series of straight lines. The provided ONNX model will attempt to guess what number it "sees".

A subset of the MNIST dataset was used to train the model. To run the Python script, you'll need the libraries: numpy, tensorflow, onnx, and tf2onnx.

## Demo - Iris Prediction

This is a toy model that randomly generates iris flowers of variable sizes. The provided ONNX model will attempt to classify which of three species it is based on the size of the flower's petal and sepal. 

For a visual of each flower type, [see here](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Machine+Learning+R/iris-machinelearning.png).

The Iris dataset was used for training. To run the Python script, you'll need the libraries: numpy, keras, sklearn, onnx, and tf2onnx.

## Demo - Simple Operations

The model demonstrates using an ONNX file with multiple inputs and outputs that use different data types. Some of the inputs/outputs also allow for variable-sized arrays.
The operations on the inputs are simple: transposing, ceiling, multiplication.

The ONNX file for this was created manually, a feature of the ONNX Python library. To run the Python script, you'll need the libraries: numpy and onnx.

## Supply Chain (Modified)

There is a model in AnyLogic's example repository called "Supply Chain", consisting of a retailer, wholesaler, and factory. It comes with an optimization experiment that seeks to find an optimal inventory policy that minimizes daily cost of the operation.

Of relevance to this modified version is how the orders are generated. The original model had a "demandGenerator" event which fired with a Rate of 10x per day (i.e., exponentially distributed interarrival time with mean 1/10). Order sizes range from 1 to 5 and their values are picked from a custom distribution: 40% of orders are size 2, 20% are size 1 or 3, 10% are size 4 or 5.

The goal of the modified version of this model is to train a recurrent neural network on the original dataset of orders (which might consist of order arrival times and their sizes) to forecast the time and size of the next order. In this way, it would provide a more dynamic (and possibly accurate) simulation model rather than simply using the dataset's aggregated statistics.

Side-note: As the arrival rate and distribution of the sizes used by this model are made-up - i.e., there is no "original dataset" - a fake dataset was generated. It consists of arrival time/datestamps and sizes that have daily and quarterly trends. Over the span of 1 year, it follows the distribution of values seen in the original model.

For this RNN, a stateful LSTM was used. It takes as input the current "epoch" time (i.e., seconds since Jan 1st, 1970) and outputs an array of two values: the seconds until the next order and its size. In the model, this process is initiated by an event which then calls a self-recurring dynamic event.



## Simple Hospital (AI Tested)

This is a model of a scenario created based on real-world datasets: one for patient length of stay and another for patient arrival to a hospital. 

This model is adapted from the one used for demonstrating Pypeline (an AnyLogic Python connector library). The h5 files in the original were converted to ONNX files using the keras2onnx library. The subsequent files were then modified to perform some of the normalization and reshaping as part of the inferencing model itself.

