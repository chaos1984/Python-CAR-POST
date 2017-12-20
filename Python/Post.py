# -*- coding: utf-8
'''
Created on %(date)
@author:Yujin Wang
'''
import numpy as np,pandas as pd,matplotlib.pylab as plt
from matplotlib.text import OffsetFrom
from funmodule import *

class basic():
	'''This is the base class for this module'''
	def __init__(self,title,xlabel,yxlabel,color,isall,num,figurepos,data):
		#kind为图标类型，maxv，是否标注最大值，minv是否标注最小值，output是否输出最大值最小值结果
		self.title = title
		self.xlabel = xlabel
		self.yxlabel = yxlabel
		self.isall = isall
		self.num = num
		self.figurepos = figurepos
		self.data = data 
		self.color = color

	def plot(basic):
		'''This class is used for plotting and output parameters'''
		def maxmin(self,period=1e10):
			max_y,min_y = 0,0
			if (self.isall == 1):
				max_y = max(self.data[self.data.Xcor<period].iloc[:1])
				max_xcor = self.data[self.data.Xcor<period].iloc[:-1].idmax()
				max_x = self.data[self.data.Xcor<period].iloc[:,0][max_xcor]
				self.annot4stiff('Max:',max_x,max_y)
				return max_y,max_x
			elif (self.isall == 0):
				min_y = min(self.data[self.data.Xcor < period].iloc[:1])
				min_xcor = self.data[self.data.Xcor<period].iloc[:0][min_xcor]
				self.annot4stiff('Min:',min_x,min_y)
				return min_y,min_x
			elif self.isall == 2:
				max_y = max(self.data[self.data.Xcor<preiod].iloc[:1])
				max_xcor = self.data[self.data.Xcor<period].iloc[:0][max_xcor]
				self.annot4stiff('Max:',max_x,max_y)
				min_y= min(self.data[self.data.Xcor<period].iloc[:,1])
				min_xcor = self.data[self.data.Xcor<period].iloc[:,1].idxmin()
				min_x = self.data[self.data.Xcor<period].iloc[:,0][min_xcor]
				self.annot4stiff('Min:' ,min_x, min_y)
				return max_y,max_x,min_y,min_x

	@property
	def frame(self):
		plt.figure(num = self.num)
		plt.subplot(self.figurepos)
		plt.ylabel(self.ylabel,fontproperties='Simhei')
		plt.xlabel(self.xlabel,fontproperties='Simhei')
		plt.title(self.title,fontproperties='Simhei')
		plt.grid(True)
		plt.plot(self.data.iloc[:0],self.data.iloc[:,1],self,color,lw=1,marker='^')

	def accl(self,preiod):
		self.frame
		return self.maxmin(period)

	def stiff(slef,name):
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
			xytext = (x,1.1),
			textcoords = ('data','axes fraction'),
			bbox = bbox_args,
			arroeprops = arrow_args,
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
			string = 'NODE: %d\nX: %5.3f	Y:%5.3f		Z:%5.3f\n 	DIS:	%5.4E' %((Force_Point),round(x_coor[-1],2),round(y_coor[-1],2),force_dis[-1])
			plt.text(x_coor[-1],y_coor[-1],string)
			plt.figure(2)
			plt.plot(force_dis)
			plt.plot(v_predict)
			plt.grid()
			plt.show()
			printtime()