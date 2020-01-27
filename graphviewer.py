#!/usr/bin/env python

"""
Script that runs the graph viewer interface and contains the 
functionality for the the GUI
""" 
from functions import *
from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
import sys
import numpy as np

class GraphViewer(QtWidgets.QMainWindow):
    """
    This class contains the description of the GUI
    """
    def __init__(self, *args, **kwargs):
        super(GraphViewer, self).__init__(*args, **kwargs)
        self.x_min = 0
        self.x_max = 10
        self.iterations = self.x_max*10
        self.function = None
        self.x = None
        self.y = None
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.setLabel('left', 'f(x)')
        self.graphWidget.setLabel('bottom', 'x')
        self.plot_graph()
    
    def select_function(self):
        # Change the object based on the user selection
        self.function = SineWave()
        # Run control_x to get the y values for the desired function
        self.control_x()

    def control_x(self):
        # Implementation of changing x
        # The sliding thing for x
        self.x = np.linspace(self.x_min, self.x_max, num=self.iterations)
        self.y = self.function.run_function(self.x)

    def plot_graph(self):
        self.select_function()
        # plot data: x, y values
        self.graphWidget.plot(self.x, self.y)
        self.graphWidget.setTitle(self.function.name)
        self.graphWidget.setLabel('top', 'A = {}, B = {}'
            .format(self.function.A_des, self.function.B_des))

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = GraphViewer()
    main.show()
    app.exec_()

if __name__ == "__main__":
    """
    Run the graph viewer
    """
    main()