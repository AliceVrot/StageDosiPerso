#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import os
#import math
from TAC import TAC
from conversionXLSXCSV import conversionXLSXCSV
from CalculDoseSelf import CalculDoseSelf
from Sorties import comparaison_DoseAbsSelf_Biomaps_Gupta
from plot import plotActivite, barplotComparaison
#from plot import plot
import argparse


#DonneesGupta = pd.read_csv('/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange1.csv', index_col=0) # conversionXLSXCSV(chemin_xlsx, 3)
#S_value_XieZaidi_annexe = pd.read_csv('/home/verot/Projet/DonneesGupta/S_values_XieZaidi1.csv', index_col=0) #conversionXLSXCSV(chemin_xlsx1, 0)
#DoseAbsorbee_SelfCross_Gupta = pd.read_csv('/home/verot/Projet/DonneesGupta/D_abs1.csv', index_col=0)#conversionXLSXCSV(chemin_xlsx2, 1)
#DoseAbsorbee_GuptaETXieZaidi=pd.read_csv('/home/verot/Projet/DonneesGupta/Figure71.csv', index_col=0)
#S_valueFigure5XieZaidi=pd.read_csv('/home/verot/Projet/DonneesGupta/S_valueFigure5XieZaidi.csv', index_col=0)
#Ainit= 15.22
#Tphys=109.771
#ordre = ['Coeur', 'Bladder', 'Spleen', 'Foie', 'Lungs', 'Cerveau', 'Estomac', 'Rein']


# === ARGUMENTS DE LIGNE DE COMMANDE ===
parser = argparse.ArgumentParser(description="Pipeline dosimétrie personnalisée")

parser.add_argument("--data", required=True, help="Chemin vers le fichier .csv des données principales (DonneesEntre)")
#parser.add_argument("--sval_annexe", required=True, help="Chemin vers le fichier des S-values (annexe)")
parser.add_argument("--S_val", required=True, help="Chemin vers les S-values")
#parser.add_argument("--dose_cross", required=True, help="Chemin vers le fichier des doses absorbées (self+cross, Gupta)")
#parser.add_argument("--dose_gupta", required=True, help="Chemin vers le fichier de comparaison dose Gupta et XieZaidi")
parser.add_argument("--ainit", type=float, required=True, help="Activité initiale injectée (MBq)")
parser.add_argument("--tphys", type=float, required=True, help="Temps physique du radionucléide (min)")
parser.add_argument("--SortieActivite", type=float, required=True, help="1 (Oui) ou 0 (Non) pour la sortie de l'activité")
#parser.add_argument("--SortieDose", type=float, required=True, help="0(non), 1(dose par organe), 2 (matrice dose absorbée par les organes cible par organe source) pour la sortie de la dose absorbée")
parser.add_argument("--EnregistrerSortieDose", type=str, required=True, help="0 ou 1 Ou nom du fichier de sortie")

args = parser.parse_args()

Ainit = args.ainit
Tphys = args.tphys

# === CHARGEMENT DES DONNÉES ===
DonneesEntre = pd.read_csv(args.data, index_col=0) #sheet_name = "Feuille1", index_col=0)
#autredonnees= pd.read_xlsx(args.data, sheet_name = "Feuille2", index_col=0)
#S_value_XieZaidi_annexe = pd.read_csv(args.sval_annexe, index_col=0)
S_value = pd.read_csv(args.S_val, index_col=0)
#DoseAbsorbee_SelfCross_Gupta = pd.read_csv(args.dose_cross, index_col=0)
#DoseAbsorbee_GuptaETXieZaidi = pd.read_csv(args.dose_gupta, index_col=0)

#Tphys = autredonnees.loc[0, 'Tphys']
#Ainit = autredonnees.loc[0, 'Ainit']

organes = DonneesEntre.columns[6:16]



temps = DonneesEntre['Délais'].to_numpy()

ActInt_corr, ActExt_corr, PartieExtrapolee, y_corr_matrice=TAC(DonneesEntre, temps, Ainit, Tphys)
#print("ActInt: ", ActInt_corr*60, "ActExt: ", ActExt_corr*60)
ActExt_corr=ActExt_corr*60
ActInt_corr=ActInt_corr*60

#print(ActExt_corr, ActInt_corr)
#print(organes)
DSelfAbsDose, SelfS_Value_XieZaidi_annexe, distribDose_parOrgane, DAbsTotale = CalculDoseSelf(ActInt_corr, ActExt_corr, organes, S_value)#  S_value_XieZaidi_annexe, S_valueFigure5XieZaidi)
#print("après fin?")
#print(DSelfAbsDose_figure5)



DSelfAbsDose=DSelfAbsDose/Ainit
#DSlfAbsDose_figure5=DSelfAbsDose_figure5/Ainit
#print("DSelfAbsDose: ", DSelfAbsDose_annexe, "DSelfAbsDose_figure5: ", DSelfAbsDose_figure5)

#organes = pd.Series(organes)
#organes.to_csv("/home/verot/Projet/DonneesGupta/organes.csv")
#Comparaison = comparaison_DoseAbsSelf_Biomaps_Gupta(organes, ActInt_corr, ActExt_corr, S_valueFigure5XieZaidi, Ainit, DSelfAbsDose_figure5, DSelfAbsDose_annexe, SelfS_Value_XieZaidi_annexe, DoseAbsorbee_SelfCross_Gupta, DoseAbsorbee_GuptaETXieZaidi)
#print(Comparaison)
#Comparaison.to_excel("/home/verot/Projet/Sorties/comparaisons.xlsx")


#plotActivite(temps, y_corr_matrice, PartieExtrapolee, organes)
#barplotComparaison(DSelfAbsDose_annexe, DSelfAbsDose_figure5, 'titre', organes)



Resultats = pd.DataFrame({
        'Organes': organes,
        'Activité Interpolée Corrigée (MBq.sec)': ActInt_corr,
        'Activité Extrapolée Corrigée (MBq.sec)': ActExt_corr,
        'Activité Accumulée Totale (MBq.sec)': (ActInt_corr + ActExt_corr),
        #'Self Absorbed S-Value': S_value,
        'Dose Absorbée (mGy.MBq⁻¹)': DAbsTotale,
    })

print (Resultats)
# === SORTIES ===
if args.SortieActivite == 1:
    #print('Activite interpolée: ', ActInt_corr, ' Activité extrapolée', ActExt_corr)
    a=1


#print(distribDose_parOrgane)
if args.EnregistrerSortieDose == "1":
    output_file = args.data.replace(".csv", "_resultats.csv")
    Resultats.to_csv(output_file,header=True, index=True)

if args.EnregistrerSortieDose.endswith(".csv"):
    output_file = args.EnregistrerSortieDose
    Resultats.to_csv(output_file,header=True, index=True)

    #distribDose_parOrgane.to_excel("/home/verot/Projet/Sorties/NOM.xlsx")