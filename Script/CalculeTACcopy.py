import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
#from TAC import TAC
#from conversionXLSXCSV import conversionXLSXCSV
#from CalculDoseSelf import CalculDoseSelf
#from Sorties import comparaison_DoseAbsSelf_Biomaps_Gupta
#from plot import plotActivite, barplotComparaison
#from plot import plot
import argparse

# === ARGUMENTS DE LIGNE DE COMMANDE ===
parser = argparse.ArgumentParser(description="Pipeline dosimétrie personnalisée")

parser.add_argument("--data", required=True, help="Chemin vers le fichier .csv des données principales (DonneesEntre)")
#parser.add_argument("--sval_annexe", required=True, help="Chemin vers le fichier des S-values (annexe)")
parser.add_argument("--s_val", required=True, help="Chemin vers les S-values")
#parser.add_argument("--dose_cross", required=True, help="Chemin vers le fichier des doses absorbées (self+cross, Gupta)")
#parser.add_argument("--dose_gupta", required=True, help="Chemin vers le fichier de comparaison dose Gupta et XieZaidi")
parser.add_argument("--ainit", type=float, required=True, help="Activité initiale injectée (MBq)")
#parser.add_argument("--tphys", type=float, required=True, help="Temps physique du radionucléide (min)")
#parser.add_argument("--SortieActivite", type=float, required=True, help="1 (Oui) ou 0 (Non) pour la sortie de l'activité")
#parser.add_argument("--SortieDose", type=float, required=True, help="0(non), 1(dose par organe), 2 (matrice dose absorbée par les organes cible par organe source) pour la sortie de la dose absorbée")
#parser.add_argument("--EnregistrerSortieDose", type=str, required=True, help="0 ou 1 Ou nom du fichier de sortie")

args = parser.parse_args()

Ainit = args.ainit
#Tphys = args.tphys


Tphys = 78.4
T_half_Zr= 78.4
T_half_Lu = 160.8

lambda_Zr = np.log(2) / T_half_Zr
lambda_Lu = np.log(2) / T_half_Lu




# === CHARGEMENT DES DONNÉES ===
DonneesEntre = pd.read_csv(args.data, sep=",") #sheet_name = "Feuille1", index_col=0)
#print(DonneesEntre.columns.tolist())
DonneesEntre.columns = DonneesEntre.columns.str.strip()
#print("REGARDE ICI")
#print(DonneesEntre['Délais'].to_numpy())
#print(DonneesEntre)
S_value = pd.read_csv(args.s_val, sep=",")


ordre = ['Coeur', 'Bladder', 'Spleen', 'Foie', 'Lungs', 'Cerveau', 'Estomac', 'Rein']
#calcul = pd.DataFrame(index=organes, columns=organes)
#print(calcul)
#print(S_value)
#S_values trouvé dans le tableau de Xie et Zaidi + traitement
#print (S_value.columns)
#S_value = S_value.iloc[:, 1:]
#S_value.set_index('Unnamed: 0', inplace=True)
#S_value = S_value.rename(columns={'Heart': 'Coeur', 'Liver': 'Foie', 'Lung': 'Lungs', 'Kidney': 'Rein', 'Stomach': 'Estomac', 'Bone': 'Os', 'bladder': 'Bladder', 'Brain': 'Cerveau'})
#S_value = S_value.rename(index={'Heart': 'Coeur', 'Liver': 'Foie', 'Lung': 'Lungs', 'Kidney': 'Rein', 'Stomach': 'Estomac', 'Bone': 'Os', 'bladder': 'Bladder', 'Brain': 'Cerveau'})
#print(S_value.index.tolist())
#print(S_value.index)
#print (S_value.columns)
#colonnes_voulues = ['Coeur', 'Foie', 'Rate', 'Lungs', 'Rein', 'Estomac', 'Os'] 
#S_value = S_value[ordre] 
#S_value = S_value.loc[ordre]


organes = DonneesEntre.columns[4:18]
#print('organes: ', organes)

print(DonneesEntre)
print(DonneesEntre.columns)
print(DonneesEntre['Délais'])
temps = DonneesEntre['Délais'].to_numpy()*60


def TAC(DonneesEntree, temps, Ainit, Tphys):
    #temps = DonneesEntree['Délais'].to_numpy()
    tempsExt=np.linspace(temps[len(temps)-1], 2*temps[len(temps)-1], 100)
    #organes = DonneesEntree.columns[6:16]
    ActInt=np.zeros(len(organes))
    ActInt_corr=np.zeros(len(organes)) 
    ActInt_act=np.zeros(len(organes))
    ActExt=np.zeros(len(organes)) 
    ActExt_corr=np.zeros(len(organes))
    ActExt_act=np.zeros(len(organes)) 
    y_corr_matrice=DonneesEntree.copy()
    PartieExtrapolee=np.zeros((len(organes), len(tempsExt)))
    for idx, i in enumerate(organes):
        y_pourc = DonneesEntree[i]
        #print("y_pourc avant", y_pourc)
        if y_pourc.dtype == object:
            y_pourc = y_pourc.str.replace(',', '.').astype(float)
        else:
            y_pourc = y_pourc.astype(float)
        #print("y_pourc après: ", y_pourc)
        #print ("Ainit: ", Ainit)
        
        y_act = y_pourc*Ainit/100
        y_corr = y_act.copy()
        for j in range(len(y_pourc)-1):
            y_corr[j]=y_act[j]*(np.exp(-(temps[j])*math.log(2)/Tphys))
            y_corr[j+1]=y_act[j+1]*(np.exp(-(temps[j+1])*math.log(2)/Tphys))
            y_corr[j] = y_corr[j]*np.exp((lambda_Zr - lambda_Lu) * temps[j])
            y_corr[j+1] = y_corr[j+1]*np.exp((lambda_Zr - lambda_Lu) * temps[j+1])
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





ActInt_corr, ActExt_corr, PartieExtrapolee, y_corr_matrice = TAC(DonneesEntre, temps, Ainit, Tphys)

Resultats = pd.DataFrame({
        'Organes': organes,
        'Activité Interpolée Corrigée (MBq.sec)': ActInt_corr,
        'Activité Extrapolée Corrigée (MBq.sec)': ActExt_corr,
        'Activité Accumulée Totale (MBq.sec)': (ActInt_corr + ActExt_corr),
        #'Self Absorbed S-Value': S_value,
        #'Dose Absorbée (mGy.MBq⁻¹)': DAbsTotale,
    })

ActExt_corr=ActExt_corr*60
ActInt_corr=ActInt_corr*60
print("Activité Interpolée Corrigée (MBq.sec): ", ActInt_corr) 
print("Activité Extrapolée Corrigée (MBq.sec): ", ActExt_corr)
print(Resultats)
#Resultats.to_csv('/home/verot/Projet/Piplinepluspropre/output/TAC.csv',header=True, index=True)
