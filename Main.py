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


#chemin = '/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange'
#chemin1 = '/home/verot/Projet/DonneesGupta/S_values_XieZaidi'
#chemin2 = '/home/verot/Projet/DonneesGupta/D_abs'



DonneesGupta = pd.read_csv('/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange1.csv', index_col=0) # conversionXLSXCSV(chemin_xlsx, 3)
S_value_XieZaidi_annexe = pd.read_csv('/home/verot/Projet/DonneesGupta/S_values_XieZaidi1.csv', index_col=0) #conversionXLSXCSV(chemin_xlsx1, 0)
DoseAbsorbee_SelfCross_Gupta = pd.read_csv('/home/verot/Projet/DonneesGupta/D_abs1.csv', index_col=0)#conversionXLSXCSV(chemin_xlsx2, 1)
DoseAbsorbee_GuptaETXieZaidi=pd.read_csv('/home/verot/Projet/DonneesGupta/Figure71.csv', index_col=0)
Ainit= 15.22
Tphys=109.771
ordre = ['Coeur', 'Bladder', 'Spleen', 'Foie', 'Lungs', 'Cerveau', 'Estomac', 'Rein']


organes = DonneesGupta.columns[6:16]

S_valueFigure5XieZaidi = pd.DataFrame({
    'valeur': [
        1.27E-01,  # Coeur
        4.56E-01,  # Bladder
        2.51E-01,  # Spleen
        1.84E-02,  # Foie
        1.72E-01,  # Lungs
        6.54E-02,  # Cerveau
        7.99E-02,  # Estomac
        9.45E-02   # Rein
    ]
}, 
index=ordre)
#print(S_valueFigure5XieZaidi)
S_valueFigure5XieZaidi.index.name = 'organe'


temps = DonneesGupta['Délais'].to_numpy()

ActInt_corr, ActExt_corr, PartieExtrapolee, y_corr_matrice=TAC(DonneesGupta, temps, Ainit, Tphys)
#print("ActInt: ", ActInt_corr*60, "ActExt: ", ActExt_corr*60)
ActExt_corr=ActExt_corr*60
ActInt_corr=ActInt_corr*60

#print(organes)
DSelfAbsDose_annexe, DSelfAbsDose_figure5, SelfS_Value_XieZaidi_annexe = CalculDoseSelf(ActInt_corr, ActExt_corr, organes , S_value_XieZaidi_annexe, S_valueFigure5XieZaidi)
DSelfAbsDose_annexe=DSelfAbsDose_annexe/Ainit
DSelfAbsDose_figure5=DSelfAbsDose_figure5/Ainit
#print("DSelfAbsDose: ", DSelfAbsDose, "DSelfAbsDose_figure5: ", DSelfAbsDose_figure5)

Comparaison = comparaison_DoseAbsSelf_Biomaps_Gupta(organes, ActInt_corr, ActExt_corr, S_valueFigure5XieZaidi, Ainit, DSelfAbsDose_figure5, DSelfAbsDose_annexe, SelfS_Value_XieZaidi_annexe, DoseAbsorbee_SelfCross_Gupta, DoseAbsorbee_GuptaETXieZaidi)
#print(Comparaison)

#print(ActInt_corr)

plotActivite(temps, y_corr_matrice, PartieExtrapolee, organes)
#barplotComparaison(DSelfAbsDose_annexe, DSelfAbsDose_figure5, 'titre', organes)