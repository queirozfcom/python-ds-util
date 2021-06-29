# python-ds-util

[![PyPI version](https://badge.fury.io/py/dsutil.png)](https://badge.fury.io/py/dsutil)

## Installation

The library is available on **pip**:

`pip install dsutil`

## Examples

For full usage examples see notebooks under [the examples directory](https://github.com/queirozfcom/python-ds-util/tree/master/examples).

### Plotting

Full examples for plotting here: [https://github.com/queirozfcom/python-ds-util/tree/master/examples/examples-plotting.ipynb]

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

- `add_value_labels()` annotates barplots, line plots and scatter plots with values for the coordinates

  ```python
  import numpy as np
  import matplotlib.pyplot as plt
  from dsutil import add_value_labels
  
  x = np.linspace(0.0,100,10)
  y = np.random.uniform(low=0,high=10,size=10)

  plt.bar(x,y)
  
  add_value_labels()
  ```
   
<p align="center">
  <img src="https://i.imgur.com/J8iZuK6.png" width="350">
  <img src="https://i.imgur.com/Wq9eKQm.png" width="350">
</p>

- `format_yaxis_percentage()`: turns values between 0 and 1 in y-axis into percentages

  ```python
  import numpy as np
  import matplotlib.pyplot as plt
  from dsutil import format_yaxis_percentage
  
  x = np.linspace(0.0,100,10)
  y = np.random.uniform(low=0,high=1,size=10)
    
  plt.bar(x,y)
  plt.yticks(np.arange(0,1.01,0.1))

  format_yaxis_percentage()
  ```
  
<p align="center">
  <img src="https://i.imgur.com/XIIJgM8.png" width="350">
  <img src="https://i.imgur.com/ybDW5hq.png" width="350">
</p>

- `format_yaxis_thousands()`: uses commas as thousands separator in the y-axis labels

  ```python
  import numpy as np
  import matplotlib.pyplot as plt
  from dsutil import format_yaxis_thousands
  
  x = np.linspace(0.0,100,10)
  y = np.random.uniform(low=10000,high=100000,size=10)

  plt.bar(x,y)
  plt.yticks(np.arange(0,100001,10000))

  format_yaxis_thousands()
  ```
  
<p align="center">
  <img src="https://i.imgur.com/1g0WYKO.png" width="350">
  <img src="https://i.imgur.com/IyTMmbr.png" width="350">
</p>