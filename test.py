import numpy as np
import network
import polytope
import random

poly0 = polytope.Polytope([(0,1),(-1,-1), (1,0)],[[1],[0]], 5)
poly1 = polytope.Polytope([(0,1),(-2,-1),(1,0)],[[0],[1]],5)

poly0.generateData()
poly1.generateData()

def packageData():

    train_data, test_data, temp = [], [], []

    random.shuffle(poly0.data)
    random.shuffle(poly1.data)

    ## Pack Training and Testing data
    for i in range(0, len(poly0.data)):
        if i < len(poly0.data) - int(0.167 * len(poly0.data)):
            train_data.append(poly0.data[i])
        else:
            test_data.append(poly0.data[i])

    for i in range(0, len(poly1.data)):
        if i < len(poly1.data) - int(0.167 * len(poly1.data)):
            train_data.append(poly1.data[i])
        else:
            test_data.append(poly1.data[i])

    ## Format test_data so that y is a single digit representing which neuron is correct, starting from 0 (basically what picard number)
    for (x, y) in test_data:
        y = np.argmax(y)
        temp.append((x,y))
    test_data = temp

    random.shuffle(test_data)
    random.shuffle(train_data)

    return (train_data, test_data)

train_data, test_data = packageData()
nets = []
aveSuccess = []

for layer in range(1,21):
    success = 0

    for i in range(0,10):
        nets.append(network.Network([10,layer,2]))
    
    for net in nets:
        net.SGD(train_data, 45, 10, 2.45, test_data=test_data)
        success += net.success / len(nets)

    aveSuccess.append(round(success,2))
    nets = []

    print("Network[10,{},2]: {}".format(layer, success))


for hidden1 in range(1,21):
    for hidden2 in range(1,21):

        success = 0

        for i in range(0, 10):
            nets.append(network.Network([10, hidden1, hidden2, 2]))

        for net in nets:
            net.SGD(train_data, 45, 10, 2.45, test_data=test_data)
            success += net.success / len(nets)

        aveSuccess.append(round(success,2))
        nets = []
        
        print("Network[10,{},{},2]: {}".format(hidden1, hidden2, success))

with open('aveSuccess.txt', 'w') as out:
    for data in aveSuccess:
        out.write(str(data) + '\n')
