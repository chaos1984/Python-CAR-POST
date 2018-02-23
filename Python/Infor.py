# -*- coding: utf-8
'''
Created on %(date)
@author:Yujin Wang
'''
import time
import Copyright
import numpy as np,pandas as pd
from funmodule import *
import datetime
from Post import *


class basic():
	def __init__(self,*vars,**kwargs):
		try:
			self.src = vars[0]
		except:
			pass

		# self.time = time.strftime('%y-%m-%d %H:%M:%S',time,localtime(time.time()))

class DynaInfo(basic):

	@property
	def Pars(self):
		isDuplicate = 0
		for line in open(self.src):
			data = string_split(line[:-1],' ')
			if '*' in line :
				keyword = 'self.' + data[0][1:]
				if data[0][1:] in dir(self):
					# print 'Duplicate'
					isDuplicate = 1
				else:
					isDuplicate = 0
					cmd = keyword + '=[]'
					exec(cmd)
				# continue
			elif('$' not in line and '*' not in line):
				if isDuplicate == 1:
					ent = '\n'
					cmd = keyword + ".extend([ent])"
					exec (cmd)
					cmd = keyword + '.extend(line)'
					exec (cmd)
					isDuplicate = 0
				else:
					exec (keyword + '.extend(line)')
			else:
				pass
				
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
	def ParsPCH(self,keyword):
		self.res = []
		res_G = {}
		isKeyword = 1
		res_title = ''
		grid_num = '99999999999'
		keyword_num = 1
		finp = open(self.src,'rb')
		# for chunk in read_in_chunks(PATH+FILE):
			# for line in chunk: #Loop file
		c1 = 1. - 2.*0.05*0.05 
		c2 = 4*0.05*0.05*(0.05*0.05 - 1)
		# print "for line in open(self.src,'rb')"
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
				
			elif '$' in line and isKeyword==0:
				isKeyword = 1 
				MaxVector = max(res_G.values())
				PHI = MaxVector /1.25
				if PHI > 0.1248:
					AlloTestFreq_n = Freq*(np.sqrt(c1 -  np.sqrt(c2+ PHI *PHI))) 
				else:
					AlloTestFreq_n  = 9999999
				cmd = 'self.res.append([keyword_num,Freq,MaxVector,AlloTestFreq_n])'
				# print res_G
				# print max(res_G.values)
				exec(cmd)
				keyword_num += 1
				# print res[res_title]
				# print  pd.DataFrame(res)
				# self.res = pd.concat([self.res,pd.DataFrame(res)],axis=0)

			else:
				isKeyword = 0 
				if len(data) > 0:
					if 'CONT' not in line :
						grid_num = data[0]
						# try:
						res_G[grid_num]=disp_mag( [float(i) for i in data[2:] ])
						# except:
							# print res_G
							# print data
							
							# break
					# else:
						# res_G[grid_num].extend([float(i) for i in data[1:] ])
				# else:
					# print [float(i) for i in data[2:] ]
					# print line 
		
		cmd = 'self.res.append([keyword_num,Freq,MaxVector,AlloTestFreq_n])'
		exec(cmd)
		# self.res = pd.concat([self.res,pd.DataFrame(res)],axis=0)
		# self.res.index = ['subcase'+str(i+1)+ '_'+str(j+1) for i in range(len(res.keys())) for j in range(len(res_G[grid_num]))]
		


##Test k file for dyna
# if __name__ == '__main__':
	# PATH = r'C:\github\Nastran-master\test/'
	# FILE = 'test.key'
	# TestFile = DynaInfo(PATH+FILE)
	# TestFile.Pars
	# # TestFile.InfoPrint(['PART','SECTION_SHELL_TITLE'])
	# print 'ok'

# # Test pch file for Optistruct   
if __name__ == '__main__':   

	starttime = datetime.datetime.now()
	print starttime
	PATH = r'C:\temp\bigdata'
	FILE = '\ESR2.pch'
	TestFile = OptistructInfo(PATH+FILE)

	TestFile.ParsPCH('EIGENVALUE')
	endtime = datetime.datetime.now()
	print endtime

	print (endtime - starttime)
	
	PltData = pd.DataFrame(TestFile.res,columns = ['Order','Frequence','maxVector','AllowableTestFrequence'])
	res_plot = CurvePlot(' ','Order','maxVector','r',1,1,111,PltData[ ['Order','maxVector']])
	res_plot.frame
	# res_plot.maxmin()
	# pic = PATH+FILE
	plt.show()
	# plt.savefig(pic,dpi=100)
	print 'The allowable test frequence: %f Hz.' %(min(PltData.AllowableTestFrequence))

	
