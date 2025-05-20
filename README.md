# Exemple de commande
python Main.py --data /home/verot/Projet/DonneesGupta/Donnes_Gupta_Arrange1.csv --s_val /home/verot/Projet/DonneesGupta/S_values_XieZaidi1.csv --ainit 15.22 --tphys 109.771 --SortieActivite 1 --EnregistrerSortieDose /home/verot/Projet/Sorties/recapitulatif.csv

--data: chemin vers le fichier csv d'entrée

--s_val: chemin vers le fichier contenant les S-values. Peut contenir juste les S_value Self absorbed ou toutes les S_values

--ainit: activité initiale: l'activité injectée dans la sourie en MBq (par exemple 15.22)

--tphys: Période physique du radionucléide utilisé en minutes (par exemple 109.771 pour le Fluor 18)

--SortieActivite: entrée possibles: 0 ou 1; 1: Enregistre un fichier csv contenant l'activité calculé, 0 ne fait rien 

--enregistrerSortieDose: entrée possibles: nom du fichier de sortie désiré : les résultats seront enregistrés sous ce fichier; 1 : le fichier sera enregistré sous le nom du fichier d'entré + _résultat, autre entrée: ne fait rien


## Dosimétrie personnalisée
L’objectif de ce projet est d’évaluer la distribution de dose absorbée dans les organes à risque chez la souris après administration d’un ⁸⁹Zr-anti-PD-L1, en combinant des données d’imagerie TEP/SPECT et CT, et de comparer plusieurs méthodes de dosimétrie: dosimétrie à l'échelle de l'organe ou du voxel.
Une pipeline de dosimetrie pour ces deux modalitésas été/ sera développée.
Utilisation de simulation Monte Carlo à l'aide de GATE10

- #### Dosimétrie à l'echelle de l'organe
  - Utilisation du formalisme MIRD
  - Fantôme MOBY
  - Simulation Monte Carlo pour chaque organe source. Détermination de distribution d'energie déposée, distribution de la dose, nombre de coup et incertitude locale
    
- #### Dosimétrie à l'echelle du voxel
  - Fantôme voxélisé basé sur l'imagerie du patient/ de la sourie
  - Calcul de distribution d'energie déposée, distribution de la dose, nombre de coup et incertitude locale



### Structure du code
- Le fichier principale est main.py
  - TAC.py  permet de calculer l'activité cumulée dans les organes à partir des mesures issue de l'imagerie TEP/SPECT
  - CalculDoseSelf.py  Permet de calculer la dose absorbée due à l'irradiation de l'organe envers lui même
  - Sorties.py
  - plot.py




### Utiliser le code

1. Créer un environnement virtuel conda
2. Installer opengate (pas necessaire pour ce qu'il y a dans le repository à date mais sera important plus tard)
3. Cloner ce repository
4. Installer les packages avec conda install --file requirements.txt
5. Changer les chemins vers les données d'entré
6. Modifier Ainit (l'activité injectée en MBq) et Tphys (période physique de l'isotope utilisé en minutes) en fonction du projet



## Installation opengate
https://opengate-python.readthedocs.io/en/master/user_guide/user_guide_installation.html


