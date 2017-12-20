# -*- coding: utf-8 -*-
'''
Created on Tue Oct 10 2017
@author: wangyj04
'''

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.util import Cm,Pt,Inches
from pptx.enum.shapes import MSO_SHAPE
import os

class StiffPPT():
#载入模板
	def __init__(self,muban_path,case_path):
		self.case_path = case_path
		self.prs = Presentation(muban_path)
		#模板库
		self.CoverPage = self.prs.slide_layouts[0]
		self.ContentPage = self.prs.slide_layouts[1]
		self.SummaryPage = self.prs.slide_layouts[2]
		self.BlankPage = self.prs.slide_layouts[3]
		self.TablePage = self.prs.slide_layouts[4]
		self.black = RGBColor(0x00,0x00,0x00)
		self.white = RGBColor(0xFF,0xFF,0xFF)

	def CoverPageCreate(self,Title,Company,Date):
		#CoverPage
		slide = self.prs.slides.add_slide(self.CoverPage)#增加幻灯片
		shapes = slide.shapes[0]
		shapes.text = Title
		shapes = slide.shapes[1]
		shapes.text = Company
		shapes = slide.shapes[2]
		shapes.text = Date

	def SummaryPageCreate(self,Title = ' ',Analysis = ' ',Software = ' ',Author = ' ',Date = ' ',AnalysisContent = ' ',AnalysisConclusion = ' '):
		slide = self.prs.slides.add_slide(self.SummaryPage)
		shapes = slide.shapes[0]
		shapes.text = Title
		shapes = slide.shapes[1]
		shapes.text = ' '
		shapes = slide.shapes[2]
		shapes.text = Analysis
		shapes = slide.shapes[3]
		shapes.text = Software
		shapes = slide.shapes[4]
		shapes.text = Author
		shapes = slide.shapes[5]
		shapes.text = Date
		shapes = slide.shapes[6]
		shapes.text = ' '
		shapes = slide.shapes[7]
		shapes.text = ' '
		shapes = slide.shapes[8]
		shapes.text = ' '
		shapes = slide.shapes[9]
		shapes.text = ' '
		shapes = slide.shapes[10]
		shapes.text = ' '
		shapes = slide.shapes[11]
		shapes.text = ' '
		shapes = slide.shapes[12]
		shapes.text = AnalysisContent
		shapes = slide.shapes[13]
		shapes.text = AnalysisConclusion
#目录页
	def ContentsPageCreate(self,ReportContents):
		slide = self.prs.slides.add_slide(self.BlankPage)
		shapes = slide.shapes[0]
		shapes.text = '目录'
		shapes = slide.shapes[1]
		shapes.text = ReportContents

#模型描述1
	def BlankPageCreate(self,haeding,subheading,Paragraphs = [],Pictures = []):
		slide = self.prs.slides.add_slide(self.ContentPage)
		shapes = slide.shapes[0]
		shapes.text = haeding
		shapes = slide.shapes[1]
		shapes.text = subheading
		tf = shapes.text_frame
		try:
			print (u'本页含有 %d 段文字！' %(len(Paragraphs)))
			for i in range(len(Paragraphs)):
				p = tf.add_paragraph()
				p.text = Paragraphs[i]
				p.level = 1
		except:
			print (u'文字输入个故事有误！')

		try:
			print (u'本页含有 %d 图片！' %(len(Pictures)))
			for i in range(len(Pictures)):
				slide.shapes.add_picture(self.case_path + Pictures[i][0],Pictures[i][1],Pictures[i][2],Pictures[i][3],Pictures[i][4])
		except:
			print (u'图片输入格式有误！')

#模型描述2
	def TablePageCreate(self,heading,subheading,TableValue,Pictures=[]):
		rows = len(TableValue);cols = len(TableValue[0])
		slide = self.prs.slides.add_slide(self.TablePage)
		shapes = slide.shapes[0]
		shapes.text = heading
		shapes = slide.shapes[1]
		shapes.text = subheading

		shapes = slide.shapesp[2]
		MatTable = shapes.insert_table(row,cols).table 
		MatTable,first_row = False
		#Set column widths
		MatTable.columns[0].width = Inches(2.0)
		#Write column heading
		for i in range(rows):
			for j in range(cols):
				MatTable.cell(i,j).fill.background()
				MatTable.cell(i,j).text = TableValue[i][j]
		try:
			print (u'本页含有 %d 图片！' %(len(Pictures)))
			for i in range(len(Pictures)):
				slide.shapes.add_picture(self.case_path + Pictures[i][0],Pictures[i][1],Pictures[i][2],Pictures[i][3],Pictures[i][4])
		except:
			print(u'图片输入格式有误！')

	def PPTCreate(self,AnalysisType)：
		self.prs.save(self.case_path + AnalysisType)

if __name__ == '__main__':
	Title = u'SC00白车身扭转刚度\分析报告（焊接工艺变更）'
	Company = u'**汽车有限公司'
	Analysis = u'强度耐久'
	Author = u'王予津'
	Date = '2017.10.17'
	Software = 'MD_NASTRAN2010'
	ReportContentsList = ['一.模型描述',' 二.计算结果','三.分析结论']
	AnalysisContent = '本报告'
	AnalysisConclusion = 'BIP模型的扭转刚度达到10000'
	ReportContents = '\n'.join(ReportContentsList)
	case_path = r'\n'
	data_path = r'\n'
	muban_path = r'\n'
	

	A = StiffPPT(muban_path,case_path)
	#封面
	A.CoverPageCreate(Title,Company)
	#目录页
	A.SummaryPageCreate(Title=Title,Analysis=Analysis,Software=Software,Author=Author,Date=Date,AnalysisContent=AnalysisContent,AnalysisConclusion=AnalysisConclusion)
	#概要页
	A.ContentsPageCreate(ReportContents)
	#模型描述页
	Paragraphs = [u'12',u'32',u'312']
	Pictures = ['/car.png',Cm(2.4),Cm(8),Cm(16),Cm(12)]
	A.BlankPageCreate(ReportContentsList[0],'有限元模型信息',paragraphs,Pictures=Pictures)
	#材料页
	TableValue = [[' ','弹性模量\n（MPa）','泊松比','密度\n(Ton/mm^3'],['1','弹性模量\n（MPa）','泊松比','密度\n(Ton/mm^3']]
	A.TablePageCreate(ReportContentsList[0],'材料模型',TableValue)
	#分析结果页
	Pictures = [['/bend.png',Cm(2.4),Cm(8),Cm(16),Cm(12)],['/torq.png',Cm(2.4),Cm(8),Cm(16),Cm(12)]]
	A.BlankPageCreate(ReportContentsList[1],'扭转刚度',Pictures=Pictures)
	#总结页
	paragraphs = ['BIP模型的扭转刚度']
	A.BlankPageCreate(ReportContentsList[2],'经过计算，结果如下：',paragraphs)
	A.PPTCreate
