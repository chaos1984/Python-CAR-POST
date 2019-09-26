import sys
import random
import time
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from function import *
import pandas as pd

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
		self.gL1.addWidget(self.center,0,0,2,2)
		self.framelayout = QtWidgets.QGridLayout() 
		self.center.setLayout(self.framelayout)
		#
		#QLabel
		self.l1 = QtWidgets.QLabel(r'用户名:')
		self.l1.setObjectName('l1')
		self.framelayout.addWidget(self.l1,0,0)
		#
		#QLabel
		self.l2 = QtWidgets.QLabel(r'密 码:')
		self.l2.setObjectName('l2')
		self.framelayout.addWidget(self.l2,1,0)
		#
		#LineEdit
		self.e1 = QtWidgets.QLineEdit()
		self.e1.setValidator(QtGui.QIntValidator())
		self.e1.setMaxLength(6)
		self.e1.setAlignment(QtCore.Qt.AlignRight)
		self.e1.setObjectName('e1')
		self.e1.setFont(QtGui.QFont("Arial",10))
		self.framelayout.addWidget(self.e1,0,1)
		#
		#LineEdit
		self.e2 = QtWidgets.QLineEdit()
		self.e2.setValidator(QtGui.QIntValidator())
		self.e2.setMaxLength(6)
		self.e2.setAlignment(QtCore.Qt.AlignRight)
		self.e2.setObjectName('e2')
		self.e2.setFont(QtGui.QFont("Arial",10))
		self.framelayout.addWidget(self.e2,1,1)
		#
		#QPushButton
		self.bt1 = QtWidgets.QPushButton("OK")
		self.bt1.setObjectName("bt1")
		self.framelayout.addWidget(self.bt1,1,2)
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
		#
		self.tabWidget = QtWidgets.QTabWidget()
		self.splitter.addWidget(self.tabWidget)
		#
		self.tabWidget.addTab(self.wdg1, 'Wdg 1')
		self.wdg1_layout = QtWidgets.QVBoxLayout() 
		self.wdg1.setLayout(self.wdg1_layout)
		#
		self.tabWidget.addTab(self.wdg2, 'Wdg 2')
		self.wdg2_layout = QtWidgets.QVBoxLayout() 
		self.wdg2.setLayout(self.wdg2_layout)
		self.wdg2_pixMap =  QtGui.QPixmap('test_image1.png')
		self.wdg2_label = QtWidgets.QLabel()
		self.wdg2_label.setPixmap(self.wdg2_pixMap)
		self.wdg2_layout.addWidget(self.wdg2_label)
		#
		#QCheck
		self.checkbox = QtWidgets.QCheckBox("Awesome?")
		self.checkbox.stateChanged.connect(self.clickBox)
		self.splitter.addWidget(self.checkbox)
		#
		#Canvas
		self.main_widget = QWidget()
		self.sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
		self.wdg1_layout.addWidget(self.sc)
		#
		#QGroupBox
		self.echoGroup =  QtWidgets.QGroupBox('Echo')
		self.echoLayout = QtWidgets.QGridLayout()
		self.echoGroup.setLayout(self.echoLayout)
		self.echoLabel = QtWidgets.QLabel('Mode:')
		self.echoLayout.addWidget(self.echoLabel,0,0)
		self.framelayout.addWidget(self.echoGroup,0,2)
		#QCombox
		self.comboLayout = QtWidgets.QGridLayout()
		self.combobox2 = QtWidgets.QComboBox(minimumWidth=200)
		self.comboLayout.addWidget(QtWidgets.QLabel("增加单项，不带数据"))
		self.comboLayout.addWidget(self.combobox2)
		self.comboLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum))
		items_list=["C","C++","Java","Python","JavaScript","C#","Swift","go","Ruby","Lua","PHP"]
		datas_list=[1972,1983,1995,1991,1992,2000,2014,2009,1995,1993,1995]
		for i in range(len(items_list)):
			self.combobox2.addItem(items_list[i],datas_list[i])
		self.combobox2.setCurrentIndex(-1)
		self.combobox2.activated.connect(self.on_combobox2_Activate)
		self.gL.addWidget(self.combobox2,1,2)
		#QTable
		self.dataTable = QtWidgets.QTableWidget()
		self.dataTable.setRowCount(1)
		self.dataTable.setColumnCount(1)
		self.gL.addWidget(self.dataTable,2,2)
		#
		#QFileDir
		self.btn2 = QtWidgets.QPushButton("输入文件")
		self.echoLayout.addWidget(self.btn2)
		self.btn2.clicked.connect(self.filedirgetfile)
		#
		#QFileDir
		self.btn3 = QtWidgets.QPushButton("输出文件")
		self.echoLayout.addWidget(self.btn3)
		self.btn3.clicked.connect(self.filedirsavefile)
		#
###################################################################################
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
	def on_combobox2_Activate(self, index):
		print(self.combobox2.currentText())
		print(self.combobox2.currentData())
	def filedirgetfile(self):
		self.filedir,_ = QtWidgets.QFileDialog.getOpenFileName(caption='打开文件',directory="C:\\Users\\yujin.wang\\Desktop\\New folder",filter="CSV files(*.txt *.csv)")
		df = pd.read_csv(self.filedir)
		self.dataTable.setRowCount(np.shape(df)[0])
		self.dataTable.setColumnCount(np.shape(df)[1])
		self.dataTable.setHorizontalHeaderLabels(df.columns)
		for i in range(np.shape(df)[0]-1):
			for j in range(np.shape(df)[1]):
				self.dataTable.setItem(i,j,QtWidgets.QTableWidgetItem(str(df.iloc[i,j])))
	def filedirsavefile(self):
		self.headers = []
		# print (self.dataTable.horizontalHeaderItem(1))
		for column in range(self.dataTable.columnCount()):
			header = self.dataTable.horizontalHeaderItem(column)
			self.headers.append(header.text())
		dd = pd.DataFrame(columns = self.headers)
		len1 = len(self.dataTable.horizontalHeader())
		# print (len(self.dataTable.horizontalHeader()))
		# print (self.dataTable.rowCount(),self.dataTable.columnCount())
		for i in range(self.dataTable.rowCount()):
				dd.append([self.dataTable.item(i,j).text() for j in range(len1)])
		self.filedir,_ = QtWidgets.QFileDialog.getSaveFileName(caption='打开文件',directory="C:\\Users\\yujin.wang\\Desktop\\New folder",filter="CSV files(*.txt *.csv)")
		dd.to_csv(self.filedir)
		
####################################################################################
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ex = Ui_MainWindow()
	w = QtWidgets.QMainWindow()
	ex.setupUi(w)
	w.show()
	sys.exit(app.exec_())
####################################################################################