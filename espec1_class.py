from matplotlib import mlab
import numpy as np
class Espec:
    '''Calcula o espectro simples e cruzado de series reais'''
    def __init__(self,x,nfft,fs):
        self.x=x
        self.nfft=nfft
        self.fs=fs
    def espec1(self):
        sp=mlab.psd(self.x,NFFT=self.nfft,Fs=self.fs,detrend=mlab.detrend_mean,window=mlab.window_hanning,noverlap=self.nfft/2)
        f,sp = sp[1][1:], sp[0][1:]
        gl=len(self.x)/self.nfft*2
        ici = sp*gl/26.12
        ics = sp*gl/5.63
        a = np.array([f,sp,ici,ics]).T
        return aa
    def espec2(self,y)


