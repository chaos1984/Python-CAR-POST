import sys
import os
import time
import getpass
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def findkeyword(string,keyword,s0,inc):
    start = string.find(keyword)
    # print (string)
    # print (start,inc)
    return string[start+s0:start+s0+inc]

def parserKeyfile(filedir):
	matdic = {}
	try:
		for line in open(filedir):
			if 'M000' in line:
				matdic['Cushion'] =  line
			elif 'M200' in line:
				matdic['Cover'] = line
			elif 'M300' in line:
				matdic['Housing'] = line
			elif 'M400' in line:
				matdic['Emblem'] = line
		print (matdic)
		return matdic
	except:
		print ('ERROR:Check KeyFile!')

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		self.screen = QtWidgets.QDesktopWidget().screenGeometry()
		MainWindow.setGeometry(10, 50, self.screen.width()/4,self.screen.height()/4)
		# MainWindow.resize(self.screen.width()/4,self.screen.height()/4)
		# MainWindow.showMaximized()
		self.centralWidget = QtWidgets.QWidget(MainWindow)
		self.centralWidget.setObjectName("centralWidget")
		MainWindow.setCentralWidget(self.centralWidget)
		self.Author = getpass.getuser()
		self.time = time.strftime("%Y-%m-%d", time.localtime())
####################################################################################
		#QGridLayout
		self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
		self.gridLayout.setSpacing(6)
		self.gridLayout.setObjectName("gridLayout")
		#
		#QSplit
		self.splitter = QtWidgets.QSplitter(orientation=QtCore.Qt.Horizontal)
		self.gridLayout.addWidget(self.splitter)
		self.splitter.setSizes([self.splitter.size().height() * 0.8, self.splitter.size().height() * 0.2])
		#
		#QGroupBox
		self.echoGroup =  QtWidgets.QGroupBox('Control')
		self.echoLayout = QtWidgets.QGridLayout()
		self.echoGroup.setLayout(self.echoLayout)
		self.splitter.addWidget(self.echoGroup)
		#
		# #QFileDir
		# self.btn2 = QtWidgets.QPushButton("DAB Info dir.")
		# self.echoLayout.addWidget(self.btn2)
		# self.btn2.clicked.connect(self.filedirgetfile)
		#
		#QFileDir
		self.btn3 = QtWidgets.QPushButton("Save")
		self.echoLayout.addWidget(self.btn3)
		self.btn3.clicked.connect(self.filedirsavefile)
		#
		#QButton_add
		self.btn4 = QtWidgets.QPushButton("Insert line")
		self.echoLayout.addWidget(self.btn4)
		self.btn4.clicked.connect(self.table_insert)
		#QButton_add
		self.btn5 = QtWidgets.QPushButton("Delete line")
		self.echoLayout.addWidget(self.btn5)
		self.btn5.clicked.connect(self.table_delete)
		#QButton_sort
		self.btn6 = QtWidgets.QPushButton("Sort")
		self.echoLayout.addWidget(self.btn6)
		self.btn6.clicked.connect(self.table_sort)
		#QTable
		self.dataTable = QtWidgets.QTableWidget()
		self.dataTable.setRowCount(2)
		self.dataTable.setColumnCount(3)
		self.splitter.addWidget(self.dataTable)
		self.des_sort = True
		#
		#LineEdit
		self.e1 = QtWidgets.QLineEdit()
		# self.e1.setValidator(QtGui.QIntValidator())
		self.e1.setMaxLength(6)
		self.e1.setAlignment(QtCore.Qt.AlignRight)
		self.e1.setObjectName('e1')
		self.e1.setFont(QtGui.QFont("Arial",10))
		self.echoLayout.addWidget(self.e1)
		#
		#QButton_sort
		self.btn7 = QtWidgets.QPushButton("Filter")
		self.echoLayout.addWidget(self.btn7)
		self.btn7.clicked.connect(self.rowhidden)
		#
		#QCombox_x
		self.comboLayout = QtWidgets.QGridLayout()
		self.combobox1 = QtWidgets.QComboBox(minimumWidth=200)
		self.comboLayout.addWidget(QtWidgets.QLabel("X-Axis:"))
		self.comboLayout.addWidget(self.combobox1)
		self.comboLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum))
		# datas_list=[1972,1983,1995,1991,1992,2000,2014,2009,1995,1993,1995]
		# for i in range(len(items_list)):
			# self.combobox2.addItem(items_list[i])
		self.combobox1.setCurrentIndex(-1)
		self.combobox1.activated.connect(self.on_combobox2_Activate)
		self.echoLayout.addWidget(self.combobox1)
		#QCombox_y
		self.comboLayout = QtWidgets.QGridLayout()
		self.combobox2 = QtWidgets.QComboBox(minimumWidth=200)
		self.comboLayout.addWidget(QtWidgets.QLabel("Y-Axis:"))
		self.comboLayout.addWidget(self.combobox2)
		self.comboLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum))
		# items_list=self.headers
		# datas_list=[1972,1983,1995,1991,1992,2000,2014,2009,1995,1993,1995]
		# for i in range(len(items_list)):
			# self.combobox2.addItem(items_list[i])
		self.combobox1.setCurrentIndex(-1)
		self.combobox1.activated.connect(self.on_combobox1_Activate)
		self.echoLayout.addWidget(self.combobox2)
		#QButton_plot
		self.btn8 = QtWidgets.QPushButton("Plot")
		self.echoLayout.addWidget(self.btn8)
		self.btn8.clicked.connect(self.figureplot)
