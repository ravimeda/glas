# Copyright 2017 The Nader Akoury. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

""" The Cell model """
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import tensorflow.contrib.framework as framework
import tensorflow.contrib.rnn as rnn

from glas.model.rnn import RNN


class Cell(RNN):
    """ Cell model """
    def __init__(self, num_units, num_layers=1, scope='Cell'):
        """ Initialize the cell """
        super(Cell, self).__init__(scope=scope)

        self.num_units = num_units
        self.num_layers = num_layers

    @property
    def cell(self):
        """ Return the cell """
        with tf.variable_scope(self.variable_scope, reuse=self.reuse):
            cell = rnn.LSTMCell(self.num_units, reuse=self.reuse)

            if self.num_layers > 1:
                cell = rnn.MultiRNNCell([cell] * self.num_layers)

        return cell

    @property
    def output_size(self):
        """ Return the cell output size """
        return self.cell.output_size

    @property
    def state_size(self):
        """ Return the cell state size """
        return self.cell.state_size

    def zero_output_like(self, tensor):
        """ Get the zero output like the passed in tensor """
        batch_size = tensor.get_shape().as_list()[0]
        return tf.zeros((batch_size, self.output_size), tensor.dtype)

    def zero_state_like(self, tensor):
        """ Get the zero state like the passed in tensor """
        batch_size = tensor.get_shape().as_list()[0]
        return self.cell.zero_state(batch_size, tensor.dtype)

    @framework.add_arg_scope
    @RNN.step_fn
    def __call__(self, data, outputs_collections=None):
        """ Execute the next time step of the cell """
        state = self.state if self.step > 0 else self.zero_state_like(data)

        return self.cell(data, state)

    next = __call__
