# -*- coding: utf-8 -*-
import time
def statement1():
	print ('\n\
			###########################################\n\
			#                                         #\n\
			#        PYSTIFF 4 FEM POST V1.3          #\n\
			#        Author: YujinWang                #\n\
			#        E-MAIL:chaos1984@163.com         #\n\
			#               2016.XMAS                 #\n\
			###########################################\n')

def statement(func):
	def wrapped(*args,**kwargs):
		print ('\n\
				###########################################\n\
				#                                         #\n\
				#        PYSTIFF 4 FEM POST V1.3          #\n\
				#        Copyright @ YujinWang            #\n\
				#        E-MAIL:chaos1984@163.com         #\n\
				#               2016.XMAS                 #\n\
				###########################################\n')
		return func(*args,**kwargs)
	return wrapped

def exeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        print "*****%s, {%s} start*****" % (time.strftime("%X", time.localtime()), func.__name__)
        back = func(*args, **args2)
        print "*****%s, {%s} end*****" % (time.strftime("%X", time.localtime()), func.__name__)
        print "*****%.3fs taken for {%s}*****" % (time.time() - t0, func.__name__)
        return back
    return newFunc
