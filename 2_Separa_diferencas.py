import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib
import matplotlib.ticker as mtick

Dir = "E:\\Artigos\\2025_SBRH_Benford\\01_Benford\\"
os.chdir(Dir)

colors = plt.get_cmap('tab10').colors[:5]
i = 0

for f in os.listdir():
    if "1_Digito_Diario.txt" in f:
        print(f)

        tipo = f.split('_')[0]
        fonte = f.split('_')[1]

        dt_base_D = pd.read_csv(f, sep='\t', index_col=0)
        dt_benford = pd.read_csv('Probs_Teoricas_Benford.txt', sep='\t', index_col=0)

        dt_base_D = dt_base_D - dt_benford.values
        # dt_base_D = dt_base_D.loc[:, dt_base_D.max() > 0.15]
        # dt_base_D = dt_base_D[dt_base_D.max().sort_values(ascending=False).index]
        dt_base_D.to_csv(f'{f[:-4]}_Diferenca_com_Benford.txt', sep='\t')

        fig, ax = plt.subplots(figsize=(10, 5))
        dt_base_D.plot(ax=ax, c=colors[i], alpha=0.1, label='False', lw=2)
        ax.set_xlabel('First Digit')
        ax.set_ylabel('Frequency Difference(%)')
        ax.axhline(y=0.15, color='r', linestyle='--', linewidth=2)
        ax.axhline(y=-0.15, color='r', linestyle='--', linewidth=2)
        ax.set_xlim(1, 9)
        ax.set_ylim(-0.80, 0.80)
        ax.grid(which='major')
        ax.grid(which='minor', linewidth=matplotlib.rcParams['grid.linewidth'] * .5)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        ax.get_legend().remove()

        plt.title(f'{tipo} - {fonte}')
        plt.tight_layout()
        plt.savefig(f'{f[:-4]}_Diferenca_com_Benford.png', format='png')
        plt.close()

        i += 1