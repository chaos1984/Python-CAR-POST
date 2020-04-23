# -*- coding: utf-8
'''
Created on %(date)
@author:Yujin Wang
'''
import os,sys
from matplotlib import ticker
from scipy import stats
import numpy as np,pandas as pd,matplotlib.pyplot as plt
from matplotlib.text import OffsetFrom
from funmodule import *

global color 
color = ['r','b','g','c','y','m']

class basic():
	'''This is the base class for this module'''
	def __init__(self,title,xlabel,ylabel,isall,num,figurepos,delta,data,legend = False):
		'''Created date : 201703
		Modify date : 201802
		Author: Yujin Wang 
		Title -- Figure Title
		xlabel -- x coor lable
		ylabel -- y coor lable
		color -- curve color
		isall -- max\min value plot. 0:min;1:max; 2:max and min  value
		num -- Figure No.
		figrepos -- Figure position
		data -- data ploted in the figure'''
		self.title = title
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.isall = isall
		self.num = num
		self.figurepos = figurepos
		self.delta = delta
		self.data = data 
		self.legend = legend
		

class CurvePlot(basic):
	'''This class is used for plotting and output parameters'''
	def maxmin(self,period=1e10):
		max_y,min_y = 0,0
		
		if (self.isall == 1): #max
			max_y = max(self.data[self.data.iloc[:,0]<period].iloc[:,1])

			max_xcor = self.data[self.data.iloc[:,0]<period].iloc[:,1].idxmax()
			max_x = self.data[self.data.iloc[:,0]<period].iloc[:,0][max_xcor]
			self.annot4stiff('Max:',max_x,max_y)
			return max_y,max_x,max_xcor
		elif (self.isall == 0): #min
			min_y = min(self.data[self.data.iloc[:,0] < period].iloc[:,1])
			min_xcor = self.data[self.data.iloc[:,0]<period].iloc[:,1].idxmin()
			min_x= self.data[self.data.iloc[:,0]<period].iloc[:,0][min_xcor]
			self.annot4stiff('Min:',min_x,min_y)
			return min_y,min_x,min_xcor
		elif self.isall == 2: #maxmin
			max_y = max(self.data[self.data.iloc[:,0]<period].iloc[:,1])
			max_xcor = self.data[self.data.iloc[:,0]<period].iloc[:,1].idxmax()
			max_x = self.data[self.data.iloc[:,0]<period].iloc[:,0][max_xcor]
			self.annot4stiff('Max:',self.max_x,max_y)
			min_y= min(self.data[self.data.iloc[:,0]<period].iloc[:,1])
			min_xcor = self.data[self.data.iloc[:,0]<period].iloc[:,1].idxmin()
			min_x = self.data[self.data.iloc[:,0]<period].iloc[:,0][min_xcor]
			self.annot4stiff('Min:' ,min_x, min_y)
			return max_y,max_x,max_xcor,min_y,min_x,min_xcor

	@property
	def frame(self):
		plt.figure(num = self.num)
		plt.subplot(self.figurepos)
		plt.ylabel(self.ylabel,fontproperties='Simhei')
		plt.xlabel(self.xlabel,fontproperties='Simhei')
		plt.title(self.title,fontproperties='Simhei')
		plt.grid(True)
		plt.subplots_adjust(wspace=self.delta)
		for i in range(len(self.data.columns)-1):
			plt.plot(self.data.iloc[:,0],self.data.iloc[:,i+1],color[i],lw=1,marker='')
		if self.legend != False:
			plt.legend(self.data.columns[1:])
		else:
			pass
			
	def accl(self,preiod):
		self.frame
		return self.maxmin(period)

	def stiff(self,name):
		self.frame
		self.maxmin()
		plt.savefig(name,dpi=100)

	def reldis(self):
		self.frame
		return self.maxmin()
	
	def annot4stiff(self,text,x,y):
		bbox_args = dict(boxstyle = 'round', fc='0.8')
		arrow_args = dict(arrowstyle = '->')
		Label_arg = text + str(round(y,2))+'@' + str(round(x,3))
		plt.annotate(Label_arg,
			xy=(x,y),
			xytext = (2*x/3,1.1),
			textcoords = ('data','axes fraction'),
			bbox = bbox_args,
			arrowprops = arrow_args,
			horizontalalignment = 'top')
