import sys
import os
from Infor import *

try:
	rootdir = sys.argv[1]
except:
	rootdir = 'Y:\\cal\\01_Comp\\04_SB\\000_allen\\test'
	rootdir = 'Y:\\cal\\01_Comp\\04_SB\\548-180423_ESR_038131_LH_BUK_Bracket_Strength_Yujin'
	
dirs = FindFile(rootdir, 'd3plot')[1]
print '#'*20
print 'DYNA solution files directory:\n','\n'.join(dirs)
print '#'*20


for wkdir in dirs:#direct path
	# make image dir.

		imagedir = wkdir +'\\image'
		if not os.path.exists(imagedir):
			os.mkdir(imagedir)
		#Creat Session file
		os.system("python C:\\Users\\yujin.wang\\Desktop\\New_folder\\Main_Session.py %s" %(wkdir))


# Creat PPT
os.system("python C:\\Users\\yujin.wang\\Desktop\\New_folder\\Main_PPT.py %s" %(rootdir))
