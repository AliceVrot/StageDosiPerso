import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
from TAC import TAC
from conversionXLSXCSV import conversionXLSXCSV

chemin_xlsx = '/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange.xlsx'
chemin_csv = '/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange.csv'
chemin_xlsx1 = '/home/verot/Projet/DonneesGupta/S_values_XieZaidi.xlsx'
chemin_csv1 = '/home/verot/Projet/DonneesGupta/S_values_XieZaidi.csv'
chemin_xlsx2 = '/home/verot/Projet/DonneesGupta/D_abs.xlsx'
chemin_csv2 = '/home/verot/Projet/DonneesGupta/D_abs.csv'

chemin = '/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange'
chemin1 = '/home/verot/Projet/DonneesGupta/S_values_XieZaidi'
chemin2 = '/home/verot/Projet/DonneesGupta/D_abs'
# Ne convertir en .csv que si le fichier n'existe pas déjà
#if not os.path.exists(chemin_csv):
#    xlsx = pd.read_excel(chemin_xlsx)
#    xlsx.to_csv(chemin_csv)
#    print("hihihihihi")
#if not os.path.exists(chemin_csv1):
#    xlsx = pd.read_excel(chemin_xlsx1)
#    xlsx.to_csv(chemin_csv1)
#    print("hihihihihi")
#if not os.path.exists(chemin_csv2):
#    xlsx = pd.read_excel(chemin_xlsx2)
#    xlsx.to_csv(chemin_csv2)
#    print("hihihihihi")



#df = pd.read_csv(chemin_csv, header=3)
#S_value=pd.read_csv(chemin_csv1, header=0)
#D_abs=pd.read_csv(chemin_csv2, header=1).iloc[:, 1:]

df = conversionXLSXCSV(chemin_xlsx)
S_value = conversionXLSXCSV(chemin_xlsx1)
D_abs = conversionXLSXCSV(chemin_xlsx2)

x = df['Délais'].to_numpy()

ActInt_corr, ActExt_corr=(df, x)
print(ActInt_corr, ActExt_corr)