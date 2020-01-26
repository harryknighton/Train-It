import numpy as np
from time import time
from statistics import mean

import data_handling as data
import util

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
    losses = -2 * np.subtract(yHat, y)
    # Give more weighting to delayed services
    losses[:, yHat > 0.4] *= 0.75
    losses[:, yHat < 0.4] *= 0.25
    return losses

def get_accuracy(y, yHat):
    diffs = abs(np.subtract(yHat, y))
    num = (diffs < 0.05).sum()
    accuracy = 100*(num/y.shape[1])
    return round(accuracy, 2)


class NeuralNetwork:
    def __init__(self, pShape, pLearnRate, initFromFile=False, adam=False):
        # Architecture Parameters
        self.shape = pShape
        self.numLayers = len(self.shape)
        self.activationFuncs = [None, *["ReLU" for x in range(self.numLayers-2)], "Linear"]

        self.weights = [0]*self.numLayers
        self.biases = [0]*self.numLayers

        # Back-propagation Parameters
        if adam:
            self.adam = True
            self.iteration = 1
            self.beta = 0.9
            self.beta2 = 0.999
            self.epsilon = pow(10, -8)
            self.weightGradients = [0]*self.numLayers
            self.weightsSquared = [0]*self.numLayers
            self.biasGradients = [0]*self.numLayers
            self.biasesSquared = [0]*self.numLayers
        else:
            self.adam = False
        self.learnRate = pLearnRate
        self.aCache = [0]*self.numLayers
        self.zCache = [0]*self.numLayers

        if initFromFile:
            self.load_parameters()
        else:
            self.initialise_parameters()

    def initialise_parameters(self):
        """Populate weights and biases with small random floats."""
        np.random.seed(int(time()))  # Large difference between calls
        for i in range(1, self.numLayers):
            self.weights[i] = np.random.randn(self.shape[i], self.shape[i-1]) * 0.1
            self.biases[i] = np.random.rand(self.shape[i], 1) * 0.1
            if self.adam:
                self.weightGradients[i] = 0
                self.weightsSquared[i] = 0
                self.biasGradients[i] = 0
                self.biasesSquared[i] = 0

    def save_parameters(self):
        """Saves network parameters to csv files"""
        open(util.paramFilePath, 'w').close() # Clear file contents
        with open(util.paramFilePath, 'a') as outFile:
            # Write weights and biases to file
            for i in range(1, self.numLayers):
                np.savetxt(outFile, self.weights[i], delimiter=",", fmt='%.8f')
                np.savetxt(outFile, self.biases[i], delimiter=",", fmt='%.8f')

    def load_parameters(self):
        """Loads parameters into network from save file"""
        with open(util.paramFilePath, 'r') as inFile:
            for i in range(1, self.numLayers):
                self.weights[i] = np.loadtxt(inFile, delimiter=",", max_rows=self.shape[i], ndmin=2)
                self.biases[i] = np.loadtxt(inFile, delimiter=",", max_rows=self.shape[i], ndmin=2)

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

            # Adam Optimisation
            if self.adam:
                self.iteration += 1

                self.weightGradients[i] = self.beta * self.weightGradients[i] + (1 - self.beta) * dLoss_dW
                self.weightsSquared[i] = self.beta2 * self.weightsSquared[i] + (1 - self.beta2) * (np.square(dLoss_dW))
                self.biasGradients[i] = self.beta * self.biasGradients[i] + (1 - self.beta) * dLoss_db
                self.biasesSquared[i] = self.beta2 * self.biasesSquared[i] + (1 - self.beta2) * (np.square(dLoss_db ** 2))

                vdWCorrected = self.weightGradients[i] / (1 - self.beta ** self.iteration)
                sdWCorrected = self.weightsSquared[i] / (1 - self.beta2 ** self.iteration)
                vdbCorrected = self.biasGradients[i] / (1 - self.beta ** self.iteration)
                sdbCorrected = self.biasesSquared[i] / (1 - self.beta2 ** self.iteration)

                # Adjust parameters
                self.weights[i] = self.weights[i] - self.learnRate * (vdWCorrected / (np.sqrt(sdWCorrected) + self.epsilon))
                self.biases[i] = self.biases[i] - self.learnRate * (vdbCorrected / (np.sqrt(sdbCorrected) + self.epsilon))
            else:
                self.weights[i] -= self.learnRate * dLoss_dW
                self.biases[i] -= self.learnRate * dLoss_db

    def train(self, batch, features, returnAccuracy=False):
        self.aCache[0] = batch
        result = self.forward()
        dLoss = get_loss_derivative(result, features)
        self.backward(dLoss)
        if returnAccuracy:
            return get_accuracy(result, features)

    def test(self, batch, features):
        self.aCache[0] = batch
        result = self.forward()
        loss = get_loss(result, features)
        accuracy = get_accuracy(result, features)
        return loss, accuracy

    def make_prediction(self, x):
        self.aCache[0] = x
        result = self.forward()
        return data.decode_delay(result[0][0])


def train_network(network, dataset, numEpochs, batchSize, showAll=False):
    """Trains network with given data for a number of epochs"""
    train, test = data.split_data(dataset, batchSize)
    tF, tL = data.separate_features_and_labels(test)
    trainAccs = []
    maxAccuracy = -1
    for epoch in range(1, numEpochs+1):
        for batch in train:
            f, l = data.separate_features_and_labels(batch)
            trainAccs.append(network.train(f, l, returnAccuracy=True))
        loss, testAcc = network.test(tF, tL)
        trainAcc = mean(trainAccs)
        if testAcc > maxAccuracy:
            maxAccuracy = testAcc
        if showAll:
            print("Epoch", epoch)
            print("Loss:", loss)
            print("Test Accuracy:", testAcc)
            print("Train Accuracy", trainAcc)
            print()
    return maxAccuracy
