import numpy as np

# a = np.array([1])
# print(a, a.shape)

# b = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
# print(b, b.shape, b.ndim)

a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
b = np.array([[9, 10, 11]])
d = np.concatenate((a, b), axis = 0)
print(d)