################################################################################
		self.filedirgetfile()
################################################################################
	def filedirgetfile(self):
		# try:
			self.filedir= r"Y:\\comp\\02_DAB\\DAB_Information.csv"
			self.df = pd.read_csv(self.filedir)
			self.dataTable.setRowCount(np.shape(self.df)[0])
			self.dataTable.setColumnCount(np.shape(self.df)[1])
			self.dataTable.setHorizontalHeaderLabels(self.df.columns)
			self.column_dic = {}
			for index,column in enumerate(self.df.columns):
				self.column_dic[column] = index
			self.combobox_remove()
			self.combobox_load()
			self.data_rows = np.shape(self.df)[0]
			self.data_colums = np.shape(self.df)[1]
			for i in range(self.data_rows):
				for j in range(self.data_colums-1):
					self.dataTable.setItem(i,j,QtWidgets.QTableWidgetItem(str(self.df.iloc[i,j])))
				self.dataTable.setCellWidget(i,self.data_colums-1,self.buttonForRow(str(i)))
				# print (self.dataTable.item(i,self.column_dic['Close']).text())
				if self.dataTable.item(i,self.column_dic['Close']).text() == 'Lock':
					for j in range(self.data_colums-1):
						self.dataTable.item(i,j).setFlags(QtCore.Qt.ItemIsEnabled)
			self.dataTable.resizeColumnsToContents()
			# self.dataTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		# except:
			# pass
			
		#
	def combobox_remove(self):
		# print (self.combobox1.count())
		# for i in range(self.combobox1.count()):
			self.combobox1.clear()
			self.combobox2.clear()
	def combobox_load(self):
		items_list = self.df.columns
		for i in range(len(items_list)):
			self.combobox1.addItem(items_list[i])
			self.combobox2.addItem(items_list[i])
	def filedirsavefile(self):
		# try:
			# self.filedir =  r"Y:\\cal\\01_Comp\\02_DAB\\DAB_Information.csv"
			self.df.to_csv(self.filedir[:-4]+'_copy' +'.csv')
			self.headers = []
			# print (self.dataTable.horizontalHeaderItem(1))
			for column in range(self.dataTable.columnCount()):
				header = self.dataTable.horizontalHeaderItem(column)
				self.headers.append(header.text())
			len1 = len(self.dataTable.horizontalHeader())
			# print (len(self.dataTable.horizontalHeader()))
			# print (self.dataTable.rowCount(),self.dataTable.columnCount())
			data = []
			for i in range(self.dataTable.rowCount()):
				temp = []
				for j in range(len1):
					cell = self.dataTable.item(i,j)
					if cell is not None and cell.text() != '':
						temp.append(cell.text())
					else:
						temp.append(' ')
				data.append(temp)
			dd = pd.DataFrame(data,columns = self.headers)
			dd.set_index(["Author"], inplace=True)
			dd.to_csv(self.filedir)
			dd.to_csv(self.time+'_'+self.Author+'.csv')
		# except:
			# pass
	def table_insert(self):
		row = self.dataTable.rowCount()
		self.dataTable.insertRow(row)
		for col in range(self.data_colums):
			self.dataTable.setItem(row , col, QtWidgets.QTableWidgetItem(' '))
		self.dataTable.setItem(row , 0, QtWidgets.QTableWidgetItem(self.Author))
		self.dataTable.setItem(row , 2, QtWidgets.QTableWidgetItem(self.time))
		self.dataTable.setItem(row , self.column_dic['Close'], QtWidgets.QTableWidgetItem('Unlock'))
		self.dataTable.setCellWidget(row,self.data_colums-1,self.buttonForRow(str(row)))
		self.dataTable.resizeColumnsToContents()
	def table_delete(self):
		try:
			row_select = self.dataTable.selectedItems()
			row = row_select[0].row()
			self.dataTable.removeRow(row)
		except:
			pass
	def table_sort(self):
		try:
			if self.des_sort == True:
				col_select = self.dataTable.selectedItems()
				col = col_select[0].column()
				self.dataTable.sortItems(col,QtCore.Qt.DescendingOrder)
				self.des_sort = False
				# self.btn_sort.setStyleSheet('background-color:lightblue')
				self.dataTable.setSortingEnabled(True)  
			else:
				col_select = self.dataTable.selectedItems()
				col = col_select[0].column()
				self.dataTable.sortItems(col,QtCore.Qt.AscendingOrder)
				self.des_sort = True
				# self.btn_sort.setStyleSheet('background-color:lightblue')
				self.dataTable.setSortingEnabled(False)
		except:
			pass
	def rowhidden(self):
		# try:
			items = self.dataTable.findItems(self.e1.text(),QtCore.Qt.MatchContains)
			for i in range(self.dataTable.rowCount()):
				if self.e1.text() != '':
					items_row = [i.row() for i in items]
					if i in items_row:
						pass
					else:
						self.dataTable.setRowHidden(i, True)
				else:
					self.dataTable.setRowHidden(i, False)
		# except:
			# print ('ERROE:',self.e1.text())
	def on_combobox1_Activate(self, index):
		self.plot_x = self.df[self.combobox1.currentText()]
		# print(self.combobox2.currentData())
	def on_combobox2_Activate(self, index):
		self.plot_y = self.df[self.combobox2.currentText()]
		# print(self.combobox2.currentData())
	def figureplot(self):
		try:
			print (self.combobox1.currentText(),self.combobox2.currentText())
			plt.plot(self.plot_x,self.plot_y)
			plt.xlabel(self.combobox1.currentText())
			plt.ylabel(self.combobox2.currentText())
			plt.show()
		except:
			pass

	def buttonForRow(self,id):
		widget=QWidget()
		# fill
		updateBtn = QtWidgets.QPushButton('Fill')
		updateBtn.setStyleSheet(''' text-align : center;
										  background-color : NavajoWhite;
										  height : 30px;
										  border-style: outset;
										  font : 13px  ''')

		updateBtn.clicked.connect(lambda:self.fillTable(id))

		# view
		viewBtn = QtWidgets.QPushButton('View')
		viewBtn.setStyleSheet(''' text-align : center;
								  background-color : DarkSeaGreen;
								  height : 30px;
								  border-style: outset;
								  font : 13px; ''')

		viewBtn.clicked.connect(lambda: self.viewFolder(id))
		#Lock
		lockBtn = QtWidgets.QPushButton('Lock')
		lockBtn.setStyleSheet(''' text-align : center;
								  background-color : Red;
								  height : 30px;
								  border-style: outset;
								  font : 13px; ''')

		lockBtn.clicked.connect(lambda: self.lockRow(id))
		
		hLayout = QtWidgets.QHBoxLayout()
		hLayout.addWidget(updateBtn)
		hLayout.addWidget(viewBtn)
		hLayout.addWidget(lockBtn)
		hLayout.setContentsMargins(5,2,5,2)
		widget.setLayout(hLayout)
		return widget
	def viewFolder(self,id):
		cell = self.dataTable.item(int(id),self.column_dic['Keyfile'])
		try:
			path = cell.text()
			cmd = "start explorer " + path
			os.system(cmd)
		except:
			print ("ERROR:No Path!",type(self.column_dic['Keyfile']))
			self.dataTable.setItem(int(id),self.column_dic['Keyfile'] , QtWidgets.QTableWidgetItem('NO dir'))
	def fillTable(self,id):
		if self.dataTable.item(int(id),self.column_dic['Close']).text() != 'Lock':
			try:
				path = self.df['Keyfile'][int(id)]
				self.keyfiledir,_ = QtWidgets.QFileDialog.getOpenFileName(caption='Select key file',directory=path,filter="KEY files(*.k *.key *.dyn)")
			except:
				self.keyfiledir,_ = QtWidgets.QFileDialog.getOpenFileName(caption='Select key file',filter="KEY files(*.k *.key *.dyn)")
			path = self.keyfiledir	
			ESR = findkeyword(path,"ESR-",0,10)
			self.dataTable.setItem(int(id),self.column_dic["ESR"] , QtWidgets.QTableWidgetItem(str(ESR)))
			AFIS = findkeyword(path,"AFIS",4,5)
			self.dataTable.setItem(int(id),self.column_dic["AFIS"] , QtWidgets.QTableWidgetItem(str(AFIS)))
