import Autolivlib as alv

wkdir = r"C:\Users\chaos\Desktop\temp"
listCheckKey = ['PART']
listCheckPart = [100]
ChkResFile = 'CheckResult.txt'

KeyFile = alv.DynaInfo(wkdir,ChkResFile,'key')	#Read more .KEY files
Includefiles = [wkdir+"\\"+i[0] for i in KeyFile.Pars([KeyFile.files[0][0]]).INCLUDE]
KeyFile.Pars(Includefiles)
#print dir(KeyFile)
#KeyFile.CheckWrite(listCheckKey,listCheckPart)
listPartInfo = KeyFile.PartInfo()
KeyFile.GraphStru(listPartInfo)