#coding:utf-8
from Autolivlib import *
import json
import logging

try:
	rundir = sys.argv[1]
	wkdir = sys.argv[2]
except:
	print  "Default Debug Path"
	wkdir = r"Y:\cal\01_Comp\02_DAB\466_191226_ESR-066013_GWM_CHB071_Illuminated_Emblem_DAB_Deployment_AFIS66242_MingfeiLiang_Yujin\02_Run\V1"
	rundir = r"Y:\doc\08_Personal\Yujin\0508\YokingPy"

with open(rundir+r"\config\DABConfig.json", "r") as f:
    config = json.loads(f.read())
	
try:
	for line in open(wkdir +"//DAB_Session_3UL.ses",'r'):
		if '$mat=[u' in line:
			exec(line[1:-1])
			break
		else:
			rawinput('ERROR:No mat. found in the session files')
except:
	for line in open(wkdir +"//DAB_Session.ses",'r'):
		if '$mat=[u' in line:
			exec(line[1:-1])
			break
		else:
			rawinput('ERROR:No mat. found in the session files')
		
for i in mat:
	if config['MATER'][i]['PART'] == 'COV':
		dicCOV = config['MATER'][i]
	if config['MATER'][i]['PART'] == 'HOU':
		dicHOU = config['MATER'][i]
	if config['MATER'][i]['PART'] == 'EMB':
		dicEMB = config['MATER'][i]
		
wkdir += '//image//'	
PPTName = [i for i in wkdir.split('\\') if 'ESR' in i][0]
print PPTName
Title = ' '.join(PPTName.split('_')[2:-1])

#############################################################################################
muban_path = r'%s\SlideMaster\ALV_General Presentation 2017.pptx' %(rundir)
fab_info_path =r"Y:/comp/02_DAB/DAB_Information.csv"
A = StiffPPT(muban_path,wkdir)
###########################MODIFY############################################################
Date =  time.strftime("%b %d %Y", time.localtime())
Author = getpass.getuser()
logging.info('Author: %s' %Author)
#############################################################################################
try:
	df = pd.read_csv(fab_info_path)
	start = PPTName.find("ESR-")
	ESR = PPTName[start:(start+10)]
	print ESR,df['ESR'].tolist()
	if ESR in df['ESR'].tolist():
		print ("find it")
		row = df[(df['ESR']==ESR)].index.tolist()[0]
	else:
		print ("No ESR information found in FAB_INFO,Please check!")
		raw_input("PAUSE")
except:
	print ("No ESR information found in FAB_INFO,Please check!")
	raw_input("PAUSE")
	
#############################################################################################
#page1
A.CoverPageCreate(Title,Author,Date)

#page2
ReportContents = [['1. DAB Assemble CAE model\n2. Cover, Emblem & Housing material\n3. Load and Boundary condition\n4. Simulation cases\n5. FEA results \n6. Conclusion\n7. Appendix',24]]
A.BlankPageCreate('Contents',Paragraphs=ReportContents)


#page3
Pictures = []
Pictures_list = ['cushion.png','inflator.png','cover.png','housing.png','emblem.png','omegaspring.png','armature.png','foam.png','dumper.png']
loc_x = 2.;loc_y = 5.
height = 3.73; width = 10
for index,pic in enumerate(Pictures_list):
	print index
	file = wkdir + pic
# CushionPic = rundir+ r'\\image\\' + 'Cushion_fold_type.png'
	Pictures.append([file,Cm(loc_x+index/3*width),Cm(loc_y+index%3*height),Cm(3.73),Cm(10)])
A.BlankPageCreate('Assembly',Pictures=Pictures)


#page4
Pictures = []
file = wkdir+'cushion.png'
# CushionPic = rundir+ r'\\image\\' + 'Cushion_fold_type.png'
Pictures.append([file,Cm(2),Cm(10.5),Cm(6),Cm(12)])
A.BlankPageCreate('Cushion',[['Diameter:%s\nNo. of Tether: %s\nNo. of Vent: %s\nWrapper:%s\nDifussor:%s\nFold type:%s\nFabric Mat.:%s' %(df.Diam[row],df.Teth[row],df.Vent[row],df.Wrapper[row],df.Difu[row],df.Foldtype[row],df.Cushion[row]),24]],Pictures=Pictures)

