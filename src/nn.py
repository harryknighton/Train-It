import numpy as np

import data_handling as data

def ReLU(x):
    return np.maximum(0.05*x, x)


def dReLU(x):
    return np.where(x >= 0, 1, 0.05)


def get_loss(y, yHat):
    """Returns sum of MSE's of y"""
    diffs = np.subtract(yHat, y) ** 2
    loss = np.sum(diffs) / diffs.shape[1]
    return round(loss, 2)


def get_loss_derivative(y, yHat):
    """Returns loss function derivatives of y"""
    return -2 * np.subtract(yHat, y)


def get_accuracy(y, yHat):
    diffs = abs(np.subtract(yHat, y))
    num = (diffs < 0.05).sum()
    accuracy = 100*(num/y.shape[1])
    return round(accuracy, 2)


class NeuralNetwork:
    def __init__(self):
        # Architecture Parameters
        self.shape = [9, 7, 1]
        self.numLayers = len(self.shape)
        self.activationFuncs = [None, "ReLU", "Linear"]

        self.weights = [0]*self.numLayers
        self.biases = [0]*self.numLayers

        # Back-propagation Parameters
        self.learnRate = 0.001
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

    def backward(self, dLoss_dY):
        """Performs back-propagation algorithm on network"""
        dLoss_dA = dLoss_dY
        dLoss_dZ = None
        dLoss_dW = None
        # Iterate through layers backwards
        for i in range(self.numLayers-1, 0, -1):
            # Calculate Derivatives
            if self.activationFuncs[i] == "ReLU":
                dLoss_dZ = dReLU(self.zCache[i]) * dLoss_dA
            elif self.activationFuncs[i] == "Linear":
                dLoss_dZ = dLoss_dA
            else:
                raise RuntimeError
            m = self.aCache[i-1].shape[1]
            dLoss_dW = np.dot(dLoss_dZ, np.transpose(self.aCache[i-1])) / m
            dLoss_db = np.sum(dLoss_dZ, axis=1, keepdims=True) / m
            dLoss_dA = np.dot(np.transpose(self.weights[i]), dLoss_dZ)

            # Adjust parameters
            self.weights[i] -= self.learnRate * dLoss_dW
            self.biases[i] -= self.learnRate * dLoss_db

    def train(self, batch, features):
        self.aCache[0] = batch
        result = self.forward()
        dLoss = get_loss_derivative(result, features)
        self.backward(dLoss)

    def test(self, batch, features):
        self.aCache[0] = batch
        result = self.forward()
        loss = get_loss(result, features)
        accuracy = get_accuracy(result, features)
        return loss, accuracy

    def make_prediction(self, x):
        self.aCache[0] = x
        result = self.forward()
        return data.decode_delay(result)


def train_network(network, dataset, numEpochs, batchSize, showAll=False):
    train, test = data.split_data(dataset, batchSize)
    tF, tL = data.separate_features_and_labels(test)
    maxAccuracy = -1
    for epoch in range(numEpochs):
        for batch in train:
            f, l = data.separate_features_and_labels(batch)
            network.train(f, l)
        loss, acc = network.test(tF, tL)
        if acc > maxAccuracy:
            maxAccuracy = acc
        if showAll:
            print("Epoch", epoch)
            print("Loss:", loss)
            print("Accuracy:", acc)
            print()
    return maxAccuracy
