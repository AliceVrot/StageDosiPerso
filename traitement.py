import pandas as pd


df = pd.read_csv('/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange.csv', header=3)
#Organe = df.columns[6:16]

S_valueFigure5XieZaidi=pd.read_csv('/home/verot/Projet/DonneesGupta/S_valueFigure5XieZaidi.csv', header =1)
S_valueFigure5XieZaidi.set_index('Organe', inplace=True)
#print(S_valueFigure5XieZaidi)
S_valueFigure5XieZaidi.to_csv('/home/verot/Projet/DonneesGupta/S_valueFigure5XieZaidi.csv')