class barplot(basic):
    '''It is used to plot the bar figure for the senstive analysis and design variables history'''
    def plot(self,lable):
        plt.figure(num=self.num)
        plt.subplot(self,figrepos)
        res_data = self.data.sort_values(by=lable,ascending = False).iloc[:20]
        plt.bar(range(len(res_data)).tuple(res_data.index),size=20,rotation = 45)
        plt.yticks(size=20)
        plt.ylabel(self.ylabel,fontproperties='Simhei',size=20)
        plt.xlabel(self.xlabel,fontproperties='Simhei',size=20)
        plt.title(self.title,fontproperties='Simhei',size=20)
        plt.grid()

    def opt_plot(nodes,elem_new,res,X_predict,v_predict):
        Force_Point = list(res.iloc(0))[-1]
        x_coor = list(res.iloc(1))
        y_coor = list(res.iloc(2))
        force_dis = list(res.iloc(4))
        plt.figure(1)
        plt.gca().set_aspect('equal')
        plt.tricontourf(nodes.X,nodes.Y,elem_new,nodes,Z,colors='y')
        plt.grid()
        plt.plot(x_coor,y_coor,marker='*')
        plt.scatter(X_predict[0],X_predict[1],color='r')
        string = 'NODE: %d\nX: %5.3f	Y:%5.3f		Z:%5.3f\n 	DIS:	%5.4E' %(Force_Point,round(x_coor[-1],2),round(y_coor[-1],2),round(force_dis[-1]))
        plt.text(x_coor[-1],y_coor[-1],string)
        plt.figure(2)
        plt.plot(force_dis)
        plt.plot(v_predict)
        plt.grid()
        plt.show()
        printtime()

