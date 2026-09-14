
import matplotlib.pyplot as plt


years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

plt.bar(years, gdp)
plt.xlabel("Years")
plt.ylabel("GDP")

plt.title("maybe it would work")
plt.show()