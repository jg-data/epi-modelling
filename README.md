# Epidemiology modelling

## Overview

Code which allows you to construct and rum simulations for simple compartmental models, like the SIR model and its extensions.

The code includes:
 - examples of stochastic Petri nets with added data
 - a function to draw them after specifying node locations, with optinal arrow customisation
 - functions to generate the differential equations as an image, LaTeX code, PDF, and a Python function
 - a function to run simulations (calling SciPy's solve_ivp)
 - a function to draw graphs of the simulations, with option to specify colours

## Walkthrough and examples

See the included Jupyter notebook `compartmental_models.ipynb`.

## Summary of files

 - `compartmental_models.ipynb` Jupyter notebook giving examples of how to use the code
 - `SPN_functions.py` Code for the functions described above
 - `model_graphs.py` Some standard models (SIR, SIRD, SIRDS, and double SIRDS) with preset rates and display options
 - `model-sim_classes.py` A different approach, not used elsewhere, but gives useful 2x2 plot for SIRDS example

## Packages used (Python)

 - NetworkX for encoding stochastic Petri nets as directed graphs with multiple edges
 - MatPlotLib for images of models and simulations
 - SciPy for simulations by solving initial value problems
 - Copy for deep-copying models
