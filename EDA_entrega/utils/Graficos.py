
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

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
    ax_absolutas.set_title(f'Distribución de {columna}',pad=20)
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
        ax_relativas.set_title(f'Distribución de {columna}',pad=20)
        ax_relativas.set_xlabel(columna)
        ax_relativas.tick_params(axis='x', rotation=giro)

        if mostrar_valores:
            for p in ax_relativas.patches:
                height = p.get_height()
                ax_relativas.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                                    ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    plt.tight_layout()
    plt.show()


def histo_box(df, col_num, k=1.5, bin=40, ajuste_y=None):
    """
    Visualiza un histograma con KDE y un boxplot para una columna numérica en un DataFrame.

    Parametros:
    - df: DataFrame, el conjunto de datos.
    - col_num: str, el nombre de la columna numérica.
    - k: float, el factor para calcular los límites del bigote (default: 1.5).
    - bin: int, el número de bins en el histograma (default: 40).
    - ajuste_y: int, el número máximo de valores en el eje y del histograma (default: None).
    """
    # Asegurar que max_y_values sea un valor numérico entero
    if ajuste_y is not None and not isinstance(ajuste_y, int):
        raise ValueError("max_y_values debe ser un valor numérico entero.")
    
    # Crear la figura y los ejes
    fig, (ax_hist, ax_box) = plt.subplots(1, 2, figsize=(20, 10), gridspec_kw={'width_ratios': [1, 1]})

    # Graficar histograma y KDE en el primer eje
    sns.histplot(df[col_num], bins=bin, kde=True, ax=ax_hist, color="mediumslateblue", edgecolor="darkslateblue", alpha=0.5,
                  line_kws = {'linewidth':'2'},kde_kws={'bw_method': 0.5}).lines[0].set_color("darkslateblue")
    ax_hist.set_xlabel(col_num)
    ax_hist.set_title(f'Histograma y KDE ({col_num})',pad=20)
    ax_hist.set_ylabel('Frecuencia')

    # Limitar el número máximo de valores en el eje y del histograma si se especifica
    if ajuste_y is not None:
        ax_hist.set_ylim(0, ajuste_y)

    # Graficar boxplot en el segundo eje
    whisker_props={"color":"darkslateblue",
                   "linewidth": 1.5}
    box_props={"edgecolor":"darkslateblue",
               "linewidth": 1.5,
               "facecolor": "mediumslateblue", "alpha":0.5}
    median_props={"color":"darkslateblue",
                  "linewidth": 1.5}
    cap_props={"color": "darkslateblue",
               "linewidth": 1.5}
    sns.boxplot(x=df[col_num], ax=ax_box, whis=k, whiskerprops=whisker_props, boxprops=box_props, medianprops=median_props, capprops=cap_props)
    ax_box.set_title(f'Boxplot ({col_num})',pad=20)
    ax_box.set_xlabel(col_num)

    # Ajustar el diseño para que no haya superposiciones
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()


def outliers(df,col_num,k=1.5):
    Q1 = np.percentile(df[col_num], 25)
    Q3 = np.percentile(df[col_num], 75)
    IQR = Q3 - Q1
    lim_sup = Q3 + k * IQR
    lim_inf = Q1 - k * IQR

    # Recuento
    outliers_inf = df.loc[df[col_num]<lim_inf,[col_num]].value_counts().sum()
    outliers_sup = df.loc[df[col_num]>lim_sup,[col_num]].value_counts().sum()
    num_outliers = outliers_inf+outliers_sup

    # Display the number of outliers
    print(f'Lim. Superior: {lim_sup.round(2)}, Lim. Inferior: {lim_inf.round(2)}.\n'
          f'Numero de datos por encima: {outliers_sup}, numero de datos por debajo: {outliers_inf}.\n'
          f'Numero de datos fuera de límites: {num_outliers}')

