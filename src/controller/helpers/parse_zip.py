import numpy as np
import pandas as pd
import lasio 

def get_keys(file):
    las = lasio.read(file)
    mnemonic = las.keys()
    for key in range(len(mnemonic)):
      if (mnemonic[key] == 'DEPTH' or mnemonic[key] == 'DEPT'):
           mnemonic[key] = 'DEPTH'
      elif (mnemonic[key] == 'PEF' or mnemonic[key] == 'PE'):
          mnemonic[key] = 'PE'
      elif (mnemonic[key] == 'DEN' or mnemonic[key] == 'RHOB'):
          mnemonic[key] = 'DEN'
    return mnemonic

def get_data(file, skip_num):
    data = np.loadtxt(file, skiprows = skip_num)
    data = pd.DataFrame(data = data, columns=get_keys(file))
    return data