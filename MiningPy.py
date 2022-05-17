import numpy as np
from sympy import symbols, solve
import matplotlib.pyplot as plt
from astropy.table import Table
import random

def Pillar_Strength(wh, formula =[], name =[]):
    S=[]
    i=0
    while (i<len(formula)):
        s= formula[i](wh)
        S.append(s)
        print ("Pillar Strength for", name[i],":",s)
        i=i+1
    return S;

def FoS_calculate(P,wh,formula=[],name=[]):
    S = Pillar_Strength(wh, formula, name)
    FoS=[]
    i=0
    while (i<len(formula)):
        f = S[i]/P
        FoS.append(f)
        print ("FoS for", name[i],":",f)
        i=i+1
    return FoS,S,name;

def wh_calculate(P,FoS,formula=[],name=[]):
    S= P*FoS
    w =symbols('w')
    wh=[]
    i=0
    while (i<len(formula)):
        sn=solve (formula[i](w)-S,w)
        def largest(a,n):
            max=a[0]
            for i in range(1,n):
                if a[i]>max:
                    max = a[i]
            return max;
        n=len(sn)
        sol = largest(sn,n)
        wh.append(sol)
        print ("w/h ratio for", name[i],":",sol)
        i=i+1
    return FoS,S,name;
 
def FoS_Range(P,FoS_max, FoS_min, interval,formula,name):
    n = (FoS_max-FoS_min)/interval
    a =FoS_min
    F=[FoS_min]
    i=0
    while(i<n):
        a= a+interval
        F.append(a)
        i=i+1
    S=[]
    i=0
    while(i<n+1):
        b=P*F[i]
        S.append(b)
        i=i+1
    wh =[]
    w =symbols('w')
    i=0
    while(i<(n+1)):
        sni=solve (formula[0](w)-S[i],w)
        def largest(a,ni):
            max=a[0]
            for y in range(0,ni):
                if a[y]>max:
                    max = a[y]
            return max;
        ni=len(sni)
        sol = largest(sni,ni)
        wh.append(sol)
        i=i+1
    wh=np.asarray(wh)
    F=np.asarray(F)
    wh.astype(int)
    F.astype(int)
    plt.style.use('seaborn-darkgrid')
    #plt.figure(figsize=())
    plt.plot(F,wh,'r^')
    plt.xlabel("FoS")
    plt.ylabel(name)
    t = Table([F,wh],names=('FoS',name))
    print(t)
    return t,F,wh;
  
def FoS_wh_Range(P,FoS_max, FoS_min, interval,wh_max,wh_min,formula,name):
    n = (FoS_max-FoS_min)/interval
    a =FoS_min
    F=[FoS_min]
    i=0
    while(i<n):
        a= a+interval
        F.append(a)
        i=i+1
    S=[]
    i=0
    while(i<n+1):
        b=P*F[i]
        S.append(b)
        i=i+1
    wh =[]
    w =symbols('w')
    i=0
    while(i<(n+1)):
        sni=solve (formula[0](w)-S[i],w)
        def largest(a,ni):
            max=a[0]
            for y in range(0,ni):
                if a[y]>max:
                    max = a[y]
            return max;
        ni=len(sni)
        sol = largest(sni,ni)
        wh.append(sol)
        i=i+1
    wh=np.asarray(wh)
    F=np.asarray(F)
    wh.astype(int)
    F.astype(int)
    w=np.delete(wh,np.argwhere(wh>=wh_max))
    F1=np.delete(F,np.argwhere(wh>=wh_max))
    w=np.delete(w,np.argwhere(wh<=wh_min))
    F=np.delete(F1,np.argwhere(wh<=wh_min))
    np.savetxt('/content/FoS_vs_w:h_ratio.csv', np.vstack([F,w]).transpose(), delimiter=',', header='FoS,w/h_ratio', comments='')
    plt.style.use('seaborn-darkgrid')
    #plt.figure(figsize=())
    plt.plot(F,w,'r^')
    plt.xlabel("FoS")
    plt.ylabel(name)
    t = Table([F,w],names=('FoS',name))
    print(t)
    return t,F,w;
  
