The models in this directory are more practical demos.

## Supply Chain (Modified)

There is a model in AnyLogic's example repository called "Supply Chain", consisting of a retailer, wholesaler, and factory. It comes with an optimization experiment that seeks to find an optimal inventory policy that minimizes daily cost of the operation.

Of relevance to this modified version is how the orders are generated. The original model had a "demandGenerator" event which fired with a Rate of 10x per day (i.e., exponentially distributed interarrival time with mean 1/10). Order sizes range from 1 to 5 and their values are picked from a custom distribution: 40% of orders are size 2, 20% are size 1 or 3, 10% are size 4 or 5.

The goal of the modified version of this model is to train a recurrent neural network on the original dataset of orders (which might consist of order arrival times and their sizes) to forecast the time and size of the next order. In this way, it would provide a more dynamic (and possibly accurate) simulation model rather than simply using the dataset's aggregated statistics.

Side-note: As the arrival rate and distribution of the sizes used by this model are made-up - i.e., there is no "original dataset" - a fake dataset was generated. It consists of arrival time/datestamps and sizes that have daily and quarterly trends. Over the span of 1 year, it follows the distribution of values seen in the original model.

For this RNN, a stateful LSTM was used. It takes as input the current "epoch" time (i.e., seconds since Jan 1st, 1970) and outputs an array of two values: the seconds until the next order and its size. In the model, this process is initiated by an event which then calls a self-recurring dynamic event.

## Simple Hospital (AI Tested)

This is a model of a scenario created based on real-world datasets: one for patient length of stay and another for patient arrival to a hospital. 

This model is adapted from the one used for demonstrating Pypeline (an AnyLogic Python connector library). The h5 files in the original were converted to ONNX files using the keras2onnx library. The subsequent files were then modified to perform some of the normalization and reshaping as part of the inferencing model itself.
