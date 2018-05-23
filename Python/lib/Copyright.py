# -*- coding: utf-8 -*-
def statement(func):
	def wrapped(*args,**kwargs):
		print ('				###########################################\n\
				#                                         #\n\
				#        PYSTIFF 4 FEM POST V1.2          #\n\
				#        Copyright @ YujinWang            #\n\
				#        E-MAIL:chaos1984@163.com         #\n\
				#               2016.XMAS                 #\n\
				###########################################\n')
		return func(*args,**kwargs)
	return wrapped