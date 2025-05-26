import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib
import matplotlib.ticker as mtick

Dir = "E:\\Artigos\\2025_SBRH_Benford\\01_Benford\\"
os.chdir(Dir)

Dir_save = 'Correlacoes\\'

f_human_intervention = "E:\\Bases_de_Dados\\Camels\\v2\\01_CAMELS_BR_attributes\\camels_br_human_intervention.txt"
f_topography = "E:\\Bases_de_Dados\\Camels\\v2\\01_CAMELS_BR_attributes\\camels_br_topography.txt"
f_land_cover = "E:\\Bases_de_Dados\\Camels\\v2\\01_CAMELS_BR_attributes\\camels_br_land_cover.txt"
f_hydrology = "E:\\Bases_de_Dados\\Camels\\v2\\01_CAMELS_BR_attributes\\camels_br_hydrology.txt"
f_climate = "E:\\Bases_de_Dados\\Camels\\v2\\01_CAMELS_BR_attributes\\camels_br_climate.txt"
f_geology = "E:\\Bases_de_Dados\\Camels\\v2\\01_CAMELS_BR_attributes\\camels_br_geology.txt"
f_location = "E:\\Bases_de_Dados\\Camels\\v2\\01_CAMELS_BR_attributes\\camels_br_location.txt"
f_quality_check = "E:\\Bases_de_Dados\\Camels\\v2\\01_CAMELS_BR_attributes\\camels_br_quality_check.txt"
f_soil = "E:\\Bases_de_Dados\\Camels\\v2\\01_CAMELS_BR_attributes\\camels_br_soil.txt"

dt_human_intervention = pd.read_csv(f_human_intervention, sep=' ', index_col=0)
dt_topography = pd.read_csv(f_topography, sep=' ', index_col=0)
dt_land_cover = pd.read_csv(f_land_cover, sep=' ', index_col=0)
dt_hydrology = pd.read_csv(f_hydrology, sep=' ', index_col=0)
dt_climate = pd.read_csv(f_climate, sep=' ', index_col=0)
dt_geology = pd.read_csv(f_geology, sep=' ', index_col=0)
dt_location = pd.read_csv(f_location, sep=' ', index_col=0)
dt_quality_check = pd.read_csv(f_quality_check, sep=' ', index_col=0)
dt_soil = pd.read_csv(f_soil, sep=' ', index_col=0)

dt_atrib = pd.concat([dt_location, dt_climate, dt_hydrology, dt_topography, dt_land_cover, dt_geology, dt_soil, dt_quality_check, dt_human_intervention], axis=1)

for f in os.listdir():
    if "Diferenca_com_Benford.txt" in f:
        print(f)

        dt_base = pd.read_csv(f, sep='\t', index_col=0)
        max_abs = dt_base.abs().max()
        id_max_abs = dt_base.abs().idxmax()

        dt_base = dt_base.describe()

        dt_base.loc['dif_max_abs'] = max_abs
        dt_base.loc['digit_dif_max_abs'] = id_max_abs
        dt_base = dt_base.T
        dt_base.index = dt_base.index.astype('int')

        dt_base = dt_base[['mean', 'std', 'min', '25%', '50%', '75%', 'max', 'dif_max_abs', 'digit_dif_max_abs']]

        dt = dt_atrib[dt_atrib.index.isin(dt_base.index)]
        dt = pd.concat([dt_base, dt], axis=1)

        dt.to_csv(f'{Dir_save}{f[:-4]}_Diferenca_com_Benford_Atributos.txt', sep='\t')

        dt = dt.select_dtypes(exclude=['object'])

        dt_results = pd.DataFrame()
        for method in ['pearson', 'kendall', 'spearman']:
            dt_results[method] = dt.corr(method=method)['dif_max_abs']

        dt_results.to_csv(f'{Dir_save}{f[:-4]}_Correlacao_dif_max_abs.txt', sep='\t')