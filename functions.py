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
        """
        pass

class SineWave(Function):
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
