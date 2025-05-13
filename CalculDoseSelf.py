import numpy as np
import pandas as pd

def CalculDoseSelf(ActInt, ActExt, organes, S_value_XieZaidi_annexe, S_valueFigure5XieZaidi):
    #print(organes)
    DSelfAbsDose_annexe = np.zeros(len(organes))
    DSelfAbsDose_figure5 = np.zeros(len(organes))
    CrossAbs = np.zeros(len(organes))
    SelfS_Value_XieZaidi_annexe = np.zeros(len(organes))
    #CrossS_Value = np.zeros(len(organes))
    #print(S_value)
    for idx, i in enumerate(organes):
        #print(i)
        SelfS_Value_XieZaidi_annexe[idx] = S_value_XieZaidi_annexe[i][i]
        #print(SelfS_Value[idx])
        #CrossS_Value[idx] = np.zeros(len(organes))
        DSelfAbsDose_annexe[idx]= SelfS_Value_XieZaidi_annexe[idx]*(ActInt[idx]+ActExt[idx])
        CrossAbs[idx]=sum(S_value_XieZaidi_annexe[i][j]*(ActInt[idx]+ActExt[idx]) for j in organes if i != j)
        DSelfAbsDose_figure5[idx] = S_valueFigure5XieZaidi.loc[i, 'valeur'] * (ActInt[idx] + ActExt[idx])
    return DSelfAbsDose_annexe, DSelfAbsDose_figure5, SelfS_Value_XieZaidi_annexe

