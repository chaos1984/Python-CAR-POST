# -*- coding: utf-8
'''
Created on %(date)
@author:Yujin Wang
'''
import numpy as np,pandas as pd,matplotlib.pyplot as plt
from matplotlib.text import OffsetFrom
from funmodule import *

global color 
color = ['r','b','g','c','y','m']

class basic():
	'''This is the base class for this module'''
	def __init__(self,title,xlabel,ylabel,isall,num,figurepos,delta,data,legend = False):
		'''Created date : 201703
		Modify date : 201802
		Author: Yujin Wang 
		Title -- Figure Title
		xlabel -- x coor lable
		ylabel -- y coor lable
		color -- curve color
		isall -- max\min value plot. 0:min;1:max; 2:max and min  value
		num -- Figure No.
		figrepos -- Figure position
		data -- data ploted in the figure'''
		self.title = title
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.isall = isall
		self.num = num
		self.figurepos = figurepos
		self.delta = delta
		self.data = data 
		self.legend = legend
		

class CurvePlot(basic):
	'''This class is used for plotting and output parameters'''
	def maxmin(self,period=1e10):
		max_y,min_y = 0,0
		
		if (self.isall == 1): #max
			max_y = max(self.data[self.data.iloc[:,0]<period].iloc[:,1])

			max_xcor = self.data[self.data.iloc[:,0]<period].iloc[:,1].idxmax()
			max_x = self.data[self.data.iloc[:,0]<period].iloc[:,0][max_xcor]
			self.annot4stiff('Max:',max_x,max_y)
			return max_y,max_x,max_xcor
		elif (self.isall == 0): #min
			min_y = min(self.data[self.data.iloc[:,0] < period].iloc[:,1])
			min_xcor = self.data[self.data.iloc[:,0]<period].iloc[:,1].idxmin()
			min_x= self.data[self.data.iloc[:,0]<period].iloc[:,0][min_xcor]
			self.annot4stiff('Min:',min_x,min_y)
			return min_y,min_x,min_xcor
		elif self.isall == 2: #maxmin
			max_y = max(self.data[self.data.iloc[:,0]<period].iloc[:,1])
			max_xcor = self.data[self.data.iloc[:,0]<period].iloc[:,1].idxmax()
			max_x = self.data[self.data.iloc[:,0]<period].iloc[:,0][max_xcor]
			self.annot4stiff('Max:',self.max_x,max_y)
			min_y= min(self.data[self.data.iloc[:,0]<period].iloc[:,1])
			min_xcor = self.data[self.data.iloc[:,0]<period].iloc[:,1].idxmin()
			min_x = self.data[self.data.iloc[:,0]<period].iloc[:,0][min_xcor]
			self.annot4stiff('Min:' ,min_x, min_y)
			return max_y,max_x,max_xcor,min_y,min_x,min_xcor

	@property
	def frame(self):
		plt.figure(num = self.num)
		plt.subplot(self.figurepos)
		plt.ylabel(self.ylabel,fontproperties='Simhei')
		plt.xlabel(self.xlabel,fontproperties='Simhei')
		plt.title(self.title,fontproperties='Simhei')
		plt.grid(True)
		plt.subplots_adjust(wspace=self.delta)
		for i in range(len(self.data.columns)-1):
			plt.plot(self.data.iloc[:,0],self.data.iloc[:,i+1],color[i],lw=1,marker='')
		if self.legend != False:
			plt.legend(self.data.columns[1:])
		else:
			pass
			
	def accl(self,preiod):
		self.frame
		return self.maxmin(period)

	def stiff(self,name):
		self.frame
		self.maxmin()
		plt.savefig(name,dpi=100)

	def reldis(self):
		self.frame
		return self.maxmin()
	
	def annot4stiff(self,text,x,y):
		bbox_args = dict(boxstyle = 'round', fc='0.8')
		arrow_args = dict(arrowstyle = '->')
		Label_arg = text + str(round(y,2))+'@' + str(round(x,3))
		plt.annotate(Label_arg,
			xy=(x,y),
			xytext = (2*x/3,1.1),
			textcoords = ('data','axes fraction'),
			bbox = bbox_args,
			arrowprops = arrow_args,
			horizontalalignment = 'top')
class barplot(basic):
    '''It is used to plot the bar figure for the senstive analysis and design variables history'''
    def plot(self,lable):
        plt.figure(num=self.num)
        plt.subplot(self,figrepos)
        res_data = self.data.sort_values(by=lable,ascending = False).iloc[:20]
        plt.bar(range(len(res_data)).tuple(res_data.index),size=20,rotation = 45)
        plt.yticks(size=20)
        plt.ylabel(self.ylabel,fontproperties='Simhei',size=20)
        plt.xlabel(self.xlabel,fontproperties='Simhei',size=20)
        plt.title(self.title,fontproperties='Simhei',size=20)
        plt.grid()

    def opt_plot(nodes,elem_new,res,X_predict,v_predict):
        Force_Point = list(res.iloc(0))[-1]
        x_coor = list(res.iloc(1))
        y_coor = list(res.iloc(2))
        force_dis = list(res.iloc(4))
        plt.figure(1)
        plt.gca().set_aspect('equal')
        plt.tricontourf(nodes.X,nodes.Y,elem_new,nodes,Z,colors='y')
        plt.grid()
        plt.plot(x_coor,y_coor,marker='*')
        plt.scatter(X_predict[0],X_predict[1],color='r')
        string = 'NODE: %d\nX: %5.3f	Y:%5.3f		Z:%5.3f\n 	DIS:	%5.4E' %(Force_Point,round(x_coor[-1],2),round(y_coor[-1],2),round(force_dis[-1]))
        plt.text(x_coor[-1],y_coor[-1],string)
        plt.figure(2)
        plt.plot(force_dis)
        plt.plot(v_predict)
        plt.grid()
        plt.show()
        printtime()