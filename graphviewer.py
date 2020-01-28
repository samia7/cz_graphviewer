#!/usr/bin/env python

"""
Script that runs the graph viewer interface and contains the functionality 
for the the GUI
In order to add new functions to be displayed in the graph viewer add the name 
of the class defining the function in the list 'functions', found in the initialization
of the class GraphViewer
""" 
from functions import *
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
                            QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, 
                            QLabel, QComboBox)
from PyQt5.QtCore import pyqtSlot
import pyqtgraph as pg
import sys
import numpy as np


class GraphViewer(QMainWindow):
    """
    This class contains the implementation of the GUI
    """
    def __init__(self, *args, **kwargs):
        super(GraphViewer, self).__init__(*args, **kwargs)
        self.title = 'Graph Viewer'
        # All the options for the graphs that can be plotted
        # Add additional index with the name of the class for new functions
        self.functions = [SineGraph(), PowerGraph()]
        self.selected_function = None
        # Default domain
        self.x_min_default = 0
        self.x_max_default = 10
        self.x_min = self.x_min_default
        self.x_max = self.x_max_default
        self.A = None
        self.B = None
        self.initUI()

    def initUI(self):
        """
        Initializes the UI for the the graph viewer app
        """
        self.setWindowTitle(self.title)
        # Layout for combo box to choose between the functions
        combo_layout = QHBoxLayout()
        self.combo_box = QComboBox()
        self.combo_box.addItem('')
        for func in self.functions:
            self.combo_box.addItem(func.name)
        self.combo_box.activated.connect(self.on_selectComboBox)
        combo_layout.addWidget(QLabel('Select the desired function:'))
        combo_layout.addWidget(self.combo_box)
        # Layout for changing A and B parameters
        param_layout = QHBoxLayout()
        self.A_textbox = QLineEdit(self)
        self.A_button = QPushButton('Set A', self)
        self.A_button.clicked.connect(self.on_clickA)
        param_layout.addWidget(self.A_textbox)
        param_layout.addWidget(self.A_button)
        self.B_textbox = QLineEdit(self)
        self.B_button = QPushButton('Set B', self)
        self.B_button.clicked.connect(self.on_clickB)
        param_layout.addWidget(self.B_textbox)
        param_layout.addWidget(self.B_button)
        # Layout for setting the range for x
        x_layout = QHBoxLayout()
        self.xmin_textbox = QLineEdit(self)
        self.xmax_textbox = QLineEdit(self)
        self.x_button = QPushButton('Set domain', self)
        self.x_button.clicked.connect(self.on_clickx)
        x_layout.addWidget(self.xmin_textbox)
        x_layout.addWidget(QLabel('< x <'))
        x_layout.addWidget(self.xmax_textbox)
        x_layout.addWidget(self.xmin_textbox)
        x_layout.addWidget(self.x_button)
        # Compiling all the layouts together to make parent
        window = QWidget()
        layout = QVBoxLayout()
        window.setLayout(layout)
        layout.addLayout(combo_layout)
        # Adding the graph as a widget
        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)
        self.graphWidget.setLabel('left', 'f(x)')
        self.graphWidget.setLabel('bottom', 'x')
        layout.addLayout(param_layout)
        layout.addLayout(x_layout)
        self.setCentralWidget(window)

    @pyqtSlot()
    def on_clickA(self):
        """
        Handles the event when button for setting parameter A is clicked
        Reads the value in the textbox associated with the button A, 
        checks if the input is a number and calls the method to plot the function 
        for valid inputs.
        """
        try:
            self.A = float(self.A_textbox.text())
            self.is_function_selected()
        except ValueError:
            QMessageBox.question(self, 'Error!', "Parameter A must be a number", 
                                QMessageBox.Ok, QMessageBox.Ok)
        self.A_textbox.setText("")
    
    @pyqtSlot()
    def on_clickB(self):
        """
        Handles the event when button for setting parameter B is clicked
        Reads the value in the textbox associated with the button B, 
        checks if the input is a number and calls the method to plot the function 
        for valid inputs.
        """
        try:
            self.B = float(self.B_textbox.text())
            self.is_function_selected()
        except ValueError:
            QMessageBox.question(self, 'Error!', "Parameter B must be a number", 
                                QMessageBox.Ok, QMessageBox.Ok)
        self.B_textbox.setText("")

    @pyqtSlot()
    def on_clickx(self):
        """
        Handles the event when button for changing the domain is clicked.
        Reads the values in the textbox associated with x_min and x_max and 
        checks if the inputs are numbers and if x_max > x_min.
        Calls the method to plot the function for valid inputs.
        """
        x_min_value = self.xmin_textbox.text()
        x_max_value = self.xmax_textbox.text()
        # Check whether the range for x is valid
        try:
            x_min_value = float(x_min_value)
            x_max_value = float(x_max_value)
            if x_max_value > x_min_value:
                self.x_max = x_max_value
                self.x_min = x_min_value
                self.is_function_selected()
            else:
                QMessageBox.question(self, 'Error!', "x_max must be greater than x_min",
                                    QMessageBox.Ok, QMessageBox.Ok)    
        except ValueError:
            QMessageBox.question(self, 'Error!', "Domain must be a number",
                                QMessageBox.Ok, QMessageBox.Ok)
        self.xmin_textbox.setText("")
        self.xmax_textbox.setText("")

    @pyqtSlot()
    def on_selectComboBox(self):
        """
        Handles the event when an option is selected from the combo box
        Clears the graph if no function is selected
        Calls the method to plot the graph using the default parameters 
        for A and B and default domain
        """
        cur_index = self.combo_box.currentIndex()
        if cur_index == 0:
            self.graphWidget.clear()
            self.graphWidget.setTitle('')
            self.graphWidget.setLabel('top', '')
            self.selected_function = None
        else:
            self.selected_function = self.functions[cur_index-1]
            self.A = self.selected_function.A_default
            self.B = self.selected_function.B_default
            self.x_min = self.x_min_default
            self.x_max = self.x_max_default
            self.plot_graph()

    def is_function_selected(self):
        """
        Called when any of the parameter change buttons are clicked
        Checks if a function is selected from the combo box and calls the 
        method to plot the graph if a function is selected
        """
        if self.selected_function is None:
            QMessageBox.question(self, 'Error!', "No function is selected", 
                                QMessageBox.Ok, QMessageBox.Ok)
        else: 
            self.plot_graph()

    def plot_graph(self):
        """
        Uses the domain and A and B value on the selected function and calls the
        method that calculates the y values.
        The graph is then plotted and the parameters and function title displayed
        on the GUI
        """
        # The number of iterations are decided based on the size of the domain
        # This ensures that step size is small enough for accurate graph
        iterations = int((self.x_max-self.x_min)*100)
        x = np.linspace(self.x_min, self.x_max, num=iterations)
        y = self.selected_function.run_function(x, self.A, self.B)
        # plot data: x, y values
        self.graphWidget.clear()
        self.graphWidget.plot(x, y)
        self.graphWidget.setTitle(self.selected_function.name)
        self.graphWidget.setLabel('top', 'A = {} (A = {}), B = {} (B = {})'
            .format(self.selected_function.A_des, self.A, self.selected_function.B_des, self.B))

if __name__ == "__main__":
    """
    Run the graph viewer
    """
    app = QApplication(sys.argv)
    main = GraphViewer()
    main.show()
    app.exec_()