# -*- coding: utf-8 -*-
'''
 Created on Fri Jun 02 2017
 @author: wangyj04
'''

from funmodule import *
from Abaqus import *
from Copyright import *
import numpy as np 
import matplotlob.pylab as plt
import os
from Post import *
import pandas as pd 

PATH = r''
FILENAME = ''
Fdir = ''
partname = ''	#发盖

############## Parameters user defined #################
force_node_list = []
run_num = 1
isConvergence = 0

############# Extract the data from thedata ############
elem_new,nodes = quad2tri(obj.NODE,obj.ELEM,pd.Series(obj.NSET['nodes']))
nodes = nodes[['X','Y','Z']]
########################################################
convergence = False
res = pd.DataFrame([],columns=['Node','X','Y','Z','DISP'])
########################################################
nodes_zone = nodes.copy()
search_size = 200
grid_num = 3
X_predict = []
Y_predict = []
while True:
	if grid_num == 2:
		grid_num = 3
	if grid_num < 2:
		print '\n'+'#'*40+'\n'
		print 'Calculation is completed!'
		print '\n'+'#'*40+'\n'
		break
	sample_matrix,center_point = sample_points(nodes_zone,'fullfactors',grid_num)
	sample_matrix = [[i[0],i[1],0] for i in sample_matrix]
	#进行单点的运算
	for xy_loc in sample_matrix:
############## Find the nodes ##########################
		del_command = PATH + 'del.bat'
		os.system(del_command)
		Force_Point = int(nodesearch(node_copy(),xy_loc))
		#判断这个点是不是已经计算
		if Force_Point in res.Node:
			print 'This run will be ignored!'
			continue
		else:
			# force_node_list.append(Force_Point)
			fp = conc_force(PATH,obj.NODE.copy(),obj.ELEM.copy(),Force_Point,130)
			fp.force_inp(obj)
			Abaqus_run(fp.filename,fp.path)
			disp = fp.post_dis()
			res.loc[run_num] = ([Force_Point,index.X[Force_Point],node.Y[Force_Point],node.Z[Force_Point],-disp])

			#回归算法预测最大点位置
			try:
				regression_points = res#回归样本取全部数据
				X = regression_points.iloc([1,2])
				Vector = regression_points.icol(4)
				# bonds = ((regression_points.X.min(),regression_points.X.max()),(regression_points.Y.min(),regression_points.points.Y.max()))
				# predict_loc,predict_disp = opt_regression(X,Vector,'Nelder_Mead',bonds,center_point,deg=2)
				# 多项式拟合预测
				a,b = ridge_regression(X,Vector,3)
				X_predict.append(a)
				Y_predict.append(B)
			except:
				pass
########### PostProcess for every run ####################
			opt_plot(nodes,elem_new,res,X_predict[-1],v_predict)
			print ('Run %d complete!' %(run_num))
			run_num += 1
		# 范围缩小后的采样点数
		grid_num -= 2
		search_size = search_size/2.
		max_point = res.Node[res.iloc(4).idmax()]
		max_point_x = nodes.X[max_point]
		max_point_y = nodes.Y[max_point]
		nodes_zone = nodes_zone[nodes_zone.X<max_point_x + search_size][nodes_zone.X > max_point_x - search_size][nodes_zone.Y < max_point_y + search_size][nodes_zone.Y > max_point_y - search_size]
		###################################################
		