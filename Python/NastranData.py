#coding:utf-8
"""本程序用于Nasatran 计算白车身相关的程序代码
版本号：V1.0
编写：王予津
日期：2016年11月26日
"""

import math
import time
import pandas as pd
import numpy as np
from Copyright import *
from funmodule import *
from operator import itemgetter,attrgetter
from Post import *
from matplotlib.text import OffsetForm

class basic():
	"""docstring for basic"""
	def __init__(self, src,des,flag1,flag2,flag3,flag4=[]):
		try:
			self.src = src
			self.des = des
			self.flag1 = flag1
			self.flag2 = flag2
			self.flag3 = flag3
			self.flag4 = flag4
		except:
			print ('WARNNING: Input parameters are not enough!')

		self.time = time.strftime('%y-%m-%d %H:%M:%S',time,localtime(time.time()))
	
	def printdone(self,funname):
		print (self.time,('%s is done!' %funname))
	
	def printerror(self,funname):
		print (self.time,('ERROR: %s is empty!' %funname))
	
	def help(self):
		print ("可输入命令：")

class pshellextr(basic):
	def upround(self):
		self.data = round(10*self.data+0.49)/10
	def full(self):
		total = []
		isend = 0
		fout = open(self.des,'w')
		for line in open(self.src):
			if "PSHELL " in line:
				self.data = float(line[24:27])
				string = line[:24] + str(self.data)+line[27:]
				pshellnum = int(line[9:16])
				total.append([string,pshellnum])
			elif 'PSOLID' in line:
				if isend == 0:
					total.sort()
					for item in total:
						if item[1] ==500000:
							fout.write(item[0])
						else:
							fout.write(item[0])
					self.printdone('pshell_full')
					isend = 1
					fout.write(line)
				else:
					fout.write(line)
			else:
				fout.write(line)
		fout.close()
	def propnum(self):
		fout = open(self.des,"w")
		for line in open(self.src):
			if "PSHELL" in line:
				fout.write(line[9:16]+'\n')
		fout.close()
		self.printdone('PSHELL_PROPNUM')

class extr(basic):
	@property
	def mark_opt_bdf(self):
		'''This function is used to extra the opt variables
		src = string, read the datas from bdf
		des = string, write the datas to a file
		self.flag1 = list, reference No. of parts
		'''
		fout = open(self.des,'w')
		for line in open(self.src):
			if 'PSHELL' in line:
				if int(line[8:16]) in self.flag1:
					string = line[8:16] + ',' + line[24:31] + '\n'
					string.strip()
					fout.write(string)
		fout.close()

	@property
	def mark_opt_excel(self):
		'''This func is used to extra the opt variables
		src = string, read the datas from bdf
		des = string, write the datas to a file
		self.flag1 = list, reference No. of parts
		'''
		fout = open(self.des,'w')
		for line in open(self.src):
			if line[:7].isdigit():
				if int(line[:7]) in self.flag1:
					string = line[:-1] + ',Opt\n'
					fout.write(string)
				else:
					string = line[:-1] + ',Unopt\n'
					fout.write(string)
			else:
				fout.write(line)
		fout.close()

	@property
	@statement
	def opt_sub(self):
		finp1 = self.flag1
		finp2 = self.flag2
		fout = open(self.des,'w')
		list1 = []
		FLAG1 = 0
		if type(self.flag3) == list:
			list1 = self.flag3
		else:
			for line in open(finp1):
				if ('F I N A L A N A L Y S I S' in line):
					FLAG = 1
				if len(line)>70:
					if (line[40] == 'V' and FLAG1 == 1):
						value = round(eval(line[74:84])+0.49,1)
						list1.append([int(line[26:34]),value])
		partnum = [list1[i][0] for i in range(len(list1))]
		for line in open(finp2):
			try:
				if 'PSHELL ' in line and int(line[8:16]) in partnum:
					pos = partnum.index(int(line[8:16]))
					string = '%8f' %(list1[pos][i])
					line = line[:24] + string + line[32:]
					print line
					fout.write(line)
				else:
					fout.write(line)
			except:
				print ('ERROR:\n')
				print (line)
				fout.close()
	@property
	def opt_dereduce(self):
		ref = self.flag1
		fout1 = open(self.des,'w')
		for line in open(self.src):
			for item in ref:
				ishere = 0
				if str(item) in line:
					ishere = 1
					break
			if ishere == 0:
				fout1.write(line)


	def massextr(self):
		fout = open(self.des,'w')
		for line in open(self.src):
			if len(line) > 70:
				if (line[32] == 'X' and line[69] == 'X'):
					fout.write(line)
				if (line[34] == 'X' and line[35] == ' '):
					fout.write(line)
				if (line[34] == 'Y' and line[35] == ' '):
					fout.write(line)
				if (line[34] == 'Z' and line[69] == ' '):
					fout.write(line)

	def dispextr(self):
		FLAG1 = 0
		node_list = []
		res = {}
		SUB_NUM = 1
		for i in self.flag3:
			node_list.append(i[0])
			node_list.append(i[1])
			res[i[0]] = {}
			res[i[1]] = {}
		for i in self.flag4:
			node_list.append(i[0])
			node_list.append(i[1])
			res[i[0]] = {}
			res[i[1]] = {}
		for line  in open(self.src):
			if ('POINT ID.' in line and FLAG1 == 0):
				FLAG1 = 1
			if (FLAG1 == 1 and "  G  " in line and int(line[:14]) in node_list):
				try:
					subcase_num = max(res[int(line[:14])].keys())
					if subcase_num == SUB_NUM:
						SUB_NUM = subcase_num + 1
				except:
					pass
				res[int(line[:14])][SUB_NUM] = []
				for i in range(3):
					start = 26+ i*15
					end = 39 + i*15
					res[int(line[:14])][SUB_NUM].append(eval(line[start:end]))
		return res

	@statement
	def scm2extr(self,partname=[]):
		i = 1
		scm_list = []
		temp_list = []
		columns_list = []
		row_list = []
		hist_dict = {}
		partname_list = {}
		for line in open(self.src):
			try:
				data = string_split(line,' ')
				if ')' in data[0]:
					for j in data[1:]:
						temp_list.append(eval(j))
					flag1 = 1

				elif (data[0] == '0COLUMN' and flag1==1 or 'S U M M A R Y' in line):
					i += 1
