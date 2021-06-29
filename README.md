# python-ds-util

[![PyPI version](https://badge.fury.io/py/dsutil.png)](https://badge.fury.io/py/dsutil)

## Installation

The library is available on **pip**:

`pip install dsutil`

## Examples

For full usage examples see notebooks under [the examples directory](https://github.com/queirozfcom/python-ds-util/tree/master/examples).

### Plotting

- `add_grid()`: reasonable default grid settings, with weak grey lines, light alpha, etc.
   
  ```python
  import numpy as np
  import matplotlib.pyplot as plt
  from dsutil import add_grid
  
  x = np.linspace(0.0,100,10)
  y = np.random.uniform(low=0,high=10,size=10)

  plt.bar(x,y)
  add_grid()
  ```
   
<p align="center">
  <img src="https://i.imgur.com/7ZnSaZq.png" width="350">
  <img src="https://i.imgur.com/vOq2ZMZ.png" width="350">
</p>
