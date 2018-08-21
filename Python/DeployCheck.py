import Autolivlib as alv

wkdir = r"Y:\cal\01_Comp\02_DAB\385_180725_ESR-040968_DAB_Locking_plate_strength_Yujin\02_run\03_depoloy\002_ASW7_DAB_SW_deployment"
listCheckKey = ['CONTROL_OUTPUT','HOURGLASS','PART','CONTROL_CONTACT','SECTION_SHELL','SECTION_SHELL_TITLE','SECTION_SOLID']
listCheckPart = [100]
ChkResFile = 'CheckResult.txt'

KeyFile = alv.DynaInfo(wkdir,ChkResFile,'key')	#Read more .KEY files
Includefiles = [wkdir+"\\"+i[0] for i in KeyFile.Pars([KeyFile.files[0][0]]).INCLUDE]
KeyFile.Pars(Includefiles)
KeyFile.CheckWrite(listCheckKey,listCheckPart)