#					flag = 0
					columns_list.append('Rep %d' %(i-1))
					scm_list.append(temp_list)
					temp_list = []
				elif len(data) >= 8 and 'V' == data[4][0] and data[4][1].isdigit():
					partnum = data[2]
					data = line[41:].split(':')
					if partnum not in hist_dict:
						row_list.append(partnum)
						hist_dict[partnum] = [partname[str(partnum)][0],partname[str(partnum)][1]]
						for i in data[:-1]:
							hist_dict[partnum].append(eval(i))
					else:
						for i in data[:-1]:
							hist_dict[partnum].append(eval(i))
			except:
				print ('ERROR:%s' %(line))
				print ('Please check the information in .f06 file.')
			try:
				scm_data = pd.DataFrame(scm_list,index=columns_list,columns=row_list)
				scm_data = scm_data.T
			except:
				pass
			hist_index = ['PART','THICKNESS']
			for i in range(len(hist_dict[hist_dict.keys()[0]])-2):
				hist_index.append('RUN %d' %(i+1))
				hist_data = pd.DataFrame(hist_dict,index=hist_index)
				hist_data=hist_data.T 
			try:
				res = pd.concat([hist_data,scm_data],axis=1)
			except:
				print ('A discrete property values are achieved with DDVAL command!')
				res = hist_data
			csv_file = self.src.replace('f06','csv')
			res.to_csv(csv_file)
			self.printdone('scm2extr')
			return res,partname_list

	def partname(self):
		fout = open(self.des,'w')
		for line in open(self.src):
			if len(line) > 40:
				if '$HMNAME PROP' in line:
					temp = line[33:-3]
					flag =1
				elif (line[4]=='L' and flag == 1):
					string = temp[:-1] + ',' + line[24:27] +'\n'
					fout.write(line[9:16]+','+string)
					flag = 0
		fout.close()

	def gridpos(self):
		try:
			node_cor = {}
			node_list = {}
			for i in self.flag3:
				node_list.append(i[0])
				node_list.append(i[1])
			for i in self.flag4:
				node_list.append(i[0])
				node_list.append(i[1])
			for line in open(self.src):
				pos = []
				if len(line) > 40:
					if("GRID" in line and int(line[8:16]) in node_list):
						for i in range(3):
							pos.append(float(line[(24+8*i):(32+8*i)]))
							node_cor[int(line[8:16])] = pos
			return node_cor
		except:
			self.printerror("gridpos")

