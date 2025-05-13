import pandas as pd
def comparaison_DoseAbsSelf_Biomaps_Gupta(organes, ActInt_corr, ActExt_corr, S_valueFigure5XieZaidi, Ainit, DSelfAbsDose_figure5, DSelfAbsDose_annexe, SelfS_Value, D_abs, XieZaidi):
    Comparaison = pd.DataFrame({
        'Organes': organes,
        #'Intégration Interpolée TAC (sec)': ActInt,
        #'Intégration Extrapolée TAC (sec)': ActExt,
        #'Intégration TAC (sec)': ActInt + ActExt,
        'Activité Interpolée Corrigée (MBq.sec)': ActInt_corr,
        'Activité Extrapolée Corrigée (MBq.sec)': ActExt_corr,
        'Activité Accumulée Totale (MBq.sec)': (ActInt_corr + ActExt_corr),
        'Self Absorbed S-Value 5(mGy/MBq.s)': S_valueFigure5XieZaidi['valeur'],
        'Dose Absorbée Self 5(mGy.MBq⁻¹) Alice': DSelfAbsDose_figure5/Ainit,
        'Self Absorbed S-Value (mGy/MBq.s)': SelfS_Value,
        'Dose Absorbée Self (mGy.MBq⁻¹) Alice': DSelfAbsDose_annexe/Ainit,
        'Dose Absorbée Self (mGy.MBq⁻¹) Gupta': D_abs['Self-absorbed dose'],
        'Différence Alice 5 Gupta(%)': abs(DSelfAbsDose_figure5/Ainit - D_abs['Self-absorbed dose'])/ ((D_abs['Self-absorbed dose']+DSelfAbsDose_figure5/Ainit)/2) * 100,
        'Différence Alice Gupta(%)': abs(DSelfAbsDose_annexe/Ainit - D_abs['Self-absorbed dose'])/ ((D_abs['Self-absorbed dose']+DSelfAbsDose_annexe/Ainit)/2) * 100,
        'Dose Absorbée Total (mGy.MBq⁻¹) Zaidi': XieZaidi['Xie and Zaidi'],
        'Dose Absorbée Total (mGy.MBq⁻¹) Gupta': D_abs['Total absorbed dose'],
        'Différence (%)': abs(XieZaidi['Xie and Zaidi'] - D_abs['Total absorbed dose'])/ D_abs['Total absorbed dose'] * 100
    })
    return (Comparaison)