import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math

df = pd.read_csv('/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange.csv', header=3)

#print(df)

#print(df.columns[6:16])
def TAC(df, x):
    organes=df.columns[6:16]
    Ainit= 15.22
    ActInt=np.zeros(len(organes))
    ActInt_corr=np.zeros(len(organes)) 
    ActInt_act=np.zeros(len(organes))
    ActExt=np.zeros(len(organes)) 
    ActExt_corr=np.zeros(len(organes))
    ActExt_act=np.zeros(len(organes)) 

    for idx, i in enumerate(organes):
        y_pourc = df[i]#*Ainit/100
        y_act = y_pourc*Ainit/100
        y_corr = y_act.copy()
        #print(y,y[len(y)-1])
        ActExt_corr[idx]=y_pourc[len(y_pourc)-1]*110/math.log(2)
        #print(ActExt_noncorr)
        for j in range (1, len(x)):
            y_corr[j]=y_act[j]*(np.exp(-(x[j])*math.log(2)/110))
            T_corr=(x[j+1]-x[j])*(y_corr[j+1]+y_corr[j])/2
            T=(x[j+1]-x[j])*(y_pourc[j+1]+y_pourc[j])/2
            T_act=(x[j+1]-x[j])*(y_act[j+1]+y_act[j])/2
            ActInt[idx]=ActInt[idx]+T
            ActInt_corr[idx]=ActInt_corr[idx]+T_corr
            ActInt_act[idx]=ActInt_act[idx]+T_act
        #y_corr=(y*np.exp(-x*math.log(2)/110))
        #ActInt[idx]=ActInt[idx]+x[len(x)]-x[len(x)-1]*(y[len(x)]+y[len(x)-1])/2
        #print(y_corr, y)

        ActExt_corr[idx]=y_corr[len(y_corr)-1]*110/math.log(2)
        ActExt[idx]=y_pourc[len(y_pourc)-1]*110/math.log(2)
        ActExt_act[idx]=y_act[len(y_act)-1]*110/math.log(2)
    #print(ActInt, ActExt_noncorr)

    return ActInt_corr, ActExt_corr