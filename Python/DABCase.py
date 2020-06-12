#coding:utf-8
import os
import sys
import time
import logging
from Autolivlib import *

switcher = {"1":["UL_HT","UL_RT","UL_LT"],"2":["UL_HT","UL_RT","UL_LT",'LL_LT'],"3":["UL_HT","UL_RT","UL_LT","LL_LT","NL_HT","NL_RT","NL_LT"]}
temperature = {"1":["85","23","35"],"2":["85","23","35","35"],"3":["85","23","35","35","85","23","35"]}
singleinflator = ["ADP1.3B_MP_Upper_limit_HT_Correlated_20151222.k","ADP1.3B_MP_Upper_limit_RT_Correlated_20151222.k","ADP1.3B_MP_Upper_limit_LT_Correlated_20151222.k","ADP1.3B_MP_Lower_limit_LT_Correlated_20151222.k","ADP1.3B_MP_Normal_limit_HT_Correlated_20151222.k","ADP1.3B_MP_Normal_limit_RT_Correlated_20151222.k","ADP1.3B_MP_Normal_limit_LT_Correlated_20151222.k"]
dualinflator = ["ADPS-1.5_210kPa_41C424_Jean-YvesBurel_5ms_UL_HT_20140204.key","ADPS-1.5_210kPa_41C424_Jean-YvesBurel_5ms_UL_RT_20140204.key","ADPS-1.5_210kPa_41C424_Jean-YvesBurel_5ms_UL_LT_20140204.key","ADPS-1.5_210kPa_IBC_41p5_9gm_FSO_cold_mmkgms.key"]
inflatortype = raw_input("Please select inflator:\n1.Single\n2.Dual\nInput:\t")
case = raw_input("Please select the cases:\n1.3 UL\n2.3 UL & LL_LT\n3.3 UL & 3 NL & LL_LT\nInput(Item 3 is not use in Dual inflators):\t")
temp_file = FindFile(os.curdir,"key")[0][0]

isflag = 0
for i,filedir in enumerate(switcher[case]):
	try:
		os.mkdir(filedir)
	except:
		raw_input("Please check the duplicate directory:  %s" %(filedir))
		break
	fout = open(filedir+"//%s.key" %(filedir),"w")
	for line in open(temp_file):
		if "*INCLUDE_PATH" in line:
			isflag = 1
			fout.write(line)
		elif "*" in line and isflag == 1:
			fout.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$AutoGenerater$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
			fout.write("*PARAMETER\n")
			fout.write("I TEMP            %s\n" %(temperature[case][i]))
			print (inflatortype)
			if inflatortype == "1":
				fout.write("*INCLUDE\n%s\n" %(singleinflator[i]))
			elif inflatortype == "2":
				fout.write("*INCLUDE\n%s\n" %(dualinflator[i]))
			fout.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$END$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
			fout.write(line)
			isflag = 0
		else:
			fout.write(line)
	fout.close()
raw_input("wait")