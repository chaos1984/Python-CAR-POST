# -*- coding: utf-8 -*-
"""
Author:Yujin.Wang
Date:2019.04.07
The lib. is used to translate the F-D curve to MAT24 effective plastic strain - true stress.
Usage:
MAT89LCSS(fdfile,A,l0) 
return TrueStrain,TrueStress,[PeakStrain,PeakStress]
MAT24LCSS(truestrain,truestress,yieldpoint=0.02,Ymould_user=0,Peak=[0,0],strainturn=0,scaleturn=1,curvescale=1,ratio=1,extend=0,scaleextend=0,alignstrain=1.45,pointnum=50):
return x_eps_mod,y_eps_mod
CurveKey(A,l0,FDfile,strain_rate,curvenum,ratio,Ymould_user,yieldpoint,pointnum,strainturnlist,scaleturnlist,curvescalelist,alignstrain,extend,scaleextend):
No return
################################################################################
Parameters:
    A - float, Specemen Crosssection area
	l0 - float, Gage lengrh
    FDfile - Filename, Force-Disp curve
    strain_rate - list, Strain rate
    curvenum - int, Curve number in .key file
    ratio - float, Display ratio
#################################User Define###################################
    Ymould_user - float, Young modulus
    yieldpoint - float, Yield point
    pointnum - int, the number of output points
    strainturnlist - list, Turn strain 
    scaleturnlist - list,  Scale of the turn strain 
    curvescalelist - list, Curve scale equalent to SFO
    alignstrain - float, align the strain to user defined value(>max(strainturnlist))
    extend - float, Extend strain to a user defined value
    scaleextend - float, Scale of the extend strain 
"""
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate,optimize
import scipy.signal as signal


def ConditionRemove(data,condition):
    a =[]
    isflag = 1
    string ="if "+ condition +":\n"
    string +="                     for k in range(len(data)):\n   \
                        data[k].pop(i+1)\n   \
                  isflag = 1\n"
    while isflag == 1:
        a.extend(data)
        len0 = len(a[0])
        try:
            for i in range(len(a[0])):
                exec(string)
        except:
            if len(data[0]) == len0:
                break
    return data

    
def CowperSymondsFunc(x,c,p):
    rate,ES0 = x
    return ES0*(1+np.power((rate/c),1./p))


    

def MAT89LCSS(fdfile,A,l0):
    data = pd.read_csv(fdfile)
    x = data.Disp
    y = data.Force
    EngStrain = x/l0
    EngStress = y/A
    EngStressFilt =  pd.Series(signal.medfilt(EngStress,201))
    PeakStress = max(EngStressFilt[:800])
    PeakStrain = EngStrain[EngStressFilt[:800].idxmax()]
    print "PeakStress:%f\tPeakStrain:%f\t Elastic modulus:%f" %(PeakStress,PeakStrain,PeakStress/PeakStrain)
    plt.figure(1)
    plt.grid("on")
    plt.scatter(PeakStrain,PeakStress, marker='o')
    plt.title("Engineering Strain VS. Engineering Stress Curve")
    plt.xlabel("Engineering Strain[-]")
    plt.ylabel("Engineering Stress[GPa]")
#    plt.xticks([])
#    plt.yticks([])
#    plt.plot(PeakStrain,PeakStress,'p')
    plt.plot(EngStrain,EngStressFilt)
#    plt.plot(EngStrain,EngStressFilt,'--')
    plt.legend(["0.001mm/ms","0.01mm/ms","0.1mm/ms","1mm/ms"])
    TrueStrain =  np.log(1+EngStrain)
    TrueStress = EngStressFilt*(1+EngStrain)
    plt.figure(2)
#    plt.plot(EngStrain,EngStress,'b')
    plt.grid("on")
    plt.title("True Strain VS. True Stress Curve")
#    plt.xticks([])
#    plt.yticks([])
    plt.xlabel("True Strain[-]")
    plt.ylabel("True Stress[GPa]")
    plt.plot(TrueStrain,TrueStress)
    plt.legend(["0.001mm/ms","0.01mm/ms","0.1mm/ms","1mm/ms"])
    return TrueStrain,TrueStress,[PeakStrain,PeakStress]

