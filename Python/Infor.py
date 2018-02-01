# -*- coding: utf-8
'''
Created on %(date)
@author:Yujin Wang
'''
import time
import Copyright
import numpy as np,pandas as pd
from funmodule import *

class basic():
    def __init__(self,*vars,**kwargs):
        try:
            self.src = vars[0]
        except:
            pass

        # self.time = time.strftime('%y-%m-%d %H:%M:%S',time,localtime(time.time()))

class DynaInform(basic):

    @property
    def Pars(self):
        keyword =''
        isDuplicate = 0
        for line in open(self.src):
            data = string_split(line[:-1],' ')
            if '*' in line :
                keyword = 'self.' + data[0][1:]
                if data[0][1:] in dir(TestFile):
                    # print 'Duplicate'
                    isDuplicate = 1
                else:
                    isDuplicate = 0
                    exec(keyword + '=[]')
                # continue
            elif('$' not in line and '*' not in line):
                if isDuplicate == 1:
                    ent = '\n'
                    exec (keyword + ".extend([ent])")
                    exec (keyword + '.extend(line)')
                    isDuplicate = 0
                else:
                    exec (keyword + '.extend(line)')
            else:
                pass
    @statement
    def InfoPrint(self,keywords):
        for kw in keywords:
            # strName = 'TestFile.' + kw
            print kw
            cmd =  'print " ".join(' + 'self.' + kw+ ')'
            exec (cmd)
            print "*"*80+'\n'
         
            


if __name__ == '__main__':
    PATH = r'C:\github\Nastran-master\test/'
    FILE = 'test.key'
    TestFile = DynaInform(PATH+FILE)
    TestFile.Pars
    TestFile.InfoPrint(['PART','SECTION_SHELL_TITLE'])
    print 'ok'
