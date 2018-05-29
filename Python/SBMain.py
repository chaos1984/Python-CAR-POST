
rundir = r"Y:\doc\08_Personal\Yujin\0508\YokingPy"
#Define the python path
pydir = r'Y:\doc\11_Script\Python27\python.exe'
# pydir = "python"

import sys
import os
import time
sys.path.append(rundir+"\\lib")
from Infor import *
# import Copyright



@ exeTime
def main():
	try:
		wkdir = sys.argv[1]
	except:
		wkdir = r'Y:\cal\01_Comp\04_SB\551_180507_ESR-038259_JCSB_Anchor_plate_strength_Zheng\06_Run_Anchor1_Anchor2_F1_mat550'
		# wkdir = 'Y:\\cal\\01_Comp\\04_SB\\548-180423_ESR_038131_LH_BUK_Bracket_Strength_Yujin'
		
	dirs = FindFile(wkdir, 'd3plot')[1]
	if len(dirs) == 0:
		raw_input("Error:.d3plot files are not found!")
		sys.exit()

		
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
			else:
				pass
	# Create PPT
	os.system("%s %s\\SBPPT.py %s %s" %(pydir,rundir,rundir,wkdir))
if __name__ == "__main__":
	main()
	# raw_input("PAUSE")