def MAT24LCSS(x,y,yieldpoint=0.02,Ymould_user=0,Peak=[0,0],strainturn=0,scaleturn=1,curvescale=1,ratio=1,extend=0,scaleextend=0,alignstrain=1.45,pointnum=50,smoothflag=1):
    print " User defined Ymould:",Ymould_user
    y_eps = []
    x_eps = []
    for index,value in enumerate(x):
        if value >= yieldpoint and (value > x[index-1] or y[index]>y[index-1]):
            x_eps.append(value - y[index]/Ymould_user)
            y_eps.append(y[index])
    plt.figure(3)
    displayratio = int(len(x_eps)*ratio)
    plt.plot(x_eps[:displayratio],y_eps[:displayratio],'--')
    x_eps_mod =[0] 
    y_eps_mod = [y_eps[0]/3.]
    delta = int(len(x_eps)/pointnum)
    x_eps_mod.extend( [value for index,value in enumerate(x_eps) if index%delta==0]);y_eps_mod.extend([value for index,value in enumerate(y_eps) if index%delta==0])
    for index,value in enumerate(x_eps_mod):
        if value > strainturn:
            y_eps_mod[index]= y_eps_mod[index-1]+scaleturn*(x_eps_mod[index]-x_eps_mod[index-1])
        else:
            continue
    if x_eps_mod[-1] < alignstrain:
        x_eps_mod.append(alignstrain)
        y_eps_mod.append(y_eps_mod[-1]+scaleturn*(x_eps_mod[-1]-x_eps_mod[-2]))
    for index,value in enumerate(x_eps_mod):
        y_eps_mod[index] = y_eps_mod[index]*curvescale
    if extend != 0:
        x_eps_mod.append(x_eps_mod[-1]+extend)
        y_eps_mod.append(y_eps_mod[-1]+extend*(scaleextend))
        plt.title("Modified Effective Plastic Strain VS. Stress Curve")
    plt.xlabel("Effective Plastic Strain[-]")
    plt.ylabel("Stress[GPa]")
    plt.grid('on')
    if smoothflag == 1:
        print "The curve has been smoothed!"
        f = interpolate.interp1d(x_eps_mod,y_eps_mod,kind='cubic')
        x_eps_smooth = np.linspace(x_eps_mod[0],x_eps_mod[-1],pointnum)
        y_eps_smooth = f(x_eps_smooth)
        plt.plot(x_eps_smooth[:displayratio],y_eps_smooth[:displayratio])
        plt.legend(["Strain Rate 0.001/ms","Modified Strain Rate 0.001/ms","Strain Rate 0.01/ms","Modified  Strain Rate 0.01/ms","Strain Rate 0.1/ms","Modified Strain Rate 0.1/ms","Strain Rate 1/ms","Modified Strain Rate 1/ms",])
        return x_eps_smooth,y_eps_smooth
    elif smoothflag == 0:
        plt.plot(x_eps_mod[:displayratio],y_eps_mod[:displayratio])
        plt.legend(["Strain Rate 0.001/ms","Modified Strain Rate 0.001/ms","Strain Rate 0.01/ms","Modified  Strain Rate 0.01/ms","Strain Rate 0.1/ms","Modified Strain Rate 0.1/ms","Strain Rate 1/ms","Modified Strain Rate 1/ms",])
        return x_eps_mod,y_eps_mod

def CurveKey(A,l0,FDfile,strain_rate,curvenum,ratio,Ymould_user,yieldpoint,pointnum,strainturnlist,scaleturnlist,curvescalelist,alignstrain,extend,scaleextend,smooth=0):
    fout = open("Curve.key",'w')
    fout.write('*KEYWORD\n')
    fout.write('$ Created: ' + time.strftime("%d.%m.%Y %H:%M:%S") + '\n')
    fout.write('$ Parameters:\n$ A:%f\n$ l0:%f\n$ Young modulus:%f\n$ Yield point:%f\n$ Alignstrain:%f\n$ Extend strain:%f\n$ Scaleextend:%f\n' %(A,l0,Ymould_user,yieldpoint,alignstrain,extend,scaleextend))
    fout.write("$ Control List:\n$ Strain turning:%s\n$ Strain scaleturn:%s\n$ Curvescale:%s\n" %(str(strainturnlist),str(scaleturnlist),str(curvescalelist)))
    fout.write("*DEFINE_TABLE\n%d\n" %(curvenum))
    for i in strain_rate:
        fout.write("%f\n" %(i))    
    for index,File in enumerate(FDfile):
        curvenum += 1
        strainturn = strainturnlist[index];scaleturn = scaleturnlist[index];curvescale = curvescalelist[index]
        x,y,peak = MAT89LCSS(File,A,l0) 
        x_fit,y_fit= MAT24LCSS(x,y,yieldpoint=yieldpoint,Ymould_user=Ymould_user,Peak=peak,strainturn=strainturn,scaleturn=scaleturn,curvescale=curvescale,ratio=ratio,extend=extend,scaleextend=scaleextend,alignstrain =alignstrain,pointnum=pointnum,smoothflag=smooth)    
        fout.write('*DEFINE_CURVE_TITLE\nRate %.5f\t%s\n' %(pow(np.e,strain_rate[index]),File))
        fout.write('$     LCID      SIDR       SFA       SFO      OFFA      OFFO    DATTYP\n')
        fout.write('      %d         0    1.0000&scale        0.0000    0.0000\n' %(curvenum))
        for i in range(len(x_fit)):
            fout.write("%f,%f\n" %(x_fit[i],y_fit[i]))
    fout.write("*END\n")
    fout.close()
