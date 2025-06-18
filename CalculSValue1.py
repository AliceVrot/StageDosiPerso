import matplotlib.pyplot as plt
import numpy as np
import opengate as gate
import pathlib
import pyvista
import SimpleITK as sitk
import argparse
import pandas as pd

#nbparticules = 42606544 

organes_labels = {
    3: "Cerveau",
    4: "Coeur",
    5: "Poumons",
    6: "Foie",
    7: "Estomac",
    8: "Slpeen",
    9: "Rein",
    10: "Bladder"
}




def caluclmass(act, edep, nbparticules, densite): #ct, edep, dose, nbparticules, densite):
    #moby_ct = ('/home/verot/Projet/MOBY/F_LR_30g_atn_1.mhd')
    #moby_act = ('/home/verot/Projet/MOBY/F_LR_30g_act_1.mhd')
    #moby_edep = ('/home/verot/Projet/MOBY/outputMobyF18/dose_edep6h.mhd')
    Edep=sitk.ReadImage(edep)
    #Dosedep=sitk.ReadImage(dose)
    #moby_ct = sitk.ReadImage(ct)
    moby_act = sitk.ReadImage(act)
    array_act = sitk.GetArrayFromImage(moby_act)
    #mask_entiers = array_act == array_act.astype(int)
    rounded_array_act = np.floor(array_act).astype(np.int16)#np.floor(array_act + 0.5).astype(np.int16)
    #rounded_array_act = np.floor(array_act + 0.5).astype(np.int16)
    #print(np.floor(2.5 + 0.5), np.floor(2.1 + 0.5), np.floor(3.5 + 0.5), np.rint(3.5).astype(np.int16), np.round(3.5).astype(np.int16))
    unique_labels, counts = np.unique(rounded_array_act, return_counts=True)



    #densité = np.array([0, 0, 0, 1.04, 1.06, 0.3, 1.05, 1.04, 1.06, 1.05, 1.04])  # Densité en g/cm³ A CHANGER!!!
    #for label, count in zip(unique_labels, counts):
        #print(f"Label {label}: {count} voxels")
    #    a=1
    voxel_volume = np.prod(moby_act.GetSpacing())
    print(voxel_volume)
    volume = counts * voxel_volume * 1e-3  # Volume en cm³ ((0.29mm)³ par voxel)
    
    #volume = counts * (0.29*1e-1)**3

    mass = volume * densite # Masse en g

    array_edep = sitk.GetArrayFromImage(Edep)
    #array_dosedep = sitk.GetArrayFromImage(Dosedep)
    energies = np.zeros(len(unique_labels))
    #doses_mc = np.zeros(len(unique_labels))
    #unique_labels.copy()
    array_edep = sitk.GetArrayFromImage(Edep)
    #array_dose = sitk.GetArrayFromImage(Dosedep)
    print("Edep - min:", np.min(array_edep), "max:", np.max(array_edep), "mean:", np.mean(array_edep))
    #print("Dose - min:", np.min(array_dose), "max:", np.max(array_dose), "mean:", np.mean(array_dose))
    flatt_array_edep = array_edep.flatten()
    flatt_rounded_array_act = rounded_array_act.flatten()
    #flatt_array_dose = array_dosedep.flatten()
   # print("flatt_array_dose", flatt_array_dose)
    edeptot = np.sum(flatt_array_edep)
    for edep, label in zip (flatt_array_edep, flatt_rounded_array_act):
        #print(np.shape(label), np.shape(edep))
        #print(f"Label {label} has energy deposition: {edep} MeV")
        #if label == 3:
        energies[label] += edep
        #dose_mc[label] += 
        #print(f"Label {label} has energy deposition: {edep} MeV")

    #for dosemc, label in zip (flatt_array_dose, flatt_rounded_array_act):
     #   doses_mc[label] += dosemc
        #print("lalalalal")
    #print("doses_mc", doses_mc) #en eV???

    #print("Energies", energies) ##en eV???
    
    #print(unique_labels, counts)
    #print("masse", mass) #ici masse est en g
    dose = (energies * 1.6e-13) / (mass * 1e-3) 
    #print( f"dose calculée avec edep: {dose}")
    #print(f"Gy et  doses_mc: {doses_mc * 10e-9}")
    #dose_mc = 
    #print (f"dose: {dose} et nb particules: {nbparticules}")
    S_values= dose / nbparticules 
    #S_valuesGy = S_values * 1.6 * 1e-16 * 1e3 #en Gy
    S_valuesmGy_MBqs = S_values * (1e6 * 1e3) #en mGy/MBq
    #print("S_values", S_valuesmGy_MBqs)
    #S_valuesDosemGy_MBqs = (doses_mc/ nbparticules) * ( 1e6 ) #en mGy/MBq.s

    results = []

    for i in range(len(unique_labels)):
        if unique_labels[i] in organes_labels:
            #print(f"Label {unique_labels[i]} ({organes_labels[unique_labels[i]]}): {mass[i]:.2f} g, Energy: {energies[i]:.2f} MeV, S-value: {S_valuesmGy_MBqs[i]:.2f} mGy/MBq.s")
        
            results.append({
                'Organe': organes_labels[unique_labels[i]],
                'Label': unique_labels[i],
                'Volume (cm³)': f"{volume[i]}",
                'Masse (g)': f"{mass[i]:.2f}",
                'Énergie déposée (MeV)': f"{energies[i]:.3f}",
                #'Energie??': f"{(doses_mc[i] * 10e-6 * mass[i] / 1.6e-19)* 10e-6}",
                'Dose (mGy)': f"{dose[i]}",
                #'Dose MC (mGy)': f"{doses_mc[i] * 10e-6}",
                'S-value (mGy/MBq.s)': f"{S_valuesmGy_MBqs[i]}",
                #'S-value de dose (mGy/MBq.s)': f"{S_valuesDosemGy_MBqs[i]}"
            })
    df_svalues = pd.DataFrame(results)
    print(df_svalues)
        #else:
        #    print(f"Label {unique_labels[i]}: {mass[i]:.2f} g, Energy: {energies[i]:.2f} MeV, S-value: {S_valuesmGy_MBqs[i]:.2f} mGy/MBq.s")

    return mass, energies, volume, edeptot, S_valuesmGy_MBqs, df_svalues


