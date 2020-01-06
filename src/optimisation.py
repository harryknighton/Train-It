import nn
from numpy import arange

import data_handling as data


def get_next_pattern():
    """Generates all reasonable network shapes"""
    possValues = list(range(1, 20))
    possValues.remove(10)
    # One layer
    for x in possValues:
        yield [x]
    # Two layers
    for x in possValues:
        for y in possValues:
            yield [x, y]
    # Three Layers
    for x in possValues[:14]:
        for y in possValues[:10]:
            for z in possValues[:10]:
                yield [x, y, z]


def optimise_shape(data, learnRate, batchSize):
    """Experimentally determines optimal network architecture"""
    optimalShape = []
    maxAccuracy = -1
    for layers in get_next_pattern():
        architecture = [9, *layers, 1]  # Add input and output layers
        network = nn.NeuralNetwork(architecture, learnRate)
        network.initialise_parameters()  # Clear weights
        currAcc = nn.train_network(network, data, 50, batchSize)
        if currAcc > maxAccuracy + 1:  # Check if new shape is better
            maxAccuracy = currAcc
            optimalShape = architecture
    return optimalShape


def optimise_learn_rate(data, architecture, batchSize):
    """Experimentally determines optimal learning rate"""
    optimalRate = None
    maxAccuracy = -1
    # Check values around 0.001
    for rate in arange(0.0001, 0.003, 0.0001):
        rate = round(rate, 4)
        network = nn.NeuralNetwork(architecture, rate)
        for i in range(3):
            network.initialise_parameters()  # Clear weights
            currAcc = nn.train_network(network, data, 100, batchSize)
            if currAcc > maxAccuracy + 1:  # Check if new learnRate is better
                maxAccuracy = currAcc
                optimalRate = rate
    return optimalRate


def optimise_batch_size(data, architecture, learnRate):
    """Experimentally determines optimal batch size"""
    optimalBatchSize = None
    maxAccuracy = -1
    for size in [16, 32, 48, 64, 80, 96]:
        network = nn.NeuralNetwork(architecture, learnRate)
        for i in range(3):
            network.initialise_parameters()  # Clear weights
            currAcc = nn.train_network(network, data, 50, size)
            if currAcc > maxAccuracy + 1:  # Check if new size is better
                maxAccuracy = currAcc
                optimalBatchSize = size
    return optimalBatchSize


def optimise_parameters(data):
    shape = None
    learnRate = 0.001
    batchSize = 48
    for i in range(3):
        print(i+1, "- Best parameters:")
        shape = optimise_shape(data, learnRate, batchSize)
        print("Shape:", shape)
        learnRate = optimise_learn_rate(data, shape, batchSize)
        print("Learning Rate:", learnRate)
        batchSize = optimise_batch_size(data, shape, learnRate)
        print("Batch Size:", batchSize)


def optimally_train_network(network, dataset, batchSize):
    """Uses early stopping to avoid over-fitting during training"""
    optimalWeights = []
    optimalBiases = []
    maxAcc = -1
    train, test = data.split_data(dataset, batchSize)
    tF, tL = data.separate_features_and_labels(test)
    # Train
    for epoch in range(150):
        for batch in train:
            f, l = data.separate_features_and_labels(batch)
            network.train(f, l)
        loss, testAcc = network.test(tF, tL)
        print("testAcc", testAcc)
        print("num", numLower)
        if testAcc > maxAcc:
            # optimalWeights always holds best weight set
            optimalWeights = network.weights
            optimalBiases = network.biases
            maxAcc = testAcc
    return maxAcc