def roof_bolting(gallery_width,avg_density,RMR,bolts, spacing_max,spacing_min,bolt_type,ran_num):
  ran = np.random.random(ran_num)
  spacing=[]
  for i in range(len(ran)):
    interval= ran[i] * (spacing_max - spacing_min)
    spacing.append(interval+spacing_min)
  spacing=np.asarray(spacing)
  roof_load = gallery_width * avg_density* (1.7 - 0.037*RMR + 0.0002*RMR*RMR)
  if bolt_type== 'QSC':
    load_bearing = 8
  FoS = bolts* load_bearing / (roof_load*gallery_width*spacing)
  x=np.array(range(0, len(FoS)))
  plt.title("Factor of Safety")
  plt.xlabel("Random Samples Count")
  plt.ylabel("FoS")
  #plt.plot(x, FoS, color = "red", marker = "r^")
  plt.style.use('seaborn-darkgrid')
  plt.plot(x, FoS,'r^')
  #plt.axhline(y=threshold, xmin=FoS.min(), xmax=FoS.max())
  #plt.legend()
  plt.show()
  print("Maximum :",FoS.max())
  print("Minimum :",FoS.min())
  print("Mean :",FoS.mean())
  print("50th percentile : ",
       np.percentile(FoS, 50))
  print("25th percentile : ",
       np.percentile(FoS, 25))
  print("75th percentile : ",
       np.percentile(FoS, 75))
  print("97.5 percentile : ",
       np.percentile(FoS, 97.5))
  print("2.5 percentile : ",
       np.percentile(FoS, 2.5))

def lead_distance_time_wasted_saved(lead_distance_old, lead_distance_new, cycle_time,
                                    speed_max, speed_min, number_of_rounds, ran_num):
  if lead_distance_new>lead_distance_old:
    extra_distance = lead_distance_new - lead_distance_old
    time = True
  else:
    extra_distance = lead_distance_old - lead_distance_new
    time= False
  ran = np.random.random(ran_num)
  speed=[]
  for i in range(len(ran)):
    interval= ran[i] * (speed_max - speed_min)
    speed.append(interval+speed_min)
  speed=np.asarray(speed)
  time_waste= cycle_time* extra_distance/speed
  time_waste= time_waste*number_of_rounds
  time_waste=time_waste/60
  x=np.array(range(0, len(time_waste)))
  if time == True:
    time1 = 'Plotting Time Wasted'
  else:
    time1 = 'Plotting Time Saved'
  plt.title(time1)
  plt.xlabel("Random Samples Count")
  plt.ylabel("Time (hours)")
  plt.style.use('seaborn-darkgrid')
  plt.plot(x, time_waste,'r^')
  #plt.legend()
  plt.show()
  print("Maximum :",time_waste.max())
  print("Minimum :",time_waste.min())
  print("Mean :",time_waste.mean())
  print("50th percentile : ",
       np.percentile(time_waste, 50))
  print("25th percentile : ",
       np.percentile(time_waste, 25))
  print("75th percentile : ",
       np.percentile(time_waste, 75))
  print("97.5 percentile : ",
       np.percentile(time_waste, 97.5))
  print("2.5 percentile : ",
       np.percentile(time_waste, 2.5))
  
def BSA_experiment(weight_max, weight_min, height_max, height_min, ran_num):
  ran = np.random.random(ran_num)
  weight=[]
  for i in range(len(ran)):
    interval= ran[i] * (weight_max - weight_min)
    weight.append(interval+weight_min)
  weight=np.asarray(weight)

  ran = np.random.random(ran_num)
  height=[]
  for i in range(len(ran)):
    interval= ran[i] * (height_max - height_min)
    height.append(interval+height_min)
  height=np.asarray(height)
  BSA = 0.007184 * (np.power(weight,0.425)) * (np.power(height,0.725))
  #print(BSA)
  x=np.array(range(0, len(BSA)))
  plt.title("BSA")
  plt.xlabel("Random Samples Count")
  plt.ylabel("BSA (sq. m)")
  plt.style.use('seaborn-darkgrid')
  plt.plot(x, BSA,'r^')
  #plt.legend()
  plt.show()
  print("Maximum :",BSA.max())
  print("Minimum :",BSA.min())
  print("Mean :",BSA.mean())
  print("50th percentile : ",
       np.percentile(BSA, 50))
  print("25th percentile : ",
       np.percentile(BSA, 25))
  print("75th percentile : ",
       np.percentile(BSA, 75))
  print("97.5 percentile : ",
       np.percentile(BSA, 97.5))
  print("2.5 percentile : ",
       np.percentile(BSA, 2.5))
