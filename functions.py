#!/usr/bin/env python

"""
Script that contains all the functions that can be viewed using the graph viewer UI. 
The script contains an abstract class Function that is inherited by all the 
subclasses that have the description for specific functions.
In order to add new functions to be displayed by the UI, simply create a new class
describing that function, and extend Functions class.
For each class inherting Function:
Name: Defines the name identifier used in the GUI
A, B: The changable parameters defining the function
""" 
from abc import ABC, abstractmethod
from fractions import Fraction
from math import pow
import numpy as np

class Function(ABC):
    """
    This is the main abstract class that is inherited by all the function 
    subclasses.
    """
    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def name(self):
        """
        The name of the function to be displayed on the GUI
        """
        pass

    @property
    @abstractmethod
    def A_des(self):
        """
        The description of A to be displayed on the GUI
        """
        pass

    @property
    @abstractmethod
    def B_des(self):
        """
        The description of B to be displayed on the GUI
        """
        pass
    
    @property
    @abstractmethod
    def A_default(self):
        """
        The default value for A
        """
        pass

    @property
    @abstractmethod
    def B_default(self):
        """
        The default value for B
        """
        pass

    @abstractmethod
    def run_function(self, x, A, B):
        """
        This method defines the operation that is performed by a function.
        The y values are returned for an array of the input x values
        Parameter A:
        Parameter B:
        Parameter x:
        Return:
        """
        pass
    
    @abstractmethod
    def x_range(self, x_extremes, A, B):
        """
        If the function has any singularities or output that is complex for 
        any particular values of x, it should be handled in this function.
        If there are no invalid outputs just override the method and return super.
        The input parameters include A and B as some functions have invalid outputs 
        that may be dependent on A or B, for example in the power function, 
        there are invalid outputs dependent on the power (B)
        Return: An array with the x values and a dictionary with 0 key and indicating
        no modifications were made to the domain of interest
        """
        # The number of iterations are decided based on the size of the domain
        # This ensures that step size is small enough for accurate graph
        iterations = int((x_extremes[1]-x_extremes[0])*100)
        x = np.linspace(x_extremes[0], x_extremes[1], num=iterations)
        return [x, {0:''}]

class SineGraph(Function):
    """
    Name: Sine Wave
    A: The amplitude of the wave (default amplitude = 1)
    B: The time period of the wave (default period = 1)
    """
    name = "Sine Wave"
    A_des = "The amplitude of the wave"
    B_des = "The time period of the wave"
    A_default = 1
    B_default = 1

    def run_function(self, x, A, B):
        return (A*np.sin(B*x))
    
    def x_range(self, x_extremes, A, B):
        return super().x_range(x_extremes, A, B)

class PowerGraph(Function):
    """
    Name: Power Graph
    A: A constant multiplier (default multiplier = 1)
    B: The power by which x is raised (default power = 2)
    """
    name = "Power Graph"
    A_des = "A constant multiplier"
    B_des = "The power by which x is raised"
    A_default = 1
    B_default = 2

    def run_function(self, x, A, B):
        return (A*np.power(x,B))
    
    def x_range(self, x_extremes, A, B):
        """
        The domain for x is modified as 0 is a singularity point and
        negative value raised to a fraction gives a complex solution in python
        As power operations take precendence over unary operations
        Therefore for fraction powers range greater than 0 only used
        """
        iterations = int((x_extremes[1]-x_extremes[0])*100)
        if B < 1:
            x_extremes[0] = 0.0001 if x_extremes[0] <= 0 else x_extremes[0]
            x = np.linspace(x_extremes[0], x_extremes[1], num=iterations)
            change = 'Domain modified: Output only valid for x > 0'
            return [x, {1:change}]
        else:
           return super().x_range(x_extremes, A, B)

class SawToothGraph(Function):
    """
    Name: Sawtooth wave
    A: Vertical Scaling (default amplitude = 2)
    B: Vertical Shift (default shift = 1)
    """
    name = "Sawtooth wave"
    A_des = "Vertical Scaling"
    B_des = "Vertical Shift"
    A_default = 2
    B_default = 1

    def run_function(self, x, A, B):
        y = []
        x_min = x[0]
        # Check how far off the initial position is from 0
        while(x_min % 3 != 0):
            x_min = x_min + 1
        # Add horizontal shift shift based on what the starting point is
        h_shift = 3 - x_min
        # Plot the sawtooth wave, only the amount of shift changes after
        # every 3 units of x, this is taken into account by subtracting 
        # the amount of shift needed every time a number divisible by 3 comes
        # the sawtooth graph can be represented using two functions (2 lines)
        # one wavelength represents 3 coordinates, after switch the plot is shifted
        # to the right by an amount of h_shift
        for x_val in x:
            if x_val % 3 ==  0:
                h_shift = h_shift - 3
                y.append((x_val+h_shift)-0.5)
            else:
                y.append(-0.5*(x_val+h_shift)+1)
        # finally the vertical shifting and scaling is added        
        y = [(A*y_val)+B for y_val in y]
        return y
    
    def x_range(self, x_extremes, A, B):
        # Need to sample at at least twice the frequency
        # in order to not lose any data
        # Step size 1 is sufficient to ensure no data is lost
        # Simpler to sample at integer values therefore 
        # the x_extremes are converted to integers
        x = np.arange(int(x_extremes[0]), int(x_extremes[1]), 1)
        x = np.append(x, [int(x_extremes[1])])
        return [x, {0:''}]