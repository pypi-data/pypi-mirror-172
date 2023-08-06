import pandas as pd
from PyaiVS.data_utils import TVT
df = pd.read_csv('/data/jianping/bokey/OCAICM/dataset/aurorab/aurorab.csv')
total = []
for i in range(10):
    new = TVT(df['Smiles'],df['activity'])

    data_x, data_te_x, data_y, data_te_y = new.set2ten(i)
    index = data_x.index.tolist()
    total.extend(index)
print(len(set(total))==len(df))