#!/usr/bin/env python

"""
Script that contains all the functions that can be viewed using the graph viewer UI. 
The script contains an abstract class Function that is inherited by all the 
subclasses that have the description for specific functions.

To add new functions: 

functions.py: Create a new class describing that function, and extend Functions class. All the 
methods and properties that need to be overwritten are decribed in the Functions class.

graphviewer.py: Add an object of the class to the array 'functions' in the GraphViewer class.
""" 
from abc import ABC, abstractmethod
from fractions import Fraction
import numpy as np

class Function(ABC):
    """
    This is the main abstract class that is inherited by all the function 
    subclasses.
    """
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
        The description of the value A to be displayed on the GUI
        """
        pass

    @property
    @abstractmethod
    def B_des(self):
        """
        The description of the value B to be displayed on the GUI
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
    
    @property
    @abstractmethod
    def frequency(self):
        """
        For non periodic functions set frequency as 0
        For periodic functions update frequency as needed
        """
        pass

    @abstractmethod
    def run_function(self, x, A, B):
        """
        This method defines the operation that is performed by the function.
        Parameter A: User adjustable parameter
        Parameter B: User adjustable parameter
        Parameter x: array of the input values
        Return: array of the y values calculated over the x array
        """
        pass
    
    @abstractmethod
    def x_range(self, x_extremes, A, B):
        """
        The x array is created in this method based on the min and max value of x.
        The sampling size is fixed for non periodic waves and dependent on the frequency
        for the periodic waves. This is to ensure that no data is lost when going from
        discrete time to continous time (Sampling rate needs to be at least twice the 
        frequency of the wave), to overcompensate the rate is chosen for 10x frequency. 

        If the function has any singularities or output that is complex for 
        any particular values of x, overwrite the method to update the x values.
        If there are no invalid outputs just return super().

        The input parameters include A and B as some functions have invalid outputs 
        that may be dependent on A or B, for example in the power function, 
        there are invalid outputs dependent on the power (B)
        Return: An array with the array for x in the first index and any message
        for any changes made to the domain in the 2nd index
        """
        if not self.frequency:
            # For non periodic functions or if the frequency is 0, the default
            # step_size is taken to be 0.001
            step_size = 0.001 
        else:
            step_size = 1/(self.frequency*10)
        x = np.arange(x_extremes[0], x_extremes[1], step_size)
        x = np.append(x, [x_extremes[1]])
        return [x]

class SineGraph(Function):
    """
    A simple sine wave in the form Asin(Bx)
    """
    name = "Sine Wave y = Asin(Bx)"
    A_des = "The amplitude of the wave"
    B_des = "The frequency of the wave"
    A_default = 1
    B_default = 1
    frequency = B_default

    def run_function(self, x, A, B):
        return (A*np.sin(B*x))
    
    def x_range(self, x_extremes, A, B):
        """
        Set the frequency to input B and call the x_range 
        method defined in the abstract class to create x array
        """
        self.frequency = B
        return super().x_range(x_extremes, A, B)

class PowerGraph(Function):
    """
    A simple power graph in the form y = Ax^B
    """
    name = "Power Graph y = Ax^B"
    A_des = "A constant multiplier"
    B_des = "The power by which x is raised"
    A_default = 1
    B_default = 2
    frequency = 0

    def run_function(self, x, A, B):
        return (A*(x**B))
    
    def x_range(self, x_extremes, A, B):
        """
        The domain for x is modified for B < 1.
        For fractional B, x min is changed to be > 0, as negative numbers
        raised to a fractional power gives rise to a complex solution.
        For whole number negative powers, the domain is changed to not include
        x = 0.
        """
        if B < 1:
            if Fraction(B).limit_denominator(100).denominator == 1:
                x = super().x_range(x_extremes, A, B)[0]
                x = x[x!=0]
                change = 'Domain modified: Output excludes x = 0 (0 is a point of singularity)'
            else:    
                x_extremes[0] = 0.0001 if x_extremes[0] <= 0 else x_extremes[0]
                x = super().x_range(x_extremes, A, B)[0]
                change = 'Domain modified: Output only valid for x > 0'
            return [x, change]
        else:
           return super().x_range(x_extremes, A, B)

class SawToothGraph(Function):
    """
    The Sawtooth wave has no formal equation. It is an asymetric triangle 
    that is 3X units long, and is repeated over the domain.
    """
    name = "Sawtooth wave"
    A_des = "Vertical Scaling"
    B_des = "Vertical Shift"
    A_default = 2
    B_default = 1
    # The x_range method is overwritten with a fixed time step as step size of 1 
    # is large enough to ensure no data is lost
    frequency = 3

    def run_function(self, x, A, B):
        """
        The graph is plotted by using one cycle of the asymetric triangle from the
        origin and adding a horizontal shift left and right to repeat the triangle
        over the entire domain
        """
        y = []
        x_min = x[0]
        # If there are any partial waves due to the starting position, keep
        # adding 1 till a multiple of 3 is reached to calculate the amount of 
        # shift required in the starting position
        while(x_min % 3 != 0):
            x_min = x_min + 1
        # Add horizontal shift based on what the starting point is
        h_shift = 3 - x_min
        # Plot the sawtooth wave, only the amount of shift changes after
        # every 3 units of x
        # the sawtooth graph can be represented using two functions (2 lines)
        # one wavelength represents 3 coordinates, after which the plot is shifted
        # to the right by an amount of h_shift: f(x-h_shift)
        for x_val in x:
            if x_val % 3 ==  0:
                h_shift = h_shift - 3
                # Equation of the line for the left half of the triangle
                y.append((x_val+h_shift)-0.5)
            else:
                # Equation of the line for the right half of the triangle
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
        return [x]