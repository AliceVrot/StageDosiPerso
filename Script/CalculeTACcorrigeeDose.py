import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pathlib
import math
#from TAC import TAC
#from conversionXLSXCSV import conversionXLSXCSV
#from CalculDoseSelf import CalculDoseSelf
#from Sorties import comparaison_DoseAbsSelf_Biomaps_Gupta
#from plot import plotActivite, barplotComparaison
#from plot import plot
import argparse

# === ARGUMENTS DE LIGNE DE COMMANDE ===
parser = argparse.ArgumentParser(description="Pipeline dosimétrie personnalisée")

parser.add_argument("--data", required=True, help="Chemin vers le fichier .csv des données principales (DonneesEntre)")
parser.add_argument("--donnevolumes", required=True, help="Chemin vers le fichier .csv des données principales (DonneesEntre)")
#parser.add_argument("--sval_annexe", required=True, help="Chemin vers le fichier des S-values (annexe)")
parser.add_argument("--s_val", required=True, help="Chemin vers les S-values")
#parser.add_argument("--dose_cross", required=True, help="Chemin vers le fichier des doses absorbées (self+cross, Gupta)")
#parser.add_argument("--dose_gupta", required=True, help="Chemin vers le fichier de comparaison dose Gupta et XieZaidi")
parser.add_argument("--ainit", type=float, required=True, help="Activité initiale injectée (MBq)")
parser.add_argument("--tphysZr", type=float, required=True, help="Temps physique du radionucléide (min)")
parser.add_argument("--tphysLu", type=float, required=True, help="Temps physique du radionucléide (min)")
#parser.add_argument("--SortieActivite", type=float, required=True, help="1 (Oui) ou 0 (Non) pour la sortie de l'activité")
#parser.add_argument("--SortieDose", type=float, required=True, help="0(non), 1(dose par organe), 2 (matrice dose absorbée par les organes cible par organe source) pour la sortie de la dose absorbée")
#parser.add_argument("--EnregistrerSortieDose", type=str, required=True, help="0 ou 1 Ou nom du fichier de sortie")

args = parser.parse_args()

Ainit = args.ainit
#Tphys = args.tphys


TphysZr = args.tphysZr #78.41 * 60
TphysLu = args.tphysLu
#TphysZr= 78.41 * 60
#TphysLu = 159.54 * 60
lambda_Zr = np.log(2) / TphysZr
lambda_Lu = np.log(2) / TphysLu




# === CHARGEMENT DES DONNÉES ===
DonneesEntre = pd.read_csv(args.data, sep=",") #sheet_name = "Feuille1", index_col=0)
#print(DonneesEntre.columns.tolist())
DonneesEntre.columns = DonneesEntre.columns.str.strip()
#print("REGARDE ICI")
#print(DonneesEntre['Délais'].to_numpy())
#print(DonneesEntre)
S_value = pd.read_csv(args.s_val, sep=",", header=0, index_col=0)

#VolumeVOI = pd.read_csv('/home/verot/Projet/Piplinepluspropre/Données/DataspourAlice.csv',  sep=None, header=0)
VolumeVOI = pd.read_csv(args.donnevolumes, sep=",")


#print("AVAAAAANT")
#print(VolumeVOI)
delais = VolumeVOI.iloc[1]  # première ligne complète
#print(delais)
#print("APREEEEES")

ordre = ['Coeur', 'Bladder', 'Spleen', 'Foie', 'Lungs', 'Cerveau', 'Estomac', 'Rein']
#calcul = pd.DataFrame(index=organes, columns=organes)
#print(calcul)
#print(S_value)
#S_values trouvé dans le tableau de Xie et Zaidi + traitement
#print (S_value.columns)
#S_value = S_value.iloc[:, 1:]
#S_value.set_index('Unnamed: 0', inplace=True)
#S_value = S_value.rename(columns={'Heart': 'Coeur', 'Liver': 'Foie', 'Lung': 'Lungs', 'Kidney': 'Rein', 'Stomach': 'Estomac', 'Bone': 'Os', 'bladder': 'Bladder', 'Brain': 'Cerveau'})
#S_value = S_value.rename(index={'Heart': 'Coeur', 'Liver': 'Foie', 'Lung': 'Lungs', 'Kidney': 'Rein', 'Stomach': 'Estomac', 'Bone': 'Os', 'bladder': 'Bladder', 'Brain': 'Cerveau'})
#print(S_value.index.tolist())
#print(S_value.index)
#print (S_value.columns)
#colonnes_voulues = ['Coeur', 'Foie', 'Rate', 'Lungs', 'Rein', 'Estomac', 'Os'] 
#S_value = S_value[ordre] 
#S_value = S_value.loc[ordre]

