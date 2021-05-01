"""
Processamento dos dados WW3 do arquivo netCDF gerado
pela rotina spcpoint.py
henrique
"""

import xarray as xr
import matplotlib.pyplot as plt

plt.close('all')

def read_nc(filename):
    ds = xr.open_dataset('dspec200704.nc')
    freq = ds.frequencies.values
    dire = ds.directions.values
    return ds, freq, dire

def get_spec(dataset, time):
    spec2d = dataset['dspectr'].data[time,:,:]
    spec1d = spec2d.mean(axis=0)
    return spec1d, spec2d

def preppleds():
    fx1 = np.arange(0,8) # 23.9 a 12.3
    fx2 = np.arange(8,13) # 11.2 a 7.6
    fx3 = np.arange(11,16) #  
    fx4 = np.arange(16,len(vfreq))


if __name__ == '__main__':

    filename = 'dspec200704.nc'
    ds, freq, dire = read_nc(filename)
    spec1d, spec2d = get_spec(ds, time=0)







    # t = 0
    # mat2d = ds['dspectr'].data[t,:,:]

    # spec1d = get_spec1d(dataset)


    # spec1d = [ identificar_ponto_central(c) for c in processar_contornos_da_imagem(frame) ]




    # ds







    # b = read_nc('teste')
