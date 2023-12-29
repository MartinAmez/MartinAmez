
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

def barras_frecuencias(df, columna, mostrar_valores=False, giro=90, relativas=False, tamaño=False):
    # Montamos el cuadro de 2 figuras por fila si se requieren frecuencias relativas
    if relativas:
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))
        axes = axes.flatten()
    else:
        fig, ax = plt.subplots(1, 1, figsize=(20, 10))

    # Frecuencias absolutas
    if relativas:
        ax_absolutas = axes[0]
    else:
        ax_absolutas = ax

    # Tamaño de la serie
    serie_absolutas = df[columna].value_counts()  # Acotamos el numero de barras si queremos
    
    if tamaño != False and type(tamaño) == int:
        serie_absolutas = serie_absolutas.head(tamaño)
    
    sns.barplot(x=serie_absolutas.index, y=serie_absolutas, ax=ax_absolutas, palette='crest', hue=serie_absolutas.index, legend=False)
    ax_absolutas.set_ylabel('Frecuencia')
    ax_absolutas.set_title(f'Distribución de {columna}')
    ax_absolutas.set_xlabel('')
    ax_absolutas.tick_params(axis='x', rotation=giro)

    if mostrar_valores:
        for p in ax_absolutas.patches:
            height = p.get_height()
            ax_absolutas.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                                  ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    # Frecuencias Relativas (solo si relativas=True)
    if relativas:
        # Tamaño de la serie
        serie_relativas = df[columna].value_counts(normalize=True)  # Acotamos el numero de barras si queremos

        
        if tamaño != False and type(tamaño) == int:
            serie_relativas = serie_relativas.head(tamaño)
            
        ax_relativas = axes[1]
        sns.barplot(x=serie_relativas.index, y=serie_relativas, ax=ax_relativas, palette='crest', hue=serie_relativas.index, legend=False)
        ax_relativas.set_ylabel('Frecuencia Relativa')
        ax_relativas.set_title(f'Distribución de {columna}')
        ax_relativas.set_xlabel('')
        ax_relativas.tick_params(axis='x', rotation=giro)

        if mostrar_valores:
            for p in ax_relativas.patches:
                height = p.get_height()
                ax_relativas.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                                    ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    plt.tight_layout()
    plt.show()


def histo_box(df,col_cat,col_num):
    # Crear la figura y los ejes
    fig, (ax_hist, ax_box) = plt.subplots(1, 2, figsize=(20, 10), gridspec_kw={'width_ratios': [2, 1]})

    # Graficar histograma y KDE en el primer eje
    sns.histplot(df[col_num], bins=40, kde=True, ax=ax_hist, hue=df[col_cat])
    ax_hist.set_title(f'Histograma con KDE ({col_num})')

    # Graficar boxplot en el segundo eje
    sns.boxplot(x=df[col_cat], y=df[col_num], ax=ax_box)
    ax_box.set_title(f'Boxplot ({col_num} por {col_cat})')

    # Ajustar el diseño para que no haya superposiciones
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()
