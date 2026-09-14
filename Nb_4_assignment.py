import pandas as pd
import numpy as np

#Q1

price = np.array([250, 180, 90, 340, 120])
print(type(price))

zeroes = np.zeros(6) #array of 6 zeroes:
ones = np.ones(6)

lists = np.arange(0,50+1,5)
print(lists)
spaced_no = np.linspace(0,1,6)
print(spaced_no)

#Q2
print(f"shape of price array: {price.shape}")
print(f"dimension of price array: {price.ndim}")
sales_grid = np.random.randint(1,13, size=(3,4), dtype=int)
print(f"sales_grid: {sales_grid}")
print(sales_grid.ndim) #  ndim 2 because the array is made of two dimensions( rows and column)

#Q3
print(price[0], price[-1]) #first value last value

print(price[0:4], price[1:5:2]) # 1-3 values

print(sales_grid[0][0], sales_grid[-1][-1])

print(f" first two rows of sales_grid {sales_grid[0:2]}")
print(f" first two columns of sales_grid {sales_grid[0][:2]}")



#Q4
b_price = np.multiply(price,0.15)
print(b_price)
quantities = [34,453,45,70,50]
print(np.multiply(price,quantities))

print(f"10% discount on sales_grid:\n{np.multiply(0.1,sales_grid)}")

#Q5

print(f""
      f"sum of prices: {sum(price)}\n"
      f"mean price: {np.mean(price)}\n"
      f"minimum price: {np.min(price)}\n"
      f"maximum price: {np.max(price)}\n"
      f"standard deviation of price: {np.std(price):.2f}")

print(sales_grid.sum(axis=1))
print(sales_grid.sum(axis=0))

array = np.arange(1,12+1)
array_reshaped = array.reshape(4,3)
print(array_reshaped)
print(f"shape before: {array.shape} \n ew shape: {array_reshaped.shape}")




