#Define the post program path
rundir = r"Y:\doc\08_Personal\Yujin\0508\YokingPy"
# rundir = r"C:\Users\yujin.wang\Desktop\LocalPy"
#Define the python path
pydir = r'Y:\doc\11_Script\Python27\python.exe'
# pydir = 'python'


import sys
import os
sys.path.append(rundir+"\\lib")
from Infor import *


@ exeTime
def main():
	try:
		wkdir = sys.argv[1]

	except:
		wkdir = r'Y:\cal\01_Comp\09_NVH\000_Anne\test\02_run'
		
	os.system( "copy %s\\SessionFiles\\session.mvw %s" %(rundir,wkdir))
	#make image directory
	imagedir = wkdir +'\\image'
	if not os.path.exists(imagedir):
		os.mkdir(imagedir)

	#Export pictures
	os.system("%s %s\\PABSession.py %s %s" %(pydir,rundir,rundir,wkdir))

	# Create PPT
	os.system("%s %s\\PABPPT.py %s %s" %(pydir,rundir,rundir,wkdir))
if __name__ == "__main__":
	main()
	# raw_input("PAUSE")