#coding:utf-8
import sys


try:
	rundir = sys.argv[1]
	wkdir = sys.argv[2]
except:
	rundir = r"C:\Users\chaos\Documents\GitHub\Python-CAR-POST\Python"
	wkdir = r'C:\Users\chaos\Desktop\PySTIFF'
print wkdir
sys.path.append(rundir+"\\lib")
from Infor import *
from pptreport import *
import getpass


muban_path = r'C:\Users\chaos\Desktop\PySTIFF\Slidmaster\SlidMaster.pptx'
imagedir = wkdir + '\\image\\'
A = StiffPPT(muban_path,wkdir)

###########################MODIFY############################################################
PPTName = wkdir.split('\\')[-1]
Title = ' '.join(wkdir.split('\\')[-1].split('_'))
Date =  time.strftime("%b %d %Y", time.localtime())
Author = getpass.getuser()
#############################################################################################

#page1
A.CoverPageCreate(Title,Date,Author)

#page2
ReportContents= [['1.背景\n2.模拟结果\n3.结论\n',24]]
A.BlankPageCreate('背景',Paragraphs=ReportContents)

#page3
paragraphs = [["目标",24,'b'],["* 白车身弯曲刚度>15000 Nm",18]]
Pictures = [[imagedir +'bend.png',Cm(8.2),Cm(7.5),Cm(5.5),Cm(9)]]
A.BlankPageCreate('分析结果',Paragraphs =paragraphs,Pictures=Pictures)

#page4
paragraphs = [["目标",24,'b'],["* 白车身扭转刚度>15000 Nm。",18]]
Pictures = [[imagedir +'torq.png',Cm(8.2),Cm(7.5),Cm(5.5),Cm(9)]]
A.BlankPageCreate('分析结果',Paragraphs =paragraphs,Pictures=Pictures)

#page5
result = sys.argv[3].split(',')

paragraphs = [[u"图表",24,'b'],[u"分析结果表明：",18],[u"白车身刚度不满足设计要求！",18,"b","i","r"]]
TableValue = [[' ',u"扭转刚度",u"弯曲刚度","轻量化系数"],["分析结果",result[0],result[1],result[2]]]
Table = [[TableValue,Cm(8.2),Cm(7.5),Cm(3),Cm(12)]]
A.BlankPageCreate(u"结论",Paragraphs =paragraphs,Tables=Table)

#page8
A.EndPageCreate()
A.PPTCreate(PPTName)
