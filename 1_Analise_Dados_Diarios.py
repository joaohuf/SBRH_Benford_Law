import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib
import matplotlib.ticker as mtick

Dir = "E:\\Artigos\\2025_SBRH_Benford\\"
os.chdir(Dir)

Dir_dados = '00_Dados\\'
Dir_save = '01_Benford\\'

colors = plt.get_cmap('tab10').colors[:5]
i = 0

for f in os.listdir(Dir_dados):
    if f.endswith('.txt'):
        print(f)

        tipo = f.split('_')[0]
        fonte = f.split('_')[1]

        dt_base = pd.read_csv(f'{Dir_dados}{f}', sep='\t', index_col=0, parse_dates=True)
        dt_base = dt_base.round(2)

        dt_base = dt_base.drop(columns=dt_base.columns[dt_base.count() < 10*365])

        dt_benford = pd.read_csv(f'{Dir_save}Probs_Teoricas_Benford.txt', sep='\t', index_col=0)

        list_dts = []
        for col in dt_base.columns:
            values = dt_base[col].dropna().astype(str).str[:1]
            values = values.astype(int)

            # Usar quando considera os dois primeiros digitos
            # dt_base[col][dt_base[col] <= 10] = np.nan
            # values = dt_base[col].dropna().astype(str).str[:2]

            values = values.astype(int)
            list_dts.append(values.value_counts())

        dt = pd.concat(list_dts, axis=1)
        dt.columns = dt_base.columns

        dt = dt.sort_index(ascending=True)

        if 0 in dt.index:
            dt = dt.drop(0) # Para excluir o dígito 0

        dt = dt.div(dt.sum()+1, axis=1)
        dt.to_csv(f'{Dir_save}{f[:-4]}_Probs_1_Digito_Diario.txt', sep='\t')

        dt['Average'] = dt.mean(axis=1)

        fig, ax = plt.subplots(figsize=(7, 4))

        dt.plot(ax=ax, c=colors[i], alpha=0.5, label='False', lw=1, marker='o', markeredgecolor='black', ms=5)
        # dt.plot(ax=ax, cmap='winter', alpha=0.5, label='False', lw=1, marker='o', markeredgecolor='black', ms=5)
        dt[['Average']].plot(ax=ax, c='black', ls='--', lw=2, alpha=1)
        dt_benford.plot(ax=ax, c='black', ls='-', lw=2, alpha=1)
        ax.set_xlabel('First Digit')
        ax.set_ylabel('Frequency (%)')
        ax.set_xlim(0.95, 9.05)
        ax.set_ylim(0.0, 1)

        ax.grid(which='major')
        ax.grid(which='minor', linewidth=matplotlib.rcParams['grid.linewidth'] * .5)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        handles, labels = ax.get_legend_handles_labels()
        labels = labels[-2:]
        handles = handles[-2:]
        labels[0] = 'Average'
        ax.legend(handles=handles, labels=labels)

        plt.title(f'{tipo} - {fonte}')
        plt.tight_layout()
        plt.savefig(f'{Dir_save}{f[:-4]}_Probs_1_Digito_Diario.png', format='png')
        plt.close()

        i += 1