#Page5
try:
	Part = 'COVER'
	MatName = dicCOV['NAME']
	MatRO = str(dicCOV['RO'])
	MatE = str(dicCOV['E'])
	MatPR = str(dicCOV['PR'])
	MatLT = str(dicCOV['LT'])
	MatRT = str(dicCOV['RT'])
	MatHT = str(dicCOV['HT'])
	MatPic = rundir+ r'\\image\\' + dicCOV['PIC']

	Pictures = []
	file = wkdir+'cover.png'
	Pictures.append([file,Cm(2),Cm(10.5),Cm(6),Cm(12)])
	Pictures.append([MatPic,Cm(16),Cm(5),Cm(8),Cm(17)])
	TableValue = [['Part','Material','Temperature(°C)','Strain at break'],[Part,MatName,'85',MatHT],[Part,MatName,'23',MatRT],[Part,MatName,'-35',MatLT]]
	Tables = [[TableValue,Cm(15.5),Cm(13),Cm(4.5),Cm(18),14]]
	A.BlankPageCreate('Cover material',[['Mat. Name:%s(non linear, with damage)\nDens.:%s kg/mm3\nPoisson ratio:%s' %(MatName,str(MatRO),str(MatPR)),20]],Pictures=Pictures,Tables=Tables)
except:
	print 'No COVER found!'
#page4
try:
	Part = 'EMBLEM'
	MatName = dicEMB['NAME']
	MatRO = str(dicEMB['RO'])
	MatE = str(dicEMB['E'])
	MatPR = str(dicEMB['PR'])
	MatLT = str(dicEMB['LT'])
	MatRT = str(dicEMB['RT'])
	MatHT = str(dicEMB['HT'])
	MatPic = rundir+ r'\\image\\' + dicEMB['PIC']

	Pictures = []
	file = wkdir+'emblem.png'
	Pictures.append([file,Cm(2),Cm(10.5),Cm(6),Cm(12)])
	Pictures.append([MatPic,Cm(16),Cm(5),Cm(8),Cm(17)])
	TableValue = [['Part','Material','Temperature(°C)','Strain at break'],[Part,MatName,'85',MatHT],[Part,MatName,'23',MatRT],[Part,MatName,'-35',MatLT]]
	Tables = [[TableValue,Cm(15.5),Cm(13),Cm(4.5),Cm(18),14]]
	A.BlankPageCreate('Emblem material',[['Mat.:%s(non linear, with damage, replaced with T65)\nDens.:%s kg/mm3\nPoisson ratio:%s' %(MatName,str(MatRO),str(MatPR)),20]],Pictures=Pictures,Tables=Tables)
except:
	print 'No EMBLEM found!'
#page5
try:
	Part = 'HOUSING'
	MatName = dicHOU['NAME']
	MatRO = str(dicHOU['RO'])
	MatE = str(dicHOU['E'])
	MatPR = str(dicHOU['PR'])
	MatLT = str(dicHOU['LT'])
	MatRT = str(dicHOU['RT'])
	MatHT = str(dicHOU['HT'])
	MatPic = rundir+ r'\\image\\' + dicHOU['PIC']
	Pictures = []
	file = wkdir+'housing.png'
	Pictures.append([file,Cm(2),Cm(10.5),Cm(6),Cm(12)])
	Pictures.append([MatPic,Cm(16),Cm(5),Cm(8),Cm(17)])
	TableValue = [['Part','Material','Temperature(°C)','Strain at break'],[Part,MatName,'85',MatHT],[Part,MatName,'23',MatRT],[Part,MatName,'-35',MatLT]]
	Tables = [[TableValue,Cm(15.5),Cm(13),Cm(4.5),Cm(18),14]]
	A.BlankPageCreate('Housing material',[['Mat. Name:%s(non linear)\nDens.:%s kg/mm3\nPoisson ratio:%s' %(MatName,str(MatRO),str(MatPR)),20]],Pictures=Pictures,Tables=Tables)
except:
	pass

#page6
Pictures = []
file = wkdir+'side.png'
Pictures.append([file,Cm(3.2),Cm(4),Cm(10),Cm(18)])
A.BlankPageCreate("Load & Boundary Condition",Pictures=Pictures)

