
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math

chemin_xlsx = '/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange.xlsx'
chemin_csv = '/home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange.csv'
chemin_xlsx1 = '/home/verot/Projet/DonneesGupta/S_values_XieZaidi.xlsx'
chemin_csv1 = '/home/verot/Projet/DonneesGupta/S_values_XieZaidi.csv'
chemin_xlsx2 = '/home/verot/Projet/DonneesGupta/D_abs.xlsx'
chemin_csv2 = '/home/verot/Projet/DonneesGupta/D_abs.csv'
chemin3='/home/verot/Projet/DonneesGupta/Figure7.csv'
y=1

# Ne convertir en .csv que si le fichier n'existe pas déjà
if not os.path.exists(chemin_csv):
    xlsx = pd.read_excel(chemin_xlsx)
    xlsx.to_csv(chemin_csv)
    print("hihihihihi")
if not os.path.exists(chemin_csv1):
    xlsx = pd.read_excel(chemin_xlsx1)
    xlsx.to_csv(chemin_csv1)
    print("hihihihihi")
if not os.path.exists(chemin_csv2):
    xlsx = pd.read_excel(chemin_xlsx2)
    xlsx.to_csv(chemin_csv2)
    print("hihihihihi")

df = pd.read_csv(chemin_csv, header=3)
S_value=pd.read_csv(chemin_csv1, header=0)
D_abs=pd.read_csv(chemin_csv2, header=1).iloc[:, 1:]
#print(df)
#print(S_value)
XieZaidi=pd.read_csv(chemin3, header=1)
#print(XieZaidi)


x = df['Délais'].to_numpy()
x2=np.linspace(x[len(x)-1], 1.5*x[len(x)-1], 100)
#print(x2)
organes = df.columns[6:16]
fig, axs = plt.subplots(2, 4, figsize=(15, 6))
axs = axs.flatten()




Ainit= 15.22
ActInt=np.zeros(len(organes))
ActInt_corr=np.zeros(len(organes)) 
ActInt_act=np.zeros(len(organes))
ActExt=np.zeros(len(organes)) 
ActExt_corr=np.zeros(len(organes))
ActExt_act=np.zeros(len(organes)) 
Tphys=109.771

for idx, i in enumerate(organes):
    y_pourc = df[i]#*Ainit/100
    #print(i)
    #print(y_pourc)
    y_act = y_pourc*Ainit/100
    y_corr = y_act.copy()
    axs[idx].scatter(x, y_pourc, label=i, linewidth=0.7)
    #axs[idx].scatter(x, y_act, label=i, linewidth=0.7)
    axs[idx].set_title(i)
    n=max(y_pourc)+0.1*max(y_pourc)
    Amax=y_corr[len(y_pourc)-1]
    #Amax=y_act[len(y_pourc)-1]
    z = Amax*np.exp(-(x2-85)*math.log(2)/Tphys)
    #axs[idx].plot(x2, z, label=i, linewidth=0.7)
    for j in range(len(y_pourc)-1):
        y_corr[j]=y_act[j]*(np.exp(-(x[j])*math.log(2)/Tphys))
        T_corr=(x[j+1]-x[j])*(y_corr[j+1]+y_corr[j])/2
        T=(x[j+1]-x[j])*(y_pourc[j+1]+y_pourc[j])/2
        T_act=(x[j+1]-x[j])*(y_act[j+1]+y_act[j])/2
        ActInt[idx]=ActInt[idx]+T
        ActInt_corr[idx]=ActInt_corr[idx]+T_corr
        ActInt_act[idx]=ActInt_act[idx]+T_act
        #ActIntCor[idx]=ActInt[idx]/(np.exp(-(x[j])*math.log(2)/Tphys))
    #y_corr[len(y_pourc)]=y_act[len(y_pourc)]*(np.exp(-(85)*math.log(2)/Tphys))
    ActExt_corr[idx]=y_corr[len(y_corr)-1]*Tphys/math.log(2)
    ActExt[idx]=y_pourc[len(y_pourc)-1]*Tphys/math.log(2)
    ActExt_act[idx]=y_act[len(y_act)-1]*Tphys/math.log(2)
    #print(ActExt[idx], y_corr[len(y_corr)-1], Tphys/math.log(2))
    #print(y_corr[len(y_pourc)-1], y_act[len(y_pourc)-1])
    #ActExt[idx-1]=y_act[len(y_act)-1]*Tphys/math.log(2)


