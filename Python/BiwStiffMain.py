#coding:utf-8
import sys
import os
from BiwStiffSession import *

#Define the post program path
rundir = r"C:\Users\chaos\Documents\GitHub\Python-CAR-POST\Python"
#Define the python path
pydir = r'python'
sys.path.append(rundir+"\\lib")
from Copyright import *

@exeTime
def main():
	try:
		wkdir = sys.argv[1]
	
	except:
		wkdir = 'C:\Users\chaos\Desktop\BIW_STIFFNESS_ANALYSIS_REPORT'
	imagedir = wkdir +'\\image'
	if not os.path.exists(imagedir):
		os.mkdir(imagedir)
	
	#Export pictures
#		os.system("%s %s\\BiwStiffSession.py %s %s" %(pydir,rundir,rundir,wkdir))
	result = BiwSession(rundir,wkdir)
	result = ','.join([str(round(i,2)) for i in result])
	print result

	# Creat PPT
	os.system("%s %s\\BiwStiffPPT.py %s %s %s" %(pydir,rundir,rundir,wkdir,result))

if __name__ == "__main__":
	main()

