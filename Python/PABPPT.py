#coding:utf-8
import sys
import getpass
try:
	rundir = sys.argv[1]
	wkdir = sys.argv[2]
except:
	rundir = r"Y:\doc\11_Script\SBStrengthAndPABPSD"
	wkdir = r'Y:\cal\01_Comp\09_NVH\395_180507_ESR-038350_GDP_IC_Inflator_Bracket_fatigue_Anne\02_run_Bracket_2\33_3Hz'
	
sys.path.append(rundir+"\\lib")
from Infor import *
from pptreport import *

muban_path = r'%s\SlideMaster\ALV_General Presentation 2017.pptx' %(rundir)
imagedir = wkdir + '\\image\\'
A = StiffPPT(muban_path,wkdir)

###########################MODIFY############################################################
PPTName = wkdir.split('\\')[-2]
Title = ' '.join(wkdir.split('\\')[-2].split('_'))
Date =  time.strftime("%b %d %Y", time.localtime())
Author = getpass.getuser()
#############################################################################################

#page1
A.CoverPageCreate(Title,Date,Author)

#page2
ReportContents= [['1.Introduction\n2.Simulation Result\n3.Conclusion\n',24]]
A.BlankPageCreate('Contents',Paragraphs=ReportContents)

#page3
paragraphs = [["Objectives",24,'b'],["* Perform a random vibration fatigue analysis to predict whether or not the PAB, especially the bracket, can pass the vibration durability test.",18],["Input information for simulation",20,'b'],["  * Test specification: ISO_12097;\n  * PSD curve for fatigue simulation",18],["Mass balance is used to simulate the weight of the module, located at its center of mass.",18]]
Pictures = [[imagedir +'5.jpeg',Cm(5),Cm(11),Cm(7),Cm(11.5)]]
A.BlankPageCreate('Introduction',Paragraphs =paragraphs,Pictures=Pictures)

#page4
paragraphs = [["* Boundary Conditions are defined.",18],["* Connections between each part are also defined.",18],["* Density of each material can be adjusted to match the weight of each part.",18],["* Mass balance is used to simulate the weight of the module, located at its center of mass.",18]]
TableValue =[[' Part','Material','E(MPa)','Dens(g/cm3)'],['Bracket','HC340','21000','7.85']]
Tables = [[TableValue,Cm(15),Cm(13.8),Cm(3),Cm(17)]]
Pictures = [[r'%s\image\Picture1.png' %(rundir),Cm(1.5),Cm(10),Cm(7),Cm(13.31)],[imagedir +'5.jpeg',Cm(20),Cm(8),Cm(5.5),Cm(8.3)]]
A.BlankPageCreate('Introduction',Paragraphs =paragraphs,Tables=Tables,Pictures=Pictures)


#page4
paragraphs = [["Fatigue Life with vibration in each of three main axes.",24],["Note:",20,'b','','',''],["       Calculate the Fatigue Life by using the following equation:",16],["                  Fatigue Life=1/( Damage Ratio per hour);\n            And, Min. Fatigue Life = 1/(Max. Damage Ratio per hour ).",16,'b'],["Test spec: ISO_12097\nEvaluation criterion:",20,'b'],["        After X(24 hours)+Y(24 hours)+Z(24 hours),",16] ,["      If Max. Damage Ratio < 1,the bracket passes Test spec.",16,'b']]
A.BlankPageCreate('Introduction',Paragraphs = paragraphs)

#page5
paragraphs = [["Fatigue Life ",20,'b'] ,["   The estimated Damage Ratio is shown as below:",16,]]
Pictures = [[imagedir +'1.jpeg',Cm(1),Cm(8),Cm(6.95),Cm(10.42)],[imagedir +'2.jpeg',Cm(12),Cm(8),Cm(6.95),Cm(10.42)],[imagedir +'3.jpeg',Cm(23),Cm(8),Cm(6.95),Cm(10.42)]]
A.BlankPageCreate('Simulation Result',Paragraphs = paragraphs,Pictures=Pictures )

#page6
paragraphs = [["Fatigue Life ",20,'b'] ,["   The estimated Damage Ratio is shown as below:",16,]]
Pictures = [[imagedir +'4.jpeg',Cm(9.43),Cm(7.5),Cm(10),Cm(15)]]
A.BlankPageCreate('Simulation Result',Paragraphs = paragraphs,Pictures=Pictures )

#page7
paragraphs =[[ 'The bracket with HC340 is predicted to pass the random vibration fatigue test.',24]]
A.BlankPageCreate('Conclusion',Paragraphs = paragraphs)
	
#page8
A.EndPageCreate()
A.PPTCreate(PPTName)