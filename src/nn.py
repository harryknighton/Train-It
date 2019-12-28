import numpy as np


def ReLU(x):
    return np.maximum(0.05*x, x)


def dReLU(x):
    return np.where(x >= 0, 1, 0.05)


def get_loss(y, yHat):
    """Returns sum of MSE's of y"""
    diffs = np.subtract(yHat, y) ** 2
    loss = np.sum(diffs) / diffs.shape[1]
    return loss


def get_loss_derivative(y, yHat):
    """Returns loss function derivatives of y"""
    return -2 * np.subtract(yHat, y)


class NeuralNetwork:
    def __init__(self):
        # Architecture Parameters
        self.shape = [9, 7, 1]
        self.numLayers = len(self.shape)
        self.activationFuncs = [None, "ReLU", "Linear"]

        self.weights = [0]*self.numLayers
        self.biases = [0]*self.numLayers

        # Back-propagation Parameters
        self.learnRate = 0.003
        self.aCache = [0]*self.numLayers
        self.zCache = [0]*self.numLayers

        self.initialise_parameters()

    def initialise_parameters(self):
        """Populate weights and biases with small random floats."""
        np.random.seed(0)
        for i in range(1, self.numLayers):
            self.weights[i] = np.random.randn(self.shape[i], self.shape[i-1]) * 0.1
            self.biases[i] = np.random.rand(self.shape[i], 1) * 0.1

    def forward(self):
        """Feeds aCache[0] through the network."""
        for i in range(1, self.numLayers):
            z = np.dot(self.weights[i], self.aCache[i-1]) + self.biases[i]
            a = None
            # Apply correct activation function
            if self.activationFuncs[i] == "ReLU":
                a = ReLU(z)
            elif self.activationFuncs[i] == "Linear":
                a = z
            else:
                raise RuntimeError
            # Store calculation history
            self.aCache[i] = a
            self.zCache[i] = z
        # Return final value
        return self.aCache[self.numLayers-1]

    def backward(self):
        pass

    def train(self, batch, features):
        self.aCache[0] = batch
        result = self.forward()
        return result
        # dLoss = self.get_loss()
        # self.backward()
