# ONNX Wrapper Library for AnyLogic

## Installation

The library (a jar file) can be downloaded from the releases page, accessible on the right side of the GitHub page or from [this link](https://github.com/t-wolfeadam/AnyLogic-ONNX-Wrapper-Library/releases/tag/v1.2.0).

Optionally, copy/move the provided jar file in a location where it won't be accidentally moved or deleted.

Then in AnyLogic, in the Palette window, press the plus ("+") button on the bottom left corner > Manage Libraries... > Add > (Select the jar file) > (OK)

## Usage

This section assumes you have a valid ONNX file that you want to use and a model to call it in.

In the Palette window, under the ONNX Wrapper library tab, drag in an instance of the ONNX Wrapper into your model. 

### About

This object represents a single connection to an ONNX file. If you have multiple ONNX files that you want to query from, you will need multiple instances of this object (or a population, if you want to get fancy!).

When you run the model, you can click on the object to see information, including:

- the filename it's using

- the name, shape, and data type of all inputs

- the name, shape, and data type of all outputs

**Important:** if you get an error on startup, there may be a problem with your ONNX file (or compatibility with the current ONNX runtime used by this library). Check the stacktrace for any "human-readable" messages, then complain to Tyler about it :)

### Properties

There are two parameters you can set in the object.

1. ONNX File - a reference to the `.onnx` file.

2. Output return type - describes the format of the predicted values

  - "Map": returns the outputs as a Map-type, with keys as the output names and Object-typed values
  
  - "List": returns the outputs as an ordered ArrayList of Object-typed values (order is taken from the ONNX file)
  
  - "Directly or as a list": if there is only a single output, it is returned directly as an Object type; multiple outputs return as a list (same as the "List" option).
  
### Functions

#### Primary methods

There is one method called "predict" which has four variants. You can use the one that is most applicable to your use case.

`Object predict(Map<String,Object>)` - queries the ONNX model based on the provided mapping from the input name to that input's value (as expected by your ONNX model). Returns as the generic `Object` class.

`T predict(Class<T>, Map<String,Object>)` - same as the above method but allows you to specify the expected return type as the first argument (thus, no type casting required).

`Object predict(Object...)` - queries the ONNX model based on the provided list of inputs (in the order as expected by your ONNX model). Returns as the generic `Object` class.

`T predict(Class<T>, Object...)` - same as the above method but allows you to specify the expected return type as the first argument (thus, no type casting required).

Note: You do not need to cast your inputs to the `Object` type (Java will do this automatically).

#### Helper methods

`int argMax(float[])`

`int argMax(double[])` - returns the index of the maximum value in the provided array.

`int[] argMax(float[][])`

`int[] argMax(double[][])` - returns the index of the maximum value for each array in the provided 2D array.

`T convert(Object, Class<T>)` - converts the provided object to the converted class.

`T[] flatten(Object, Class<T>)` - converts a multi-dimensional array to a single dimension; pass the element type as the second argument.

## Code Examples

Each example below is introduced with a scenario to explain the ONNX model's inputs/outputs that are used in that example. Subsections may use the scenario to show different variations of a concept.

This first example demonstrates the two ways to provide input to the `predict` function. This concept is applicable regardless of what choice is selected for the "output method" parameter. The following examples will then focus on how to handle the output based on the option you selected in the helper's properties; in these examples, they will all use the direct (list) form of the `predict` method. The last set of examples demonstrate miscellaneous concepts (e.g., helper functions).

Across all examples, "`wrapper`" is used to denote an instance of the ONNX Wrapper object.

Note: The code shown is *overly explicit* and not necessarily the best/most concise way of writing the code.

### Example 0: Ways to call `predict`

Scenario: a NN was trained to divide two numbers.

Inputs:

1. "numerators", a double array with shape `(-1,)` (variable length)

2. "denominators", a double array with shape `(-1,)` (variable length)

Outputs:

1. "outputs", a double array with shape `(-1,)` (variable length)

*All arrays are assumed to be of the same size.*

#### As a map

```java
double[] numers = new double[]{1.0, 2.0, 4.0, 1.25};
double[] denoms = new double[]{5.0, 1.0, 0.1, 7.5};
Map<String,Object> inputs = Map.of("numerators", numers, "denominators", denoms);

Object outputs = wrapper.predict(inputs);
// ... handle outputs ...
```

#### As a list

```java
double[] numers = new double[]{1.0, 2.0, 4.0, 1.25};
double[] denoms = new double[]{5.0, 1.0, 0.1, 7.5};

Object outputs = wrapper.predict(numers, denoms);
// ... handle outputs ...

```

### Example 1: Single input, single output

