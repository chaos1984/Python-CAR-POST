
#Define the post program path
rundir = r"Y:\doc\08_Personal\Yujin\0508\YokingPy"
#Define the python path
pydir = r'Y:\doc\11_Script\Python27\python.exe'
# pydir = "python"

import sys
import os
sys.path.append(rundir+"\\lib")
from Infor import *


try:
	wkdir = sys.argv[1]
except:
	wkdir = r'Y:\cal\01_Comp\04_SB\000_allen\test'
	# wkdir = 'Y:\\cal\\01_Comp\\04_SB\\548-180423_ESR_038131_LH_BUK_Bracket_Strength_Yujin'
	
dirs = FindFile(wkdir, 'd3plot')[1]
print '#'*20
print 'DYNA solution files directory:\n','\n'.join(dirs)
print '#'*20


for subwkdir in dirs:#direct path
	# Make image dir.
		imagedir =  subwkdir +'\\image'
		if not os.path.exists(imagedir):
			os.mkdir(imagedir)
		#Create Session file
		os.system("%s %s\\SBSession.py %s %s %s" %(pydir,rundir,subwkdir,rundir,pydir))
# Create PPT
os.system("%s %s\\SBPPT.py %s %s" %(pydir,rundir,rundir,wkdir))
