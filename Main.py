#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import os
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

parser.add_argument("--data", required=True, help="Chemin vers le fichier .csv des données principales (DonneesGupta)")
#parser.add_argument("--sval_annexe", required=True, help="Chemin vers le fichier des S-values (annexe)")
parser.add_argument("--sval_fig5", required=True, help="Chemin vers les S-values de la figure 5")
#parser.add_argument("--dose_cross", required=True, help="Chemin vers le fichier des doses absorbées (self+cross, Gupta)")
#parser.add_argument("--dose_gupta", required=True, help="Chemin vers le fichier de comparaison dose Gupta et XieZaidi")
parser.add_argument("--ainit", type=float, required=True, help="Activité initiale injectée (MBq)")
parser.add_argument("--tphys", type=float, required=True, help="Temps physique du radionucléide (min)")

args = parser.parse_args()

Ainit = args.ainit
Tphys = args.tphys

# === CHARGEMENT DES DONNÉES ===
DonneesGupta = pd.read_csv(args.data, index_col=0) #sheet_name = "Feuille1", index_col=0)
#autredonnees= pd.read_xlsx(args.data, sheet_name = "Feuille2", index_col=0)
#S_value_XieZaidi_annexe = pd.read_csv(args.sval_annexe, index_col=0)
S_valueFigure5XieZaidi = pd.read_csv(args.sval_fig5, index_col=0)
#DoseAbsorbee_SelfCross_Gupta = pd.read_csv(args.dose_cross, index_col=0)
#DoseAbsorbee_GuptaETXieZaidi = pd.read_csv(args.dose_gupta, index_col=0)

#Tphys = autredonnees.loc[0, 'Tphys']
#Ainit = autredonnees.loc[0, 'Ainit']

organes = DonneesGupta.columns[6:16]
print(organes, DonneesGupta)




temps = DonneesGupta['Délais'].to_numpy()

ActInt_corr, ActExt_corr, PartieExtrapolee, y_corr_matrice=TAC(DonneesGupta, temps, Ainit, Tphys)
#print("ActInt: ", ActInt_corr*60, "ActExt: ", ActExt_corr*60)
ActExt_corr=ActExt_corr*60
ActInt_corr=ActInt_corr*60

#print(ActExt_corr, ActInt_corr)
#print(organes)
DSelfAbsDose_annexe, DSelfAbsDose_figure5, SelfS_Value_XieZaidi_annexe, distribDose_parOrgane, DAbsTotale = CalculDoseSelf(ActInt_corr, ActExt_corr, organes, S_valueFigure5XieZaidi)#  S_value_XieZaidi_annexe, S_valueFigure5XieZaidi)
#print("après fin?")
#print(DSelfAbsDose_figure5)



DSelfAbsDose_annexe=DSelfAbsDose_annexe/Ainit
DSelfAbsDose_figure5=DSelfAbsDose_figure5/Ainit
#print("DSelfAbsDose: ", DSelfAbsDose_annexe, "DSelfAbsDose_figure5: ", DSelfAbsDose_figure5)


#Comparaison = comparaison_DoseAbsSelf_Biomaps_Gupta(organes, ActInt_corr, ActExt_corr, S_valueFigure5XieZaidi, Ainit, DSelfAbsDose_figure5, DSelfAbsDose_annexe, SelfS_Value_XieZaidi_annexe, DoseAbsorbee_SelfCross_Gupta, DoseAbsorbee_GuptaETXieZaidi)
#print(Comparaison)
#Comparaison.to_excel("/home/verot/Projet/Sorties/comparaisons.xlsx")


#plotActivite(temps, y_corr_matrice, PartieExtrapolee, organes)
#barplotComparaison(DSelfAbsDose_annexe, DSelfAbsDose_figure5, 'titre', organes)