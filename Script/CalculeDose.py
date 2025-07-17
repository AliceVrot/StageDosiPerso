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
import ast
# === ARGUMENTS DE LIGNE DE COMMANDE ===
parser = argparse.ArgumentParser(description="Pipeline dosimétrie personnalisée")

parser.add_argument("--ActTot", required=True, help="Chemin vers le fichier .csv des données principales (DonneesEntre)")
#parser.add_argument("--sval_annexe", required=True, help="Chemin vers le fichier des S-values (annexe)")
parser.add_argument("--s_val", required=True, help="Chemin vers les S-values")
parser.add_argument("--organessource", required=True, help="organessource")
parser.add_argument("--organescibles", required=True, help="organescibless")
#parser.add_argument("--dose_cross", required=True, help="Chemin vers le fichier des doses absorbées (self+cross, Gupta)")
#parser.add_argument("--dose_gupta", required=True, help="Chemin vers le fichier de comparaison dose Gupta et XieZaidi")
#parser.add_argument("--ainit", type=float, required=True, help="Activité initiale injectée (MBq)")
#parser.add_argument("--tphys", type=float, required=True, help="Temps physique du radionucléide (min)")
#parser.add_argument("--SortieActivite", type=float, required=True, help="1 (Oui) ou 0 (Non) pour la sortie de l'activité")
#parser.add_argument("--SortieDose", type=float, required=True, help="0(non), 1(dose par organe), 2 (matrice dose absorbée par les organes cible par organe source) pour la sortie de la dose absorbée")
#parser.add_argument("--EnregistrerSortieDose", type=str, required=True, help="0 ou 1 Ou nom du fichier de sortie")

args = parser.parse_args()

#Ainit = args.ainit
#Tphys = args.tphys

# === CHARGEMENT DES DONNÉES ===
ActTot = pd.read_csv(args.ActTot,  sep=",", index_col=0) #sheet_name = "Feuille1", index_col=0)
#print(ActTot)
S_value = pd.read_csv(args.s_val, index_col=0)

organes_source = ast.literal_eval(args.organessource)
organes_cible = ast.literal_eval(args.organescibles)

#organes = ActTot.columns[4:18]


#temps = DonneesEntre['Délais'].to_numpy()

#print(organes_source, organes_cible)

#print (S_value)

#print(ActTot)
#print(ActTot[ActTot['Organes'] == 'Foie']['ActTot'].to_numpy())

def CalculDoseSelf(ActTot, organes_source, organes_cible, S_value): #, S_value_XieZaidi_annexe
    #print(organes)
    #DSelfAbsDose_annexe = np.zeros(len(organes))
    DSelfAbsDose = np.zeros(len(organes_cible))
    CrossAbs = np.zeros((len(organes_cible), len(organes_source)))
    #print("CrossAbs: ", CrossAbs)
    #SelfS_Value = np.zeros(len(organes))
    DoseParOrgane = np.zeros(len(organes_cible))
    #CrossS_Value = np.zeros(len(organes))
    #print(S_value)
    #print(np.shape(S_value))
    #if np.shape(S_value) == (len(organes), 1): S_value=S_value['Valeur'].to_numpy()
    #if np.shape(S_value) == (len(organes), len(organes)):
    for idx, i in enumerate(organes_cible):
        dose = 0.0
        for idex, j in enumerate(organes_source):
            #if i==j : print (S_value[i][j], (ActInt[idx]+ActExt[idx]), S_value[i][j]*(ActInt[idx]+ActExt[idx]))
            #print("S_value: ", S_value[i][i])
            #print("idx: ", idx)
            #print("i: ", i)
            #print("S_value[i][i]: ", S_value[i][i])
            #SelfS_Value[idx] = float(S_value[i][i].replace(',', '.'))
            #SelfS_Value[idx] = S_value[i][i]
            #print ("LALALALAAAAAA", ActTot[idx].to_numpy())
            #DSelfAbsDose[idx] = SelfS_Value[idx]* ActTot[ActTot['Organes'] == i]['ActTot'].to_numpy()
                #BLABLA CROSS
            CrossAbs[idx, idex] =float(S_value[j][i].replace(',', '.'))*ActTot[ActTot['Organes'] == j]['ActTot'].to_numpy()# for j in organes if i != j)
            dose += CrossAbs[idx, idex]#*(ActTot[ActTot['Organes'] == j]['ActTot'].to_numpy())
            #print("CrossAbs: ", CrossAbs[idx, idex])
            #print(CrossAbs[idx, idex])
            print(idx, i,idex,j, S_value[j][i].replace(',', '.'), ActTot[ActTot['Organes'] == j]['ActTot'].to_numpy())
        DoseParOrgane[idx]= dose #sum(CrossAbs[idx, idex] for idx in range(len(organes_cible)))# if i != organes[idex])
    print("CrossAbs: ", CrossAbs)
    #else:
    #    S_value=S_value['Valeur'].to_numpy()
    #    for idx, i in enumerate(organes):
            #for idex, j in enumerate(organes):
            #print(S_value)
            #S_value=S_value['Valeur'].to_numpy()
            #print(S_value)
            #print("S_value: ", S_value[i])
            #print("idx: ", idx)
            #print("i: ", i)
            #print("S_value[i]: ", S_value[i])
    #        SelfS_Value[idx] = S_value[idx]
    #        DSelfAbsDose[idx] = SelfS_Value[idx] * (ActTot[idx])
    #    print(DSelfAbsDose)
   
    #print(CrossAbs)
    #print(DoseParOrgane, DSelfAbsDose_figure5)
    return DoseParOrgane
    

DAbsTotale = CalculDoseSelf(ActTot, organes_source, organes_cible, S_value)#  S_value_XieZaidi_annexe, S_valueFigure5XieZaidi)


#DSelfAbsDose=DSelfAbsDose/Ainit

print("Dose: ", DAbsTotale)

#Resultats = pd.DataFrame({
#        'Organes': organes,
#        'Activité Interpolée Corrigée (MBq.sec)': ActInt_corr,
#        'Activité Extrapolée Corrigée (MBq.sec)': ActExt_corr,
#        'Activité Accumulée Totale (MBq.sec)': (ActInt_corr + ActExt_corr),
#        #'Self Absorbed S-Value': S_value,
#        'Dose Absorbée (mGy.MBq⁻¹)': DAbsTotale,
#    })

#print (Resultats)
# === SORTIES ===
#if args.SortieActivite == 1:
    #print('Activite interpolée: ', ActInt_corr, ' Activité extrapolée', ActExt_corr)
#    a=1


#print(distribDose_parOrgane)
#if args.EnregistrerSortieDose == "1":
#    output_file = args.data.replace(".csv", "_resultats.csv")
#    Resultats.to_csv(output_file,header=True, index=True)

#if args.EnregistrerSortieDose.endswith(".csv"):
#    output_file = args.EnregistrerSortieDose
#    Resultats.to_csv(output_file,header=True, index=True)

    #distribDose_parOrgane.to_excel("/home/verot/Projet/Sorties/NOM.xlsx")