ActInt=ActInt*60
ActInt_corr=ActInt_corr*60
ActInt_act=ActInt_act*60
ActExt=ActExt*60
ActExt_corr=ActExt_corr*60
ActExt_act=ActExt_act*60

print(ActInt_corr, ActExt_corr)
#print(organes, ActInt)
#print(ActExt)

#print(ActIntCor)
plt.tight_layout()
#plt.show()


#df['Somme_Activite'] = df[organes].sum(axis=1)
#print(df)
#df.info()



ordre = ['Coeur', 'Bladder', 'Spleen', 'Foie', 'Lungs', 'Cerveau', 'Estomac', 'Rein']
calcul = pd.DataFrame(index=organes, columns=organes)
#print(calcul)
#print(S_value)
#S_values trouvé dans le tableau de Xie et Zaidi + traitement
S_value = S_value.iloc[:, 1:]
S_value.set_index('Unnamed: 0', inplace=True)
S_value = S_value.rename(columns={'Heart': 'Coeur', 'Liver': 'Foie', 'Lung': 'Lungs', 'Kidney': 'Rein', 'Stomach': 'Estomac', 'Bone': 'Os', 'bladder': 'Bladder', 'Brain': 'Cerveau'})
S_value = S_value.rename(index={'Heart': 'Coeur', 'Liver': 'Foie', 'Lung': 'Lungs', 'Kidney': 'Rein', 'Stomach': 'Estomac', 'Bone': 'Os', 'bladder': 'Bladder', 'Brain': 'Cerveau'})
#print(S_value.index.tolist())
#print(S_value.index)
#colonnes_voulues = ['Coeur', 'Foie', 'Rate', 'Lungs', 'Rein', 'Estomac', 'Os'] 
S_value = S_value[ordre] 
S_value = S_value.loc[ordre]

