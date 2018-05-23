import sys
import os
# from Infor import *

#Define the post program path
rundir = r"Y:\doc\08_Personal\Yujin\0508\YokingPy"
#Define the python path
pydir = r'Y:\doc\11_Script\Python27\python.exe'


try:
	wkdir = sys.argv[1]

except:
	wkdir = r'Y:\cal\01_Comp\09_NVH\395_180507_ESR-038350_GDP_IC_Inflator_Bracket_fatigue_Anne\02_run_Bracket_2\33_3Hz'
	
os.system( "copy %s\\SessionFiles\\session.mvw %s" %(rundir,wkdir))
#make image directory
imagedir = wkdir +'\\image'
if not os.path.exists(imagedir):
	os.mkdir(imagedir)

#Export pictures
os.system("%s %s\\PABSession.py %s %s" %(pydir,rundir,rundir,wkdir))

# Create PPT
os.system("%s %s\\PABPPT.py %s %s" %(pydir,rundir,rundir,wkdir))
