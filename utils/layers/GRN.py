from tensorflow.keras.layers import Layer, Dense, LayerNormalization, Dropout
from .GLU import GLU

###
# Gated Residual Network
###

class GRN(Layer):
    def __init__(self, d_model, dropout_rate):
        super(GRN, self).__init__()
        self.d_model = d_model
        self.elu_dense = Dense(d_model, activation="elu")
        self.linear_dense = Dense(d_model)
        self.dropout = Dropout(dropout_rate)
        self.gated_linear_unit = GLU(d_model)
        self.layer_norm = LayerNormalization()
        self.project = Dense(d_model)

    def call(self, inputs):
        x = self.elu_dense(inputs)
        x = self.linear_dense(x)
        x = self.dropout(x)
        if inputs.shape[-1] != self.d_model:
            inputs = self.project(inputs)
        x = inputs + self.gated_linear_unit(x)
        x = self.layer_norm(x)
        return x