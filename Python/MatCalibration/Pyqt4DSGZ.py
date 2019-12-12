# -*- coding: utf-8 -*-
import sys
import os
import random
import time
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from numpy import arange
import pandas as pd
################################################################################
import ControlCanvas
from Materialcard import DSGZ_model as MatModel



def FD2ESS(dis,force,L,A):
	EngStrain = dis/L
	EngStress = force/A
	return EngStrain,EngStress

def ESS2TSS(EngStrain,EngStress):
	TrueStrain =  np.log(1+EngStrain)
	TrueStress = EngStress*(1+EngStrain)
	return TrueStrain.tolist(),TrueStress.tolist()

def TSS2EPS(TrueStrain,TrueStress,Ymould_user):
	EPStrain = []
	for i in range(len(TrueStrain)):
		EPStrain.append(TrueStrain[i] - TrueStress[i]/Ymould_user)
		
	return EPStrain,TrueStress

def stressfrommatmodel(*args,strain = np.linspace(0,3,10)):
	strain_stress = []
	strain_stress.append(strain)
	for i in range(len(args[0])):
		a	= MatModel(strain,args[0][i],args[1][i])
		stress_1 = a.DSGZ()
		strain_stress.append(stress_1)
	return strain_stress

	
	
def FindFile(start, name):
	#Find the files whose name string contains str(name), and the directory of files
	isFlag = 0
	lenname = len(name)
	if  '*' in name:
		name = name.strip('*')
		isFlag =1
		lenname = len(name)-1
	relpath =[]
	files_set = []
	dirs = []
	dirs_set = []

	if isFlag == 0:
		for relpath, dirs, files in os.walk(start):
			for i in files:
				if name == i[-lenname:]:
					full_path = os.path.join(start, relpath, i)
					files_set.append(os.path.normpath(os.path.abspath(full_path)))
					dirs_set.append(os.path.join(start, relpath))
						
	elif isFlag == 1:
		for relpath, dirs, files in os.walk(start):
			for i in files:
				if os.path.splitext(i)[-1] == name:
					full_path = os.path.join(start, relpath, i)
					files_set.append(os.path.normpath(os.path.abspath(full_path)))
					dirs_set.append(os.path.join(start, relpath))
	
	dirs_set = list(set(dirs_set))
	return files_set,dirs_set



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
		self.testing = [0,0]
