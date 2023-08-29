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
      elif (mnemonic[key] == 'AC' or mnemonic[key] == 'DT'):
          mnemonic[key] = 'AC'
    return mnemonic

def filter_keys(header):
    for key in range(len(header)):
      if (header[key] == 'DEPTH' or header[key] == 'DEPT'):
          header[key] = 'DEPTH'
      elif (header[key] == 'PEF' or header[key] == 'PE'):
          header[key] = 'PE'
      elif (header[key] == 'DEN' or header[key] == 'RHOB'):
          header[key] = 'DEN'
      elif (header[key] == 'AC' or header[key] == 'DT'):
          header[key] = 'AC'
    return header

def get_data(file):
    data = None
    keys = None
    file_name = file.split(".")
    if (file_name[len(file_name)-1] == "las"):
        data = lasio.read(file)
        keys = filter_keys(data.keys())
        data = data.data
    elif(file_name[len(file_name)-1] == "xlsx"):
        data = pd.read_excel(file)
        keys = filter_keys(data.columns.values)
        
    data = pd.DataFrame(data = data, columns=keys)
    data = data[['DEPTH', 'GR', 'PE', 'DEN', 'AC']]
    x_train = data[['GR', 'PE', 'DEN', 'AC']]
    return data, x_train

def get_supervised_training_data(file, skip_num):
    data = np.loadtxt(file, skiprows = skip_num)
    data = pd.DataFrame(data = data, columns=get_keys(file))
    return data
