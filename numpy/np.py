import numpy as np

a = np.array([[2, 2, 3],[1,2,3]])

print('二维数组', a)
print(f'数组的轴（维度）数量:{a.ndim}')
print(f'数组的形状:{a.shape}')
print(f'数组元素的总个数:{a.size}')
print(f'数组元素的类型:{a.dtype}')
print(f'数组中每个元素的字节大小:{a.itemsize}')
print(f'包含数组实际元素的缓冲区:{a.data}')

b = np.arange(12).reshape(2, 2, 3)
print('三维数组',b)
print(b.shape)
print("=============多维数组的索引,切片==================")
print(b[0])
print(b[0:, 1:, 2])

print("=============多维数组的遍历==================")
#  多维数组遍历的是根据第一个维度进行的
for i in b:
    print(i)
# 通过flat属性遍历多维数组的每个元素
# for i in b.flat:
#     print(i)
print("=============多维数组的形状==================")
