#coding:utf-8
import sys
import os 

try:
	rundir = sys.argv[1]
	wkdir = sys.argv[2]
except:
	wkdir = "Y:\cal\01_Comp\09_NVH\000_Anne\test"
	rundir="Y:\doc\08_Personal\Yujin\0508\YokingPy"
sys.path.append(rundir+"\\lib")
from Infor import *
from DynaData import *
from Main_Plot import *
statement1()

os.system( "copy %s\\SessionFiles\\session.mvw %s" %(rundir ,wkdir))


#Creat Session file
ScriptFile = wkdir +'\\script.tcl'
print "ScriptFile:%s" %(ScriptFile) 
fout = open(ScriptFile,'w')
finp = open(r"%s\\SessionFiles\\script.tcl" %(rundir ),'r')
for line in finp.readlines():
	if  "set filedir" in line :
		fout.write("set filedir \"%s\"\n"  %(repr(wkdir).strip('\'')))
	elif "sess LoadSessionFile" in line:
		sessfile = wkdir+'\\session.mvw'
		fout.write("sess LoadSessionFile \"%s\" false\n"  %(repr(sessfile).strip('\'')))
	else:
		fout.write(line)
fout.close()
try:
	os.system("C:\\CAE\\HyperWorks\\14.0\\hw\\bin\\win64\\hw.exe -b -tcl %s" %(ScriptFile))
except:
	print 'ERROR:lease check the HW directory!'