class calc():
	time = time.strftime('%y-%m-%d %H:%M:%S',time,localtime(time.time()))
	def __init_(self,A,B,C,D):
		if (type(A) != list):
			self.A = float(A)
			self.B = float(B)
			self.C = float(C)
			self.D = float(D)
		elif(type(A) == list):
			self.A = A
			self.B = B
			self.C = C
			self.D = D
		else:
			print "WARNNING:Input is empty!"

	def bendstiff(self):
		try:
			return self.A/(abs(self.B+self.C)/2.0)
		except:
			print ('Bendstiff is wrong!')

	def torqstiff(self):
		try:
			angel = (math.atan(abs(self.B-self.C)/self.D)*180./3.141592654)
			return self.A/angel,angel
		except:
			print ('ERROR:torqstiff')

		def distance(self,direction='dist'):
			try:
				X1,Y1,Z1 = self.A
				X2,Y2,Z2 = self.B
				X1 = float(X1)
				Y1 = float(Y1)
				Z1 = float(Z1)
				X2 = float(X2)
				Y2 = float(Y2)
				Z2 = float(Z2)
				if direction == 'dist':
					return math.sqrt((X1-X2)**2+(Y1-Y2)**2+(Z1-Z2)**2),X1
				elif direction == 'X':
					return np.abs(X1-X2),X1
				elif direction == 'Y':
					return np.abs(Y1-Y2),X1
				elif direction == 'Z':
					return np.abs(Z1-Z2),X1
			except:
				print ('ERROR:distance')
				print self.A
				print self.B

	def gridavesort(self):
		sortnum = self.B
		rawdata = sorted(self.A,key=lambda s:s[0],reverse=True)
		l = len(rawdata)
		dic1 = {}
		dic2 = {}
		for i,j in rawdata:
			dic2[i] = dic2.setdefault(i,0)+1
			v1 = dic1.setdefault(i,[0]*l)
			v2 = j
			v = list(map(lambda s:s[0]+s[1],zip(v2,v1)))
			dic1[i] = v
		for i,j in dic1.items():
			dic1[i] = [k/dic2[i] for k in j]
		sortlist = sorted([list(i) for i in dic1.items()],key=lambda s:s[sortnum],reverse=True)
		finalsort = []
		for i,j in sortlist:
			finalsort.append(','.join(([str(i),','.join([str(m) for m in j])])))
			return finalsort

			def gridsort(self):
				sortnum = self.B
				rawdata = sorted(self.A,key=lambda s:s[sortnum],reverse=True)
				l = len(rawdata)
				print ('该工况下数据大小为： %d' %l)
				finalsort = []
				for i in rawdata:
					finalsort.append(i)
				return finalsort

class stiffreport(basic):
	@statement
	def init(self):
		self.file1 = extr(self.flag1,'',0,0,self.flag3,self.flag4)
		self.file2 = extr(self.flag2,'',0,0,self.flag3,self.flag4)
		print self.time
		print '输入文件1为：',str(self.flag1)
		print '输入文件2为：',str(self.flag2)

	def post(self,torq_point):
		self.init()
		reslist = []
		node_cor = self.file1.gridpos()
		node_disp = self.file2.dispextr()
		print '\n******************STIFFNESS INFORMATION***************\n'
		for i in range(len(self.flag3)):
			p1,p2 = self.flag3[i]
			print ('No. %d pair.') %(i+1)
			print ('P1 = %d\tP2 = %d') %(p1,p2)
			dis = calc(node_cor[p1],node_cor[p2],0,0)
			dis1,X1 = dis.distance(direction='Y')
			p1_z = node_disp[p1][1][2]
			p2_z = node_disp[p2][1][2]
			stif = calc(2000.,p1,p2,dis1)
			print p1_z,p2_z,dis1
			res,angel = stif.torqstiff()
			reslist.append(('Torque',p1,p2,X1,p1_z,p2_z,dis1,angel,res))
		for i in range(len(self.flag3)):
			p1,p2 = self.flag3[i]
			print ('No. %d pair.') %(i+1)
			print ('P1 = %d\tP2 = %d') %(p1,p2)
			dis = calc(node_cor[p1],node_cor[p2],0,0)
			dis1,X1 = dis.distance(direction='Y')
			p1_z = node_disp[p1][2][2]
			p2_z = node_disp[p2][2][2]
			stif = calc(6000.,p1,p2,dis1)
			print p1_z,p2_z,dis1
			res,angel = stif.bendstiff()
			reslist.append(('Bend',p1,p2,X1,p1_z,p2_z,dis1,(p1_z+p2_z)/2,res))

		restable = pd.DataFrame(reslist,columns=['Type','p1','p2','Xcor','p1_z','p2_z','distance','Ang & Dis','stiff'])
		restable.to_csv(self.des + '/report_Stiff.csv')
		print ('\n**************DOORS AND WINDOWS FORMATION***********\n')
		deformlist = []
				
		for i in range(len(self.flag4)):
			p1,p2 = self.flag4[i]
			print ('No. %d pair.') %(i+1)
			print ('P1 = %d\tP2 = %d') %(p1,p2)
			dis = calc(node_cor[p1],node_cor[p2],0,0)
			dis1,X1 = dis.distance(direction='dist')
			p1_deform = [node_cor[p1][i] + node_disp[p1][1][i] for i in range[3]]
			p2_deform = [node_cor[p2][i] + node_disp[p2][1][i] for i in range[3]]
			dis = calc(p1_deform,p2_deform,0,0)
			dis2,X2 = dis.distance(direction='dist')
			deform_length = dis2-dis1
			ratio = abs((dis2-dis1)/dis1*100)
			temp = 'Deform:%10.2f\t Ratio:%10.2f' %(deform_length,ratio)
			print temp

			deformtable = pd.DataFrame(deformlist,columns=['p1','p2','Length','Deformed_length','deform_Value','Deform_Ratio'])
			deformtable.to_csv(self.des+'/report_Deform.csv')

			torq = restable[restable.Type == 'Torque'].loc[:,['Xcor','Ang & Dis']]
			figure1 = plot(u'扭转变形',u'X向位置',u'转角(°)','k',0,1,'111',torq)
			figure1.stiff(self.des+'/torq')

			bend = restable[restable.Type == 'Bend'].loc[:,['Xcor','Ang & Dis']]
			figure1 = plot(u'弯曲变形',u'X向位置',u'Z向位移(mm)','k',0,2,'111',bend)
			figure1.stiff(self.des+'/bend')
			torq_stiff = restable.stiff[torq_point]
			bend_stiff = restable.stiff[restable.Type == 'Bend'].min()
			print ('Bending Stiffness:%10.1f \tAverage Z-displacement:%10.4f\n ') %(bend_stiff,bend['Ang & Dis'].min())
			print ('Torsinal Stiffness:%10.1f \tAverage Z-displacement:%10.4f\n ' %(torq_stiff,torq['Ang & Dis'].iloc[torq_point]))
			return [torq_stiff,bend_stiff,torq["Ang & Dis"].iloc[torq_point],bend["Ang & Dis"].min()],deformtable