####################################################################################
		#QGridLayout
		self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
		self.gridLayout.setSpacing(2)
		self.gridLayout.setObjectName("gridLayout")
		#splitter
		self.splitter = QtWidgets.QSplitter(orientation=QtCore.Qt.Horizontal)
		self.gridLayout.addWidget(self.splitter,1,0,8,0)
		self.splitter.setSizes([self.splitter.size().height() * 0.8, self.splitter.size().height() * 0.2])
		#DataTableGroup 
		self.DataTableGroup =  QtWidgets.QGroupBox('Control pars table')
		self.DataTableLayout = QtWidgets.QGridLayout()
		self.DataTableGroup.setLayout(self.DataTableLayout)
		self.splitter.addWidget(self.DataTableGroup)
		# Canvas
		self.main_widget = QWidget()
		self.canvaslayout = QtWidgets.QVBoxLayout()
		self.main_widget.setLayout(self.canvaslayout)
		self.dc = ControlCanvas.MyControlMplCanvas(self.main_widget, width=20, height=20, dpi=100)
		self.mpl_toolbar = NavigationToolbar(self.dc,self.main_widget)
		self.canvaslayout.addWidget(self.mpl_toolbar)
		self.canvaslayout.addWidget(self.dc)
		#
		self.splitter.addWidget(self.main_widget)
		# self.gridLayout.addWidget(self.dc,rowspan=-1)
		#
		#QVBoxLayout
		self.verticallayout = QtWidgets.QVBoxLayout()
		# self.verticallayout.setContentsMargins(11, 11, 11, 11)
		self.verticallayout.setSpacing(6)
		self.verticallayout.setObjectName("verticallayout")
		self.gridLayout.addLayout(self.verticallayout, 0, 1)
		#
		self.lb = []
		self.hs = []
		self.sp = []
		self.CalibrationGroup =  QtWidgets.QGroupBox('')
		self.echoLayout = QtWidgets.QGridLayout()
		self.CalibrationGroup.setLayout(self.echoLayout)
		sp_inital_value = [0.01396,-1.0414,-1.24794,1.,4.,1.,0.073,1.0]
		sp_range = [[0.00001,9999],[-500.,500.],[-500.,500.],[0.,500.],[0.,1000.],[0.,100.],[0.,9999.],[0.,100.]]
		lb_name = ['K-scale','C1-curve trend','C2-curve trend','C3--Yiled strain','C4-init strain softening','alpha','m-strain rate','a-init']
		
		sp_start = 2
		for i in range(8):
			self.lb.append(i);self.hs.append(i);self.sp.append(i)
			self.lb[i] = QtWidgets.QLabel(lb_name[i])
			self.echoLayout.addWidget(self.lb[i],i+sp_start,0)
			self.hs[i] = QtWidgets.QSlider(self.centralWidget)
			self.hs[i].setOrientation(QtCore.Qt.Horizontal)
			self.hs[i].setRange(sp_range[i][0],sp_range[i][1])
			self.echoLayout.addWidget(self.hs[i],i+sp_start,2)

			self.sp[i] = QtWidgets.QDoubleSpinBox()
			self.sp[i].setDecimals(5)

			# self.sp[i].valueFromText('0.2')
			self.sp[i].setValue(sp_inital_value[i])
			self.sp[i].setSingleStep(0.01*abs(sp_inital_value[i]) )
			self.sp[i].setRange(sp_range[i][0],sp_range[i][1])
			self.echoLayout.addWidget(self.sp[i],i+sp_start,1)
			self.hs[i].valueChanged.connect(self.sp[i].setValue)
			self.sp[i].valueChanged.connect(self.hs[i].setValue)
			self.hs[i].sliderReleased.connect(lambda: self.dc.update_figure(self.DSGZ_args()))
			self.sp[i].valueChanged.connect(lambda: self.dc.update_figure(self.DSGZ_args()))
		#
		self.testingGroup =  QtWidgets.QGroupBox('Testing')
		self.testingLayout = QtWidgets.QGridLayout()
		self.testingGroup.setLayout(self.testingLayout)
		self.gridLayout.addWidget(self.testingGroup,0,0)
		#
		self.cb1 = QtWidgets.QCheckBox('Clear')
		self.testingLayout.addWidget(self.cb1,0,2)
		#LineEdit
		self.e1 = QtWidgets.QLineEdit()
		self.e1.setMaxLength(80)
		self.e1.setText('')
		self.e1.setAlignment(QtCore.Qt.AlignRight)
		self.testingLayout.addWidget(self.e1,0,0)
		##QFileDir
		self.btn2 = QtWidgets.QPushButton("打开目标文件")
		self.testingLayout.addWidget(self.btn2,0,1)
		self.btn2.clicked.connect(self.filedirgetfile)
		#Group2_Spin_X
		self.sp_testing_x = QtWidgets.QDoubleSpinBox()
		self.sp_testing_x.setDecimals(0)
		self.echoLayout.addWidget(self.sp_testing_x,0,2)
		self.sp_testing_x.setRange(0,9999)
		self.sp_testing_x.valueChanged.connect(lambda: self.dc.update_figure(self.DSGZ_args()))
		#
		#Group2_Spin_y
		self.sp_testing_y = QtWidgets.QDoubleSpinBox()
		self.sp_testing_y.setDecimals(0)
		self.echoLayout.addWidget(self.sp_testing_y,0,3)
		self.sp_testing_y.valueChanged.connect(lambda: self.dc.update_figure(self.DSGZ_args()))
		#
		#reset
		self.btn3 = QtWidgets.QPushButton("Reset")
		self.echoLayout.addWidget(self.btn3,0,4)
		self.btn3.clicked.connect(self.testing_reset)
		#Group2_Qlist
		self.combobox2 = QtWidgets.QComboBox(minimumWidth=100)
		self.echoLayout.addWidget(QtWidgets.QLabel("试验数据调整"),0,0)
		self.echoLayout.addWidget(self.combobox2,0,1)
		##
		#Combox for strain
		self.combobox1 = QtWidgets.QComboBox(minimumWidth=100)
		self.echoLayout.addWidget(QtWidgets.QLabel("单独曲线调整"),1,0)
		self.echoLayout.addWidget(self.combobox1,1,2)
		#LineEdit for strain rate
		self.e2 = QtWidgets.QLineEdit()
		self.e2.setMaxLength(80)
		self.e2.setText("0.0001,0.01,0.1,1,10")
		self.e2.setAlignment(QtCore.Qt.AlignRight)
		self.e2.returnPressed.connect(lambda:self.straincombox())
		self.echoLayout.addWidget(self.e2,1,1)
		#checkbox for select all
		self.cb2 = QtWidgets.QCheckBox('单选')
		self.echoLayout.addWidget(self.cb2,1,3)
		#
		#READ DSGZ PARS
		self.btn1 = QtWidgets.QPushButton("读取已有DSGZ参数")
		self.echoLayout.addWidget(self.btn1,10,0)
		self.btn1.clicked.connect(self.read_dsgz_file)
		#DSGZ PARS FILE DIR.
		self.e3 = QtWidgets.QLineEdit()
		self.e3.setMaxLength(80)
		self.e3.setText("User/DSGZ_PAR.txt")
		self.e3.setAlignment(QtCore.Qt.AlignRight)
		self.echoLayout.addWidget(self.e3,10,2)
		#WRITE DSGZ PARS
		self.btn3 = QtWidgets.QPushButton("写出DSGZ参数")
		self.echoLayout.addWidget(self.btn3,10,3)
		self.btn3.clicked.connect(self.write_dsgz_file)
		#
		#QTab
		self.wdg1 = QtWidgets.QWidget()
		self.wdg2 = QtWidgets.QWidget()
		#
		self.tabWidget = QtWidgets.QTabWidget()
		self.splitter.addWidget(self.tabWidget)
		#
		self.tabWidget.addTab(self.wdg1, 'Calibration control')
		self.wdg1_layout = QtWidgets.QVBoxLayout() 
		self.wdg1.setLayout(self.wdg1_layout)
		self.wdg1_layout.addWidget(self.CalibrationGroup)
		#
		self.tabWidget.addTab(self.wdg2, 'Material card')
		self.wdg2_layout = QtWidgets.QVBoxLayout() 
		self.wdg2.setLayout(self.wdg2_layout)
		#
		self.MaterialGroup =  QtWidgets.QGroupBox('')
		self.MaterialGroupLayout = QtWidgets.QGridLayout()
		self.MaterialGroup.setLayout(self.MaterialGroupLayout)
		
		self.MaterialGrouplb_name = ['Curve NO.','Point No.','Elastic modulus','Max. Strain']
		self.MaterialGrouple_text = ['2350','80','1.5','3']
		self.MaterialGrouplb=[];self.MaterialGrouple=[]
		MaterialGrouplb_rownum = 0
		for i,lbname in enumerate(self.MaterialGrouplb_name):
			MaterialGrouplb_rownum += 1 
			self.MaterialGrouplb.append(i);self.MaterialGrouple.append(i)
			self.MaterialGrouplb[i] = QtWidgets.QLabel(lbname)
			self.MaterialGrouple[i] = QtWidgets.QLineEdit()
			self.MaterialGrouple[i].setText(self.MaterialGrouple_text[i])
			self.MaterialGroupLayout.addWidget(self.MaterialGrouplb[i],i,0)
			self.MaterialGroupLayout.addWidget(self.MaterialGrouple[i],i,1)
			
		self.MaterialGrouplematdir = QtWidgets.QLineEdit()
		self.MaterialGrouplematdir.setText('User/Curve.key')
		self.MaterialGroupbtn1 = QtWidgets.QPushButton('Write')
		self.MaterialGroupLayout.addWidget(QtWidgets.QLabel('材料卡片路径'))
		self.MaterialGroupLayout.addWidget(self.MaterialGrouplematdir,MaterialGrouplb_rownum,1)
		self.MaterialGroupLayout.addWidget(self.MaterialGroupbtn1,MaterialGrouplb_rownum,2)
		self.MaterialGroupbtn1.clicked.connect(lambda:self.CurveKey())
		self.wdg2_layout.addWidget(self.MaterialGroup)
		#Data table
		self.dataTable = QtWidgets.QTableWidget()
		self.dataTable.setColumnCount(8)
		self.dataTable.setHorizontalHeaderLabels(lb_name)
		self.DataTableLayout.addWidget(self.dataTable,0,0,1,0)
		#Data table plot
		self.dataTablebt = QtWidgets.QPushButton("Replot")
		# self.dataTablebt.setCheckable(True)
		self.DataTableLayout.addWidget(self.dataTablebt,2,1)
		self.dataTablebt.clicked.connect(lambda: self.dc.update_figure(self.DSGZ_args_table()))
