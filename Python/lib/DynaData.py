# -*- coding: utf-8
'''
Created on %(date)
@author:Yujin Wang
'''
import time
from funmodule import *
import Copyright
import numpy as np,pandas as pd 
from operator import itemgetter,attrgetter
from scipy import signal
from Post import *


class basic():
	'''This is the base class for for the module'''
	try:
		def __init__(self,src,des,flag1,flag2,flag3):
			self.src = src
			self.des = des
			self.flag1 = flag1
			self.flag2 = flag2
			self.flag3 = flag3
			self.time = time.strftime('%y-%m-%d %H:%M:%S',time.localtime(time.time()))
	except:
		print ("Some arguments don't be inputted! Please! LOL!")

class nodout_SMP(basic):
	'''This class is used 4 share memory process!'''
	@property
	def simply(self):
		self.data1 = []
		self.data2 = []
		for line in open(self.src):
			if ('time' in line):
				timestep = float(line[105:116])
			elif (len(line) == 155):
				string1 = []
				string1.append(timestep)
				string1.append(int(line[:10]))
				for i in range(12):
					string1.append(float(line[(11+i*12):(22+i*12)]))
				self.data1.append(string1)
			elif (len(line)==119 and 'n' not in line):
				string2 = []
				for i in range(3):
					string2.append(float(line[(11+i*12):(22+i*12)]))
				self.data2.append(string2)
		res1 = pd.DataFrame(self.data1,columns=['Xcor','Node','x-disp','y-disp','z-disp','x-vel','y-vel','z-vel','x-accl','y-accl','z-accl','xc','yc','zc'])
		res2 = pd.DataFrame(self.data2,columns=['x-rot','y-rot','z-rot'])
		res.merge(res1,res2,left_index=True,right_index=True)
		return res

class nodout_MPP(basic):

	'''This class is used 4 share memory process!'''
	@property
	def simply(self):
		self.data1 = []
		self.data2 = []
		for line in open(self.src):
			if ('time' in line):
				timestep = float(line[104:116])
			elif (len(line) == 155):
				string1 = []
				string1.append(timestep)
				string1.append(int(line[:10]))
				for i in range(12):
					string1.append(float(line[(10+i*12):(22+i*12)]))
				self.data1.append(string1)
			elif (len(line)==119 and 'n' not in line):
				string2 = []
				for i in range(3):
					string2.append(float(line[(10+i*12):(22+i*12)]))
				self.data2.append(string2)
		res1 = pd.DataFrame(self.data1,columns=['Xcor','Node','x-disp','y-disp','z-disp','x-vel','y-vel','z-vel','x-accl','y-accl','z-accl','xc','yc','zc'])
		res2 = pd.DataFrame(self.data2,columns=['x-rot','y-rot','z-rot'])
		res.merge(res1,res2,left_index=True,right_index=True)
		return res

	class Rep4FRB(basic):
		'''It is used to achieve the FRB results from nodal file'''
		def Rep4Dis(self):
			'''It is used to calculate the node displacement in tracking system'''
			scalename = self.flag1
			list1 = self.flag2
			refnum = self.flag3
			data1 = self.src
			reld = []
			for nodenum in list1:
				title = str(nodenum) + scalename
				inputdata = plotdata(data1,nodenum,scalename)
				if scalename in ['x-disp','y-disp','z-disp']:
					inputdata.iloc[:,1] = rel_disp(data1,nodenum,refnum)
				figure = plot(title,'Time','Disp','k',1,1,'111',inputdata)
				reld.append([nodenum,figure.reldis()[0],figure.reldis()[1]])#plot
				res = pd.DataFrame(reld,columns=[scalename,'Max','Min'])
			max_y = max(res['MAX'])#Find the maximum value
			max_xid = res['MAX'].idmax()
			max_x = res[scalename][max_xid]
			node_maxdis = reld
			reld = []
			plt.clf()
			title = str(max_x) + scalename
			inpoutdata.iloc[:,1] = rel_disp(data1,max_x,refnum)
			figure = plot(title,u'时间/s',u'侵入量/mm','k',1,1,'111',inputdata)
			reld.append([max_x,figure.reldis()[0],figure.reldis()[1]])
			string = 'Max rel_Disp:\n %10.2f	@	%10d\n' %(max_y,max_x)
			plt.savefig('Displacement figure.png',dpi=1000)
			return string,node_maxdis

	def Rep4Accl(self,accllist,period):
		'''It is used to calculate the node accelerating'''
		data1 = self.src
		res = []
		corr = {}
		for node in accllist:
			Res = plotdata(data1,node,'x-accl')
			Res.iloc[:,1] = list(cfc60(np.array(Res['x-accl']/9810.)))
			figure = plot(u'Acceleration',u'Time/s','ACC/g',u'b',1,2,'111',Res)
			res.append(figure.accl(period))
			corr[node] = Res.iloc[:,1]
		string = 'B pillar acceleration:	%10.2f\t@%10.3f\n :%10.2f\t@%10.3f\n' %(res[0][0],res[0][1],res[1][0],res[1][1])
		return string,corr

	def Rep4Corr(self,basefile,casedata,list1,scalename,period):
		'''It is used to calculate the correlation coefficient'''
		data = nodout_MPP(basefile,'',0,0,0)
		data = data.simply
		string = ''
		for nodenum in list1:
			basedata = plotdata(data,nodenum,scalename)
			basedata.iloc[:,1] = list(cfc60(np.array(basedata['x-accl']/9810.)))
			figure = plot(u'Acceleration',u'Time/s',u'ACC/g',u'b',1,2,'111',basedata)
			corr = round(np.corrcoef(casedata[nodenum],basedata.iloc[:,1][:len(casedata[nodenum])])[0][1],2)
			string += 'Correlation Coefficient(Base data) @%-8d:%5.2f\n' %(nodenum,corr)
		plt.legend('C1006','C1007','B1006','B1007').loc = 'best'
		plt.savefig('Acceleration figure.png',dpi=1000)
		return string

	def report(self,*args):
		'''The FRB report will be generated!'''
		print (len(args))
		print (self.statement)
		string1,node_maxdis = self.Rep4Dis()
		string2,corr = self.Rep4Accl([1006,1007],1,1)
		string3 = 'Correlation Coefficient(B-Pillar);\t'+str(round(np.corrcoef(corr[1006],corr[1007])[0][1],2)) + '\n'
		string4 = 'Compared files:\n'
		if len(args) > 0:
			for i in args:
				string4 += i + '\n'
				temp = self.Rep4Corr(i,corr,[1006,1007],'x-accl,1100')
				string4 += temp
		fout = open(self.des,'w')
		print (string1,string2,string3,string4)
		fout.write(string1+string2+string3+string4)
		fout.close()
		plt.show()
		return node_maxdis

