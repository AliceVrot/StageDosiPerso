import numpy as np
import pandas as pd

def CalculDoseSelf(ActInt, ActExt, organes, S_value, ): #, S_value_XieZaidi_annexe
    #print(organes)
    DSelfAbsDose_annexe = np.zeros(len(organes))
    DSelfAbsDose_figure5 = np.zeros(len(organes))
    CrossAbs = np.zeros((len(organes), len(organes)))
    SelfS_Value = np.zeros(len(organes))
    DoseParOrgane = np.zeros(len(organes))
    #CrossS_Value = np.zeros(len(organes))
    #print(S_value)
    #print(np.shape(S_value))
    #print(S_value)
    for idx, i in enumerate(organes):
        if np.shape(S_value)== (len(organes), len(organes)):
            for idex, j in enumerate(organes):
                #if i==j : print (S_value[i][j], (ActInt[idx]+ActExt[idx]), S_value[i][j]*(ActInt[idx]+ActExt[idx]))
                #print("S_value: ", S_value[i][i])
                #print("idx: ", idx)
                #print("i: ", i)
                #print("S_value[i][i]: ", S_value[i][i])
                SelfS_Value[idx] = S_value[i][i]
                DSelfAbsDose_figure5[idx] = SelfS_Value[idx]* (ActInt[idx] + ActExt[idx])
                #BLABLA CROSS
                CrossAbs[idx, idex] =S_value[i][j]*(ActInt[idx]+ActExt[idx])# for j in organes if i != j)
            DoseParOrgane[idx]= sum(CrossAbs[idx, idex] for idex in range(len(organes)))# if i != organes[idex])
            
        else:
            #for idex, j in enumerate(organes):
            S_value=S_value['Valeur'].to_numpy()
            print(S_value)
            #print("S_value: ", S_value[i])
            #print("idx: ", idx)
            #print("i: ", i)
            #print("S_value[i]: ", S_value[i])
            SelfS_Value[idx] = S_value[idx]
            DSelfAbsDose_figure5[idx] = SelfS_Value[idx] * (ActInt[idx] + ActExt[idx])
        #print(i)
        #SelfS_Value_XieZaidi_annexe[idx] = S_value_XieZaidi_annexe[i][i]
        #print(SelfS_Value[idx])
        #CrossS_Value[idx] = np.zeros(len(organes))
        #DSelfAbsDose_annexe[idx]= SelfS_Value_XieZaidi_annexe[idx]*(ActInt[idx]+ActExt[idx])
        #CrossAbs[idx]=sum(S_value_XieZaidi_annexe[i][j]*(ActInt[idx]+ActExt[idx]) for j in organes if i != j)
        #print(S_valueFigure5XieZaidi.loc[i, 'Valeur'])
        #DSelfAbsDose_figure5[idx] = S_value[idx]* (ActInt[idx] + ActExt[idx])
        #print(ActInt[idx]+ActExt[idx], "s-value", S_valueFigure5XieZaidi[idx], "dose: ", DSelfAbsDose_figure5[idx])

    #print(CrossAbs)
    #print(DoseParOrgane, DSelfAbsDose_figure5)
    return DSelfAbsDose_annexe, DSelfAbsDose_figure5, SelfS_Value, CrossAbs, DoseParOrgane

    