################################################################################
	def read_dsgz_file(self):
		try:
			finp_dir,_ = QtWidgets.QFileDialog.getOpenFileName(caption="读入DSGZ参数",directory="D:\\",filter="CSV files(*.txt *.csv)")
			for cmdline in open(finp_dir,'r'):
				if '#' not in cmdline:
					exec('self.DSGZ_Args = '+cmdline)
			self.table_fill()
			# print (self.finpdir)
		except:
			print ('ERROR:'+finp_dir)
			
	def write_dsgz_file(self):
		try:
			fout = open(self.e3.text(),'a')
			fout.write('#\n#'+time.strftime("%d.%m.%Y %H:%M:%S")+'\n')
			fout.write(str(self.DSGZ_Args)+'\n')
			fout.close()
		except:
			print ('ERROR:Check filedir or DSGZ_Args')
		#
	def on_combobox2_Activate(self, index):
		try:
			i = self.combobox2.currentData()
			self.testing_cutoff[2*i+0]=self.sp_testing_x.value()
			self.testing_cutoff[2*i+1]=self.sp_testing_y.value()
			# print (self.testing_cutoff)
		except:
			pass
		#
		#Define call function
	def filedirgetfile(self):
		# try:
			self.testing = []
			self.testing_cutoff = []
			self.csv_files = FindFile(self.e1.text(),'.csv')[0]
			for index,i in enumerate(self.csv_files):
				self.testing_cutoff.extend([0,0])
				self.combobox2.addItem(i,index)
			self.combobox2.setCurrentIndex(-1)
			self.combobox2.activated.connect(self.on_combobox2_Activate)
			self.testing_data()
			self.combobox2.setCurrentIndex(0)
			self.straincombox()
			self.DSGZ_Args = [[self.sp[i].value() for i in range(8)] for j in range(len(self.strainrate_item))]
		# except:
			# print ('error')
	#
	def testing_data(self):
		try:
			for file in self.csv_files:
				fd = pd.read_csv(file)
				EES = FD2ESS(fd.Disp,fd.Force,20.,12.)
				a,b = ESS2TSS(EES[0],EES[1])
				self.testing.append(a);self.testing.append(b)
		except:
			print ('ERROR:Testing data is wrong!')
			print (file)
		
	def testing_reset(self):
		try:
			self.testing_cutoff = [0 for i in self.testing_cutoff]
			self.sp_testing_x.setValue(0)
			self.sp_testing_y.setValue(0)
			self.DSGZ_args()
		except:
			pass
	def straincombox(self):
		self.strainrate_item = self.e2.text()
		self.strainrate_item = self.strainrate_item.split(',')
		self.combobox1.clear()
		self.combobox1.addItems(self.strainrate_item)
		
	def table_fill(self):
		self.dataTable.setRowCount(len(self.DSGZ_Args))
		self.dataTable.setColumnCount(8)
		for row in range(len(self.DSGZ_Args)):
			for col in range(8):
				self.dataTable.setItem(row , col, QtWidgets.QTableWidgetItem(str(self.DSGZ_Args[row][col])))
		self.dataTable.resizeColumnsToContents()	

		
	def DSGZ_args(self):
		# try:
		######Achieve the testing strain rate item##############################
			# self.straincombox()
		######
			self.Curveinit()
			i = self.combobox2.currentData()
			self.testing_cutoff[2*i+0] = int(self.sp_testing_x.value())
			self.testing_cutoff[2*i+1] = int(self.sp_testing_y.value())
			testing_copy = self.testing.copy()
			for i in range(int(len(self.testing)/2)):
				testing_offset_x = self.testing_cutoff[2*i+0];testing_offset_y = self.testing_cutoff[2*i+1]
				strain_offset =  testing_copy[2*i+0][testing_offset_x];stress_offset =  testing_copy[2*i+1][testing_offset_x]
				testing_copy[2*i+0] =[ j - strain_offset for j in testing_copy[2*i+0][testing_offset_x :]]
				testing_copy[2*i+1] = [ j - stress_offset for j in testing_copy[2*i+1][testing_offset_x :]]

			if self.cb2.checkState() == 2:
				strainrate_DSGZ = self.combobox1.currentIndex() 
				self.DSGZ_Args[strainrate_DSGZ] = [self.sp[i].value() for i in range(8)]
			else:
				self.DSGZ_Args = [[self.sp[i].value() for i in range(8)] for j in range(len(self.strainrate_item))]
			# self.table_fill()
			self.ss = stressfrommatmodel(self.DSGZ_Args,self.strainrate_item,strain = self.strainrange)
			return self.ss,testing_copy,self.cb1.checkState(),self.strainrate_item
		# except:
			# pass
			
	def DSGZ_args_table(self):
		try:
			self.Curveinit()
			self.DSGZ_Args = []
			for i in range(self.dataTable.rowCount()):
					temp = []
					for j in range(8):
						cell = self.dataTable.item(i,j)
						if cell is not None and cell.text() != '':
							temp.append(float(cell.text()))
						else:
							temp.append(' ')
					self.DSGZ_Args.append(temp)
			testing_copy = self.testing.copy()
			self.ss = stressfrommatmodel(self.DSGZ_Args,self.strainrate_item,strain = self.strainrange)
			return self.ss,testing_copy,self.cb1.checkState(),self.strainrate_item
		except:
			pass
	
	def Curveinit(self):
		self.curvenum = int(self.MaterialGrouple[0].text())
		self.pointnum = int(self.MaterialGrouple[1].text())
		self.ymodulus = float(self.MaterialGrouple[2].text())
		self.maxstrain = float(self.MaterialGrouple[3].text())
		self.strainrange =  np.linspace(0.,self.maxstrain,self.pointnum)
		for i in range(len(self.MaterialGrouplb_name)):
			print (self.MaterialGrouplb_name[i]+':\t'+self.MaterialGrouple[i].text())
