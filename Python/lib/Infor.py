# -*- coding: utf-8
'''
Created on %(date)
@author:Yujin Wang
This is used to parse the info. of FEM
'''
import os
import time
import datetime
import Copyright
import sqlite3
import numpy as np,pandas as pd
from funmodule import *
from Post import *

@try_except
@exeTime
def ReadKeys(wkdir):
	MainFile = FindFile(wkdir , '*.key')[0]
	print '#'*20
	print 'Key files:','\n'.join(MainFile)
	print '#'*20
	isMoreFiles = 0
	for  i in MainFile:
		temp = DynaInfo(i)
		temp.Pars
		if isMoreFiles >0:
			KeyFile.__dict__.update(temp.__dict__)
		else:
			KeyFile = temp
			isMoreFiles+=1
	return KeyFile

@try_except
def FindFile(start, name):
	#Find the files whose name string contains str(name), and the directory of files
	isFlag = 0
	if  '*' in name:
		name = name.strip('*')
		isFlag =1
	relpath =[]
	files_set = []
	dirs = []
	dirs_set = []

	if isFlag == 0:
		for relpath, dirs, files in os.walk(start):
			for i in files:
				if name in i:
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

class basic():
	def __init__(self,*vars,**kwargs):
		try:
			self.src = vars[0]
		except:
			pass

		# self.time = time.strftime('%y-%m-%d %H:%M:%S',time,localtime(time.time()))

class DynaInfo(basic):

	@property
	@try_except
	def Pars(self):
	
		ParsFlag = 0
		for line in open(self.src):
			try:#
				data = string_split(line[:-1],' ')
				if '*' in line and line.strip()[0] != '$' :
					if data[0][1:] not in dir(self):
						keyword = 'self.' + data[0][1:]
						cmd = keyword + '=[]'
						exec(cmd)
					else:
						keyword = 'self.' + data[0][1:]
					if  'ELEMENT_'  in line:
						ParsFlag = 1
						delta = 8
						continue
					elif 'MAT_'  in line:
						ParsFlag = 1
						delta = 10
						continue
					else:
						ParsFlag = 0
					
				elif(line[0] != '$' and '*' not in line and ParsFlag == 0):
						cmd = keyword + '.append(data)'
						exec (cmd)	
				elif (line[0] != '$' and '*' not in line and ParsFlag ==1):
						try:
							data = [int(line[0+delta*i:delta+delta*i]) for i in range(len(line[:-1])/delta)]
						except:
							# print 'WARNNING:',line
							data = [line[0+delta*i:delta+delta*i].strip() for i in range(len(line[:-1])/delta)]
						cmd = keyword + '.append(data)'
						exec (cmd)	
			
			except:
				print 'ERROR:',line
				
	@statement
	def InfoPrint(self,keywords):
		for kw in keywords:
			# strName = 'TestFile.' + kw
			print kw
			cmd =  'print " ".join(' + 'self.' + kw+ ')'
			exec (cmd)
			print "*"*80+'\n'
		 
class OptistructInfo(basic):

	@property
	def ParsFEM(self):
		isDuplicate = 0
		for line in open(self.src):
			if '$' not in line:
				if ',' in line :
					data = string_split(line[:-1],',')
				else:
					data = string_split(line[:-1],' ')

			else:
				continue
			keyword = 'self.' + data[0]
			if data[0] in dir(self):
				isDuplicate = 1
			else:
				isDuplicate = 0
				cmd = keyword + '=[]'
				print cmd
				exec(cmd)
			
			if isDuplicate == 1:
					ent = '\n'
					cmd = keyword + ".extend([ent])"
					exec (cmd)
					cmd = keyword + '.extend(data[1:])'
					exec (cmd)
					isDuplicate = 0
			else:
				exec (keyword + '.extend(data[1:])')
				
	@statement
	def ParsPCH(self,keyword,isdbfile=0):
		'''
		keyword: str, punch file keyword
		sidbfile: 0 or 1,output .db file
		'''
		self.res = []
		res_G = {}
		isKeyword = 1
		res_title = ''
		grid_num = '99999999999'
		keyword_num = 1
		finp = open(self.src,'rb')

		c1 = 1. - 2.*0.05*0.05 
		c2 = 4*0.05*0.05*(0.05*0.05 - 1)
		if isdbfile == 1:
			conn = sqlite3.connect(self.src+".db")
			conn.execute("create table if not exists rst(id integer primary key not null, Node not null, x real,y real,z real)")
		
		for line in open(self.src,'rb'):
			data = string_split(line[:-1],' ')
		
			'''
			print  'finp.readline()'
			while True:
				line = finp.readline()
				if not line :
					break
				data = string_split(line[:-1],' ')
			'''
			'''
			print  'lines = finp.readlines()'
			lines = finp.readlines()
			for line in lines:
			data = string_split(line[:-1],' ')
			'''
		# while True:
				# line = finp.readline()
				# if not line :
					# break
				# data = string_split(line[:-1],' ')
				
			if '$' in line and isKeyword==1:# check keyword
				if keyword in line :
					Freq = np.sqrt(float(data[2]))/2/np.pi
					listVector = []
			elif '$' in line and isKeyword==0:
				isKeyword = 1 
				MaxVector = max(listVector)
				PHI = MaxVector /1.25
				if PHI > 0.1248:
					AllowableTestFreq_n = Freq*(np.sqrt(c1 -  np.sqrt(c2+ PHI *PHI))) 
				else:
					AllowableTestFreq_n  = 9999999
				cmd = 'self.res.append([keyword_num,Freq,MaxVector,AllowableTestFreq_n])'

				exec(cmd)
				keyword_num += 1
				
			else:
				isKeyword = 0 
				if len(data) > 0:
					if 'CONT' not in line :
						grid_num = data[0]
						temp = [float(i) for i in data[2:] ]
						res_G[grid_num] = disp_mag(temp)
						listVector.extend(temp)
						if isdbfile == 1:
							# Creat .db file with sqlite3
							dbcommand = "INSERT INTO rst (Node,x,y,z) VALUES (%i,%f,%f,%f)" %(int(grid_num),temp[0],temp[1],temp[2])
							conn.execute(dbcommand);
							
		if isdbfile == 1:
			conn.commit()
			conn.close()
			
		cmd = 'self.res.append([keyword_num,Freq,MaxVector,AllowableTestFreq_n])'
		exec(cmd)
 
if __name__ == '__main__':   
	# # test for frequency
	# starttime = datetime.datetime.now()
	# print starttime
	# PATH = r'C:\temp\bigdata'
	# FILE = '\ESR.pch'
	# TestFile = OptistructInfo(PATH+FILE)

	# TestFile.ParsPCH('EIGENVALUE',0)
	# endtime = datetime.datetime.now()
	# print endtime

	# print (endtime - starttime)
	
	# PltData = pd.DataFrame(TestFile.res,columns = ['Order','Frequence','maxVector','AllowableTestFrequence'])
	# res_plot = CurvePlot(' ','Order','maxVector','r',1,1,111,PltData[ ['Order','maxVector']])
	# res_plot.frame
	# res_plot.maxmin()
	# # pic = PATH+FILE
	# plt.show()
	# # plt.savefig(pic,dpi=100)
	# print 'The allowable test frequence: %f Hz.' %(min(PltData.AllowableTestFrequence))
	# # test for file find
	GeomFile =  DynaInfo('Y:\\cal\\01_Comp\\04_SB\\000_allen\\test\\F1\\Geometry.key')
	GeomFile.Pars
	
