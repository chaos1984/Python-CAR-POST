#coding:utf-8
import sys

try:
	rundir = sys.argv[1]
	wkdir = sys.argv[2]
except:
	print  "Default Debug Path"
	wkdir = r'Y:\cal\01_Comp\04_SB\566_180611_ESR-039680_BKL_double_buckle_strength_Allen\02_run'
	rundir = r"C:\Users\yujin.wang\Desktop\LocalPy"
	
sys.path.append(rundir+"\\lib")
import time
from Infor import *
from pptreport import *
import getpass



# Material collection in key file

Files = FindFile(wkdir, 'rst.txt')[0]

MatName =[]
LoadForce = {}
for i in Files:
	print i
	Load = i.split('\\')[-3]
	for line in open(i):
		data = string_split(line,' ')
		if 'Mat' in line:
			MatName.append(data[1][:-1])
		elif 'MaxForce' in line:
			cmd = "LoadForce['%s'] = %f" %(Load,round(float(data[1]),2))
			exec(cmd)
MatName = list(set(MatName))


	

#############################################################################################
muban_path = r'%s\SlideMaster\ALV_General Presentation 2017.pptx' %(rundir)
A = StiffPPT(muban_path,wkdir)
###########################MODIFY############################################################
PPTName = "Report"
Title = "ESR-XXXX Anchor Plate Strength"
Date =  time.strftime("%b %d %Y", time.localtime())
Author = getpass.getuser()

#############################################################################################
dirs = FindFile(wkdir, 'd3plot')[1]




#page1
A.CoverPageCreate(Title,Author,Date)

#page2
ReportContents = [['1.FE Model\n2.Material Specification\n3.Load & Boundary Condition\n4.Results\n5.Conclusion',24]]
A.BlankPageCreate('Contents',Paragraphs=ReportContents)

#Page3
Pictures = []
for i,j in enumerate(dirs):
	file = FindFile(j,'model.jpg')[0]
	Pictures.append([file[0],Cm(i*12+1),Cm(10),Cm(8),Cm(15)])
TableValue = [[' Part','Element Type','Material'],['Bolt','Tetra','Elasto-steel'],['Fixture','Hex','Rigid']]
for mat in MatName:
	
	TableValue .append(['Bracket','Hex',mat])

Tables = [[TableValue,Cm(14),Cm(3),Cm(4),Cm(18)]]
A.BlankPageCreate('FE Model',Pictures=Pictures,Tables=Tables)

#page4

file1 = FindFile(wkdir,'stress_strain.png')[0]
Pictures = [[file1[0],Cm(8.9),Cm(10.5),Cm(8),Cm(16)]]
A.BlankPageCreate("Material Specification",[["Material Type: "+','.join(MatName),18],["Density: 7.85e-06 kg/mm3",18],["Young's modulus: 210 GPa",18],["New failure model has been used for this material element will be removed if failure occur.\nCurrent material use the lowest break limit.",18]],Pictures=Pictures)

#page5
A.BlankPageCreate("Load & Boundary Condition")

#page6
for dirname in dirs:#direct path
	# try:
		image_dir =  dirname  +'\\image\\'
		Pictures = [[image_dir +'deforc.png',Cm(15),Cm(5),Cm(6),Cm(13)]]
		Movies = [[image_dir  +'anim.avi',Cm(3),Cm(8),Cm(10),Cm(9)]]
		Load = dirname.split('\\')[-1]
		Title = 'Simulation Results'+' ('+Load+') '
		A.BlankPageCreate(Title,Pictures=Pictures,Movies=Movies)
		
		Pictures=[]
		for  i in range(3):
			for j in range(2):
				x = 1+10*i
				y = 5 + 7*j
				Pictures .append([image_dir +'stress'+str(i+1+j*3)+'.jpg',Cm(x),Cm(y),Cm(6.5),Cm(9.7)])
		A.BlankPageCreate(Title+'stress contour plot',Pictures=Pictures)
		
		Pictures=[]
		for  i in range(3):
			for j in range(2):
				x = 1+10*i
				y = 5 + 7*j
				Pictures .append([image_dir +'strain'+str(i+1+j*3)+'.jpg',Cm(x),Cm(y),Cm(6.5),Cm(9.7)])
		A.BlankPageCreate(Title+'strain contour plot',Pictures=Pictures)
	# except:
		# break

#page7
row1 = ['Load Cases'];row2 =['Target tensile force(kN)'];row3=['Maximal tensile force(kN)'];row4=['Result']

for i in LoadForce:
	row1.append(i)
	row2.append(' ')
	row3.append(str(LoadForce[i]))
	row4.append(' ')
	
TableValue = [row1,row2,row3,row4]

Tables = [[TableValue,Cm(2.8),Cm(5.0),Cm(6),Cm(28)]]

A.BlankPageCreate('Conclusion',[['',200],['Current maximum displacement occurs on the anchor plate is 16.7mm, and no breakage occurs on the anchor plate during a tensile force of 22KN.\n\nIn general, current design meets the analysis requirement.\n\nNote: Current material use the lowest break limit.',18]],Tables=Tables)
	
#page8
A.EndPageCreate()
A.PPTCreate(PPTName)