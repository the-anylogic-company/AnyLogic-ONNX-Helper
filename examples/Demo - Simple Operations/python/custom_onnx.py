# Reference:
# https://towardsdatascience.com/creating-onnx-from-scratch-4063eab80fcd

import os
os.environ['ONNX_ML'] = '1'  # necessary if using any node types from Operators-ML
from onnx import helper as h
from onnx import TensorProto as tp
from onnx import checker
from onnx import save
import numpy as np

def custom_onnx():
    """ Generate an ONNX file with multiple inputs and outputs (of various shapes and dimensions). """
    
    # Build all the nodes in the graph
    # Note 1: The ONNX library auto-handles all intermediary connections (e.g., trans_resultA),
    #           but the exposed inputs/outputs need to be defined as value info prototypes (below).
    # Note 2: The node names (e.g., Transpose) are the operators,
    #           as defined here: https://github.com/onnx/onnx/blob/master/docs/Operators.md
    trans_node1 = h.make_node('Transpose',
                             inputs=['toTranspose_A'],
                             outputs=['trans_resultA'])
    trans_node2 = h.make_node('Transpose',
                             inputs=['toTranspose_B'],
                             outputs=['trans_resultB'])
    ceil_node = h.make_node('Ceil',
                            inputs=['ceil_matrix'],
                            outputs=[ 'tmp_matrix' ])
    mult_node = h.make_node('Mul',
                            inputs=['tmp_matrix', 'mult_matrix'],
                            outputs=['result_matrix'])
    graph_nodes = [trans_node1, trans_node2, ceil_node, mult_node]
    
    # Build the list of value info prototypes used in the input
    graph_inputs = [h.make_tensor_value_info('toTranspose_A', tp.INT64, [None,3]),
                    h.make_tensor_value_info('toTranspose_B', tp.INT8, [None,3]),
                    h.make_tensor_value_info('ceil_matrix', tp.FLOAT, [2,3]),
                    h.make_tensor_value_info('mult_matrix', tp.FLOAT, [2,3]),
                    h.make_tensor_value_info('ignored', tp.INT32, [4,1,5])
                    ]
    
    # Build the list of value info protoypes used in the output
    graph_outputs = [h.make_tensor_value_info('trans_resultB', tp.INT8, [3,None]), # purposefully reorder
                     h.make_tensor_value_info('trans_resultA', tp.INT64, [3,None]),
                     h.make_tensor_value_info('result_matrix', tp.FLOAT, [2,3]),
                     ]
    
    # Build a model from the described graph, check its validity, and save it!
    graph = h.make_graph(graph_nodes, "multiio_graph",
                         graph_inputs,
                         graph_outputs)
    mod = h.make_model(graph, producer_name="custom_onnx.py")
    checker.check_model(mod, True)
    save(mod, r"..\simple_ops.onnx")
    return mod