#print(S_value)
#organes = DonneesEntre.columns[4:18]
organesCible=S_value.columns
#print(organesCible)
#print(DonneesEntre.columns)
#print('organes: ', organes)

#print(DonneesEntre)

#print(DonneesEntre.columns)
temps = DonneesEntre['Délais'].to_numpy()*60

VolumeOrgane=VolumeVOI['volume organe ex-vivo'].to_numpy()
#VolumeVOIs = VolumeVOI['Volumes (ccm)'].to_numpy()
#print("REGAAAARDE", VolumeVOI.columns)
#VolumeOrgane = VolumeVOI['masse'].to_numpy()
#print(VolumeOrgane)
#print(temps)

def TAC(DonneesEntree, temps, Ainit, TphysZr, TphysLu):
    #temps = DonneesEntree['Délais'].to_numpy()
    tempsExt=np.linspace(temps[len(temps)-1], 2*temps[len(temps)-1], 100)
    organes = DonneesEntree.columns[4:16]
    #print(organes)
    #ActInt=np.zeros(len(organes))
    ActInt_corr=np.zeros(len(organes)) 
    ActInt_corrLu=np.zeros(len(organes)) 
    ActInt_corrLuOrgane=np.zeros(len(organes)) 
    ActInt_act=np.zeros(len(organes))
    #ActExt=np.zeros(len(organes)) 
    ActExt_corr=np.zeros(len(organes))
    ActExt_corrLu=np.zeros(len(organes))
    ActExt_corrLuOrgane=np.zeros(len(organes))
    ActExt_act=np.zeros(len(organes)) 
    y_corr_matrice=DonneesEntree.copy()
    #PartieExtrapolee=np.zeros((len(organes), len(tempsExt)))
    #x = temps
    #tempsExt=np.linspace(x[len(x)-1], 2*x[len(x)-1], 100)
    fig, axs = plt.subplots(2, 3, figsize=(15, 6))
    axs = axs.flatten()
    organes_source = ['Cœur', 'Tumeur Gauche', 'Tumeur Droite', 'Foie', 'Os']
    organes_filtres = [i for i in organes if i in organes_source]
    index=0
    #print(organes)

    for idx, i in enumerate(organes):
        #print (VolumeVOI['volume organe ex-vivo'].to_numpy())
        #print(VolumeOrgane[idx])
        
        y_act = DonneesEntree[i]
        if y_act.dtype == object:
            y_act = y_act.str.replace(',', '.')
            y_act = y_act[y_act.str.replace('.', '', 1).str.isnumeric()]
            y_act = y_act.astype(float)
        else:
            y_act = y_act.astype(float)
        
        #y_act = y_pourc*Ainit/100
        y_corr = y_act.copy()
        y_corrLu = y_act.copy()
        y_corrLuOrgane = y_act.copy()
        for j in range(len(y_act)-1):
            volume_organe = VolumeOrgane[idx]
            volume_organe = float(volume_organe.replace(',', '.')) if isinstance(volume_organe, str) else float(volume_organe)
            colonne = f'Volumes (ccm) {int(temps[j]/60)}'
            y_corr[j]=y_act[j]*(np.exp(-(temps[j])*math.log(2)/TphysZr))
            y_corr[j+1]=y_act[j+1]*(np.exp(-(temps[j+1])*math.log(2)/TphysZr))

            y_corrLu[j] = y_corr[j]*np.exp((lambda_Zr - lambda_Lu) * temps[j])
            y_corrLu[j+1] = y_corr[j+1]*np.exp((lambda_Zr - lambda_Lu) * temps[j+1])
            if colonne in VolumeVOI.columns:
                if not np.isnan(volume_organe):
                    
                    #print(VolumeVOI[colonne].to_numpy())
                    volumevoiorg = VolumeVOI[colonne].to_numpy()[idx]
                    volumevoiorg = volumevoiorg.replace(',', '.') if isinstance(volumevoiorg, str) else volumevoiorg
                    volumevoiorg = float(volumevoiorg) if not pd.isna(volumevoiorg) else 0.0
                    #print("organe:", i,"temps:", temps[j]/60, "volume organe:", volume_organe, "volume VOI:", volumevoiorg)
                
                    #if volume_organe exist: print volume_organe
                    #print("volume organe: ", volume_organe)
                    #if np.isnan(volume_organe): print (volume_organe)
                    #print("ICIIIIIII", volumevoiorg, type(volumevoiorg))
                    #VolumeOrgane[idx]=float(VolumeOrgane[idx].replace(',', '.'))
                    y_corrLuOrgane[j] = y_corrLu[j] * (volume_organe / volumevoiorg)
                    y_corrLuOrgane[j+1] = y_corrLu[j+1] * (volume_organe / volumevoiorg)
                    #print("organe:", i,"temps:", temps[j]/60, "volume organe:", volume_organe, "volume VOI:", volumevoiorg)
                #print(colonne)
                else:
                    y_corrLuOrgane[j] = y_corrLu[j]
                    y_corrLuOrgane[j+1] = y_corrLu[j+1]
                    #print("organe:", i,"temps:", temps[j]/60, "volume organe:", volume_organe, "volume VOI:", volumevoiorg)
            else:
                y_corrLuOrgane[j] = y_corrLu[j]
                y_corrLuOrgane[j+1] = y_corrLu[j+1]
                #print( 'volume lalala', "organe", i,"temps", temps[j]/60)
            #print(f"organe: {i}, j: {j}, temps[j]: {temps[j]}")    
            #print(f"y_corrLuOrgane[j]: {y_corrLuOrgane[j]}, y_corrLuOrgane[j+1]: {y_corrLuOrgane[j+1]}, y_corrLu[j]: {y_corrLu[j]}, y_corrLu[j+1]: {y_corrLu[j+1]}, volume_organe: {volume_organe}, volumevoiorg: {volumevoiorg}")  
            #y_corrLuOrgane[j] = y_corrLu[j]*np.exp((lambda_Zr - lambda_Lu) * temps[j])
            #y_corrLuOrgane[j+1] = y_corrLu[j+1]*np.exp((lambda_Zr - lambda_Lu) * temps[j+1])
            trapeze_corr=(temps[j+1]-temps[j])*(y_corr[j+1]+y_corr[j])/2
            trapeze_corrLu=(temps[j+1]-temps[j])*(y_corrLu[j+1]+y_corrLu[j])/2
            trapeze_corrLuOrgane=(temps[j+1]-temps[j])*(y_corrLuOrgane[j+1]+y_corrLuOrgane[j])/2
            #trapeze=(temps[j+1]-temps[j])*(y_pourc[j+1]+y_pourc[j])/2
            trapeze_act=(temps[j+1]-temps[j])*(y_act[j+1]+y_act[j])/2
            #ActInt[idx]=ActInt[idx]+trapeze
            ActInt_corr[idx]=ActInt_corr[idx]+trapeze_corr
            ActInt_corrLu[idx]=ActInt_corrLu[idx]+trapeze_corrLu
            ActInt_corrLuOrgane[idx]=ActInt_corrLuOrgane[idx]+trapeze_corrLuOrgane
            ActInt_act[idx]=ActInt_act[idx]+trapeze_act
        #Derniereactivite=y_corr[len(y_corr)-1]
        #PartieExtrapolee[idx] = Derniereactivite*np.exp(-(tempsExt-temps[len(temps)-1])*math.log(2)/TphysZr)
        print ("LALALALAAAAAAA", len(y_corr))
        ActExt_corr[idx]=y_corr[len(y_corr)-1]*TphysZr/math.log(2)
        ActExt_corrLuOrgane[idx]=y_corrLuOrgane[len(y_corr)-1]*TphysLu/math.log(2)
        ActExt_corrLu[idx]=y_corrLu[len(y_corr)-1]*TphysLu/math.log(2)
        y_corr_matrice[i]=y_corr
        #Amax=y_act[len(y_act)-1]
        Amax=y_corr[len(y_act)-1]
        AmaxLu=y_corrLu[len(y_act)-1]
        AmaxLuOrgane=y_corrLuOrgane[len(y_act)-1]
        PartieExtrapolee = Amax*np.exp(-(tempsExt-temps[len(temps)-1])*math.log(2)/TphysZr)
        PartieExtrapoleeLu= AmaxLu*np.exp(-(tempsExt-temps[len(temps)-1])*math.log(2)/TphysLu)
        PartieExtrapoleeLuOrgane = AmaxLuOrgane*np.exp(-(tempsExt-temps[len(temps)-1])*math.log(2)/TphysLu)
        
        if i in organes_filtres:
            #print ("LAAAAAAAAA",index, idx, i)
            axs[index].set_title(i)
            #axs[index].plot(tempsExt/60, PartieExtrapoleeLuOrgane, label=i, linewidth=0.7)
            axs[index].plot(tempsExt/60, PartieExtrapoleeLuOrgane, label=i, linewidth=0.7)
            #axs.label.set_size(10)
            axs[index].set_xlabel('Temps (heures)')
            axs[index].set_ylabel('Activité (MBq)')
            #axs[idx].scatter(x, y_corr, label=i, linewidth=0.7)
            #axs[idx].plot(tempsExt, PartieExtrapolee, label=i, linewidth=0.7)
            
            #print(x, y_pourc)
            #axs[index].scatter(temps/60, y_corrLuOrgane, label=i, linewidth=0.7)
            axs[index].scatter(temps/60, y_corrLuOrgane, label=i, linewidth=0.7)
            axs[index].set_title(i)
            index = index+1
            #axs[idx].set_ylim(0, max(y_pourc)*1.1)
            
    #fig, ax = plt.subplots()        
    #ax.plot(temps/60, np.exp(-(temps/60)*math.log(2)/TphysZr), label='Activité Corrigée Lu', linewidth=0.7, color='blue')
    plt.tight_layout()
    plt.show()
    #plt.show()

    Activitecumule = pd.DataFrame({
        'Organes': organes,
        'ActTot': ActInt_corr+ActExt_corr
    })
    print(Activitecumule)
        

    return ActInt_corr, ActInt_corrLu, ActInt_corrLuOrgane, ActExt_corr, ActExt_corrLu, ActExt_corrLuOrgane, PartieExtrapoleeLuOrgane, y_corr_matrice, Activitecumule

