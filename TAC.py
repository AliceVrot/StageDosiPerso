import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math

df = pd.read_csv('/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange.csv', header=3)

#print(df)

#print(df.columns[6:16])
def TAC(df, x, Ainit, Tphys):
    x = df['Délais'].to_numpy()
    x2=np.linspace(x[len(x)-1], 2*x[len(x)-1], 100)
    #print(x2)
    organes = df.columns[6:16]
    #fig, axs = plt.subplots(2, 4, figsize=(15, 6))
    #axs = axs.flatten()
    organes=df.columns[6:16]
    #Ainit= 15.22
    ActInt=np.zeros(len(organes))
    ActInt_corr=np.zeros(len(organes)) 
    ActInt_act=np.zeros(len(organes))
    ActExt=np.zeros(len(organes)) 
    ActExt_corr=np.zeros(len(organes))
    ActExt_act=np.zeros(len(organes)) 
    #Tphys=109.771

    for idx, i in enumerate(organes):
        y_pourc = df[i]#*Ainit/100
        y_act = y_pourc*Ainit/100
        y_corr = y_act.copy()
        for j in range(len(y_pourc)-1):
            #print(j)
            y_corr[j]=y_act[j]*(np.exp(-(x[j])*math.log(2)/Tphys))
            y_corr[j+1]=y_act[j+1]*(np.exp(-(x[j+1])*math.log(2)/Tphys))
            #print(y_corr[j], y_act[j], y_pourc[j], j)
            T_corr=(x[j+1]-x[j])*(y_corr[j+1]+y_corr[j])/2
            T=(x[j+1]-x[j])*(y_pourc[j+1]+y_pourc[j])/2
            T_act=(x[j+1]-x[j])*(y_act[j+1]+y_act[j])/2
            ActInt[idx]=ActInt[idx]+T
            ActInt_corr[idx]=ActInt_corr[idx]+T_corr
            ActInt_act[idx]=ActInt_act[idx]+T_act
        Amax=y_corr[len(y_corr)-1]
        #Amax=y_act[len(y_pourc)-1]
        z = Amax*np.exp(-(x2-85)*math.log(2)/Tphys)
        ActExt_corr[idx]=y_corr[len(y_corr)-1]*Tphys/math.log(2)
        #print(y_corr[len(y_corr)-1], ActInt_corr[idx], y_corr[len(y_corr)-1]*Tphys/math.log(2), ActExt_corr[idx])
        ActExt[idx]=y_pourc[len(y_pourc)-1]*Tphys/math.log(2)
        ActExt_act[idx]=y_act[len(y_act)-1]*Tphys/math.log(2)
        


    return ActInt_corr, ActExt_corr