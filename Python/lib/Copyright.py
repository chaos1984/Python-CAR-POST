# -*- coding: utf-8 -*-
import time
import sys,traceback
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
		
def get_decorator(errors=(Exception, ), default_value=''):

    def decorator(func):

        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors, e:
                print "Error! %s" %( func.__name__), repr(e)
                return default_value

        return new_func

    return decorator

# @get_decorator
def example1(a):
		return a['b']		


def try_except(f):
    def handle_problems(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
            message = '\n{0}\n{1}:\n{2}'.format(
                formatted_traceback,
                exc_type.__name__,
                exc_instance
            )
#             raise exc_type(message)
            raw_input(exc_type(message))

        finally:
            pass
    return handle_problems

		
@try_except
def  chu(x, y):
    return(x/y)		
if  __name__ == '__main__':
	chu(1,0)