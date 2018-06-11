from Infor import *
starttime = datetime.datetime.now()
print starttime
PATH = r'Y:\cal\01_Comp\09_NVH\378_180319_ESR-036949_Simulation_virbration_fixture_Opt_Yujin\02_Run\opt3'
FILE = '\solve.pch'
TestFile = OptistructInfo(PATH+FILE)

TestFile.ParsPCH('EIGENVALUE')
endtime = datetime.datetime.now()
print endtime

print (endtime - starttime)

PltData = pd.DataFrame(TestFile.res,columns = ['Order','Frequence','maxVector','AllowableTestFrequence'])
res_plot = CurvePlot(' ','Order','maxVector','b',1,1,111,PltData[ ['Order','maxVector']])
res_plot.frame
x=[1,max(PltData['Order'])]
y=[0.05,0.05]
plt.plot(x,y,'r')
plt.show()
print 'The allowable test frequence: %f Hz.' %(min(PltData.AllowableTestFrequence))
