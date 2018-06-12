#coding:utf-8
import sys
import os

try:
	rundir = sys.argv[1]
	wkdir = sys.argv[2]
except:
	wkdir = r'Y:\cal\01_Comp\04_SB\551_180507_ESR-038259_JCSB_Anchor_plate_strength_Zheng\1233221'
	rundir = r"Y:\doc\08_Personal\Yujin\0508\YokingPy"
	
sys.path.append(rundir+"\\lib")
import time
from Infor import *
from pptreport import *
import getpass

muban_path = r'%s\SlideMaster\ALV_General Presentation 2017.pptx' %(rundir)
A = StiffPPT(muban_path,wkdir)
###########################MODIFY############################################################
PPTName = "Report"
Title = "ESR-XXXX Anchor Plate Strength"
Date =  time.strftime("%b %d %Y", time.localtime())
Author = getpass.getuser()

#############################################################################################
dirs = FindFile(wkdir, 'd3plot')[1]
print 'wkdir',wkdir
print 'dirs:',dirs
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
# if file2 !=[]:
	# Pictures.append([file2[0],Cm(1),Cm(10),Cm(8),Cm(15)])
# print Pictures
TableValue =[[' Part','Element Type','Material'],['Bracket','Hex','S550Y600T_low'],['Bolt','Hex','Elastro-steel'],['Fixture','Hex','Rigid']]
Tables = [[TableValue,Cm(16),Cm(3),Cm(4),Cm(16)]]
A.BlankPageCreate('FE Model',Pictures=Pictures,Tables=Tables)

#page4

file1 = FindFile(wkdir,'stress_strain.png')[0]
Pictures = [[file1[0],Cm(8.9),Cm(10.5),Cm(8),Cm(16)]]
A.BlankPageCreate("Material Specification",[["Material Type: S500MC",18],["Density 7.85e-06 kg/mm3",18],["Young's modulus 210 GPa",18],["New failure model has been used for this material element will be removed if failure occur.\nCurrent material use the lowest break limit.",18]],Pictures=Pictures)

#page5
A.BlankPageCreate("Load & Boundary Condition")

#page6
for dirname in dirs:#direct path
	# try:
		image_dir =  dirname  +'\\image\\'
		Pictures = [[image_dir +'deforc.png',Cm(15),Cm(5),Cm(6),Cm(13)]]
		Movies = [[image_dir  +'anim.avi',Cm(3),Cm(8),Cm(10),Cm(9)]]
		Title = 'Simulation Results'+'('+dirname.split('\\')[-1]+') '
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
A.BlankPageCreate('Conclusion',[['Current maximum displacement occurs on the anchor plate is 16.7mm, and no breakage occurs on the anchor plate during a tensile force of 22KN.\nIn general, current design meets the analysis requirement.\nCurrent material use the lowest break limit.',18]])
	
#page8
A.EndPageCreate()
A.PPTCreate(PPTName)