#    plt.show()


if __name__ == '__main__':
    A = 30; l0 = 30 #样件截面积，标距
    FDfile = ["test10.txt","test100.txt","test1000.txt","test10000.txt"]#力位移曲线
    strain_rate = [-6.907,-4.605,-2.302,0] #力位移曲线对应的应变率
    curvenum = 2350 #key文件中曲线的编号起始编号
    ratio = 1 #显示比例
#################################User Define###################################
    Ymould_user = 1.5 #定义弹性模量
    yieldpoint= 0.100 #屈服点（避开交叉区域）
    pointnum = 80     #输出点的个数
    strainturnlist=[1.3,1.3,1.35,0.9]#指定每根曲线发生转折的应变
    scaleturnlist=[0.08,0.08,0.06,0.0450];#指定每根曲线发生转折的比例
    curvescalelist = [1,1.05,1.05,1.1]#指定每个区县整体偏移的比例
#    strainturnlist=[1.2,1.2,1.2,0.75];scaleturnlist=[0.06,0.06,0.055,0.050];curvescalelist = [1,1.,1.05,1.05]
    alignstrain = 1.45#应力应变曲线对齐的位置（应变值）
    extend = 0.5     #对齐后曲线延长距离（应变值）
    scaleextend=0.08 #延长段的增量
#################################User Define###################################
    CurveKey(A,l0,FDfile,strain_rate,curvenum,ratio,Ymould_user,yieldpoint,pointnum,strainturnlist,scaleturnlist,curvescalelist,alignstrain,extend,scaleextend)
    ratelist = [np.power(np.e,i) for i in strain_rate]
    y_p = []
    x_eps=[];y_eps=[]
    for index,File in enumerate(FDfile):
        x,y,peak = MAT89LCSS(File,A,l0)
        y_p.append(peak[1])
        if index == 0:
            print type(x.tolist())
            x0,y0 = ConditionRemove([x.tolist(),y.tolist()],"(a[0][i]>=a[0][i+1] or a[1][i]>=a[1][i+1])")
    popt,pcov = optimize.curve_fit(CowperSymondsFunc,[ratelist,y_p[0]],y_p,[1,1])
    c,p = popt
    print 'c:',c
    print 'p:',p
    plt.figure(5)
    plt.scatter(ratelist,y_p,color='r',marker='*')
    y_p_fit=CowperSymondsFunc([ratelist,y_p[0]],c,p)
    plt.scatter(ratelist,y_p_fit)
#    x_eps_fit = np.linspace(0,x.tolist()[-1],pointnum)
    plt.figure(3)
    delta = int(len(x0)/pointnum)-1
    print delta
    fout = open("Curve.key",'w')
    fout.write('*KEYWORD\n')
    fout.write("*DEFINE_TABLE\n%d\n" %(curvenum))
    for i in strain_rate:
        fout.write("%f\n" %(i))    
    for rate in ratelist:
        curvenum += 1
        y_eps_fit = CowperSymondsFunc([rate,np.array(y0)],c,p)
        fout.write('*DEFINE_CURVE_TITLE\nRate %.5f\n' %(rate))
        fout.write('$     LCID      SIDR       SFA       SFO      OFFA      OFFO    DATTYP\n')
        fout.write('      %d         0    1.0000    1.0000    0.0000    0.0000\n' %(curvenum))
        for i in range(pointnum):
            fout.write("%f,%f\n" %(x0[i*delta],y_eps_fit[i*delta]))
        plt.plot(x0,y_eps_fit,dashes=[2, 2, 10, 2])
    fout.write("*END\n")
    # plt.show()
    
#    x,y = CowperSymondsCurve(FDfile[0],A,l0,Ymould_user,80,ratelist,x_p,y_p)
