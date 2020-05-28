import pandas as pd
import numpy as np
from datetime import datetime
from pandas_datareader import data as web


def ROC(df, n):  
    M = df.diff(n - 1)  
    N = df.shift(n - 1)  
    ROC = pd.Series(((M / N) * 100), name = 'ROC_' + str(n))   
    return ROC


def get_stock(stock,start,end):
     return web.DataReader(stock,'yahoo',start,end)['Close']
    
    
def buy_sell(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    
    
    for i in range(len(data)):
        if data['SMAROC20'][i] > 0 and data['SMAROC50'][i] > 0 and data['SMAROC100'][i] > 0 and data['SMAROC200'][i] > 0:
            if flag != 1:
                sigPriceBuy.append(data['Close'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)

        elif data['SMAROC20'][i] < 0 and data['SMAROC50'][i] < 0 and data['SMAROC100'][i] < 0 and data['SMAROC200'][i] < 0:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['Close'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)  
    
    return (sigPriceBuy, sigPriceSell)