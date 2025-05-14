# Dosimétrie personnalisée
L’objectif de ce projet est d’évaluer la distribution de dose absorbée dans les organes à risque chez la souris après administration d’un ⁸⁹Zr-anti-PD-L1, en combinant des données d’imagerie TEP et CT, et de comparer plusieurs méthodes de dosimétrie: dosimétrie à l'échelle de l'organe ou du voxel.
Une pipeline de dosimetrie pour ces deux modalitésas été/ sera développée.

- #### Dosimétrie à l'echelle de l'organe
  Formalisme MIRD: rapide explication

- #### Dosimétrie à l'echelle du voxel
  Input et output de monte carlo

avec une modélisation dosimétrique multicritère (MIRD, S-values, Monte Carlo).

## Structure du code
- Le fichier principale est main.py
  - TAC.py
  - CalculDoseSelf.py
  - Sorties.py
  - plot.py

Dans les premières lignes dans fichier main.py corresponent à l'importation de la bibliothèque pandas (il faut l'installer au préalable) puis les autres fonctions qui constituent ce projet. Il faut donc les enregistrer dans le dossier de travail au préalable.

Les lignes suivants correspondent à l'importations des données d'entrée. Il peut être important de changer le chemin vers le fichier.

Il peut aussi être utile de changer Ainit (l'activité injectée) en fonction du projet, et Tphys (période physique de l'isotope utilisé).


## Utiliser le code

1. Cloner ce repository
2. Installer les packages avec conda install --file requirements.txt
3. 


