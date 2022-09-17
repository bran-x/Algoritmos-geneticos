from turtle import forward
import numpy as np


class NNet:
    def __init__(self, inputs, hidden, outputs):
        self.inputs = inputs
        self.hidden = hidden
        self.outputs = outputs
        self.i_layer = np.random.uniform(-1., 1., (hidden, inputs + 1))
        self.h_layer = np.random.uniform(-1., 1., (hidden, hidden + 1))
        self.o_layer = np.random.uniform(-1., 1., (outputs, hidden + 1))

    def forward(self, x):
        x = np.append(x, [1])
        z1 = self.sigmoid(self.i_layer @ x)
        z1 = np.append(z1, [1])
        z2 = self.sigmoid(self.h_layer @ z1)
        z2 = np.append(z2, [1])
        z3 = self.sigmoid(self.o_layer @ z2)
        return z3

    def crossover(self, other):
        new_net = NNet(self.inputs, self.hidden, self.outputs)
        new_net.i_layer = self.crossover_matrix(self.i_layer, other.i_layer)
        new_net.h_layer = self.crossover_matrix(self.h_layer, other.h_layer)
        new_net.o_layer = self.crossover_matrix(self.o_layer, other.o_layer)
        return new_net
    
    @staticmethod
    def crossover_matrix(m1,m2):
        n, m = m1.shape
        row = np.random.randint(0, n)
        col = np.random.randint(0,m)
        m3 = m2.copy()
        m3[:row, :col] = m1[:row, :col]
        return m3

    def mutate(self, mutation_rate):
        self.i_layer = self.mutate_matrix(self.i_layer, mutation_rate)
        self.h_layer = self.mutate_matrix(self.h_layer, mutation_rate)
        self.o_layer = self.mutate_matrix(self.o_layer, mutation_rate)

    @staticmethod
    def mutate_matrix(m1, mutation_rate):
        n, m = m1.shape
        new_mat = m1.copy()
        random_mat = np.random.random((n,m))
        random_vals = np.random.uniform(-0.4, 0.4, (n,m))
        select = random_mat<mutation_rate
        new_mat[select] = new_mat[select] + random_vals[select]
        return new_mat

    @staticmethod
    def relu(x):
        return x*np.array(x>0, dtype=np.float32)

    @staticmethod
    def sigmoid(x):
        return 1/(1+np.exp(-x))

    @staticmethod
    def softmax(x):
        return np.exp(x)/np.sum(np.exp(x))