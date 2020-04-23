#coding:utf-8
import os
import sys
import Autolivlib
print  'Autolivlib dir.:',Autolivlib.__path__[0]

@ Autolivlib.exeTime
def main(wkdir,pydir = "python",rundir = r"Y:\doc\08_Personal\Yujin\0508\YokingPy"):
	try:
		wkdir = sys.argv[1]
	except:
		print "Dyna file dir. cann't be found!"
		
	dirs = Autolivlib.FindFile(wkdir, 'd3plot')[1]
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

	# Create PPT
	os.system("%s %s\\SBPPT.py %s %s" %(pydir,rundir,rundir,wkdir))
if __name__ == "__main__":
	main(sys.argv[1])
	raw_input("PAUSE")