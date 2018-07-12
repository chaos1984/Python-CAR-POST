#coding:utf-8
from lib import *
# from lib.DynaData import *
# from lib.Main_Plot import *

try:
	rundir = sys.argv[1]
	wkdir = sys.argv[2]
except:
	wkdir = "Y:\cal\01_Comp\09_NVH\000_Anne\test"
	rundir="Y:\doc\08_Personal\Yujin\0508\YokingPy"


os.system( "copy %s\\SessionFiles\\session.mvw %s" %(rundir ,wkdir))
statement1()

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
	os.system("C:\\CAE\\HYPERWORKS\\2017.2\\hw\\bin\\win64\\hw.exe -b -tcl %s" %(ScriptFile))
except:
	print 'ERROR:Please check the HW directory!'