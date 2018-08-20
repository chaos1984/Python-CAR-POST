import Autolivlib as alv

wkdir = r"C:\Users\chaos\Desktop\temp"
checklist = ['CONTROL_OUTPUT','HOURGLASS']
ChkResFile = 'CheckResult.txt'

KeyFile = alv.DynaInfo(wkdir,ChkResFile,'key')	#Read more .KEY files
Includefiles = [i[0] for i in KeyFile.Pars([KeyFile.files[0][0]]).INCLUDE]
KeyFile.Pars(Includefiles)
KeyFile.CheckWrite(checklist)