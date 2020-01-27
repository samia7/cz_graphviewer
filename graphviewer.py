#!/usr/bin/env python

"""
Script that runs the graph viewer interface and contains the functionality 
for the the GUI
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
    This class contains the description of the GUI
    """
    def __init__(self, *args, **kwargs):
        super(GraphViewer, self).__init__(*args, **kwargs)
        self.title = 'Graph Viewer'
        # Default domain
        self.x_min = 0
        self.x_max = 10
        self.iterations = self.x_max*100
        self.function = None
        self.x = None
        self.y = None
        self.A = None
        self.B = None
        self.initUI()

    def initUI(self):
        """
        This method initializes the UI for the the graph viewer app
        """
        self.setWindowTitle(self.title)
        # Layout for combo box to choose between the functions
        combo_layout = QHBoxLayout()
        self.combo_box = QComboBox()
        self.combo_box.addItems(["1",'2'])
        self.combo_box.activated.connect(self.select_function)
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
        # self.plot_graph() 
        layout.addLayout(param_layout)
        layout.addLayout(x_layout)
        self.setCentralWidget(window)
        self.select_function()

    @pyqtSlot()
    def on_clickA(self):
        try:
            self.A = float(self.A_textbox.text())
            self.plot_graph()
        except ValueError:
            QMessageBox.question(self, 'Error!', "Parameter A must be a number", QMessageBox.Ok, QMessageBox.Ok)
        self.A_textbox.setText("")
    
    @pyqtSlot()
    def on_clickB(self):
        try:
            self.B = float(self.B_textbox.text())
            self.plot_graph()
        except ValueError:
            QMessageBox.question(self, 'Error!', "Parameter B must be a number", QMessageBox.Ok, QMessageBox.Ok)
        self.B_textbox.setText("")

    @pyqtSlot()
    def on_clickx(self):
        x_min_value = self.xmin_textbox.text()
        x_max_value = self.xmax_textbox.text()
        # Check whether the range for x is invalid
        try:
            x_min_value = float(x_min_value)
            x_max_value = float(x_max_value)
            if x_max_value > x_min_value:
                self.x_max = x_max_value
                self.x_min = x_min_value
                self.plot_graph()
            else:
                QMessageBox.question(self, 'Error!', "x_max must be greater than x_min", QMessageBox.Ok, QMessageBox.Ok)    
        except ValueError:
            QMessageBox.question(self, 'Error!', "Domain must be a number", QMessageBox.Ok, QMessageBox.Ok)
        self.xmin_textbox.setText("")
        self.xmax_textbox.setText("")

    @pyqtSlot()
    def select_function(self):
        #print (self.combo_box.currentText())
        # Change the object based on the user selection
        self.function = SineWave()
        self.A = self.function.A_default
        self.B = self.function.B_default
        self.plot_graph()

    def control_x(self):
        # Implementation of changing x
        # The sliding thing for x
        self.x = np.linspace(self.x_min, self.x_max, num=self.iterations)
        self.y = self.function.run_function(self.x, self.A, self.B)

    def plot_graph(self):
        self.control_x()
        # plot data: x, y values
        self.graphWidget.clear()
        self.graphWidget.plot(self.x, self.y)
        self.graphWidget.setTitle(self.function.name)
        self.graphWidget.setLabel('top', 'A = {} (A = {}), B = {} (B = {})'
            .format(self.function.A_des, self.A, self.function.B_des, self.B))

def main():
    app = QApplication(sys.argv)
    main = GraphViewer()
    main.show()
    app.exec_()

if __name__ == "__main__":
    """
    Run the graph viewer
    """
    main()