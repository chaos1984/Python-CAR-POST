##----------------------------------------------------------------------------
##----------------------------------------------------------------------------
##----------------------------------------------------------------------------
##----------------------------------------------------------------------------
##----------------------------------------------------------------------------
# Python snippet to parse d3hsp file from dyna run, to check for
#  -smallest element timesteps
#  -added mass during simulation rund
#  -time step during simulation rund
#  -Energy time historys
#  -Implicit/Explicit parsing

# v1.1
#  - Implementation of an error msg box
#  - known issue: Not working for beam-dominated smallest timestep

# v1.2
# - Fixed bug while extacting smallest timestep if beam or axial element are used

# v1.3
# - Added information of PID controlling min. timesteps
#  
# Author: Stefan Schilling, ANG
# Version: 1.3
# Date: 09.01.18
##----------------------------------------------------------------------------
##----------------------------------------------------------------------------
##----------------------------------------------------------------------------
import os,sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import Tkinter as tk
import sys
from scipy import stats
    
sys.path.append('Y:\cal\01_Comp\02_DAB\401_181025_ESR-045011_Chery_T1C_DAB_2rd_Yujin\02_run\UL_RT')

#filein = sys.argv[1]
filein = r"Y:\cal\01_Comp\02_DAB\401_181025_ESR-045011_Chery_T1C_DAB_2rd_Yujin\02_run\UL_RT\d3hsp"
fileinGLAST = r"Y:\cal\01_Comp\02_DAB\401_181025_ESR-045011_Chery_T1C_DAB_2rd_Yujin\02_run\UL_RT\glstat"
fileinMATSUM =r"Y:\cal\01_Comp\02_DAB\401_181025_ESR-045011_Chery_T1C_DAB_2rd_Yujin\02_run\UL_RT\matsum"

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
root = tk.Tk() 
width_mm = root.winfo_screenmmwidth()
height_mm = root.winfo_screenmmheight() 

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
	SmallestTimesteps_array[i_smallesttimesteps,2]=float(tmp[-1]) #"Time step"
	
	i_smallesttimesteps = i_smallesttimesteps + 1

	
 #----------------------------------------------------------------------------
#Applied mass scaled time step
#----------------------------------------------------------------------------
if MASSSCALING:
	tmp=AppliedMASSSCALING.strip() #Remove trailing blanks
	tmp=(" ".join(tmp.split()).replace(" ",",").split(",")) #Remove intermediate blanks 
	AppliedMASSSCALING = float(tmp[9])*-1
	if AppliedMASSSCALING == 0.0:
		MASSSCALING = False
						   
						   
#----------------------------------------------------------------------------
#Cricitcal contact time step
#----------------------------------------------------------------------------                           
if CONTACTTIMESTEP:
	tmp=ContactTIMESTEP.strip() #Remove trailing blanks
	tmp=(" ".join(tmp.split()).replace(" ",",").split(",")) #Remove intermediate blanks 
	ContactTIMESTEP = float(tmp[8])  


#----------------------------------------------------------------------------
#Plotting of histogram for smallest element time steps
#----------------------------------------------------------------------------
plt.subplot(221)
plt.hist(SmallestTimesteps_array[:,2],bins=30)
if MASSSCALING:
	plt.axvline(x=AppliedMASSSCALING,linestyle='dashed',color='b', label='Mass scaled time step='+str(AppliedMASSSCALING)+'s')
if CONTACTTIMESTEP:
	plt.axvline(x=ContactTIMESTEP,linestyle='dashed',color='r',label='Contact time step='+str(ContactTIMESTEP)+'s')
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
plt.xlabel('Time step size / s')
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

	ax1.set_xlabel('Simulation time / s')
	ax1.set_ylabel('Added mass / %')   
		
		
	ax2 = ax1.twinx()
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
	plt.plot(SimCurrentTime, SimCurrentTimestep, label="Time step")
	plt.legend(loc=0)
	plt.xlabel('Simulation time / s')
	plt.ylabel('Time step / s')
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
	plt.show() 		
		

	  
