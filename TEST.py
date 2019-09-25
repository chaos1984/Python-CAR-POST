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
from function import *

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(519, 387)
		self.centralWidget = QtWidgets.QWidget(MainWindow)
		self.centralWidget.setObjectName("centralWidget")
		MainWindow.setCentralWidget(self.centralWidget)
####################################################################################
		#gL
		self.gL = QtWidgets.QGridLayout(self.centralWidget)
		# self.gridLayout.setContentsMargins(11, 11, 11, 11)
		self.gL.setSpacing(6)
		self.gL.setObjectName("gL")
		#
		#QHBoxLayout
		self.hL1 = QtWidgets.QHBoxLayout()
		self.hL1.setSpacing(6)
		self.hL1.setObjectName("hL1")
		self.gL.addLayout(self.hL1,0,0)
		#
		#GridLayout
		self.gL1 = QtWidgets.QGridLayout(self.centralWidget)
		self.gL1.setContentsMargins(11, 11, 11, 11)
		self.gL1.setSpacing(6)
		self.gL1.setObjectName("gL1")
		self.gL.addLayout(self.gL1,0,1)
		#
		#QFrame
		self.center = QtWidgets.QFrame()
		# self.center.resize(100,100)
		self.center.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.gL1.addWidget(self.center,0,0,2,3)
		#
		#QLabel
		self.l1 = QtWidgets.QLabel(r'用户名:')
		self.l1.setObjectName('l1')
		self.gL1.addWidget(self.l1,0,0)
		#
		#QLabel
		self.l2 = QtWidgets.QLabel(r'密 码:')
		self.l2.setObjectName('l2')
		self.gL1.addWidget(self.l2,1,0)
		#
		#LineEdit
		self.e1 = QtWidgets.QLineEdit()
		self.e1.setValidator(QtGui.QIntValidator())
		self.e1.setMaxLength(6)
		self.e1.setAlignment(QtCore.Qt.AlignRight)
		self.e1.setObjectName('e1')
		self.e1.setFont(QtGui.QFont("Arial",10))
		self.gL1.addWidget(self.e1,0,1)
		#
		#LineEdit
		self.e2 = QtWidgets.QLineEdit()
		self.e2.setValidator(QtGui.QIntValidator())
		self.e2.setMaxLength(6)
		self.e2.setAlignment(QtCore.Qt.AlignRight)
		self.e2.setObjectName('e2')
		self.e2.setFont(QtGui.QFont("Arial",10))
		self.gL1.addWidget(self.e2,1,1)
		#
		#QPushButton
		self.bt1 = QtWidgets.QPushButton("OK")
		self.bt1.setObjectName("bt1")
		self.gL1.addWidget(self.bt1,1,2)
		#
		#Qlist
		self.listwidget  =  QtWidgets.QListWidget()
		self.listwidget.addItems({"a":3,"b":4})
		self.gL1.addWidget(self.listwidget,2,0)
		self.listwidget.itemClicked.connect(self.itemclicked)
		#QTree
		self.treewidget  = QtWidgets.QTreeWidget()
		self.treewidget.setHeaderLabels(['This','is','a','TreeWidgets!'])
		self.root = QtWidgets.QTreeWidgetItem(self.treewidget)
		self.child1 =  QtWidgets.QTreeWidgetItem(self.root)
		self.child1.setText(0,'child1')
		self.child1.setText(1,'name1')
		self.child2 = QtWidgets.QTreeWidgetItem(self.child1)
		self.child2.setText(0,'1231')
		self.gL1.addWidget(self.treewidget,2,1)
		#
		self.bt1.clicked.connect(self.showDialog)
		#
		#Canvas
		self.main_widget = QWidget()
		self.sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
		self.gL1.addWidget(self.sc,0,2,0,2)
		#
		#QSplit
		self.splitter = QtWidgets.QSplitter(orientation=QtCore.Qt.Horizontal)
		self.gL.addWidget(self.splitter,2,1)
		self.splitter.setSizes([self.splitter.size().height() * 0.3, self.splitter.size().height() * 0.3,self.splitter.size().height() * 0.4])
		#
		#QTextEdit
		self.textedit = QtWidgets.QTextEdit()
		self.splitter.addWidget(self.textedit)
		#
		#QTab
		self.wdg1 = QtWidgets.QWidget()
		self.wdg2 = QtWidgets.QWidget()
		self.tabWidget = QtWidgets.QTabWidget()
		self.tabWidget.addTab(self.wdg1, 'Wdg 1')
		self.tabWidget.addTab(self.wdg2, 'Wdg 2')
		self.splitter.addWidget(self.tabWidget)
		#
		#QCheck
		self.checkbox = QtWidgets.QCheckBox("Awesome?")
		self.checkbox.stateChanged.connect(self.clickBox)
		self.splitter.addWidget(self.checkbox)
		#
	def showDialog(self):
		# MessageBox
		QtWidgets.QMessageBox.information(self.bt1,'标题','消息对话框正文',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
		#
	def itemclicked(self,item):
		print (item.text())
	def clickBox(self, state):
		if state == QtCore.Qt.Checked:
			print('Checked')
		else:
			print('Unchecked')
####################################################################################
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ex = Ui_MainWindow()
	w = QtWidgets.QMainWindow()
	ex.setupUi(w)
	w.show()
	sys.exit(app.exec_())
####################################################################################