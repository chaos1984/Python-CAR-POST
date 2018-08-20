import os
import sys
import Autolivlib as alv

wkdir = r"Y:\cal\01_Comp\02_DAB\385_180725_ESR-040968_DAB_Locking_plate_strength_Yujin\02_run\03_depoloy\_20180816_"
MainFile = alv.FindFile(wkdir, 'key')[0]
print MainFile[0]
KeyFile = alv.ReadKeys(MainFile[0])	#Read more .KEY files