#densite = np.array([0, 0, 0, 1.04, 1.06, 0.3, 1.05, 1.04, 1.06, 1.05, 1.04])  # Densité en g/cm³ A CHANGER!!!


#mass, energies, volume, edeptot, S_values = caluclmass('/home/verot/Projet/MOBY/F_LR_30g_act_1.mhd', '/home/verot/Projet/MOBY/F_LR_30g_atn_1.mhd', '/home/verot/Projet/MOBY/outputMobyF18/dose_edep6h.mhd', nbparticules, densite)
#mass, energies, volume, edeptot, S_values = caluclmass(
#    '/home/verot/Projet/MOBY/F_LR_30g_act_1.mhd',   # act
#    '/home/verot/Projet/MOBY/F_LR_30g_atn_1.mhd',   # ct
#    '/home/verot/Projet/MOBY/outputMobyF18/dose_edep6h.mhd',
#    nbparticules,
#    densite
#)
#print(S_values)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcul S-values (version simple)")
    #parser.add_argument("--ct", required=True, help="Fichier .mhd du CT")
    parser.add_argument("--act", required=True, help="Fichier .mhd de l'activité")
    parser.add_argument("--edep", required=True, help="Fichier .mhd de l'énergie déposée")
    #parser.add_argument("--dose", required=True, help="Fichier .mhd de la dose")
    parser.add_argument("--n", type=float, required=True, help="Nombre de particules simulées")
    parser.add_argument("--densities", nargs="+", type=float, required=True, help="Liste des densités par label")

    args = parser.parse_args()

    mass, energies, volume, edeptot, S_values, df_svalues = caluclmass(args.act, args.edep, args.n, np.array(args.densities))#caluclmass(args.act,args.ct, args.edep, args.dose, args.n, np.array(args.densities))
    
    reponse = input("Voulez-vous enregistrer les résultats dans un fichier CSV ? (y/n): ")
    if reponse.lower() in ["y", "yes", "o", "oui"]:
        fichier = input("Entrez le nom du fichier CSV (par défaut 'svalues_results.csv'): ")
        if not fichier:
            df_svalues.to_csv("svalues_results.csv", index=False)
            print("Résultats enregistrés dans 'svalues_results.csv'.")
        else:
            df_svalues.to_csv(fichier, index=False)
        #df_svalues.to_csv("svalues_results.csv", index=False)
            print(f"Résultats enregistrés dans ", fichier)

    #print("S-values (mGy/MBq.s) :", S_values)