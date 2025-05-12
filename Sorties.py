import pandas as pd
def comparaison_DoseAbsSelf_Biomaps_Gupta(organes, ActInt_corr, ActExt_corr, S_value5, Ainit, SelfAbs1, SelfAbs, SelfS_Value, D_abs, XieZaidi):
    Comparaison = pd.DataFrame({
        'Organes': organes,
        #'Intégration Interpolée TAC (sec)': ActInt,
        #'Intégration Extrapolée TAC (sec)': ActExt,
        #'Intégration TAC (sec)': ActInt + ActExt,
        'Activité Interpolée Corrigée (MBq.sec)': ActInt_corr,
        'Activité Extrapolée Corrigée (MBq.sec)': ActExt_corr,
        'Activité Accumulée Totale (MBq.sec)': (ActInt_corr + ActExt_corr),
        'Self Absorbed S-Value 5(mGy/MBq.s)': S_value5['valeur'],
        'Dose Absorbée Self 5(mGy.MBq⁻¹) Alice': SelfAbs1/Ainit,
        'Self Absorbed S-Value (mGy/MBq.s)': SelfS_Value,
        'Dose Absorbée Self (mGy.MBq⁻¹) Alice': SelfAbs/Ainit,
        'Dose Absorbée Self (mGy.MBq⁻¹) Gupta': D_abs['Self-absorbed dose'],
        'Différence Alice 5 Gupta(%)': abs(SelfAbs1/Ainit - D_abs['Self-absorbed dose'])/ D_abs['Self-absorbed dose'] * 100,
        'Différence Alice Gupta(%)': abs(SelfAbs/Ainit - D_abs['Self-absorbed dose'])/ D_abs['Self-absorbed dose'] * 100,
        'Dose Absorbée Total (mGy.MBq⁻¹) Zaidi': XieZaidi['Xie and Zaidi'],
        'Dose Absorbée Total (mGy.MBq⁻¹) Gupta': D_abs['Total absorbed dose'],
        'Différence (%)': abs(XieZaidi['Xie and Zaidi'] - D_abs['Total absorbed dose'])/ D_abs['Total absorbed dose'] * 100
    })
    return (Comparaison)