#coding:utf-8
import sys
import os 

try:
	wkdir = sys.argv[1]
	rundir = sys.argv[2]
	pydir = sys.argv[3]
except:
	print "*"*40
	print  "Default Debug Path"
	wkdir = r'Y:\cal\01_Comp\04_SB\566_180611_ESR-039680_BKL_double_buckle_strength_Allen\02_run'
	rundir  = r"C:\Users\yujin.wang\Desktop\LocalPy"
	pydir = r'python.exe'
	print "*"*40

sys.path.append(rundir+"\\lib")
from Infor import *
from DynaData import *
from Main_Plot import *
import Copyright
os.chdir(wkdir)
os.system("%s C:\\CAE\\scripts\\Python\ASG_HPC_DYN_l2a.py" %(pydir))
statement1()	
rstfile = open(wkdir+'\\image'+'\\rst.txt','w')

#Get the matdic
MatDic = {}
try:
	for line in open(rundir+"\\SessionFiles\\MatDic.txt"):
		data = string_split(line,' ')
		MatDic[int(data[0])] = data[1] 
	print 'MatDic has been read!'
except :
	raw_input('MatDic is not load!')
	sys.exit()

#Extract binout files
KeyFile = ReadKeys(wkdir )#Read more .KEY files
#Get model information 
Node = pd.DataFrame(KeyFile.NODE,columns=['node','x','y','z','tc','rc'])
Elem = pd.DataFrame(KeyFile.ELEMENT_SOLID,columns=['elem','PartID','n1','n2','n3','n4','n5','n6','n7','n8'])
PartID = Elem.PartID.drop_duplicates()[Elem.PartID<=225].tolist()
MatID = dynaMatCurvePlot(KeyFile,PartID,wkdir +'\\image',1000)#plot mat stress-strain curve	

	
# Capture camera vector
try:
	Spring = KeyFile.ELEMENT_DISCRETE
	Coord = KeyFile.DEFINE_COORDINATE_NODES
	print "Current No. DISCRETE ELEMENT is %d" %(len(Spring))
except:
	raw_input('ERROR:Load Spring are not found!')
	sys.exit()
	
# Plot curve
try:	
	if len(Spring ) == 2:
		LoadFlag = Spring[0][2] in Spring[1] or Spring[0][3] in Spring[1]
		# LoadFlag =  len(set(Spring[0])&set(Spring[1]))== 0
		OriginNode1 = Node[Node['node']==Coord[0][1]].values.tolist()[0]
		OriginNode2 = Node[Node['node']==Coord[1][1]].values.tolist()[0]
		OriginNode  = [(float(OriginNode1[i+1]) + float(OriginNode2[i+1]))/2 for i in range(3)]
		if LoadFlag :
			print "Current analysis is single load."
			figuremax = DeforcPlot(wkdir,1)
		else:
			print "Current analysis is two load."
			figuremax = DeforcPlot(wkdir,2)
	else:
		print 'ERROR: No. Please check the number of Coordinate(load) is 1 or 2!'
	
except:
	raw_input('ERROR:Please check Deforce and Glstat files!')	
	sys.exit()
	
rstfile.write('MaxForce %s\n' %(str(figuremax[0])))
GlstatPlot(wkdir) # plot Glstat


#Creat Session files
SessionFile = wkdir +'\Session.txt'
print "SessionFile:%s" %(SessionFile) 
fout = open(SessionFile,'w')
finp = open(r"%s\\SessionFiles\\session.txt" %(rundir),'r')
for line in finp.readlines():
	if '$' not in line:
		if 'crs pos' in line :
			fout.write("crs pos nod %s no1 %s no2 %s\n" %(Coord[0][1],Coord[0][2],Coord[0][3]))
		elif 'vie cam upv nod' in line:
			fout.write("vie cam upv nod %s\n" %(Coord[0][1]))
		elif  'rea' in line:
			for i in MatID:
				# print MatDic[int(i)],type(MatDic[int(i)])
				rstfile.write("Mat " +MatDic[int(i)]+ "\n")
			line = "s[0]:rea fil \"Automatic\" '%s\\d3plot' GEO=0:PartID:all DIS=0:all FUN=0:all:\"max. pl. strain (Shell/Solid)\" FUN=0:all:\"max. v. Mises (Shell/Solid)\" ADD=no " %(wkdir)
			fout.write(line)
		elif 'rec' in line or 'wri' in line:
			line = line.replace('image',wkdir+'\image')
			# if 'model.png' in line and LoadFlag is not True:
				# line = line.replace('model','model2')
			fout.write(line)
		elif 'sta set tim' in line:
			line = 'sta set tim %f\n' %(figuremax[1])
			fout.write(line)
		else:
			fout.write(line)
	else:
		fout.write(line)
fout.close()

#Pictures for post
try: 
 	os.system(r"C:\CAE\Animator4\2.3.0\StartA4_64_fbo.exe -b -s %s" %(SessionFile))
	pass
except:
	print 'ERROR:Please check the Animator directory!'

rstfile.close()