import numpy as np


arr = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]
])
print(arr)
arr = arr.tolist()
print(arr)
arr.pop(0)
print(arr)
arr = np.array(arr)
print(arr)