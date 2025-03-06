import numpy as np

a = np.arange(20).reshape(2, 2, 5)
print(a)
print(type(a))
print(f'数组的轴（维度）数量:{a.ndim}')
print(f'数组的形状:{a.shape}')
print(f'数组元素的总个数:{a.size}')
print(f'数组元素的类型:{a.dtype}')
print(f'数组中每个元素的字节大小:{a.itemsize}')
print(f'包含数组实际元素的缓冲区:{a.data}')

