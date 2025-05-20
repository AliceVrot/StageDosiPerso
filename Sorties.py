import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from plot import plotActivite, barplotComparaison

def comparaison_DoseAbsSelf_Biomaps_Gupta(organes, ActInt_corr, ActExt_corr, S_valueFigure5XieZaidi, Ainit, DSelfAbsDose_figure5, DSelfAbsDose_annexe, SelfS_Value, D_abs, XieZaidi):
    Comparaison = pd.DataFrame({
        'Organes': organes,
        #'Intégration Interpolée TAC (sec)': ActInt,
        #'Intégration Extrapolée TAC (sec)': ActExt,
        #'Intégration TAC (sec)': ActInt + ActExt,
        'Activité Interpolée Corrigée (MBq.sec)': ActInt_corr,
        'Activité Extrapolée Corrigée (MBq.sec)': ActExt_corr,
        'Activité Accumulée Totale (MBq.sec)': (ActInt_corr + ActExt_corr),
        'Self Absorbed S-Value 5(mGy/MBq.s)': S_valueFigure5XieZaidi,
        'Dose Absorbée Self 5(mGy.MBq⁻¹) Alice': DSelfAbsDose_figure5,
        'Self Absorbed S-Value (mGy/MBq.s)': SelfS_Value,
        'Dose Absorbée Self (mGy.MBq⁻¹) Alice': DSelfAbsDose_annexe,
        'Dose Absorbée Self (mGy.MBq⁻¹) Gupta': D_abs['Self-absorbed dose'],
        'Différence Alice 5 Gupta(%)': abs(DSelfAbsDose_figure5 - D_abs['Self-absorbed dose'])/ ((D_abs['Self-absorbed dose']+DSelfAbsDose_figure5)/2) * 100,
        'Différence Alice Gupta(%)': abs(DSelfAbsDose_annexe - D_abs['Self-absorbed dose'])/ ((D_abs['Self-absorbed dose']+DSelfAbsDose_annexe)/2) * 100,
        'Dose Absorbée Total (mGy.MBq⁻¹) Zaidi': XieZaidi['Xie and Zaidi'],
        'Dose Absorbée Total (mGy.MBq⁻¹) Gupta': D_abs['Total absorbed dose'],
        'Différence (%)': abs(XieZaidi['Xie and Zaidi'] - D_abs['Total absorbed dose'])/ D_abs['Total absorbed dose'] * 100
    })
    return (Comparaison)


#parser = argparse.ArgumentParser(description="Définition des sorties")
#parser.add_argument("--data1", required=True, help="Chemin vers le fichier .csv des données principales (DonneesEntre)")
#parser.add_argument("--data2", required=True, help="Chemin vers le fichier .csv des données principales (DonneesEntre)")
#args = parser.parse_args()

#DonneesEntre = pd.read_csv(args.data, index_col=0)
#temps = DonneesEntre['Délais'].to_numpy()