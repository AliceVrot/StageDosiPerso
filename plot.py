import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import os
#import math


def plotActivite(temps,Activite,PartieExtrapolee,titre):
    fig, axs = plt.subplots(2, 4, figsize=(15, 6))
    axs = axs.flatten()
    x2 = np.linspace(temps[len(temps)-1], 2*temps[len(temps)-1], 100)
    for idx, i in enumerate (titre):
        axs[idx].scatter(temps, Activite[i], label=titre, linewidth=0.7)
        axs[idx].plot(x2, PartieExtrapolee[idx], label=i, linewidth=0.7)
        axs[idx].set_title(titre[idx])
        axs[idx].set_ylim(0, max(Activite[i])*1.1)

    plt.tight_layout()
    #plt.show()


def barplotComparaison(Dose1, Dose2, titre, xlabel):

    #plt.figure(figsize=(10, 5))
    diff=2*(Dose1-Dose2)/((Dose1+Dose2)/2)*100
    diff = pd.DataFrame({
        'Diff (%)': diff
    },
    index=xlabel)
    diff.index.name = 'Organe'
    print(diff)
    diff.plot(kind='bar', legend=False, figsize=(10, 6))

    #abs_max = max(abs(truc))
    #plt.ylim(-abs_max * 1.1, abs_max * 1.1)
    plt.title(titre)
    #plt.xlabel(diff['Organe'])
    plt.ylabel('Différence (%)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
    #plt.bar(DF_result['Organs'], truc, label='Nous', alpha=0.5)