Scenario: a NN was trained on the [iris dataset](https://archive.ics.uci.edu/ml/datasets/iris) to classify the type of iris given four attributes.

Inputs:

1. "iris_input", a float array with shape `(4,)`; describes a single flower's attributes (length and width of sepal and petal)

Outputs:

1. "iris_output", an int array with shape `(3,)`; a one-hot array of the expected class (Setosa, Versicolour, or Virginica)

#### Return type as 'Map'

The following demonstrates handling the outputs returned as a map, the keys of which are defined by the ONNX file.

Note that both the return of `predict` and the map's values are returned as the Object-type, and thus will need to be casted before they can be properly used.

```java
float[] raw_input = new float[]{4.9, 3.1, 1.5, 0.2};

Object output_obj = wrapper.predict(raw_input);

HashMap<String, Object> output_map = (HashMap) output_obj;

int[] raw_output = (int[]) output_map.get("iris_output");
```

#### Return type as 'List'

The following demonstrates handling the outputs returned as a list (always); the order of which is defined by the ONNX file.

Note that both the return of `predict` and the list's values are returned as the Object-type, and thus will need to be casted before they can be properly used.

```java
float[] raw_input = new float[]{4.9, 3.1, 1.5, 0.2};

Object output_obj = wrapper.predict(raw_input);

ArrayList<Object> output_list = (ArrayList) output_obj;

int[] raw_output = (int[]) output_list.get(0);
```

#### Return type as 'Direct or list'

The following demonstrates handling the outputs returned directly (when singular; ie, this case) or a list otherwise (ie, *not* this case).

Note that because the return of `predict` is an Object, and there is only one output, a single casting is required to access the value.

```java
float[] raw_input = new float[]{4.9, 3.1, 1.5, 0.2};

Object output_obj = wrapper.predict(raw_input);

int[] raw_output = (int[]) output_obj;
```

### Example 2: Multiple inputs, multiple outputs

Scenario: a NN was trained for forecasting one step in the future based on attributes of 10 different cities from the past 30 days of data.

Inputs:

1. "i_temperatures", a float array with shape `(10, 30, 1)`

2. "i_icecream_sales", a float array with shape `(10, 30, 1)`

Outputs:

1. "o_temperatures", a float array with shape `(10, 1, 1)`

2. "o_murderrates", a float array with shape `(10, 1, 1)`

Note: Any non-wrapper function calls shown below can be assumed to retrieve relevant data.

#### Return type as 'Map'

The following demonstrates handling the outputs returned as a map, the keys of which are defined by the ONNX file.

Note that both the return of `predict` and the map's values are returned as the Object-type, and thus will need to be casted before they can be properly used.

```java
float[][][] recentTemps = getRecentCityTemps();
float[][][] recentSales = getRecentCitySales();

Object output_obj = wrapper.predict(recentTemps, recentSales);

HashMap<String, Object> output_map = (HashMap) output_obj;

float[][][] forecastedTemps = (float[][][]) output_map.get("o_temperatures");
float[][][] forecastedRates = (float[][][]) output_map.get("o_murderrates");
```

#### Return type as 'List'

The following demonstrates handling the outputs returned as a list (always); the order of which is defined by the ONNX file.

Note that both the return of `predict` and the list's values are returned as the Object-type, and thus will need to be casted before they can be properly used.

```java
float[][][] recentTemps = getRecentCityTemps();
float[][][] recentSales = getRecentCitySales();

Object output_obj = wrapper.predict(recentTemps, recentSales);

ArrayList<Object> output_list = (ArrayList) output_obj;

float[][][] forecastedTemps = (float[][][]) output_list.get(0);
float[][][] forecastedRates = (float[][][]) output_list.get(1);
```

#### Return type as 'Direct or list'

The following demonstrates handling the outputs returned directly (when singular; ie, *not* this case) or a list otherwise (ie, this case).

Note that because the return of `predict` is an Object, and there is more than one output, the example code is *exactly* the same as the "List" example above.

```java
float[][][] recentTemps = getRecentCityTemps();
float[][][] recentSales = getRecentCitySales();

Object output_obj = wrapper.predict(recentTemps, recentSales);

ArrayList<Object> output_list = (ArrayList) output_obj;

float[][][] forecastedTemps = (float[][][]) output_list.get(0);
float[][][] forecastedRates = (float[][][]) output_list.get(1);
```

### Other examples

The following is for any helper methods or demoing miscellaneous topics. See the built-in javadocs for more details.

#### argMax

With a 1D list:

```java
double[] values = new double[]{0.1, 0.2, 100.23, 100.22222229, -5.0};

int maxIndex = wrapper.argMax(values); // = 2
```

With a 2D list:

```java
float[][] values = new float[][]{
					{1f, 2f},
					{-1f, -2f, -3f, -4f, -5f},
					{0.75f, 0.25f, 0.50f}
					};
int[] maxIndices = wrapper.argMax(values) // = [0, 4, 1]
```

#### convert

In the following, assume "getDataPerAgent" is a valid function that returns a 2D *double* array, comprised of "rows" of numerical data per agent in some population.

The ONNX model being used in this example expects a 2D *float* array.

```java
double[][] data_array = getDataPerAgent();

float[][] nn_input = wrapper.convert(data_array, float[][].class);

Object output = wrapper.predict(nn_input);
// ...
```

#### flatten

Note that this method returns an array using the wrapper type of the original class (e.g., Integer for int arrays).

```java
int[][] data2d = new int[][] { {0,1,2}, {3,4,5}, {6,7,8} };

Integer[] data1d = wrapper.flatten(data2d, int.class);
// = [0,1,2,3,4,5,6,7,8]
```
