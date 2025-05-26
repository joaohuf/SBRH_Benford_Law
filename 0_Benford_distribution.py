import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib
import matplotlib.ticker as mtick
import numpy as np

Dir = "E:\\Artigos\\2025_SBRH_Benford\\01_Benford\\"
os.chdir(Dir)

dt_benford = pd.DataFrame(index=np.arange(1, 9+1, 1), data=np.arange(1,9+1, 1))
dt_benford = dt_benford.map(lambda x: np.log10(1+1/x))
dt_benford.columns = ["Benford's Law"]

dt_benford.to_csv('Probs_Teoricas_Benford.txt', sep='\t')
