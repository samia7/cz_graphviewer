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
        self.x = None
        self.y = None
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.plot_graph()
    
    def control_x(self):
        self.x = np.linspace(self.x_min, self.x_max, num=self.iterations)
        self.y = SineWave().run_function(self.x)

    def plot_graph(self):
        self.control_x()
        # plot data: x, y values
        self.graphWidget.plot(self.x, self.y)

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