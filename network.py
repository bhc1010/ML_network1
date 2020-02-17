import numpy as np 
import random 

class Network:

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(layer,1) for layer in sizes[1:]]
        self.weights = [np.random.randn(layer,prevLayer) for prevLayer, layer in zip(sizes[:-1], sizes[1:])]
        self.success = 0

    # a' = wa + b
    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w,a) + b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        if test_data : n_test = len(test_data)
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k + mini_batch_size] for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_network(mini_batch, eta)
            # if test_data:
            #     print("Epoch {0}: {1} / {2}".format(j, self.evaluate(test_data), n_test))
            # else:
            #     print("Epoch {0} complete".format(j))

        if test_data: self.success = self.evaluate(test_data)
        

    def update_network(self, mini_batch, eta):

        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        for x,y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x,y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]

        self.weights = [w - (eta/len(mini_batch))*nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (eta/len(mini_batch))*nb for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):

        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # Feed forward
        activation = x
        activations = [x] # List of all activations, layer by layer
        zs = [] # List of all z vectors
        
        #### FEED FORWARD FUNCTION ####
        # b, w, and z are all vectors. activations is a matrix (or vector of vectors)
        # activation = sigmoid(z) gives the activation vector of the next layer
        # thus feedforward iterates through each layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b ## z vector represents entire layer
            zs.append(z)
            activation = sigmoid(z)       ## activation vector represents entire layer
            activations.append(activation)

        #### BACKWARD PASS ####
        ## NOTE:
        ## delta is da/dz * dC/da
        ## da/dz = sigmoidPrime
        ## dC/da = cost_derivative
        ## grad_b of C = dz/db * da/dz * dC/da = delta (since dz/db = 1)
        ## grad_w of C = dz/dw * da/dz * dC/da = delta * a^(L-1)

        # Pass to layer before last
        delta = self.cost_derivative(activations[-1], y) * \
                    sigmoidPrime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, np.transpose(activations[-2]))
        
        # Pass to every layer after starting with L - 2
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoidPrime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, np.transpose(activations[-l-1]))
        
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        return (output_activations - y) 

def sigmoid(z):
    return 1.0/(1.0 + np.exp(-z))

def sigmoidPrime(z):
    return (np.exp(-z)/np.square((1.0 + np.exp(-z))))
