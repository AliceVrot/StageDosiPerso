def conversionXLSXCSV(chemin):
    import os
    import pandas as pd
    chemin_csv = chemin.replace(".xlsx", ".csv")

    if not os.path.exists(chemin_csv):
        df = pd.read_excel(chemin, header=3)
        df.to_csv(chemin_csv, index=False)
        print(f"Conversion effectuée : {chemin_csv}")
    else:
        df = pd.read_csv(chemin_csv, header=3)
        print(f"Fichier déjà converti : {chemin_csv}")
    
    return df