def Parsing(wkdir,imagedir):


	#filein = sys.argv[1]
	filein = wkdir+r"\d3hsp"
	fileinGLAST = wkdir+r"\glstat"
	fileinMATSUM =wkdir+r"\matsum"

	FoundOfPROBLEMCYCLE = False
	FoundOfCURRENTTIMESTEP = False
	FoundEndOfCURRENTTIMESTEP = False
	FoundEndOfPROBLEMCYCLE = False
	StartOfSMALLESTTIMESTEPS = 0
	EndOfSMALLESTTIMESTEPS = 0
	StartOfPROBLEMCYCLE = 0
	EndOfPROBLEMCYCLE = 0
	StartOfCURRENTTIMESTEP = 0
	EndOfCURRENTTIMESTEP = 0
	MASSSCALING = False
	CONTACTTIMESTEP = False
	EXPLICIT = True
	FoundEndOfIMPLICIT = False
	FoundStartOfIMPLICIT = False
	IMPLICIT_NLPRINT2 = False


	#----------------------------------------------------------------------------
	#----------------------------------------------------------------------------
	#Configure plot size
	#----------------------------------------------------------------------------
	#----------------------------------------------------------------------------

	width_mm = 508
	height_mm = 286 
	#----------------------------------------------------------------------------
	#----------------------------------------------------------------------------
	#----------------------------------------------------------------------------
	#Read data from matsum
	#----------------------------------------------------------------------------

	plt.subplots(figsize=(width_mm/25, height_mm/25))

	# Matsum file read by Yoking 
	ax1 = plt.subplot(224)
	inputdeck = open(fileinMATSUM, 'r')
	inputdeck.close
	findexMATSUM = 0
	Matsum = {}
	addmass_parts = []
	for line in inputdeck.readlines():
		if ('time =' in line):
			time = float(line.strip().split()[2])
			Matsum[time] = {}
		if 'mat.#=' in line:
			mat = int(line.strip().split()[1])
			Matsum[time][mat] = []
		if (len(line.strip()) != 0 and line.strip().split()[0] in ['mat.#=','x-mom=','x-rbv=','hgeng=']):
			for i,j in enumerate(line.strip().split()):
				if i%2 == 1:
					Matsum[time][mat].append(float(j))
	for mat in Matsum[0].keys():
		if 200<= mat<299 or 400<= mat<499:
			addmass_parts.append(mat)
	maxy = 0
	for part in addmass_parts:
		xdata = np.sort(Matsum.keys())
		ydata = [Matsum[i][part][-1] for i in xdata]
		if max(ydata) > maxy:
			maxy = max(ydata)
		plt.plot(xdata ,ydata,label='PID:'+str(part))
	formatter = ticker.ScalarFormatter(useMathText=True)
	formatter.set_scientific(True) 
	formatter.set_powerlimits((-1,1)) 
	ax1.yaxis.set_major_formatter(formatter) 
	plt.xlabel('Time step size / ms')
	plt.ylabel('Added Mass / kg')
	plt.title('Added Mass of Cover(200-299) and Emblem(400-499) over simulation time')
	plt.axis([0,max(xdata),-0.1*maxy,1.1*maxy]) 
	plt.grid()
	plt.legend()

	#----------------------------------------------------------------------------
	#----------------------------------------------------------------------------
	#----------------------------------------------------------------------------
	#Read data from d3hsp
	#----------------------------------------------------------------------------
	inputdeck = open(filein, 'r')
	filelines = inputdeck.readlines()
	inputdeck.close
	findex = 0

	while findex <len(filelines):
		fileline = filelines[findex]
	#----------------------------------------------------------------------------
	#Smallest 100 timesteps
	#----------------------------------------------------------------------------   
		if (' 100 smallest timesteps') in fileline:
				StartOfSMALLESTTIMESTEPS = findex + 3
				EndOfSMALLESTTIMESTEPS = StartOfSMALLESTTIMESTEPS + 100
				foundSMALLESTTIMESTEPS = True

	#----------------------------------------------------------------------------
	#Find mass scaled time step and type of MSCL
	#----------------------------------------------------------------------------
		if ('    time step size for mass scaled solution') in fileline:
			MASSSCALING = True
			AppliedMASSSCALING = fileline
		if ('    flag for selective mass scaling................') in fileline:        
			tmp= fileline.strip().split(" ") #Last entry of str-List for selective mass (0,1,2)
			SELECTIVEMASSCALING=int(tmp[-1])

	#----------------------------------------------------------------------------
	#Find critical contact time step   
	#----------------------------------------------------------------------------        
		if (' The LS-DYNA time step size should not exceed') in fileline:
			CONTACTTIMESTEP = True
			ContactTIMESTEP = fileline
				
	#----------------------------------------------------------------------------
	#Added Masses
	#----------------------------------------------------------------------------            
		if not FoundOfPROBLEMCYCLE:
				if (' problem cycle') in fileline:
					StartOfPROBLEMCYCLE = findex
					FoundOfPROBLEMCYCLE = True
				
		if (' *** termination time reached ***') in fileline or (' *** Error ') in fileline:   
			EndOfPROBLEMCYCLE = findex 
			FoundEndOfPROBLEMCYCLE = True
		elif not FoundEndOfPROBLEMCYCLE:
			EndOfPROBLEMCYCLE = findex            

	#----------------------------------------------------------------------------
	#Current time step
	#----------------------------------------------------------------------------            
		if not FoundOfCURRENTTIMESTEP:
			if (' flush i/o buffers            ') in fileline:
				StartOfCURRENTTIMESTEP = findex            
				FoundOfCURRENTTIMESTEP = True
				
		if (' *** termination time reached ***') in fileline or (' *** Error ') in fileline:
			EndOfCURRENTTIMESTEP = findex
			FoundEndOfCURRENTTIMESTEP = True
		elif not FoundEndOfCURRENTTIMESTEP:
			EndOfCURRENTTIMESTEP = findex
			
	#----------------------------------------------------------------------------
	#Check for Implicit solution
	#----------------------------------------------------------------------------    
		if ('    nonlinear solver print flag ...................       2') in fileline:
			IMPLICIT_NLPRINT2= True
		if ('    nonlinear solver print flag ...................       3') in fileline:
			IMPLICIT_NLPRINT2= True        
		if (' BEGIN implicit') in fileline:
			EXPLICIT = False        
		
		if (' Iteration:') in fileline and not EXPLICIT and not FoundStartOfIMPLICIT:
			FoundStartOfIMPLICIT = True
			StartOfIMPLICIT = findex
			
		if (' *** termination time reached ***') in fileline or (' *** Error ') in fileline:   
			EndOfIMPLICIT = findex 
			FoundEndOfIMPLICIT = True
		elif not FoundEndOfIMPLICIT:
			EndOfIMPLICIT = findex        

	#----------------------------------------------------------------------------
	#Find termination time
	#----------------------------------------------------------------------------

		if ('    termination time...............................') in fileline:
			tmp_termtime=fileline.strip().split()
			TERMINATIONtime=float(tmp_termtime[2])
			   
		
		findex = findex + 1
		

	#----------------------------------------------------------------------------
	#----------------------------------------------------------------------------
	#----------------------------------------------------------------------------
	#Read data from d3hsp
	#----------------------------------------------------------------------------    
	inputdeck = open(fileinGLAST, 'r')
	filelinesGLSTAT = inputdeck.readlines()
	inputdeck.close
	findexGLSTAT = 0

	ENERGYkinetic = []
	ENERGYinternal = []
	ENERGYhourglass = []
	ENERGYsliding = []
	ENERGYtotal = []
	Time = []

	while findexGLSTAT <len(filelinesGLSTAT):
		fileline = filelinesGLSTAT[findexGLSTAT]

		if (' time...........................') in fileline:
			tmp = filelinesGLSTAT[findexGLSTAT].strip().split()
			Time.append(float(tmp[1]))
		if (' kinetic energy.................') in fileline:        
			tmp = filelinesGLSTAT[findexGLSTAT].strip().split()
			ENERGYkinetic.append(float(tmp[2]))
		if (' internal energy................') in fileline:  
			tmp = filelinesGLSTAT[findexGLSTAT].strip().split()
			ENERGYinternal.append(float(tmp[2]))
		if (' hourglass energy ..............') in fileline:  
			tmp = filelinesGLSTAT[findexGLSTAT].strip().split()
			ENERGYhourglass.append(float(tmp[3]))
		if (' sliding interface energy.......') in fileline:  
			tmp = filelinesGLSTAT[findexGLSTAT].strip().split()
			ENERGYsliding.append(float(tmp[3]))        
		if (' total energy...................') in fileline:  
			tmp = filelinesGLSTAT[findexGLSTAT].strip().split()
			ENERGYtotal.append(float(tmp[2]))
			#         
		
		findexGLSTAT = findexGLSTAT + 1    

	#----------------------------------------------------------------------------
	#----------------------------------------------------------------------------    
	#----------------------------------------------------------------------------
	#Smallest time step data extraction
	#----------------------------------------------------------------------------
	SmallestTimesteps = filelines[StartOfSMALLESTTIMESTEPS:EndOfSMALLESTTIMESTEPS]

	SmallestTimesteps_array = np.zeros((100,3))
	i_smallesttimesteps = 0
	while i_smallesttimesteps < len(SmallestTimesteps):
		tmp=SmallestTimesteps[i_smallesttimesteps].strip() #Remove trailing blanks
		tmp=(" ".join(tmp.split()).replace(" ",",").split(",")) #Remove intermediate blanks
		
		SmallestTimesteps_array[i_smallesttimesteps,0]=int(tmp[1]) #"Element ID"
		SmallestTimesteps_array[i_smallesttimesteps,1]=int(tmp[-2]) #"Part ID"
		SmallestTimesteps_array[i_smallesttimesteps,2]=float(tmp[-1])*1000 #"Time step"
		
		i_smallesttimesteps = i_smallesttimesteps + 1

		
	 #----------------------------------------------------------------------------
	#Applied mass scaled time step
	#----------------------------------------------------------------------------
	if MASSSCALING:
		tmp=AppliedMASSSCALING.strip() #Remove trailing blanks
		tmp=(" ".join(tmp.split()).replace(" ",",").split(",")) #Remove intermediate blanks 
		AppliedMASSSCALING = 1000*float(tmp[9])*-1
		if AppliedMASSSCALING == 0.0:
			MASSSCALING = False
							   
							   
	#----------------------------------------------------------------------------
	#Cricitcal contact time step
	#----------------------------------------------------------------------------                           
	if CONTACTTIMESTEP:
		tmp=ContactTIMESTEP.strip() #Remove trailing blanks
		tmp=(" ".join(tmp.split()).replace(" ",",").split(",")) #Remove intermediate blanks 
		ContactTIMESTEP = 1000*float(tmp[8])  


	#----------------------------------------------------------------------------
	#Plotting of histogram for smallest element time steps
	#----------------------------------------------------------------------------
	plt.subplot(221)
	plt.hist(SmallestTimesteps_array[:,2],bins=30)
	if MASSSCALING:
		plt.axvline(x=AppliedMASSSCALING,linestyle='dashed',color='b', label='Mass scaled time step='+str(AppliedMASSSCALING*0.9)+'ms')
	if CONTACTTIMESTEP:
		plt.axvline(x=ContactTIMESTEP,linestyle='dashed',color='r',label='Contact time step='+str(ContactTIMESTEP)+'ms')
	plt.legend(loc=0)
	x1,x2,y1,y2 = plt.axis()
	if CONTACTTIMESTEP and MASSSCALING:
		plt.axis([0.99*min(min(SmallestTimesteps_array[:,2]),AppliedMASSSCALING,ContactTIMESTEP), 1.01*max(max(SmallestTimesteps_array[:,2]),AppliedMASSSCALING,ContactTIMESTEP),y1,y2])
	if CONTACTTIMESTEP and not MASSSCALING:
		plt.axis([0.99*min(min(SmallestTimesteps_array[:,2]),ContactTIMESTEP), 1.01*max(max(SmallestTimesteps_array[:,2]),ContactTIMESTEP),y1,y2])    
	if MASSSCALING and not CONTACTTIMESTEP:
		plt.axis([0.99*min(min(SmallestTimesteps_array[:,2]),AppliedMASSSCALING), 1.01*max(max(SmallestTimesteps_array[:,2]),AppliedMASSSCALING),y1,y2])    
	if not CONTACTTIMESTEP and not MASSSCALING:
		plt.axis([0.99*min(SmallestTimesteps_array[:,2]), 1.01*max(SmallestTimesteps_array[:,2]),y1,y2])    
	plt.xlabel('Time step size / ms')
	plt.ylabel('Frequency')
	plt.grid()
	plt.title('Histogramm of 100 smallest time steps')



	#Calculation of PID controlling smallest timesteps

	SmallestTimesteps_controlled_by_PID = stats.itemfreq(SmallestTimesteps_array[:,1])
			  
	info_txt = "Min. timestep by PID: " +str(int(SmallestTimesteps_array[0,1])) + "\nHistogram evaluation:"
	for i_PID_timestep in range(len(SmallestTimesteps_controlled_by_PID[:,0])):
		info_txt = info_txt + "\n PID:" +str(int(SmallestTimesteps_controlled_by_PID[i_PID_timestep,0]))+ ", Counting: " + str(int(SmallestTimesteps_controlled_by_PID[i_PID_timestep,1]))
	x1,x2,y1,y2 = plt.axis()
	plt.text(x1+(x1+x2)/2*.1,0.5*y2, info_txt, fontsize=8, bbox=dict(facecolor='white', alpha=0.7))
			
			
	if EXPLICIT:
		#----------------------------------------------------------------------------
		#----------------------------------------------------------------------------    
		#----------------------------------------------------------------------------
		#Added mass time history
		#----------------------------------------------------------------------------
		SimTimestep = [0]
		SimAddedMassHF = [0]
		SimAddedMassLF = [0]
		i_mass = StartOfPROBLEMCYCLE
		
		while i_mass < EndOfPROBLEMCYCLE:
			if (' problem cycle') in filelines[i_mass]:       
				tmp_timestep = filelines[i_mass+1].strip().split("=")
				SimTimestep.append(float(tmp_timestep[1]))
				if SELECTIVEMASSCALING==1 or SELECTIVEMASSCALING==2:
					tmp_mass = filelines[i_mass+3].strip().split("=") #Added high frequency mass
					SimAddedMassLF.append(float(tmp_mass[1])) #Added high frequency mass
					tmp_mass = filelines[i_mass+5].strip().split("=") #Added high frequency mass
					SimAddedMassHF.append(float(tmp_mass[1])) #Added high frequency mass
				elif SELECTIVEMASSCALING==0:
					tmp_mass = filelines[i_mass+3].strip().split("=") #Added mass
					SimAddedMassLF.append(float(tmp_mass[1])) #Added mass
					
		
				
			i_mass = i_mass + 1
		
		#----------------------------------------------------------------------------
		#----------------------------------------------------------------------------    
		#----------------------------------------------------------------------------
		#Current simulation time step time history
		#----------------------------------------------------------------------------
		SimCurrentTimestep = []
		SimCurrentTime = []
		i_currentTime = StartOfCURRENTTIMESTEP
		
		while i_currentTime < EndOfCURRENTTIMESTEP:
			if (' flush i/o buffers') in filelines[i_currentTime]:
				tmp_timestep = filelines[i_currentTime].strip() #Remove trailing blanks
				tmp_timestep = (" ".join(tmp_timestep.split()).replace(" ",",").split(","))  # Remove intermediate blanks
				SimCurrentTime.append(float(tmp_timestep[2]))
				SimCurrentTimestep.append(float(tmp_timestep[4]))
				
			i_currentTime = i_currentTime + 1        
		#----------------------------------------------------------------------------
		#Plotting of added mass time history and simulation time step size time history
		#----------------------------------------------------------------------------    
	  
		ax1 = plt.subplot(222)
		if SELECTIVEMASSCALING==1 or SELECTIVEMASSCALING==2:
			ax1.plot(SimTimestep, SimAddedMassLF, label="Low frequency mass")
			ax1.plot(SimTimestep, SimAddedMassHF, label="High frequency mass")
			ax1.axis([min(SimTimestep), max(SimTimestep), 0.95*(min(-0.001,min(SimAddedMassLF+SimAddedMassHF))), 1.05*(max(0.001,max(SimAddedMassLF+SimAddedMassHF)))])
		elif SELECTIVEMASSCALING==0:
			ax1.plot(SimTimestep, SimAddedMassLF, label="Added mass")
			ax1.axis([min(SimTimestep), max(SimTimestep), 0.95*(min(-0.001,min(SimAddedMassLF))), 1.05*(max(0.001,max(SimAddedMassLF)))])

		ax1.set_xlabel('Simulation time / ms')
		ax1.set_ylabel('Added mass / %')   
			
			
		ax2 = ax1.twinx()
		SimCurrentTimestep = [i*1000 for i in SimCurrentTimestep]
		ax2.plot(SimCurrentTime, SimCurrentTimestep, label="Time step", color='r')
		ax2.set_ylabel('Time step / ms', color='r')
		ax2.tick_params('y', colors='r')  
		ax2.set_ylim(0.95*min(SimCurrentTimestep),1.05*max(SimCurrentTimestep))
		ax1.set_xlim(min(SimCurrentTime), TERMINATIONtime)
			
		ax1.legend(loc=0)
		plt.title('Change in mass and time step over simulation time')
		
		plt.grid()
		

			
	#----------------------------------------------------------------------------
	#Plotting of energy time history     
	#----------------------------------------------------------------------------    
	ax1 = plt.subplot(223)
	ax1.plot(Time, ENERGYkinetic, label="Kinetic Energy", color='b')
	ax1.plot(Time, ENERGYinternal, label="Internal Energy", color='g')
	ax1.plot(Time, ENERGYhourglass, label="Hourglass Energy", color='c')
	ax1.plot(Time, ENERGYsliding, label="Sliding Interf. Energy", color='y')    
	ax1.plot(Time, ENERGYtotal, label="Total Energy", color='m')
	ax1.legend(loc=0)

	ax1.set_xlabel('Simulation time / ms')
	ax1.set_ylabel('Energy / mJ')      

	ax2 = ax1.twinx()
	EnergyRatio = [(x*100)/y for x, y in zip(ENERGYkinetic, ENERGYinternal)]
	ax2.plot(Time, EnergyRatio, label="Energy ratio", color='r')
	ax2.set_ylabel('Kinetic/Internal Energy ratio / %', color='r')
	ax2.tick_params('y', colors='r')  
	ax2.set_ylim(0,min(100, max(EnergyRatio)))
	ax1.set_xlim(min(SimCurrentTime), TERMINATIONtime)    

	plt.title('Change in energy over simulation time')
	plt.grid()
	plt.tight_layout()
	try:
		plt.savefig(imagedir,dpi=100)
	except:
		plt.show()
	#    
		
	if not EXPLICIT:
		#----------------------------------------------------------------------------
		#----------------------------------------------------------------------------    
		#----------------------------------------------------------------------------
		#Time step history for for Implicit simulations
		#---------------------------------------------------------------------------- 
		#----------------------------------------------------------------------------
		#----------------------------------------------------------------------------    
		#----------------------------------------------------------------------------
		#Current simulation time step time history
		#----------------------------------------------------------------------------
		SimCurrentTimestep = []
		SimCurrentTime = []
		i_currentTime = StartOfCURRENTTIMESTEP
	  
		while i_currentTime < EndOfCURRENTTIMESTEP:
			if (' write d3plot file') in filelines[i_currentTime]:
				tmp_timestep = filelines[i_currentTime].strip() #Remove trailing blanks
				tmp_timestep = (" ".join(tmp_timestep.split()).replace(" ",",").split(","))  # Remove intermediate blanks
				SimCurrentTime.append(float(tmp_timestep[2]))
				SimCurrentTimestep.append(float(tmp_timestep[4]))
				
			i_currentTime = i_currentTime + 1
			
		#----------------------------------------------------------------------------
		#Plotting of simulation time step size time history     
		#----------------------------------------------------------------------------    
		plt.subplot(223)
		plt.plot(SimCurrentTime, SimCurrentTimestep*1000, label="Time step")
		plt.legend(loc=0)
		plt.xlabel('Simulation time / ms')
		plt.ylabel('Time step / ms')
		plt.title('Change in time step over simulation time')
		plt.axis([min(SimCurrentTime), TERMINATIONtime, 0.95*min(SimCurrentTimestep), 1.05*max(SimCurrentTimestep)])
		plt.grid()
		plt.tight_layout()
		
		
		
		#----------------------------------------------------------------------------
		#----------------------------------------------------------------------------    
		#----------------------------------------------------------------------------
		#Convergency iterations for Implicit simulations
		#----------------------------------------------------------------------------        
		Iteration = []
		EquilibrIteration = []
		DisplacementNorm = []
		EnergyNorm = []
		i_implicit = StartOfIMPLICIT
		
		
		while i_implicit < EndOfIMPLICIT:
			if IMPLICIT_NLPRINT2 and (' Iteration:') in filelines[i_implicit]:       
				tmp_timestep = filelines[i_implicit].strip()
				tmp_timestep = (" ".join(tmp_timestep.split()).replace(" ",",").split(","))
				Iteration.append(int(tmp_timestep[1]))
				tmp_displNorm = filelines[i_implicit+2].strip()
				tmp_displNorm =  (" ".join(tmp_displNorm.split()).replace(" ",",").split(","))
				DisplacementNorm.append(float(tmp_displNorm[2])) 
				EnergyNorm.append(float(tmp_displNorm[4])) 
				if len(Iteration)>1:
					if Iteration[-1]-Iteration[-1-1]<0: #Eintragen der Gleichgewichtsinterationen 
						EquilibrIteration.append(Iteration[-1-1])
			elif not IMPLICIT_NLPRINT2 and (' Iteration:') in filelines[i_implicit]:
				tmp_timestep = filelines[i_implicit].strip()
				tmp_timestep = (" ".join(tmp_timestep.split()).replace(" ",",").split(","))
				Iteration.append(int(tmp_timestep[1]))
				tmp_displNorm = filelines[i_implicit].strip()
				tmp_displNorm =  (" ".join(tmp_displNorm.split()).replace(" ",",").split(","))
				DisplacementNorm.append(float(tmp_displNorm[4])) 
				EnergyNorm.append(float(tmp_displNorm[7]))   
				if len(Iteration)>1:
					if Iteration[-1]-Iteration[-1-1]<0: #Eintragen der Gleichgewichtsinterationen
						EquilibrIteration.append(Iteration[-1-1])
	  
				
			i_implicit = i_implicit + 1
	   
		#----------------------------------------------------------------------------
		#Plotting of convergency norm over iteration 
		#----------------------------------------------------------------------------
		i_equilibriumIteration = 0    
			
		plt.subplot(222)
		plt.semilogy(DisplacementNorm, label="Displacement Norm")
		plt.semilogy(EnergyNorm, label="Energy Norm") 
		while i_equilibriumIteration <= len(EquilibrIteration):
			plt.axvline(x=sum(EquilibrIteration[0:i_equilibriumIteration]), linestyle='dashed',color='r')
			i_equilibriumIteration = i_equilibriumIteration + 1
		plt.legend(loc=0)
		plt.xlabel('Iteration')
		plt.ylabel('Norm ratio')
		plt.title('Convergency norm over Iterations')
		plt.axis([0, len(DisplacementNorm), min(EnergyNorm+DisplacementNorm), max(EnergyNorm+DisplacementNorm)])
		plt.grid()
		plt.tight_layout()
		try:
			plt.savefig(imagedir,dpi=100)
		except:
			plt.show()	