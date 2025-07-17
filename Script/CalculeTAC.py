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
#parser.add_argument("--s_val", required=True, help="Chemin vers les S-values")
#parser.add_argument("--dose_cross", required=True, help="Chemin vers le fichier des doses absorbées (self+cross, Gupta)")
#parser.add_argument("--dose_gupta", required=True, help="Chemin vers le fichier de comparaison dose Gupta et XieZaidi")
parser.add_argument("--ainit", type=float, required=True, help="Activité initiale injectée (MBq)")
parser.add_argument("--tphysZr", type=float, required=True, help="Temps physique du radionucléide (min)")
parser.add_argument("--tphysLu", type=float, required=True, help="Temps physique du radionucléide (min)")
#parser.add_argument("--SortieActivite", type=float, required=True, help="1 (Oui) ou 0 (Non) pour la sortie de l'activité")
#parser.add_argument("--SortieDose", type=float, required=True, help="0(non), 1(dose par organe), 2 (matrice dose absorbée par les organes cible par organe source) pour la sortie de la dose absorbée")
#parser.add_argument("--EnregistrerSortieDose", type=str, required=True, help="0 ou 1 Ou nom du fichier de sortie")

args = parser.parse_args()

Ainit = args.ainit
#Tphys = args.tphys


TphysZr = args.tphysZr #78.41 * 60
TphysLu = args.tphysLu
#TphysZr= 78.41 * 60
#TphysLu = 159.54 * 60
lambda_Zr = np.log(2) / TphysZr
lambda_Lu = np.log(2) / TphysLu




# === CHARGEMENT DES DONNÉES ===
DonneesEntre = pd.read_csv(args.data, sep=",") #sheet_name = "Feuille1", index_col=0)
#print(DonneesEntre.columns.tolist())
DonneesEntre.columns = DonneesEntre.columns.str.strip()
#print("REGARDE ICI")
#print(DonneesEntre['Délais'].to_numpy())
#print(DonneesEntre)
#S_value = pd.read_csv(args.s_val, sep=",")


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
temps = DonneesEntre['Délais'].to_numpy()*60
print(temps)