def grupal_num_disc(df, columnas, bin_width=1):
    num_columnas = len(columnas)

    # Determinar el número de filas y columnas para subplots
    if num_columnas % 2 == 0:
        rows, cols = num_columnas // 2, 2
    elif num_columnas % 3 == 0:
        rows, cols = num_columnas // 3, 3
    elif num_columnas % 5 == 0:
        rows, cols = num_columnas // 5, 5
    elif num_columnas % 7 == 0:
        rows, cols = num_columnas // 7, 7
    else:
        rows, cols = 1, num_columnas

    fig, ax = plt.subplots(rows, cols, figsize=(num_columnas * 4, 10), gridspec_kw={'width_ratios': [1] * cols})

    # Asegurarse de que 'ax' sea siempre un array, incluso si solo hay un subplot
    if rows == 1 and cols == 1:
        ax = np.array([[ax]])

    for i, columna in enumerate(columnas):
        # Calcular la posición en el arreglo 2D de subplots
        row_index, col_index = divmod(i, cols)
        current_ax = ax[row_index, col_index]

        # Calcular los límites de los bins
        min_value = 0
        max_value = 25
        bins = np.arange(min_value, max_value + bin_width, bin_width)

        # Llamar a la función 'histplot' con la columna específica del DataFrame
        sns.histplot(df[columna], kde=True, bins=bins, color="indianred", edgecolor="brown", alpha=0.7, 
                     line_kws={'color': 'red', 'linewidth': '2'}, kde_kws={'bw_method': 0.8}, ax=current_ax)
        
        # Configuraciones y títulos específicos para cada subgráfica
        current_ax.set_title(f'Distribución de {columna}')
        current_ax.set_xlabel('Número de Fallecidos')
        current_ax.set_ylabel('Frecuencia')
        
        # Fijar los límites del eje y para todas las gráficas
        current_ax.set_ylim(0, 200)
        
        # Fijar los límites del eje x para todas las gráficas
        current_ax.set_xlim(min_value, max_value)

    plt.tight_layout()
    plt.show()

def fallecidos(df, kde=False ,bin=20, medio_trans=None):
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))

    if medio_trans is None:
        columna = "Fallecidos"
    else:
        columna = f"{medio_trans} Fallecidos"
    if kde:
        sns.histplot(df[columna], kde=True, bins=bin, color="indianred", edgecolor="brown", alpha=0.7, line_kws={'color': 'red', 'linewidth': '2'},kde_kws={'bw_method': 0.8})
    else:
        sns.histplot(df[columna], kde=False,bins=bin, color="indianred",edgecolor="brown", alpha=0.7)

    ax.set_title(f'Distribución de {columna}')
    ax.set_xlabel('Número de Fallecidos')
    ax.set_ylabel('Frecuencia')
    ax.set_ylim(0,200)
    ax.set_xlim(1,50)

    plt.show()

def plot_cat_num(df, categorical_col, numerical_col, show_values=False, measure='mean'):
    # Calcula la medida de tendencia central (mean o median)
    if measure == 'median':
        grouped_data = df.groupby(categorical_col)[numerical_col].median()
    elif measure=="sum":
        grouped_data = df.groupby(categorical_col)[numerical_col].sum()
    else:
        # Por defecto, usa la media
        grouped_data = df.groupby(categorical_col)[numerical_col].mean()

    # Ordena los valores
    grouped_data = grouped_data.sort_values(ascending=False)

    # Si hay más de 5 categorías, las divide en grupos de 5
    if grouped_data.shape[0] > 5:
        unique_categories = grouped_data.index.unique()
        num_plots = int(np.ceil(len(unique_categories) / 5))

        for i in range(num_plots):
            # Selecciona un subconjunto de categorías para cada gráfico
            categories_subset = unique_categories[i * 5:(i + 1) * 5]
            data_subset = grouped_data.loc[categories_subset].reset_index()

            # Crea el gráfico
            plt.figure(figsize=(20, 10))
            ax = sns.barplot(x=data_subset[categorical_col], y=data_subset[numerical_col], palette="magma")

            # Añade títulos y etiquetas
            plt.title(f'Relación entre {categorical_col} y {numerical_col} - Grupo {i + 1}')
            plt.xlabel(categorical_col)
            plt.ylabel(f'{measure.capitalize()} de {numerical_col}')
            plt.xticks(rotation=45)

            # Mostrar valores en el gráfico
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                                textcoords='offset points')

            # Muestra el gráfico
            plt.show()
    else:
        # Crea el gráfico para menos de 5 categorías
        plt.figure(figsize=(20,10))
        ax = sns.barplot(x=grouped_data.index, y=grouped_data.values, palette="magma")

        # Añade títulos y etiquetas
        plt.title(f'Relación entre {categorical_col} y {numerical_col}')
        plt.xlabel(categorical_col)
        plt.ylabel(f'{measure.capitalize()} de {numerical_col}')
        plt.xticks(rotation=45)

        # Mostrar valores en el gráfico
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')

        # Muestra el gráfico
        plt.show()
    