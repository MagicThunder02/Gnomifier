from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import numpy as np

res = np.random.normal(0.5, 0.1, size=10000)
for n in res:
    if n < 0:
        n = 0
    if n > 1:
        n = 1

plt.hist(res, bins=20)
plt.show()

# https://en.wikipedia.org/wiki/Inverse_transform_sampling
