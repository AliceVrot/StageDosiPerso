#CODE CHATGPT PAS VERIFIE



import numpy as np
import matplotlib.pyplot as plt

# --- Données ---
# Demi-vies en heures
T_half_Zr = 78.4  # Zr-89
T_half_Lu = 160.8  # Lu-177 (6.7 jours)

# Constantes de décroissance
lambda_Zr = np.log(2) / T_half_Zr
lambda_Lu = np.log(2) / T_half_Lu

# Échelle de temps (en heures)
t = np.linspace(0, 200, 500)  # 0 à 200 h, 500 points

# Exemple de courbe d’activité Zr-89 (fictive)
# Une montée exponentielle + décroissance radioactive
A0 = 1.0
A_bio = np.exp(-0.01 * t)  # décroissance biologique
A_Zr = A0 * A_bio * np.exp(-lambda_Zr * t)  # signal mesuré Zr-89

# Transposition vers Lu-177
A_Lu = A_Zr * np.exp((lambda_Zr - lambda_Lu) * t)

# --- Tracé ---
plt.plot(t, A_Zr, label='Zr-89 mesuré')
plt.plot(t, A_Lu, label='Lu-177 simulé')
plt.xlabel("Temps (h)")
plt.ylabel("Activité relative (a.u.)")
plt.title("Transposition Zr-89 → Lu-177")
plt.legend()
plt.grid()
plt.show()
