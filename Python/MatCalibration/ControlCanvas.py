# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import numpy as np

class MyMplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=50, height=50, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		# self.axes.set_adjustable('datalim')
		# 每次plot()调用的时候，我们希望原来的坐标轴被清除(所以False)
		self.compute_initial_figure()
		#
		FigureCanvas.__init__(self, fig)
		self.setParent(parent)
 
		FigureCanvas.setSizePolicy(self,
									QSizePolicy.Expanding,
									QSizePolicy.Expanding)
		self.axes.set_xlabel('Strain[-]')
		self.axes.set_ylabel('Stress[GPa]')
		
		FigureCanvas.updateGeometry(self)
 
	def compute_initial_figure(self):
		pass
 
class MyControlMplCanvas(MyMplCanvas):#
	def __init__(self, *args, **kwargs):
		MyMplCanvas.__init__(self, *args, **kwargs)
		# timer = QtCore.QTimer(self)
		# timer.timeout.connect(self.update_figure)
		# timer.start(1000)
 
	def compute_initial_figure(self):
		self.axes.plot([0, 0, 0, 0], [1, 2, 3, 4], 'r')
 
	def update_figure(self,*args):
		args = args[0]
		curvedata = args[0]
		# print ('here2',args[0])
		strainrate = [float(i) for i in args[3]]
		# print (args[0][0])
		testing = args[1]
		# try:
		if args[2] == 2:
			self.axes.cla()
		legend = []
		for i in range(int(len(testing)/2)):
			self.axes.plot(testing[2*i+0], testing[2*i+1],'--')
			legend.append(i)
		self.axes.legend(legend)
		for i in range(len(curvedata)-1):
			# print (curvedata[0], curvedata[i+1])
			self.axes.plot(curvedata[0], curvedata[i+1])
		self.axes.grid('on')
		legend.extend(strainrate)
		self.axes.set_xlabel('Strain[-]')
		self.axes.set_ylabel('Stress[GPa]')
		self.axes.legend(legend)
		self.draw()