#S-value de Xie et Zaidi tableau 5
S_value5 = pd.DataFrame({
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
S_value5.index.name = 'organe'

#print(S_value)
SelfAbs = np.zeros(len(organes))
CrossAbs = np.zeros(len(organes))
SelfS_Value = np.zeros(len(organes))
#CrossS_Value = np.zeros(len(organes))

for idx, i in enumerate(organes):
    SelfS_Value[idx] = S_value[i][i]
    #CrossS_Value[idx] = np.zeros(len(organes))
    #SelfAbs[idx]= SelfS_Value[idx]*(ActInt_corr[idx]+ActExt_corr[idx])
    CrossAbs[idx]=sum(S_value[i][j]*(ActInt[idx]+ActExt[idx]) for j in organes if i != j)
    SelfAbs[idx] = S_value5.loc[i, 'valeur'] * (ActInt_corr[idx] + ActExt_corr[idx])

#print(SelfAbs)
#Abs_nous=SelfAbs+CrossAbs
#print(Abs_nous)
#S_value['SelfAbs'] = SelfAbs
#S_value['CrossAbs'] = S_value[CrossAbs].fillna(0)
#S_value['TotalAbs'] = S_value[SelfAbs] + S_value[CrossAbs]

#print(S_value)
#D_abs = D_abs.iloc[:, 1:]
D_abs.set_index('Organs', inplace=True)
D_abs = D_abs.rename(index={'Heart wall': 'Coeur', 'Liver': 'Foie', 'Kidneys': 'Rein', 'Stomach wall': 'Estomac', 'Bladder wall': 'Bladder', 'Brain': 'Cerveau'})
D_abs = D_abs.loc[ordre] 


#Les résultats de calcul de dose absorbée de Xie et Zaidi
XieZaidi.set_index('Organe', inplace=True)
XieZaidi = XieZaidi.rename(index={'Heart wall': 'Coeur', 'Liver': 'Foie', 'Kidneys': 'Rein', 'Stomach wall': 'Estomac', 'Bladder wall': 'Bladder'})
XieZaidi = XieZaidi.reindex(ordre, fill_value=0)
#XieZaidi = XieZaidi.loc[['Coeur', 'Bladder', 'Spleen', 'Foie', 'Lungs', 'Cerveau', 'Estomac', 'Rein']] 
#print(XieZaidi)



tout = pd.DataFrame({
    'Organes': organes,
    'Activité Interpolée (min⁻1)': ActInt,
    'Activité Interpolée Corrigée (MBq.min)': ActInt_corr,
    'Activité Extrapolée (MBq.min)': ActExt,
    'Activité Extrapolée Corrigée (MBq.min)': ActExt_corr,
    'Activité Totale (MBq.min)': ActInt + ActExt,
    'Activité Totale Corrigée (MBq.min)': ActInt_corr + ActExt_corr,
    'Dose Absorbée Self (Gy) Alice': SelfAbs/Ainit,
    'Dose Absorbée Self (Gy) Gupta': D_abs['Self-absorbed dose'],
    'Dose Absorbée Cross (Gy) Alice': CrossAbs/Ainit,
    'Dose Absorbée Cross (Gy) Gupta': D_abs['Cross-absorbed dose'],
    'Dose Absorbée Total (Gy) Alice': (SelfAbs + CrossAbs)/Ainit,
    'Dose Absorbée Total (Gy) Gupta': D_abs['Total absorbed dose']
})



Comparaison = pd.DataFrame({
    'Organes': organes,
    'Intégration TAC (sec)': ActInt + ActExt,
    'Activité Accumulée Totale (MBq.sec)': (ActInt_corr + ActExt_corr),
    'Self Absorbed S-Value (mGy/MBq.s)': S_value5['valeur'],
    'Dose Absorbée Self (mGy.MBq⁻¹) Alice': SelfAbs/Ainit,
    'Dose Absorbée Self (mGy.MBq⁻¹) Gupta': D_abs['Self-absorbed dose'],
    'Différence Alice Gupta(%)': abs(SelfAbs/Ainit - D_abs['Self-absorbed dose'])/ D_abs['Self-absorbed dose'] * 100,
    'Dose Absorbée Total (mGy.MBq⁻¹) Zaidi': XieZaidi['Xie and Zaidi'],
    'Dose Absorbée Total (mGy.MBq⁻¹) Gupta': D_abs['Total absorbed dose'],
    'Différence (%)': abs(XieZaidi['Xie and Zaidi'] - D_abs['Total absorbed dose'])/ D_abs['Total absorbed dose'] * 100
})

print(Comparaison)
Comparaison.to_excel("/home/verot/Projet/Sorties/comparaison.xlsx")

#print(tout)
#print(DF_result)
#DF_results=pd.merge(D_ab, Abs_nous, left_on = ['organes'])
#print(DF_result)
plt.figure(figsize=(10, 5))
truc=2*(tout['Dose Absorbée Total (Gy) Alice']-tout['Dose Absorbée Total (Gy) Gupta'])/(tout['Dose Absorbée Total (Gy) Alice']+tout['Dose Absorbée Total (Gy) Gupta'])*100
truc.plot(kind='bar', legend=False, figsize=(10, 6))

#abs_max = max(abs(truc))
#plt.ylim(-abs_max * 1.1, abs_max * 1.1)
plt.title('Comparaison des doses absorbées')
plt.xlabel('Organes')
plt.ylabel('Différence (%)')
plt.legend()
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
#plt.show()
#plt.bar(DF_result['Organs'], truc, label='Nous', alpha=0.5)

if y==1:
    plt.savefig("/home/verot/Projet/Sorties/barplot_organs.png", dpi=300) 
#DF_result.to_excel("/home/verot/Projet/Sorties/tableau_comparaison.xlsx")
    tout.to_excel("/home/verot/Projet/Sorties/tout!.xlsx")
A_l_envers = np.zeros(len(organes))
#print(A_l_envers)
for idx, i in enumerate(organes):

    A_l_envers[idx]=D_abs['Self-absorbed dose'][i]/S_value[i][i]

#print(A_l_envers*Ainit)
#print((ActInt+ActExt))