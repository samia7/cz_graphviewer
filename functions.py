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
import numpy as np

class Function(ABC):
    """
    This is the main abstract class that is inherited by all the function 
    subclasses.
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def run_function(self, x):
        """
        This method defines the operation that is performed by a function.
        """
        pass
    
    @abstractmethod
    def invalid_case(self):
        """
        This method handles all invalid parameters for A and B
        """
        pass

class SineWave(Function):
    """
    Name: Sine Wave
    A: The amplitude of the wave (default amplitude = 1)
    B: The time period of the wave (default period = 1)
    """
    def __init__(self, A=1, B=1):
        self.A = A
        self.B = B

    def run_function(self, x):
        return (self.A*np.sin(self.B*x))
    
    def invalid_case(self):
        return super().invalid_case()