def plotdata(inputdata,nodenum,dataloc):
	'''Extract the data used for plotting from the database'''
	return inputdata[inputdata['Node'],isin([nodenum])].loc[:,['Xcor',dataloc]]

def cfc60(data):
	'''This is a filter function used 4 handling the accelaration, which is a butterworth filter. Please refer to SAE J211-2003'''
	b,a = signal.butter(4,0.0278,'lowpass')
	return signal.filtfilt(b,a,data)

def cfc180(data):
	'''This is a filter function used 4 handling the accelaration, which is a butterworth filter. Please refer to SAE J211-2003'''
	b,a = signal.butter(4,0.075,'lowpass')
	return signal.filtfilt(b,a,data)

def rel_disp(data,nodenum,ref):
	'''This function is used to achieve the relative displacement in the user-defined system or a node'''
	A = np.array(data[data['Node'].isin([nodenum])].iloc[:,['xc','yc','zc']])
	O = np.array(data[data['Node'].isin([ref['O']])].iloc[:,['xc','yc','zc']])
	X = np.array(data[data['Node'].isin([ref['X']])].iloc[:,['xc','yc','zc']])
	'''预留侧碰
	Y = np.array(data[data['Node'].isin([ref['Y']])].iloc[:,['xc','yc','zc']])
	'''
	OX_mode = [sum([(X[j][i] - O[j][i])**2 for i in range(3)])**0.5 for j in range(len(x))]
	tracking_system_disX = [np.vdot(np.subtract(A[i],O[i]),np.subtract(X[i],O[i]))/OX_mode[i] for i in range(len(A))]
	tracking_system_disX = cfc180([abs(tracking_system_disX[i]-tracking_system_disX[0]) for i in range(len(tracking_system_disX))])
	return tracking_system_disX

def rep_diff(data1,data2):
	'''This function is used to print the relation between two datas'''
	x1,y1 = maxdata(data1)
	x2,y2 = maxdata(data2)
	d1 = data1.loc[:,data1.columns[1]]
	d2 = data2.loc[:,data2.columns[1]]
	data_corr = d1.corr(d2)
	if x2*0.95<x1<x2*1.05:
		print ('#'*80)
		print ('The MAX Diffenrence : %10.5f g@ %10.5f s%(10.5f s)' %(abs(y1-y2),x1,x2))
		print ('#'*80)

def maxdata(data):
	'''Find the maximum value and location'''
	max_y = max(data.loc[:,data.columns[1]])
	max_xcor = data.loc[:,data.columns[1]].idmax()
	max_x = data.loc[:,data.columns[0]][max_xcor]
	return max_x,max_y