def TAC(DonneesEntree, temps, Ainit, TphysZr, TphysLu):
    #temps = DonneesEntree['Délais'].to_numpy()
    tempsExt=np.linspace(temps[len(temps)-1], 2*temps[len(temps)-1], 100)
    #organes = DonneesEntree.columns[6:16]
    #ActInt=np.zeros(len(organes))
    ActInt_corr=np.zeros(len(organes)) 
    ActInt_corrLu=np.zeros(len(organes)) 
    ActInt_act=np.zeros(len(organes))
    #ActExt=np.zeros(len(organes)) 
    ActExt_corr=np.zeros(len(organes))
    ActExt_corrLu=np.zeros(len(organes))
    ActExt_act=np.zeros(len(organes)) 
    y_corr_matrice=DonneesEntree.copy()
    #PartieExtrapolee=np.zeros((len(organes), len(tempsExt)))

    #x = temps
    #tempsExt=np.linspace(x[len(x)-1], 2*x[len(x)-1], 100)
    fig, axs = plt.subplots(2, 3, figsize=(15, 6))
    axs = axs.flatten()
    organes_source = ['Cœur', 'Tumeur Gauche', 'Tumeur Droite', 'Foie', 'Os']
    organes_filtres = [i for i in organes if i in organes_source]
    index=0
    
    for idx, i in enumerate(organes):
    
        y_act = DonneesEntree[i]
        if y_act.dtype == object:
            y_act = y_act.str.replace(',', '.').astype(float)
        else:
            y_act = y_act.astype(float)
        
        #y_act = y_pourc*Ainit/100
        y_corr = y_act.copy()
        y_corrLu = y_act.copy()

        for j in range(len(y_act)-1):
            y_corr[j]=y_act[j]*(np.exp(-(temps[j])*math.log(2)/TphysZr))
            y_corr[j+1]=y_act[j+1]*(np.exp(-(temps[j+1])*math.log(2)/TphysZr))
            y_corrLu[j] = y_corr[j]*np.exp((lambda_Zr - lambda_Lu) * temps[j])
            y_corrLu[j+1] = y_corr[j+1]*np.exp((lambda_Zr - lambda_Lu) * temps[j+1])
            trapeze_corr=(temps[j+1]-temps[j])*(y_corr[j+1]+y_corr[j])/2
            trapeze_corrLu=(temps[j+1]-temps[j])*(y_corrLu[j+1]+y_corrLu[j])/2
            #trapeze=(temps[j+1]-temps[j])*(y_pourc[j+1]+y_pourc[j])/2
            trapeze_act=(temps[j+1]-temps[j])*(y_act[j+1]+y_act[j])/2
            #ActInt[idx]=ActInt[idx]+trapeze
            ActInt_corr[idx]=ActInt_corr[idx]+trapeze_corr
            ActInt_corrLu[idx]=ActInt_corrLu[idx]+trapeze_corrLu
            ActInt_act[idx]=ActInt_act[idx]+trapeze_act
        #Derniereactivite=y_corr[len(y_corr)-1]
        #PartieExtrapolee[idx] = Derniereactivite*np.exp(-(tempsExt-temps[len(temps)-1])*math.log(2)/TphysZr)
        ActExt_corr[idx]=y_corr[len(y_corr)-1]*TphysZr/math.log(2)
        ActExt_corrLu[idx]=y_corrLu[len(y_corr)-1]*TphysZr/math.log(2)
        y_corr_matrice[i]=y_corr
        #Amax=y_act[len(y_act)-1]
        Amax=y_corr[len(y_act)-1]
        AmaxLu=y_corrLu[len(y_act)-1]
        PartieExtrapolee = Amax*np.exp(-(tempsExt-temps[len(temps)-1])*math.log(2)/TphysZr)
        PartieExtrapoleeLu = AmaxLu*np.exp(-(tempsExt-temps[len(temps)-1])*math.log(2)/TphysLu)
        
        if i in organes_filtres:
            #print ("LAAAAAAAAA",index, idx, i)
            axs[index].set_title(i)
            axs[index].plot(tempsExt, PartieExtrapoleeLu, label=i, linewidth=0.7)
            #axs[idx].scatter(x, y_corr, label=i, linewidth=0.7)
            #axs[idx].plot(tempsExt, PartieExtrapolee, label=i, linewidth=0.7)
            #print(x, y_pourc)
            axs[index].scatter(temps, y_corrLu, label=i, linewidth=0.7)
            axs[index].set_title(i)
            index = index+1
            #axs[idx].set_ylim(0, max(y_pourc)*1.1)

    plt.tight_layout()
    plt.show()
    #plt.show()

        

    return ActInt_corr, ActExt_corr, ActExt_corrLu, ActInt_corrLu, PartieExtrapoleeLu, y_corr_matrice

#plt.tight_layout()




ActInt_corr, ActExt_corr, ActExt_corrLu, ActInt_corrLu, PartieExtrapolee, y_corr_matrice = TAC(DonneesEntre, temps, Ainit, TphysZr, TphysLu)

Resultats = pd.DataFrame({
        'Organes': organes,
        'Activité Interpolée Corrigée Lu(MBq.min) dans la VOI': ActInt_corrLu*60/1000,
        'Activité Extrapolée Corrigée Lu(MBq.min) dans la VOI': ActExt_corrLu*60/1000,
        'Activité Accumulée Totale Lu(MBq.min) dans la VOI': (ActInt_corrLu + ActExt_corrLu)*60/1000,
        'Activité cumulée corrigée Totale Zr(MBq.min) dans la VOI': (ActInt_corr+ActExt_corr)*60/1000,
        #'Self Absorbed S-Value': S_value,
        #'Dose Absorbée (mGy.MBq⁻¹)': DAbsTotale,
    })

ActExt_corr=ActExt_corr*60
ActInt_corr=ActInt_corr*60
print("Activité Interpolée Corrigée (MBq.sec): ", ActInt_corr) 
print("Activité Extrapolée Corrigée (MBq.sec): ", ActExt_corr)
print(Resultats)
Resultats.to_csv('/home/verot/Projet/Piplinepluspropre/output/TACAnneLaure1.csv',header=True, index=True)
