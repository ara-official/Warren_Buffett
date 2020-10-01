import numpy

# exercise
t = numpy.array([0, 1, 2, 3, 4, 5, 6])
print(t)
print("rank of t: ", t.ndim)
print("Shape of t: ", t.shape)
print(t[3:-1])

t2 = numpy.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
print(t2)
print("rank of t: ", t2.ndim)
print("Shape of t: ", t2.shape)


t3 = numpy.array([[[0, 1], [2, 3]], [[4, 5], [6, 7]], [[8, 9], [10, 11]]])

print(t3)
print("rank of t: ", t3.ndim)
print("Shape of t: ", t3.shape)