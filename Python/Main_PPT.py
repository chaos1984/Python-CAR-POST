import sys
import os
from Infor import *
from pptreport import *

try:
	wkdir = sys.argv[1]
except:
	wkdir = 'Y:\cal\01_Comp\04_SB\548-180423_ESR_038128_CTR_BUK_Bracket_Strength_Yujin\02_run'
	
AnalysisType ='Anchor'
Title = u'ESR-036622_SX11_AND_SX12_rear_single_anchor_plate_strength'
Date = '2018-04-24'
Author = u'Yujin Wang'
ReportContentsList = ['1.FE Model\n','2.Material Specification\n','3.Load & Boundary Condition\n','4.Results\n','5.Conclusion\n']
AnalysisContent = 'FE model'
AnalysisConclusion = 'Current maximum displacement occurs on the anchor plate is 16.7mm, and no breakage occurs on the anchor plate during a tensile force of 22KN.In general, current design meets the analysis requirement.'
muban_path = r'C:\Users\yujin.wang\Desktop\New_folder\ALV_General Presentation 2017.pptx'

	
dirs = FindFile(wkdir, 'd3plot')[1]
A = StiffPPT(muban_path,wkdir)

print 'wkdir',wkdir
print 'dirs:',dirs

#page1
A.CoverPageCreate(Title,Date,Author)

#page2
ReportContents = '\n'.join(ReportContentsList)
A.BlankPageCreate('Contents',ReportContents)

#Page3
Pictures = []
for i,j in enumerate(dirs):
	file = FindFile(j,'model.png')[0]
	Pictures.append([file[0],Cm(i*8+1),Cm(10),Cm(8),Cm(15)])
# if file2 !=[]:
	# Pictures .append([file2[0],Cm(1),Cm(10),Cm(8),Cm(15)])
# print Pictures
TableValue =[[' Part','Element Type','Material'],['Bracket','Hex','S550Y600T_low'],['Bolt','Hex','Elastro-steel'],['Fixture','Hex','Rigid']]
Tables = [[TableValue,Cm(16),Cm(3),Cm(4),Cm(16)]]
A.BlankPageCreate('FE Model','',Pictures=Pictures,Tables=Tables)

#page4

file1 = FindFile(wkdir,'stress_strain.png')[0]
Pictures = [[file1[0],Cm(16),Cm(4),Cm(8),Cm(16)]]
A.BlankPageCreate("Material Specification","Material Type: S500MC\nDensity 7.85e-09 t/mm3 \nYoung's modulus 210000 Mpa\nNew failure model has been used for this material element will be removed if failure occur",Pictures=Pictures)

#page5
A.BlankPageCreate("Load & Boundary Condition")

#page6
for dirname in dirs:#direct path
	# try:
		image_dir =  dirname  +'\\image\\'
		Pictures = [[image_dir +'deforc.png',Cm(15),Cm(5),Cm(6),Cm(13)]]
		Movies = [[image_dir  +'anim.avi',Cm(3),Cm(8),Cm(10),Cm(9)]]
		title = 'Simulation Results'+dirname
		A.BlankPageCreate('Simulation Results','',Pictures=Pictures,Movies=Movies)
		
		Pictures=[]
		for  i in range(3):
			for j in range(2):
				x = 1+10*i
				y = 5 + 7*j
				Pictures .append([image_dir +'stress'+str(i+1+j*3)+'.png',Cm(x),Cm(y),Cm(4.71),Cm(7.06)])
		A.BlankPageCreate('Simulation Results','',Pictures=Pictures)
		
		Pictures=[]
		for  i in range(3):
			for j in range(2):
				x = 1+10*i
				y = 5 + 7*j
				Pictures .append([image_dir +'strain'+str(i+1+j*3)+'.png',Cm(x),Cm(y),Cm(4.71),Cm(7.06)])
		A.BlankPageCreate('Simulation Results','',Pictures=Pictures)
	# except:
		# break

#page7
A.BlankPageCreate('Conclusion','Current maximum displacement occurs on the anchor plate is 16.7mm, and no breakage occurs on the anchor plate during a tensile force of 22KN.\nIn general, current design meets the analysis requirement.')
	
#page8
A.EndPageCreate()
A.PPTCreate(AnalysisType)
