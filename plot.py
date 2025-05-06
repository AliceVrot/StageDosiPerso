import matplotlib.pyplot as plt
import numpy as np

# Création des données
x = np.linspace(0, 1000, 1000)         # x de 0 à 5 avec 100 points
y = np.exp(-x*np.log(2)/110)                      # y = e^x

# Création de la figure et des axes
fig, ax = plt.subplots()

# Tracé de la courbe
ax.plot(x, y, label='y = exp(x)', color='blue')

# Ajout de titre et légende
ax.set_title("Fonction exponentielle")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()

# Affichage
plt.show()