class stressreport(basic):
	def run(self):
		reslist = []
		res = self.flag1
		partnum = self.flag2
		stresstype = self.flag3
		if stresstype == 1:
			stressstring = 'Maximum p1'
		else:
			stressstring = 'Maximum Von Mises'
		fnm = self.src[:-4] + "_rep" + self.src[-4:]
		fout = open(fnm,'w')
		for i in partnum:
			string  = 'Part Num:\t' + str(i) + '\t' + 'Node\t' + stressstring + '\n'
			fout.write(string)
			for j in res:
				if (str(j[0])[:3] == str(i)):
					string ='\t'*4 + str(j[0]) + '\t' + str(j[stresstype]) + '\n'
					fout.write(string)
					break
			reslist.append([str(i),str(j[stresstype])])
		fout.close()	
		return reslist

	def stress_fullreport(filename,data):
		fout = open(filename,'w')
		print len(data)
		string = 'Subcase,' + 'Part,Stress,'*len(data[0])+'\n'
		fout.write(string)
		for i,j in data:
			string1 = []
			for t in j:
				string1.append(',',join(t))
			string = str(i) + ',' + ','.join(string1) + '\n'
			fout.write(string)

	@statement
	def opt_Com2Prop(path,filename,assem_flag = '',deviation = 0):
		isFlag = 0
		OptComplist = []
		OptProplist = []
		for line in open(path+filename):
			if assem_flag in line:
				isFlag = 1
			elif isFlag == 1 and 'HMASSEM_IDS' in line:
				try:
					for i in range(8):
						OptComplist.append(line[16+i*8:24+i*8].strip())
				except:
					pass
			else:
				isFlag = 0

		fout1 = open(path + '/DESVAR.dat','w')
		fout2 = open(path + '/DVPREL1.dat','w')
		print ('优化的部件编号：\n')
		print (','.join(OptComplist))
		print ('*'*20+'\n')
		j=1
		for line in open(path+filename):
			if "HMNAME COMP" in line and '_T' in line:
				data = string_split(line,'"')
				ComID = string_split(data[0],' ')[2]
				PropID = int(data[2].strip())
				sym_id = data[1].index('_T')
				ComName = data[1]
				bench_thick = float(data[1][sym_id + 2:sym_id +5])/100
				if ComID in OptComplist:
					OptProplist.append(int(PropID))
					string_fout1 = '$%s\nDESVAR,%d,V%d,%3.2f,%3.2f,%3.2f,0.5,1\n' %(ComName,PropID,j,bench_thick,bench_thick-deviation,bench_thick+deviation)
					fout1.write(string_fout1)
					string_fout2= '$%s\nDVPREL1,%d,PSHELL,%d,T,%3.2f,%3.2f\n,%d,1.0\n' %(ComName,j,PropID,bench_thick-deviation,bench_thick+deviation,PropID)
					fout2.write(string_fout2)
					j += 1
			print ('优化部件属性编号：\n')
			print (','.join(str(i)) for i in OptProplist)
			print ('\n优化的部件数量：%d' %(len(OptProplist)))
			fout1.close()
			fout2.close()
			return OptComplist,OptProplist


