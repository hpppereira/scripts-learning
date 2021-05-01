# plotagem do scalograma feito pelo parente em matlab

import numpy as np
import pandas as pd
from matplotlib import mlab
import matplotlib.pyplot as plt
from scipy.signal import lfilter
plt.close('all')

def calc_daat_wavelet_matri(x, nfft, fs):
    """
    """
    qq1, f = mlab.psd(x=df.n1.values, NFFT=int(nfft), Fs=fs, detrend=mlab.detrend_mean,
                     window=mlab.window_hanning, noverlap=int(nfft/2))
    qq1, f = qq1[1:], f[1:]

    # menos 1 para ficar igual ao matlab
    ff=np.array([7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,27,29,32,35,39,43,49,55,62]) - 1

    mn = np.round(3*1.0/f[ff]).astype(int)

    wavecos = np.zeros((int(mn.max()),len(ff)))
    wavesen = np.copy(wavecos)

    for i in np.arange(len(ff)):
        out2 = np.linspace(-3.14, 3.14, mn[i])
        gau = np.hanning(mn[i])
        out1 = gau * np.cos(3*out2)
        out3 = gau * np.sin(3*out2)
        wavecos[:len(out1),i] = out1
        wavesen[:len(out3),i] = out3

    matri = np.zeros((len(ff),len(df)))

    for iwq in np.arange(len(ff)):
        out1 = wavecos[:mn[iwq], iwq]
        out3 = wavesen[:mn[iwq], iwq]
        m = mn[iwq]
        a1 = lfilter((out1+1j*out3), 1, df.n1.values)
        a4 = np.real((2*dt / m) * (a1 * np.conj(a1)))
        matri[iwq, :len(a4)] = a4
    return f, ff, matri

def plot_spectrograma(t, x, f, ff, matri):
    """
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(t, x, 'k')
    ax1.set_ylabel('Heave (m)')
    ax1.set_xlim(700, 1000)
    ax2 = fig.add_subplot(212, sharex=ax1)
    ax2.contour(t, f[ff], matri, levels=15, cmap='gray')
    ax2.grid()
    ax2.set_ylabel('Frequency (Hz)')
    ax2.set_xlabel('Time (s)')
    return fig


if __name__ == "__main__":
    df = pd.read_csv('/home/hp/Documents/pnboia/dados/rio_grande/HNE/200905/200905060900.HNE',
                     skiprows=11, header=None, sep='\s+', names=['time', 'n1', 'n2', 'n3'],
                     index_col='time')

    fs = 1.28
    dt = 1.0 / fs
    t = np.arange(0, len(df)*dt, dt)
    nfft = 328 # 8 gl
    x = df.n1.values

    f, ff, matri = calc_daat_wavelet_matri(x, nfft, fs)

    fig = plot_spectrograma(df.index, x, f, ff, matri)

    plt.show()