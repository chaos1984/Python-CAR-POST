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
import Copyright
os.system( "copy %s\\SessionFiles\\session.mvw %s" %(rundir ,wkdir))
statement1()


#Capture mode
isFlag = 0
for line in open(wkdir +'\\X\\eigout'):
	if 'EIGENVALUE' in line:
		isFlag = 1
		continue
	elif (isFlag ==1 and 'MODE' not in line):
		freq = float( string_split(line[:-1],' ')[3])
		if freq > 300:
			mode = int( string_split(line[:-1],' ')[0])-1
			break

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
	elif 'set mode_num' in line:
		fout.write('set mode_num %d\n' %(mode))
	else:
		fout.write(line)
fout.close()
try:
	os.system("C:\\CAE\\HyperWorks\\14.0\\hw\\bin\\win64\\hw.exe -b -tcl %s" %(ScriptFile))
except:
	print 'ERROR:lease check the HW directory!'