#plt.tight_layout()




ActInt_corr, ActInt_corrLu, ActInt_corrLuOrgane, ActExt_corr, ActExt_corrLu, ActExt_corrLuOrgane, PartieExtrapoleeLuOrgane, y_corr_matrice, Activitecumule = TAC(DonneesEntre, temps, Ainit, TphysZr, TphysLu)
ActTot=ActInt_corr+ActExt_corr
#print("iciiiiii", ActTot)
#ActInt_corr, ActExt_corr, ActExt_corrLu, ActInt_corrLu, PartieExtrapolee, y_corr_matrice, Activitecumule = TAC(DonneesEntre, temps, Ainit, TphysZr, TphysLu)
#print(Activitecumule)

def CalculDoseSelf(ActTot, organes, S_value): #, S_value_XieZaidi_annexe
    #print(organes)
    #DSelfAbsDose_annexe = np.zeros(len(organes))
    DSelfAbsDose = np.zeros(len(organes))
    CrossAbs = np.zeros((len(organes), len(organes)))
    SelfS_Value = np.zeros(len(organes))
    DoseParOrgane = np.zeros(len(organes))
    #CrossS_Value = np.zeros(len(organes))
    #print(S_value)
    #print(np.shape(S_value))
    #if np.shape(S_value) == (len(organes), 1): S_value=S_value['Valeur'].to_numpy()
    #if np.shape(S_value) == (len(organes), len(organes)):
    for idx, i in enumerate(organes):
        for idex, j in enumerate(organes):
            #if i==j : print (S_value[i][j], (ActInt[idx]+ActExt[idx]), S_value[i][j]*(ActInt[idx]+ActExt[idx]))
            #print("S_value: ", S_value[i][i])
            #print("idx: ", idx)
            #print("i: ", i)
            #print("S_value[i][i]: ", S_value[i][i])
            SelfS_Value[idx] = float(S_value[i][i].replace(',', '.'))
            #SelfS_Value[idx] = S_value[i][i]
            DSelfAbsDose[idx] = SelfS_Value[idx]* ActTot[idx] 
                #BLABLA CROSS
            CrossAbs[idx, idex] =float(S_value[i][j].replace(',', '.'))*(ActTot[idx])# for j in organes if i != j)
            #print(CrossAbs[idx, idex])
        DoseParOrgane[idx]= sum(CrossAbs[idx, idex] for idex in range(len(organes)))# if i != organes[idex])
          
    #else:
    #    S_value=S_value['Valeur'].to_numpy()
    #    for idx, i in enumerate(organes):
            #for idex, j in enumerate(organes):
            #print(S_value)
            #S_value=S_value['Valeur'].to_numpy()
            #print(S_value)
            #print("S_value: ", S_value[i])
            #print("idx: ", idx)
            #print("i: ", i)
            #print("S_value[i]: ", S_value[i])
    #        SelfS_Value[idx] = S_value[idx]
    #        DSelfAbsDose[idx] = SelfS_Value[idx] * (ActTot[idx])
    #    print(DSelfAbsDose)
   
    #print(CrossAbs)
    #print(DoseParOrgane, DSelfAbsDose_figure5)
    return DSelfAbsDose, SelfS_Value, CrossAbs, DoseParOrgane

    
