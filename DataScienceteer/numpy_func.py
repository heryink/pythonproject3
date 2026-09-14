import math
from typing import List, Tuple, Callable

Vector = List[float]

def add(a: Vector, b: Vector)-> Vector:
    """add two vectors"""
    assert len(a) == len(b), "length of vector must be the same"
    return [i+j for i,j in zip(a,b)]

def subtract(a: Vector, b: Vector)-> Vector:
    """subtract two vectors"""
    assert len(a) == len(b), "length of vector must be the same"
    return [i-j for i, j in zip(a,b)]

def vector_sum(Vectors: List[Vector])-> Vector:
    n = len(Vectors[0])

    assert all(len(vector) == n  for vector in Vectors), "sizes of vectors must be the same"
    return [sum(vector[i] for vector in Vectors) for i in range(n)]

def scaler_multuplication(c:float|int, v: Vector)-> Vector:
    """multiplies every element by c"""
    return [c*v[i] for i in v]

def vector_mean(v:List[Vector])-> Vector:
    n = len(v)
    return scaler_multuplication(1/n, vector_sum(v))

def dot(a:Vector, b:Vector) -> Vector:
    assert len(a) == len(b), "Vector size must be equal"
    return [i*j for i,j in zip(a,b)]

def sum_of_squares(a:Vector) -> float:
    return sum(dot(a,a))

def magnitude(v:Vector)-> float:
    return math.sqrt(sum_of_squares(v))

def squared_distance(a:Vector, b:Vector) -> float:
    return sum_of_squares(subtract(a,b))

def distance(v: Vector, w: Vector) -> float:
    return magnitude(subtract(v, w))


Matrix = List[List[float]]

def shape(A: Matrix) -> Tuple[int, int]:
    """Returns (# of rows of A, # of columns of A)"""
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0

def make_matrix(num_rows: int,
                num_cols: int,
                entry_fn: Callable[[int, int], float]) -> Matrix:
    """Returns a num_rows x num_cols matrix whose (i,j)-th entry is entry_fn(i, j) """
    return [[entry_fn(i, j) for j in range(num_cols)]
            for i in range(num_rows)]