#             AFIS = findkeyword(path,"AFIS",9)
# 			self.dataTable.setItem(int(id),self.column_dic["AFIS"] , QtWidgets.QTableWidgetItem(str(AFIS)))
			try:
				matdic = parserKeyfile(self.keyfiledir)
				for key in matdic.keys():
					self.dataTable.setItem(int(id),self.column_dic[key] , QtWidgets.QTableWidgetItem(matdic[key]))
				self.dataTable.setItem(int(id),self.column_dic['Keyfile'] , QtWidgets.QTableWidgetItem(self.keyfiledir.replace('/','\\')))
			except:
				print ('ERROR: Fill table')
				
			
			
	def lockRow(self,id):
		try:
			# print (self.dataTable.item(int(id),self.column_dic['Close']).text())
			if self.dataTable.item(int(id),self.column_dic['Close']).text() != 'Lock':
				# if self.dataTable.item(int(id),i)
				self.dataTable.setItem(int(id),self.column_dic['Close'],QtWidgets.QTableWidgetItem('Lock'))
				for i in range(self.data_colums-1):
					self.dataTable.item(int(id),i).setFlags(QtCore.Qt.ItemIsEnabled)
			else:
				self.dataTable.setItem(int(id),self.column_dic['Close'],QtWidgets.QTableWidgetItem('Unlock'))
				for i in range(self.data_colums-1):
					self.dataTable.item(int(id),i).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
		except:
			pass
			# if lockBtn.isChecked():
				# print('button pressed')
			# else:
				# print('button released')

####################################################################################
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	# message = MessageWindow()
	ex = Ui_MainWindow()
	w = QtWidgets.QMainWindow()
	ex.setupUi(w)
	w.show()
	sys.exit(app.exec_())
####################################################################################