organes = DonneesEntre.columns[4:16]
#DSelfAbsDose, SelfS_Value_XieZaidi_annexe, distribDose_parOrgane, DAbsTotale = CalculDoseSelf(ActTot, organesCible, S_value)
#print(f"DSelfAbsDose: {DSelfAbsDose}, distribDose_parOrgane: {distribDose_parOrgane}, DAbsTotale: {DAbsTotale}")
Resultats = pd.DataFrame({
        'Organes': organes,
        'Activité Cumulée Interpolée Corrigée Lu(MBq.min) dans la VOI': ActInt_corrLu*60/1000,
        'Activité Cumulée Extrapolée Corrigée Lu(MBq.min) dans la VOI': ActExt_corrLu*60/1000,
        'Activité  Accumulée Totale Lu(MBq.min) dans la VOI': (ActInt_corrLu + ActExt_corrLu)*60/1000,
        'Activité Cumulée Interpolée Corrigée Zr(MBq.min) dans la VOI': ActInt_corr*60/1000,
        'Activité Cumulée Extrapolée Corrigée Zr(MBq.min) dans la VOI': ActExt_corr*60/1000,
        'Activité cumulée corrigée Totale Zr(MBq.min) dans la VOI': (ActInt_corr+ActExt_corr)*60/1000,
        'Activité Cumulé Interpolée Corrigée Lu(MBq) dans l organe': ActInt_corrLuOrgane*60/1000,
        'Activité Cumulée Extrapolée Corrigée Lu(MBq) dans l organe': ActExt_corrLuOrgane*60/1000,
        'Activité Cumulée Totale Lu(MBq) dans l organe': (ActInt_corrLuOrgane + ActExt_corrLuOrgane)*60/1000
        #'Self Absorbed S-Value': S_value,
        #'Dose Absorbée (mGy.MBq⁻¹)': DAbsTotale,
    })

