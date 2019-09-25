import sys
import random
import time
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange, sin, pi
import tushare as ts


class MyMplCanvas(FigureCanvas):#画布基类
	"""这是一个窗口部件，即QWidget（当然也是FigureCanvasAgg）"""
	def __init__(self, parent=None, width=50, height=50, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		# 每次plot()调用的时候，我们希望原来的坐标轴被清除(所以False)
		self.compute_initial_figure()
 
		#
		FigureCanvas.__init__(self, fig)
		self.setParent(parent)
 
		FigureCanvas.setSizePolicy(self,
									QSizePolicy.Expanding,
									QSizePolicy.Expanding)
		self.axes.set_xlabel('x')
		self.axes.set_ylabel('y')
		FigureCanvas.updateGeometry(self)
 
	def compute_initial_figure(self):
		pass
 
class MyStaticMplCanvas(MyMplCanvas):#单个画布
	"""静态画布：一条正弦线"""
	def compute_initial_figure(self):
		t = arange(0.0, 3.0, 0.01)
		s = sin(4*pi*t)
		self.axes.plot(t, s)
 
class MyControlMplCanvas(MyMplCanvas):#单个画布
	"""动态画布：每秒自动更新，更换一条折线。"""
	def __init__(self, *args, **kwargs):
		MyMplCanvas.__init__(self, *args, **kwargs)
		timer = QtCore.QTimer(self)
		timer.timeout.connect(self.update_figure)
		timer.start(1000)
 
	def compute_initial_figure(self):
		self.axes.plot([0, 0, 0, 0], [1, 2, 3, 4], 'r')
 
	def update_figure(self,x):
		# 构建4个随机整数，位于闭区间[0, 10]
		t = arange(0.0, 3.0, 0.01)
		s = sin(2*pi*t+x/100.*2*pi)
		self.axes.cla()
		self.axes.plot(df.time, df.price ,'r')
		self.axes.set_xlabel('time')
		self.axes.set_ylabel('pRICE')
		self.draw()
 
class MyDynamicMplCanvas(MyMplCanvas):#单个画布
	"""动态画布：每秒自动更新，更换一条折线。"""
	def __init__(self, *args, **kwargs):
		MyMplCanvas.__init__(self, *args, **kwargs)
		timer = QtCore.QTimer(self)
		timer.timeout.connect(self.update_figure)
		timer.start(10000)
 
	def compute_initial_figure(self):
		self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
 
	def update_figure(self,stock_id=str(600848),cur_date=time.strftime("%Y-%m-%d",time.gmtime())):
		# 构建4个随机整数，位于闭区间[0, 10]
		df = ts.get_tick_data(stock_id,date=cur_date,src='tt')
		self.axes.cla()
		self.axes.plot(df.time, df.price ,'r')
		self.axes.set_xlabel('time')
		self.axes.set_ylabel('price')
		self.draw()
		

	
