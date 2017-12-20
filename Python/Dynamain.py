# -*- coding: utf-8 -*-
'''
 Created on Fri Jun 02 2017
 @author: wangyj04
'''
import numpy as np,pandas as np,matplotlib.pylab as plt

from matplotlib.text import OffsetFrom
from Post import *
from DynaData import *
from NastranData import *

cmpfile = ''
data = nodout_MPP('nodout','',0,0,0)
list1 = [111,222] #输出节点
data1 = data.symply
scalename = 'x_disp'
ref = {'O':1,'Y':2,'Z':3}
f = Rep4FRB(data1,'RES.txt',scalename,list1,ref)
f.report(compfile)