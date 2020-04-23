#coding:utf-8
import os
import sys
import time
import logging
import Autolivlib
print  'Autolivlib dir.:',Autolivlib.__path__[0]

@ Autolivlib.exeTime
def main(wkdir,pydir = "python",rundir = r"Y:\comp\doc\08_Personal\Yujin\0508\YokingPy"):
	FORMAT = "%(asctime)-15s %(message)s"
	logging.basicConfig(filename=wkdir+'\DABPost.log',level=logging.INFO,format=FORMAT)
	logging.info('#'*50)
	logging.info('pydir:%s' %pydir)
	logging.info('wkdir:%s' %wkdir)
	logging.info('rundir:%s' %rundir)
	dirs = Autolivlib.FindFile(wkdir, 'd3plot')[1]
	if len(dirs) == 0:
		logging.error(".d3plot files are not found!")
		sys.exit()

		
	print '#'*20
	print 'DYNA solution files directory:\n','\n'.join(dirs)
	print '#'*20


	# Make image dir.
	imagedir =  wkdir +'\\image'
	curdir = os.curdir
	if not os.path.exists(imagedir):
		os.mkdir(imagedir)
	for i in dirs:
		os.chdir(i)
		if not os.path.exists(i+'\matsum'):		
			os.system("%s C:\\CAE\\scripts\\Python\\ASG_HPC_DYN_l2a.py" %(pydir))
	time.sleep(10)
	for i in dirs:
		os.chdir(curdir)
		try:
			imagename = i.split('\\')[-1]
			Autolivlib.Parsing(i,imagedir+'\\'+imagename)
		except:
			logging.warning('No .d3hsp glstat matsum found! Pls check!')
	#Create Session file
	logging.info('$'*20+'Pictures'+'$'*20)
	os.system("%s %s\\DABSession.py %s %s %s" %(pydir,rundir,wkdir,rundir,pydir))
# # Create PPT
	logging.info('$'*20+'PPT Report'+'$'*20)
	os.system("%s %s\\DABPPT.py %s %s" %(pydir,rundir,rundir,wkdir))
	if not os.path.exists(imagedir):
		os.mkdir(imagedir)
	logging.info('#'*50)
if __name__ == "__main__":
	try:
		wkdir = sys.argv[1]
	except:
		wkdir = r'Y:\cal\01_Comp\02_DAB\449_190819_ESR-058562_DC1E_DAB_Deployment_Yujin\02_Run'
	main(wkdir)
	raw_input("PAUSE")