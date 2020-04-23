#coding:utf-8
from Autolivlib import *
import json
import threading

def startAnimator(sessionfile):
	try:
		os.system(r"C:\CAE\Animator4\2.3.3\StartA4_64_fbo.exe -b -s %s" %(sessionfile))
	except:
		os.system(r"StartA4_64_fbo.exe -b -s %s" %(sessionfile))
	finally:
		print("ERROR:Animator dir. is wrong! Pls. check!")	
	
def DABSession(SessionFile,wkdir,rundir,config):
	print "SessionFile:%s" %(SessionFile)
	fout = open(wkdir+'\\'+SessionFile,'w')
	fout.write('$mat='+str(mat)+'\n')
	finp = open(r"%s\\SessionFiles\\%s"  %(rundir,SessionFile),'r')
	for line in finp.readlines():
		try:
			if '&cov&' in line:
				for i in mat:
					if 'LT' in line and config['MATER'][i]['PART'] == 'COV':
						limit = config['MATER'][i]['LT']
					if 'RT' in line and config['MATER'][i]['PART'] == 'COV':
						limit = config['MATER'][i]['RT']
					if 'HT' in line and config['MATER'][i]['PART'] == 'COV':
						limit = config['MATER'][i]['HT']
				line =line.replace('&cov&',str(limit))
			if '&hou&' in line:
				for i in mat:
					if 'LT' in line and config['MATER'][i]['PART'] == 'HOU':
						limit = config['MATER'][i]['LT']
					if 'RT' in line and config['MATER'][i]['PART'] == 'HOU':
						limit = config['MATER'][i]['RT']
					if 'HT' in line and config['MATER'][i]['PART'] == 'HOU':
						limit = config['MATER'][i]['HT']
				line =line.replace('&hou&',str(limit))
			if '&emb&' in line:
				for i in mat:
					if 'LT' in line and config['MATER'][i]['PART'] == 'EMB':
						limit = config['MATER'][i]['LT']
					if 'RT' in line and config['MATER'][i]['PART'] == 'EMB':
						limit = config['MATER'][i]['RT']
					if 'HT' in line and config['MATER'][i]['PART'] == 'EMB':
						limit = config['MATER'][i]['HT']
				line =line.replace('&emb&',str(limit))
		except:
			print 'ERROR:'
			print line
		fout.write(line)
	fout.close()
	finp.close()


print 'SUBROUTINE: Session file modify program'
try:
	wkdir = sys.argv[1]
	rundir = sys.argv[2]
	pydir = sys.argv[3]
except:
	print "*"*40
	print  "Default Debug Path"
	wkdir = r'Y:\cal\01_Comp\02_DAB\449_190819_ESR-058562_DC1E_DAB_Deployment_Yujin\02_Run\V7'
	rundir = r"Y:\doc\08_Personal\Yujin\0508\YokingPy"
	pydir = r'python.exe'
	print "*"*40

with open(rundir+r"\config\DABConfig.json", "r") as f:
    config = json.loads(f.read())

os.chdir(wkdir)

dirs = FindFile(wkdir, 'd3plot')[1]
try:
	Keyfile = DynaInfo(dirs[0],'','.key')
	print dirs[0]
	Keyfile.Pars(Keyfile.files[0])
	mat = []
	for i in config['MATER'].keys():
		for j in Keyfile.INCLUDE:
			if i in j[0] and i not in mat:
				print i
				mat.append(i)
except:
	print ('ERROR:No master file found! Pls check file format(.key)')
	print dirs[0]




thread_list = []
#Pictures for post
if 'NL' in str(dirs):
	try:
		SessionFile2 = 'DAB_Session_3.ses'
		DABSession(SessionFile2,wkdir,rundir,config)
		t = threading.Thread(target = startAnimator(SessionFile2))
		thread_list.append(t)
	except:
		print 'ERROR:Please check the Animator directory OR DAB_Session_3.ses!'
#Pictures for post
if 'UL' in str(dirs):
	if 'LL' in str(dirs):
		SessionFile1 = 'DAB_Session.ses'
		DABSession(SessionFile1,wkdir,rundir,config)
		try:
			t = threading.Thread(target = startAnimator(SessionFile1))
		except:
			print 'ERROR:Please check the Animator directory OR DAB_Session.ses!'
	else:
		try:
			SessionFile1 = 'DAB_Session_3UL.ses'
			DABSession(SessionFile1,wkdir,rundir,config)
			t = threading.Thread(target = startAnimator(SessionFile1))
		except:
			print 'ERROR:Please check the Animator directory OR DAB_Session_3UL.ses!'
		thread_list.append(t)
		for t in thread_list:
			t.join()
	
