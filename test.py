import numpy as np

def function_1(X):
    return np.sin(X) 

def function_2(X):
    return 3. * np.sin(X) 

def function_3(X):
    return np.sin(X + 1.) 

X = np.arange(100)

# mean
print function_1(X).mean()

# std dev
print function_1(X).std()

# to plot
from matplotlib import pyplot as mp
mp.plot(X, function_1(X))
mp.hlines(function_1(X).mean(), 0, 100)
mp.show()