import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
import matplotlib.ticker as ticker
from s3_joao import estats

Dir = "E:\\Artigos\\2025_SBRH_Benford\\01_Benford\\Correlacoes\\"
os.chdir(Dir)

vars = ['max', 'std', 'dif_max_abs']
labels = ['Máxima Diferença', 'Desvio Padrão', 'Maior Diferença Absoluta', 'Dígito com a Maior Diferença Absoluta']
x_lims = [[0, 0.7], [0, 0.7], [0, 0.7], [0.5, 9.5]]
y_lims = [[0, 100], [0, 100], [0, 100], [0, 100]]
bins = [50, 50, 50, 9]
range_bins = [[0, 1], [0, 1], [0, 1], [0.5, 9.5]]

list_dts = []
for f in os.listdir():
    if "_Diferenca_com_Benford_Atributos.txt" in f:

        tipo = f.split('_')[0]
        fonte = f.split('_')[1]

        dt = pd.read_csv(f, sep='\t', index_col=0)
        dt = dt[vars]
        list_dts_kimbal = []
        for var in vars:
            dt_kimbal = estats.curva_frequencia(dt[var].values, Crescente=False, dataframe=True, tipo='Kimbal')
            dt_kimbal = dt_kimbal[['Prob Acum', 'Amostra']]
            dt_kimbal['Prob Acum'] *= 100
            dt_kimbal = dt_kimbal.set_index('Prob Acum')
            dt_kimbal.columns = [var]

            list_dts_kimbal.append(dt_kimbal)

        dt = pd.concat(list_dts_kimbal, axis=1)
        new_columns = pd.MultiIndex.from_product([[tipo], [fonte], dt.columns])
        dt.columns = new_columns
        list_dts.append(dt)

dt = pd.concat(list_dts, axis=0)
dt = dt.melt(ignore_index=False)
dt.columns = ['Variable', 'Source', 'Metric', 'Value']
dt['Source'] = dt['Variable'] + ' - ' + dt['Source']
dt = dt.reset_index()

for var, label, x_lim, y_lim, bin, range_bin in zip(vars, labels, x_lims, y_lims, bins, range_bins):

    dt_pivot = dt[dt["Metric"] == var]

    ax = sns.lineplot(dt_pivot, x="Value", y="Prob Acum", hue="Source", style="Source", lw=2)

    ax.set_xlabel(label)
    ax.set_ylabel('Percentual (%)')
    ax.set_ylim(y_lim[0], y_lim[1])
    ax.set_xlim(x_lim[0], x_lim[1])

    ax.grid(which='major')

    if label != "Dígito com a Maior Diferença Absoluta":
        locator = ticker.MaxNLocator(nbins=ax.get_xticks().size * 2)
        ax.xaxis.set_major_locator(locator)

    plt.tight_layout()
    plt.savefig(f'Curva_Permanencia_{var}.png', format='png')

    ax.set_ylim(0.1, 110)
    ax.set_yscale('log')
    ax.grid(True, which='both', linestyle='-')
    plt.savefig(f'Curva_Permanencia_{var}_log.png', format='png')

    plt.close()