import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import math

Dir = "E:\\Artigos\\2025_SBRH_Benford\\01_Benford\\Correlacoes\\"
os.chdir(Dir)

vars = ['dif_max_abs']
labels = ['Maior Diferença Absoluta']

list_dts = []
for f in os.listdir():
    if "_Diferenca_com_Benford_Atributos.txt" in f:

        tipo = f.split('_')[0]
        fonte = f.split('_')[1]

        dt = pd.read_csv(f, sep='\t', index_col=0)
        dt = dt[vars]

        new_columns = pd.MultiIndex.from_product([[tipo], [fonte], dt.columns])
        dt.columns = new_columns
        list_dts.append(dt)

dt = pd.concat(list_dts, axis=1)


for var, label in zip(vars, labels):

    cores = [['dodgerblue'], ['mediumseagreen', 'crimson']]
    titulos = ['Séries de Vazão', 'Séries de Precipitação']
    tipos = ['Prec', 'Vazao']
    for tipo, cor, titulo in zip(tipos, cores, titulos):
        mask = (dt.columns.get_level_values(2) == var) & (dt.columns.get_level_values(0) == tipo)
        dt_pivot = dt.loc[:, mask]
        dt_pivot.columns = dt_pivot.columns.get_level_values(1)

        if 'Hidroweb' in dt_pivot.columns:
            dt_pivot = dt_pivot.set_index('Hidroweb')
            label_x = 'Hidroweb'
            label_y = 'CABra e Camels'
        else:
            dt_pivot = dt_pivot.set_index('CABra')
            label_x = 'CABra'
            label_y = 'Camels'

        fig, ax = plt.subplots(figsize=(8, 7))
        dt_pivot.plot(ax=ax, ls='', color=cor, marker='o', ms=5, markeredgewidth=0.5, markeredgecolor='black', alpha=0.5)

        ax.set_xlabel(label_x)
        ax.set_ylabel(label_y)

        plt.title(label)
        ax.grid(which='major')

        if len(dt_pivot.columns) == 1:
            ax.get_legend().remove()

        maximum = np.max((ax.get_xlim(), ax.get_ylim()))
        maximum = round(math.ceil(maximum / 0.05) * 0.05, 2)

        ax.set_xlim(0, maximum)
        ax.set_ylim(0, maximum)

        ax.axline([0, 0], [1, 1], label='Linha de 45°', ls='--', c='black')
        plt.title(titulo)

        plt.tight_layout()
        plt.savefig(f'Dispersao_{tipo}_{var}.png', format='png')
        plt.close()