#page7
if not os.path.exists(wkdir+'side_3.avi'):
	A.BlankPageCreate("Simulation cases:",[['Case 1: Single ADP-1.3B Upper limit - LT (UL_LT)\n\n',24],['Case 2: Single ADP-1.3B Upper limit - RT (UL_RT)\n\n',24],['Case 3: Single ADP-1.3B Upper limit - HT (UL_HT)\n\n',24],['Case 4: Single ADP-1.3B Lower limit - LT (LL_LT)',24]])
else:
	A.BlankPageCreate("Simulation cases:",[['Case 1: Single ADP-1.3B Upper limit - LT (UL_LT)\n',24],['Case 2: Single ADP-1.3B Upper limit - RT (UL_RT)\n',24],['Case 3: Single ADP-1.3B Upper limit - HT (UL_HT)\n',24],['Case 4: Single ADP-1.3B Lower limit - LT (LL_LT)\n',24],['Case 5: Single ADP-1.3B Normal limit - LT (NL_LT)\n',24],['Case 6: Single ADP-1.3B Normal limit - LT (NL_RT)\n',24],['Case 7: Single ADP-1.3B Normal limit - LT (NL_HT)\n',24]])

#page8
Movies = []
file = wkdir+'top.avi'
Movies.append([file,Cm(1.5),Cm(6),Cm(12),Cm(30)])
A.BlankPageCreate('FEA results', [['-Top view',24]],Movies = Movies)

#page8
if os.path.exists(wkdir+'top_3.avi'):
	#page9
	Movies = []
	file = wkdir+'top_3.avi'
	Movies.append([file,Cm(1.5),Cm(6),Cm(12),Cm(30)])
	A.BlankPageCreate('FEA results',[['-Top view',24]],Movies = Movies)
	
#page10
Movies = []
file = wkdir+'side.avi'
Movies.append([file,Cm(1.5),Cm(6),Cm(12),Cm(30)])
A.BlankPageCreate('FEA results',[['-Side view',24]],Movies = Movies)

#page11
if os.path.exists(wkdir+'side_3.avi'):

	Movies = []
	file = wkdir+'side_3.avi'
	Movies.append([file,Cm(1.5),Cm(6),Cm(12),Cm(30)])
	A.BlankPageCreate('FEA results',[['-Side view',24]],Movies = Movies)

#page12
Movies = []
file = wkdir+'Cover.avi'
Movies.append([file,Cm(1.5),Cm(6),Cm(12),Cm(30)])
A.BlankPageCreate('FEA results',[['-Cover',24]],Movies = Movies)

#page13
if os.path.exists(wkdir+'Cover_3.avi'):
	Movies = []
	file = wkdir+'Cover_3.avi'
	Movies.append([file,Cm(1.5),Cm(6),Cm(12),Cm(30)])
	A.BlankPageCreate('FEA results',[['-Cover',24]],Movies = Movies)
	
#page14
Pictures = []
file = wkdir+'cover_strain.png'
Pictures.append([file,Cm(2.5),Cm(5),Cm(11),Cm(30)])
A.BlankPageCreate('FEA results',[['-The distribution of the effective plastic strain on cover.',24]],Pictures=Pictures)

if os.path.exists(wkdir+'cover_strain_3.png'):
	#page10
	Pictures = []
	file = wkdir+'cover_strain_3.png'
	Pictures.append([file,Cm(2.5),Cm(5),Cm(11),Cm(30)])
	A.BlankPageCreate('FEA results',[['-The distribution of the effective plastic strain on cover.',24]],Pictures=Pictures)

#page9
Movies = []
file = wkdir+'Emblem.avi'
Movies.append([file,Cm(1.5),Cm(6),Cm(12),Cm(30)])
A.BlankPageCreate('FEA results',[['-Emblem',24]],Movies = Movies)

#page9
if os.path.exists(wkdir+'Emblem_3.avi'):
	Movies = []
	file = wkdir+'Emblem_3.avi'
	Movies.append([file,Cm(1.5),Cm(6),Cm(12),Cm(30)])
	A.BlankPageCreate('FEA results',[['-Emblem',24]],Movies = Movies)
		