class Dyna_extr(basic):
	@property
	def subs(self):
		'''self.src = read a modified file(csv)
			self.flag1 = write a updata mainfile(Dyna)
			self.flag2 = write a updata materialfile(Dyna)
		'''
		print self.statement
		isStart = 0
		fout1 = open('New_'+self.flag1,'w')
		fout2 = open('New_' + self.flag2,'w')
		part = pd.read_csv(self.src)
		partlist = list(part.iloc[:,0])
		for line in open(self.flag1):
			if '*PART\n' in line:
				fout1.write(line)
				isStart = 1
			elif isStart == 1 and line[:10].strip().isdigit():
				if int(line[:10]) not in partlist:
					fout1.write(line)
				else:
					pos = part[part.iloc[:,0] == int(line[:10])].iloc[0,:]
					partnum = pos[0]
					matnum = pos[2]
					secnum = pos[3]
					if self.flag3 == 'Unknown':
						string = '%10d%10d%10d\n' %(partnum,secnum,matnum)
					else:
						string = '%10d%10d' %(partnum,secnum)
					fout1.write(string+line[:20])
			elif '*' in line and 'PART' not in line:
				fout1.write(line)
				isStart = 0
			else:
				fout1.write(line)
		fout1.close()
		isStart = 1
		for line in open(self.flag2):
			if isStart == 1 and '*SECTION_SHELL_TITLE' in line:
				isStart = 0
				for i in range(len(part)):
					pos = part.iloc[i,:]
					partname = pos[1]
					secnum = pos[3]
					thick = pos[4]
					fout2.write('*SECTION_SHELL_TITLE\n')
					fout2.write(partname + '\n')
					fout2.write('$#	secid	elform	shrf	nip	propt	qr/irid	icomp	setyp\n')
					fout2.write('%10d	2	0.83333	3	0	0	0	0\n' %secnum)
					fout2.write('$#	t1	t2	t3	t4	nloc	marea	idof	edgset\n')
					fout2.write('%10f%10f%10f%10f	0.00	0.00	1.000000	0\n' %(thick,thick,thick,thick))
					fout2.write('*SECTION_SHELL_TITLE\n')
			else:
				fout2.write(line)
		fout2.close()
		data = [[part.iloc[i,5],part.iloc[i,4]] for i in range(len(part))]
		return data
		
		
class Deforce(basic): 
	@property
	def  run(self):
		time = []
		spr_dam = []
		xf = []
		yf = []
		zf = []
		rf = []
		lenchange = []
		current_time   = 0
		for line in open(self.src):
			data = string_split(line[:-1],' ')
			try:
				value = eval(data[-1])
			except:
				continue
			if 'time'  in line :
				current_time = value 
			elif 'spring' in line:
				time .append(current_time)
				spr_dam.append(int(value))
			elif 'x-force' in line:
				xf.append(value )
			elif 'y-force' in line:
				yf.append(value )
			elif 'z-force' in line:
				zf.append(value )
			elif 'resultant force' in line:
				rf.append(value )	
			elif 'change in length' in line:
				lenchange .append(value )
			else:
				pass
		res = pd.DataFrame([time,spr_dam,xf,yf,zf,rf,lenchange],index=['Time','spr_dam','xf','yf','zf','rf','lenchange'])
		return res
		
class Glstate(basic): 
	@property
	def  run(self):
		time = []
		total_data = []
		time_data = []
		index = []
		index_flag = 0
		for line in open(self.src):
			if len(line) == 47:
				line_data = string_split(line[:-1], ' ')
				if 'time..' in line and len(time_data) > 1:
					total_data.append(time_data)
					index_flag = 1
					time_data = []

				if index_flag == 0:
					par_name = string_split(line[:-1], '.')
					index.append(par_name[0].strip())

				time_data.append(eval(line_data[-1]))

		return pd.DataFrame(total_data,columns=index)
		
@try_except
def dynaMatCurvePlot(KeyFile,Pid,filepath,Scale):
	#Index the mid
	PartIDPar = []
	for i in KeyFile.PART:
		try:
			if int(i[0]) in Pid:
				PartIDPar.append(i[1].split('&')[1])
		except:
			pass

	MatID = []
	for i in KeyFile.PARAMETER:
		try:
			if i[1] in PartIDPar:
				if i[2] not in MatID:
					MatID.append( i[2])
		except:
			pass

	CurveID = []
	for mat in MatID:
		for i,j in enumerate(KeyFile.MAT_PIECEWISE_LINEAR_PLASTICITY_TITLE):
			if mat == j[0]:
				CurveID.append(KeyFile.MAT_PIECEWISE_LINEAR_PLASTICITY_TITLE[i+1][2].strip())
			
	CurveStart = 0
	print '#'*20
	for k,l in enumerate(CurveID):
		Curve = []
		for i,j in enumerate(KeyFile.DEFINE_CURVE_TITLE):
			if  j[0] == l:
				CurveStart = 1
			elif CurveStart == 1 and len(j)==2:
				Curve.append([ float(j[0]),float(j[1])/Scale])
			elif len(j)!=2:
				CurveStart = 0
		figpos = int('1'+str(len(CurveID))+str(k+1))

		curveplot = CurvePlot('Mat ID:%s' %(l),'Effective plastic strain','Effective stress(GPa)',-1,1,figpos ,0.3,pd.DataFrame(Curve))
		curveplot.frame
		print 'Material ID: %s is Ploted! Curve ID: %s' %(MatID[k],l)
	pic = filepath +'\\stress_strain.png'
	plt.savefig(pic,dpi=100)
	print '#'*20	
	return CurveID
		
		
if __name__ == '__main__':
	PATH = r'Y:\cal\01_Comp\04_SB\000_allen\test\f1'
	FILE = '\glstat'
	# TestFile =Deforce(PATH+FILE,0,0,0,0)
	TestFile =Glstate(PATH+FILE,0,0,0,0)
	res = TestFile.run
