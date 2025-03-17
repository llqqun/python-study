import numpy as np

# a = np.array([[[1, 2], [3, 4]],
#                  [[4, 3], [2, 1]]])

# a = np.array([1, 2, 3])

# a = np.array([[1, 2, 3],
#                  [4, 5, 6]])
a = np.arange(12).reshape(3, 4)
b = np.array([2,3,4,5]).reshape(1,4)
print(a, b)
print(a/b)
# b = np.array([[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]])

# print(a, b)
# print(a + b)
# b = np.max(a, axis = 0)
# print(np.max(a, axis = -3))
print(f'数组的轴（维度）数量:{a.ndim}')
print(f'数组的形状:{a.shape}')
print(f'数组元素的总个数:{a.size}')
print(f'数组元素的类型:{a.dtype}')
print(f'数组中每个元素的字节大小:{a.itemsize}')
print(f'包含数组实际元素的缓冲区:{a.data}')

