# -*- coding: utf-8 -*-
import numpy as np
class DSGZ_model():
	def __init__(self,*args):
		# try:
			# print ('here',args[0])
			self.strain = args[0]
			self.K = args[1][0]
			self.c1 = args[1][1]
			self.c2 = args[1][2]
			self.c3 = args[1][3]
			self.c4 = args[1][4]
			self.a = args[1][5]
			self.m =  args[1][6]
			self.alpha = args[1][7]
			self.strainrate = float(args[2])
			print ('K\tc1\tc2\tc3\tc4\ta\tm\talpha\t')
			print (args[1])
			# for i in args[1]:
				# print (str(i)+'\t')
		# except:
			# print ('ERROR: DGSZ model parameters are not correct!')
			# print (args[0][0:])
	def f_strain(self):
		return (np.power(np.e,-self.c1*self.strain) + np.power(self.strain,self.c2))*(1.-np.power(np.e,-self.a*self.strain))

	def h_strainrate_T(self):
		return np.power(self.strainrate,self.m)*np.power(np.e,self.alpha/296.)

	def DSGZ(self):
		f = self.f_strain()
		h = self.h_strainrate_T()
		value = self.K * ( f + (self.strain*np.power(np.e,(1.-self.strain/(self.c3*h)))/(self.c3*h)-f) * np.power(np.e,(np.log(h)-self.c4)*self.strain))*h
		return value

			