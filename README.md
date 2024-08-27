# ONNX Helper Library for AnyLogic

## About

This library provides a custom object that allows you to easily call predictions from an ONNX file. 

Even though AnyLogic is intended to be used by business-oriented users, it does not hide or limit the possibilities of its internal language (i.e., Java) from the end user. The features this library provides are simply an abstraction on top of the already existing ONNX Runtime Java Library, to make the functionalities more accessible for all! 

## Getting Started

### Installation

The library (a jar file) can be downloaded from the releases page, accessible on the right side of the GitHub page or from [this link](https://github.com/the-anylogic-company/AnyLogic-ONNX-Helper/releases).

After downloading, copy/move the provided jar file in a location where it won't be accidentally moved or deleted.

Then in AnyLogic, in the Palette panel, press the plus ("+") button on the bottom left corner > Manage Libraries... > Add > (Select the jar file) > (OK)

### Usage

The object in this library - "ONNX Helper" - represents a single connection to an ONNX file (.onnx). If you have multiple ONNX files that you want to query from, you can use multiple instances of this object, or a population if you want to get fancy!

After dragging an instance of the helper object into your model, its only property is to reference your desired ONNX file (as a local or absolute path). The helper object has one basic `predict` function with a few variants depending on your preferences and a handful of miscellaneous functions for common operations.

If you run the simulation model, you can click on the helper object to see information about the ONNX model, including:

- the filename

- the name, shape, and data type of all inputs

- the name, shape, and data type of all outputs

For more detailed information about these topics, see this project's Wiki, accessible from the tab on the top of this project's repo.
