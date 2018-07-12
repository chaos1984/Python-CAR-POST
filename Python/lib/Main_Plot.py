import sys
import os 
from DynaData import *
import matplotlib.pyplot as plt
import Post
import Copyright

@try_except
def DeforcPlot(wkdir,figures):
	imagedir = wkdir+'\\image'
	if not os.path.exists(imagedir):
		os.mkdir(wkdir +'\\image')
	file = r'\\deforc'

	TestFile = Deforce(wkdir+file,0,0,0,0)
	res = TestFile.run
	res = res.T
	
	figure_res = [0,0,0]
	for i in range(figures):
		PltData = res[res['spr_dam']==res['spr_dam'][i]]
		PltData = PltData[['Time','rf']]
		# PltData = PltData[PltData.index<PltData['rf'].idxmax()+10]
		fig_pos = '1' + str(figures) +  str(i+1)
		Tittle = 'Spring:'+str(int(res['spr_dam'][i]))
		res_plot = Post.CurvePlot(Tittle,'Time','Force(kN)',1,1,fig_pos,0.3,PltData)
		res_plot.frame
		temp = list(res_plot.maxmin())
		
		if figures == 2:
			if temp[0] > figure_res[0] :
				figure_res[1:] = temp[1:]
			figure_res[0] += temp[0]

		else:
			figure_res = temp
		# break
	pic = wkdir+'\image'+file
	plt.savefig(pic,dpi=100)
	print '#'*20
	print  'DEFORC is plotted: %s'%(pic )
	print '#'*20
	return figure_res
	
@try_except
def GlstatPlot(wkdir):
	imagedir = wkdir+'\\image'
	if not os.path.exists(imagedir):
		os.mkdir(wkdir +'\\image')
	file = r'\\glstat'
	TestFile =Glstate(wkdir+file,0,0,0,0)
	res = TestFile.run
	PltData = res[['time','kinetic energy','internal energy','total energy','external work']]
	res_plot = Post.CurvePlot(' ','time','kinetic energy',-1,1,111,0.3,PltData,legend=True)
	res_plot.frame
	res_plot.maxmin()
	pic = wkdir+'\image'+file
	# plt.show()
	plt.savefig(pic,dpi=100)
	print '#'*20
	print  'GLSTAT is plotted: %s'%(pic)
	print '#'*20

if __name__ == '__main__':
	wkdir = "Y:\\cal\\01_Comp\\04_SB\\548-180423_ESR_038127_CTR_BUK_Bracket_Strength_Yujin\\02_run"
	figures = 1
	DeforcPlot(wkdir,figures)
	GlstatPlot(wkdir)

	
