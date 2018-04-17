import sys
import os
from pptreport import *
case_path = sys.argv[1]+'\\image\\'
AnalysisType ='Anchor'
Title = u'ESR-036622_SX11_AND_SX12_rear_single_anchor_plate_strength'
Date = '2018-03-09'
Author = u'Allen Zhu'
ReportContentsList = ['1.FE Model\n','2.Material Specification\n','3.Load & Boundary Condition\n','4.Results\n','5.Conclusion\n']
AnalysisContent = 'FE model'
AnalysisConclusion = 'Current maximum displacement occurs on the anchor plate is 16.7mm, and no breakage occurs on the anchor plate during a tensile force of 22KN.In general, current design meets the analysis requirement.'
muban_path = r'C:\Users\yujin.wang\Desktop\New_folder\ALV_General Presentation 2017.pptx'

A = StiffPPT(muban_path,case_path)
#page1
A.CoverPageCreate(Title,Date,Author)

#page2
ReportContents = '\n'.join(ReportContentsList)
A.BlankPageCreate('Contents',ReportContents)

#Page3
Pictures = [['\\deforc.png',Cm(1),Cm(10),Cm(8),Cm(15)]]
TableValue =[[' Part','Element Type','Material'],['Bracket','Hex','S550Y600T_low'],['Bolt','Hex','Elastro-steel'],['Fixture','Hex','Rigid']]
Tables = [[TableValue ,Cm(16),Cm(3),Cm(4),Cm(16)]]
A.BlankPageCreate('FE Model','',Pictures=Pictures,Tables=Tables)

#page4
Pictures = [['\\deforc.png',Cm(16),Cm(4),Cm(8),Cm(16)],[r'deforc.png',Cm(11),Cm(4),Cm(8),Cm(16)]]
A.BlankPageCreate("Material Specification","Material Type: S500MC\nDensity 7.85e-09 t/mm3 \nYoung's modulus 210000 Mpa\nNew failure model has been used for this material element will be removed if failure occur",Pictures=Pictures)

#page5

A.BlankPageCreate("Load & Boundary Condition")

#page6
Pictures = [['deforc.png',Cm(15),Cm(5),Cm(6),Cm(13)],[r'deforc.png',Cm(15),Cm(12),Cm(6),Cm(13)]]
Movies = [['anim.avi',Cm(3),Cm(8),Cm(10),Cm(9)]]
A.BlankPageCreate('Simulation Results (load 1)','',Pictures=Pictures,Movies=Movies)

#page7
A.BlankPageCreate('Conclusion','Current maximum displacement occurs on the anchor plate is 16.7mm, and no breakage occurs on the anchor plate during a tensile force of 22KN.\nIn general, current design meets the analysis requirement.')

#page8
A.EndPageCreate()
A.PPTCreate(AnalysisType)