###############################TAB2#################################################
	def CurveKey(self):
			dir = self.MaterialGrouplematdir.text()
			self.Curveinit()
			# try:
			fout = open(dir,'w')
			fout.write('*KEYWORD\n')
			fout.write('$ Created: ' + time.strftime("%d.%m.%Y %H:%M:%S") + '\n')
			fout.write("*DEFINE_TABLE\n%d\n" %(self.curvenum))
			for i in self.strainrate_item:
				fout.write("%f\n" %(np.log(float(i))))
			for i in range(len(self.strainrate_item)):
				# print ('****',self.ss[0],self.ss[1],self.ymodulus)
				x,y = TSS2EPS(self.ss[0],self.ss[i+1],self.ymodulus)	
				self.curvenum += 1
				flag = 0 
				fout.write('*DEFINE_CURVE_TITLE\nRate %s\n' %(self.strainrate_item[i]))
				fout.write('$     LCID      SIDR       SFA       SFO      OFFA      OFFO    DATTYP\n')
				fout.write('      %d         0    1.0000    1.0000    0.0000    0.0000\n' %(self.curvenum))
				for i in range(len(x)):
					if x[i] > 0:
						if flag == 0 :
							fout.write("%f,%f\n" %(0,y[i]))
							flag = 1
						if flag != 0 :
							fout.write("%f,%f\n" %(x[i],y[i]))
			fout.write("*END\n")
			fout.close()
			# except:
				# pass
####################################################################################
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	app.setStyle('Fusion')
	ex = Ui_MainWindow()
	w = QtWidgets.QMainWindow()
	ex.setupUi(w)
	w.show()
	sys.exit(app.exec_())
####################################################################################