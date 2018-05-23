import sys
import os
# from Infor import *

#Define the post program path
rundir = r"C:\Users\chaos\Documents\GitHub\Python-CAR-POST\Python"
#Define the python path
pydir = r'python'


try:
	wkdir = sys.argv[1]

except:
	wkdir = r'C:\Users\chaos\Desktop\PySTIFF'
	
# os.system( "copy %s\\SessionFiles\\session.mvw %s" %(rundir,wkdir))
#make image directory
imagedir = wkdir +'\\image'
if not os.path.exists(imagedir):
	os.mkdir(imagedir)

#Export pictures
os.system("%s %s\\BiwStiffSession.py %s %s" %(pydir,rundir,rundir,wkdir))

# Creat PPT
# os.system("%s %s\\PABPPT.py %s %s" %(pydir,rundir,rundir,wkdir))