#page11
Pictures = []
file = wkdir+'emblem_strain_top.png'
Pictures.append([file,Cm(2.5),Cm(5),Cm(11),Cm(30)])
A.BlankPageCreate('FEA results',[['-The distribution of the effective plastic strain on emblem.',24]],Pictures=Pictures)

if os.path.exists(wkdir+'side_3.avi'):
	#page10
	Pictures = []
	file = wkdir+'emblem_strain_top_3.png'
	Pictures.append([file,Cm(2.5),Cm(5),Cm(11),Cm(30)])
	A.BlankPageCreate('FEA results',[['-The distribution of the effective plastic strain on emblem.',24]],Pictures=Pictures)


#page12
Pictures = []
file = wkdir+'emblem_strain_bottom.png'
Pictures.append([file,Cm(2.5),Cm(5),Cm(11),Cm(30)])
A.BlankPageCreate('FEA results',[['-The distribution of the effective plastic strain on emblem.',24]],Pictures=Pictures)
if os.path.exists(wkdir+'side_3.avi'):
	#page10
	Pictures = []
	file = wkdir+'emblem_strain_bottom_3.png'
	Pictures.append([file,Cm(2.5),Cm(5),Cm(11),Cm(30)])
	A.BlankPageCreate('FEA results',[['-The distribution of the effective plastic strain on emblem.',24]],Pictures=Pictures)


#page13
Pictures = []
file = wkdir+'housing_strain_top.png'
Pictures.append([file,Cm(2.5),Cm(5),Cm(11),Cm(30)])
A.BlankPageCreate('FEA results',[['-The distribution of the effective plastic strain on housing.',24]],Pictures=Pictures)

if os.path.exists(wkdir+'side_3.avi'):
	Pictures = []
	file = wkdir+'housing_strain_top_3.png'
	Pictures.append([file,Cm(2.5),Cm(5),Cm(11),Cm(30)])
	A.BlankPageCreate('FEA results',[['-The distribution of the effective plastic strain on housing.',24]],Pictures=Pictures)


#page14
Pictures = []
file = wkdir+'housing_strain_bottom.png'
Pictures.append([file,Cm(2.5),Cm(5),Cm(11),Cm(30)])
A.BlankPageCreate('FEA results',[['-The distribution of the effective plastic strain on housing.',24]],Pictures=Pictures)

if os.path.exists(wkdir+'side_3.avi'):
	Pictures = []
	file = wkdir+'housing_strain_bottom_3.png'
	Pictures.append([file,Cm(2.5),Cm(5),Cm(11),Cm(30)])
	A.BlankPageCreate('FEA results',[['-The distribution of the effective plastic strain on housing.',24]],Pictures=Pictures)


#page15
TableValue = [['Part','LL_LT','UL_LT','UL_RT','UL_HT'],['Cover','OK','OK','OK','OK'],['Emblem','OK','OK','OK','OK'],['Housing(body)','OK','OK','OK','OK'],['Housing(3H)','OK','OK','OK','OK'],['Housing(6H)','OK','OK','OK','OK'],['Housing(9H)','OK','OK','OK','OK']]
Tables = [[TableValue,Cm(7),Cm(12),Cm(6),Cm(20),14]]
A.BlankPageCreate('Conclusion',[['1. Cover has no breakage risk under UL_LT and UL-RT, but has over tear risk and breakage risk in  LL_HT.\n2. Emblem is broken after it hit on the SW in  UL_HT case, the other cases are ok.\n3. The 6H hook has crack risk under all cases, and the 3H and 6H hooks have crack risk under UL_HT.\n4. Airbag can deploy in LL_LT.',20]],Tables=Tables)

#page16-19
for i in ['LL_LT','UL_LT','UL_RT','UL_HT','NL_LT','NL_RT','NL_HT']:
	if os.path.exists(wkdir+i+'.png'):
		Pictures = []
		file = wkdir+i+'.png'
		Pictures.append([file,Cm(3.2),Cm(4),Cm(15),Cm(27)])
		A.BlankPageCreate('Appendix-%s' %(i),Pictures=Pictures)

#page20
A.EndPageCreate()
print wkdir+PPTName
if os.path.exists(wkdir+PPTName+'.pptx'):
	PPTtime =  time.strftime("_%d_%H_%M", time.localtime())
	A.PPTCreate(PPTName+PPTtime)
else:
	A.PPTCreate(PPTName)