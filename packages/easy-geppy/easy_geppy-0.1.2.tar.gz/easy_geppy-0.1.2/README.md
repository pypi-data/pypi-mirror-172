# EasyGeppy

EasyGeppy is an easy to use programming interface for [Geppy](https://github.com/ShuhuaGao/geppy) from Shuhua Gao [1], and proposed by C. Ferreira  in 2001 [2] for [Gene Expression Programming](https://en.wikipedia.org/wiki/Gene_expression_programming) (GEP). 

EasyGeppy provides a minimized and pre-defined pipeline setup for solving simple and multiple regression problems using Geppy along with Pandas [3] and Numpy [4].

The pipeline is based on the following Shuhua Gao's notebook: [Simple mathematical expression inference](https://github.com/ShuhuaGao/geppy/blob/master/examples/sr/numerical_expression_inference-ENC.ipynb).

Nonetheless, EasyGeppy allows you to set your custom configuration to its setup by accessing the class EasyGeppy attributes.

Feel free to contribute.

## How to install
~~~
pip install easy_geppy
~~~

## How to use
~~~

#import
from easy_geppy import EasyGeppy

# Initialize
egp = EasyGeppy(df, #Pandas DataFrame
                 x_columns=['column1','column2','column3'],
                 y_column='column_y')

egp.default_initialization()

# Train
egp.launch_evolution(n_pop=300, n_gen=100)

# Get resulting function for making predictions
best_func = egp.get_best_solution_as_function()

# Make predictions
df['y_predicted'] = best_func(df)

# Get symbolic representation of the resulting function
egp.get_best_solution_simplified()

~~~
## Example
1. [EasyGeppy-Example](./tests/EasyGeppy-Example.ipynb)

## Reference
[1] Shuhua Gao (2020) Geppy [Source code]. https://github.com/ShuhuaGao/geppy.
[2] Ferreira, C. (2001). Gene Expression Programming: a New Adaptive Algorithm for Solving Problems. Complex Systems, 13.
[3] McKinney, W. & others, 2010. Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference. pp. 51–56.
[4] Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 10.1038/s41586-020-2649-2. (Publisher link).