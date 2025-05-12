import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
from TAC import TAC
from conversionXLSXCSV import conversionXLSXCSV
from CalculDoseSelf import CalculDoseSelf
from Sorties import comparaison_DoseAbsSelf_Biomaps_Gupta
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


x = DonneesGupta['Délais'].to_numpy()

ActInt_corr, ActExt_corr=TAC(DonneesGupta, x, Ainit, Tphys)
#print("ActInt: ", ActInt_corr*60, "ActExt: ", ActExt_corr*60)
ActExt_corr=ActExt_corr*60
ActInt_corr=ActInt_corr*60

#print(organes)
DSelfAbsDose, DSelfAbsDose1, SelfS_Value = CalculDoseSelf(ActInt_corr, ActExt_corr, organes , S_value_XieZaidi_annexe, S_valueFigure5XieZaidi)
DSelfAbsDose=DSelfAbsDose/Ainit
DSelfAbsDose1=DSelfAbsDose1/Ainit
print("DSelfAbsDose: ", DSelfAbsDose, "DSelfAbsDose1: ", DSelfAbsDose1)

Comparaison = comparaison_DoseAbsSelf_Biomaps_Gupta(organes, ActInt_corr, ActExt_corr, S_valueFigure5XieZaidi, Ainit, DSelfAbsDose1, DSelfAbsDose, SelfS_Value, DoseAbsorbee_SelfCross_Gupta, DoseAbsorbee_GuptaETXieZaidi)
print(Comparaison)