ActExt_corr=ActExt_corr*60
ActInt_corr=ActInt_corr*60
#print("Activité Interpolée Corrigée (MBq.sec): ", ActInt_corr) 
#print("Activité Extrapolée Corrigée (MBq.sec): ", ActExt_corr)
#print(DAbsTotale)
#print(ActTot)

current_path = pathlib.Path(__file__).parent.resolve()
Activitecumule.to_csv(current_path / 'ActTot.csv',header=True, index=True)
Resultats.to_csv('/home/verot/Projet/Piplinepluspropre/output/TACAnneLaure1.csv',header=True, index=True)
print(Resultats)


reponse = input("Voulez-vous enregistrer les résultats dans un fichier CSV ? (y/n): ")
if reponse.lower() in ["y", "yes", "o", "oui"]:
    fichier = input("Entrez le nom du fichier CSV (par défaut '/home/verot/Projet/Piplinepluspropre/output/TACAnneLaure1.csv'): ")
    if not fichier:
        Resultats.to_csv("/home/verot/Projet/Piplinepluspropre/output/TACAnneLaure1.csv", index=False)
        #print("Résultats enregistrés dans 'svalues_results.csv'.")
    else:
        Resultats.to_csv(fichier, index=False)
        #df_svalues.to_csv("svalues_results.csv", index=False)
        print(f"Résultats enregistrés dans ", fichier)