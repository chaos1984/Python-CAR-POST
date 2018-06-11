#coding:utf-8
#coding:gb2312
import sys
try:
	rundir = sys.argv[1]
	wkdir = sys.argv[2]
except:
	wkdir = r"C:\Users\chaos\Desktop\PySTIFF"
	rundir = r"C:\Users\chaos\Documents\GitHub\Python-CAR-POST\Python"

sys.path.append(rundir+"\\lib")
from NastranData import *
from Post import *
from matplotlib.text import OffsetFrom

def BiwSession(rundir,wkdir):
	filename = r"\SOLVE"
	
	#SG00
	list1 = [[600001,700001],[600002,700002],[600003,700003],[600004,700004],[600005,700005],[600006,700006],[600007,700007],[600008,700008],[600009,700009],[600010,700010],[600011,700011],[600012,700012],[600013,700013],[600014,700014],[600015,700015],[600016,700016],[600017,700017],[600018,700018],[600019,700019]]
	# list1 = [[600001,700001],[600002,700002],[600003,700003],[600004,700004],[600005,700005],[600006,700006],[600007,700007],[600008,700008],[600009,700009],[600010,700010],[600011,700011],[52128485,51749507],[52129196,52133578],[52129282,52133637],[600015,700015],[600016,700016],[600017,700017],[600018,700018],[600019,700019]]
	list2 = [[1418293,963177],[1412890,1413934],[1429124,1436649],[1428758,1426037],[927402,52565109],[929943,52559058]]
	torq_point = [600002,700002]
	Weight = 310.5 ; Area = 4.0
	
	
	filedir = wkdir + filename
	report1 = stiffreport(0,wkdir+"/image",filedir+".bdf",filedir+".f06",list1,list2)
	res = report1.post(torq_point)
	
	torq=res[res.Type == 'Torque'].loc[:,['Xcor','Ang & Dis']]
	figure1=CurvePlot(u'Torsion Stiffness',u'X coor',u'Angel',-1,1,'111',0.3,torq)
	figure1.stiff(wkdir+"/image/torq")
	bend=res[res.Type == 'Bend'].loc[:,['Xcor','Ang & Dis']]
	figure2=CurvePlot(u'Bend Stiffness',u'X coor',u'Z Displacement',-1,2,'111',0.3,bend)
	figure2.stiff(wkdir+"/image/bend")
	
	
	torq_stiff = res.stiff[list1.index(torq_point)]
	print "Tors stiffness: %10.2f" %(torq_stiff )# ID is used to 10 points, u can chang it to 20 point and so on.
	print "Bend stiffness: %10.2f" %(res.stiff[res.Type == 'Bend'].min())
	if (Weight != '' and Area != ''):
		LightWeight_Coeff = Weight/torq_stiff/Area*1000
		print LightWeight_Coeff
		print "LightWeight Coeff: %10.4f" %(LightWeight_Coeff)
	return torq_stiff,res.stiff[res.Type == 'Bend'].min(),LightWeight_Coeff
if __name__ == "__main__":
	try:
		rundir = sys.argv[1]
		wkdir = sys.argv[2]
	except:
		wkdir = r"C:\Users\chaos\Desktop\PySTIFF"
		rundir = r"C:\Users\chaos\Documents\GitHub\Python-CAR-POST\Python"
		BiwSession(rundir,wkdir)