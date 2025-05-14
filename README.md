# Dosimétrie personnalisée
L’objectif de ce projet est d’évaluer la distribution de dose absorbée dans les organes à risque chez la souris après administration d’un ⁸⁹Zr-anti-PD-L1, en combinant des données d’imagerie TEP/SPECT et CT, et de comparer plusieurs méthodes de dosimétrie: dosimétrie à l'échelle de l'organe ou du voxel.
Une pipeline de dosimetrie pour ces deux modalitésas été/ sera développée.
Utilisation de simulation MonteCarlo à l'aide de GATE10

- #### Dosimétrie à l'echelle de l'organe
  - Utilisation du formalisme MIRD
  - Fantôme MOBY
  - Simulation Mmonte Carlo pour chaque organe source. Détermination de distribution d'energie déposée, distribution de la dose, nombre de coup et incertitude locale
    
- #### Dosimétrie à l'echelle du voxel
  - Fantôme voxélisé basé sur l'imagerie du patient/ de la sourie
  - Calcul de distribution d'energie déposée, distribution de la dose, nombre de coup et incertitude locale



## Structure du code
- Le fichier principale est main.py
  - TAC.py  permet de calculer l'activité cumulée dans les organes à partir des mesures issue de l'imagerie TEP/SPECT
  - CalculDoseSelf.py  Permet de calculer la dose absorbée due à l'irradiation de l'organe envers lui même
  - Sorties.py
  - plot.py




## Utiliser le code

1. Créer un environnement virtuel conda
2. Cloner ce repository
3. Installer les packages avec conda install --file requirements.txt
4. Changer les chemins vers les données d'entré
5. Modifier Ainit (l'activité injectée en MBq) et Tphys (période physique de l'isotope utilisé en minutes) en fonction du projet


