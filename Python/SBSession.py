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
	wkdir = "Y:\\cal\\01_Comp\\04_SB\\548-180423_ESR_038128_CTR_BUK_Bracket_Strength_Yujin\\02_run"
	rundir  = "Y:\doc\08_Personal\Yujin\0508\YokingPy"
	pydir = r'Y:\\doc\\11_Script\\Python27\\python.exe'
	print "*"*40
	
sys.path.append(rundir+"\\lib")
from Infor import *
from DynaData import *
from Main_Plot import *
	
	

try:
	#Extract binout files
	os.chdir(wkdir)
	os.system("%s C:\\CAE\\scripts\\Python\ASG_HPC_DYN_l2a.py" %(pydir))
	KeyFile = ReadKeys(wkdir )#Read more .KEY files
	#Get model information 
	Node = pd.DataFrame(KeyFile.NODE,columns=['node','x','y','z','tc','rc'])
	Elem = pd.DataFrame(KeyFile.ELEMENT_SOLID,columns=['elem','PartID','n1','n2','n3','n4','n5','n6','n7','n8'])
	PartID = Elem.PartID.drop_duplicates()[Elem.PartID<=225].tolist()
	filepath = wkdir +'\\image'
	dynaMatCurvePlot(KeyFile,PartID,filepath)#plot mat stress-strain curve	
	# Capture camera vector
	Coord = KeyFile.DEFINE_COORDINATE_NODES
	print "Current No. Coord is %d" %(len(Coord))
	if len(Coord ) == 2:
		LoadFlag = Coord[0][1] in Coord[1] and Coord[0][2] in Coord[1] and Coord[0][3] in Coord[1]
		OriginNode1 = Node[Node['node']==Coord[0][1]].values.tolist()[0]
		OriginNode2 = Node[Node['node']==Coord[1][1]].values.tolist()[0]
		OriginNode  = [(float(OriginNode1[i+1]) + float(OriginNode2[i+1]))/2 for i in range(3)]
		if LoadFlag == True:
			print "Current analysis is single load."
			DeforcPlot(wkdir,1)
		else:
			print "Current analysis is two load."
			DeforcPlot(wkdir,2)
	else:
		print 'ERROR: No. Pleasche the number of Coordinate(load) is 1 or 2!'
		
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
				line = "s[0]:rea fil \"Automatic\" '%s\\d3plot' GEO=0:PartID:all DIS=0:all FUN=0:all:\"max. pl. strain (Shell/Solid)\" FUN=0:all:\"max. v. Mises (Shell/Solid)\" ADD=no " %(wkdir)
				fout.write(line)
			elif 'rec' in line or 'wri' in line:
				line = line.replace('image',wkdir+'\image')
				# if 'model.png' in line and LoadFlag is not True:
					# line = line.replace('model','model2')
				fout.write(line)
			else:
				fout.write(line)
		else:
			fout.write(line)
	fout.close()

	#Pictures for post
	try: 
		os.system(r"C:\CAE\Animator4\2.3.0\StartA4_64_fbo.exe -b -s %s" %(SessionFile))
	except:
		print 'ERROR:lease check the Animator directory!'

except :
	print '#'*20
	print '.key files are no found!'
	print '#'*20