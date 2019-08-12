# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import FD2Mat24
A = 30; l0 = 10 #样件截面积，标距
FDfile = ["test10.txt","test100.txt","test1000.txt","test10000.txt"]#力位移曲线
strain_rate = [-6.907,-4.605,-2.302,0] #力位移曲线对应的应变率
curvenum = 2350 #key文件中曲线的编号起始编号
ratio = 1 #显示比例
#################################User Define###################################
Ymould_user = 1.5 #定义弹性模量_固定值
yieldpoint= 0.2 #屈服点（避开交叉区域）_固定值
pointnum = 80     #输出点的个数_固定值
strainturnlist=[1.2,1.2,1.2,0.75]#指定每根曲线发生转折的应变
scaleturnlist=[0.09,0.09,0.085,0.06];#指定每根曲线发生转折的比例
curvescalelist = [1,1.00,1.03,1.03]#指定每个曲线整体偏移的比例
#strainturnlist=[1.2,1.2,1.2,0.8]#指定每根曲线发生转折的应变
#scaleturnlist=[0.070,0.070,0.060,0.047];#指定每根曲线发生转折的比例
#curvescalelist = [1.05,1.05,1.05,1.09]#指定每个曲线整体偏移的比例
alignstrain =1.45#应力应变曲线对齐的位置（应变值）
extend = 0.5     #对齐后曲线延长距离（应变值）
scaleextend=0.08 #延长段的增量
smooth=1
#################################User Define###################################
FD2Mat24.CurveKey(A,l0,FDfile,strain_rate,curvenum,ratio,Ymould_user,yieldpoint,pointnum,strainturnlist,scaleturnlist,curvescalelist,alignstrain,extend,scaleextend,smooth)
