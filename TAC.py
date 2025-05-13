import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import os
import math

DonneesGupta = pd.read_csv('/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange.csv', header=3)

def TAC(DonneesGupta, temps, Ainit, Tphys):
    temps = DonneesGupta['Délais'].to_numpy()
    tempsExt=np.linspace(temps[len(temps)-1], 2*temps[len(temps)-1], 100)
    organes = DonneesGupta.columns[6:16]
    ActInt=np.zeros(len(organes))
    ActInt_corr=np.zeros(len(organes)) 
    ActInt_act=np.zeros(len(organes))
    ActExt=np.zeros(len(organes)) 
    ActExt_corr=np.zeros(len(organes))
    ActExt_act=np.zeros(len(organes)) 
    y_corr_matrice=DonneesGupta.copy()
    PartieExtrapolee=np.zeros((len(organes), len(tempsExt)))
    for idx, i in enumerate(organes):
        y_pourc = DonneesGupta[i]
        y_act = y_pourc*Ainit/100
        y_corr = y_act.copy()
        for j in range(len(y_pourc)-1):
            y_corr[j]=y_act[j]*(np.exp(-(temps[j])*math.log(2)/Tphys))
            y_corr[j+1]=y_act[j+1]*(np.exp(-(temps[j+1])*math.log(2)/Tphys))
            trapeze_corr=(temps[j+1]-temps[j])*(y_corr[j+1]+y_corr[j])/2
            trapeze=(temps[j+1]-temps[j])*(y_pourc[j+1]+y_pourc[j])/2
            trapeze_act=(temps[j+1]-temps[j])*(y_act[j+1]+y_act[j])/2
            ActInt[idx]=ActInt[idx]+trapeze
            ActInt_corr[idx]=ActInt_corr[idx]+trapeze_corr
            ActInt_act[idx]=ActInt_act[idx]+trapeze_act
        Derniereactivite=y_corr[len(y_corr)-1]
        PartieExtrapolee[idx] = Derniereactivite*np.exp(-(tempsExt-temps[len(temps)-1])*math.log(2)/Tphys)
        ActExt_corr[idx]=y_corr[len(y_corr)-1]*Tphys/math.log(2)
        ActExt[idx]=y_pourc[len(y_pourc)-1]*Tphys/math.log(2)
        ActExt_act[idx]=y_act[len(y_act)-1]*Tphys/math.log(2)
        y_corr_matrice[i]=y_corr
        
   

    return ActInt_corr, ActExt_corr, PartieExtrapolee, y_corr_matrice