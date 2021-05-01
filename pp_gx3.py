import espec
import scipy.io
import numpy as np

pathname = '/home/lioc/Dropbox/ensaios_laboc/dados/'

mat = scipy.io.loadmat(pathname + 'mar1_gx3_py.mat') #valores de heave, pitch e roll do mar 1
mat1 = scipy.io.loadmat(pathname + 'acz_pitch_roll_mar1.mat') #valores de acZ, pitch e roll do mar 1

h = mat.values()[:][4][:,0]
p = mat.values()[:][2][:,0]
r = mat.values()[:][5][:,0]

z = mat1.values()[:][0][:,0]
p = mat1.values()[:][3][:,0]
r = mat1.values()[:][4][:,0]

nfft = h.shape[0]/8 #para ficar com 32 gl
fs = 100

aah = espec.espec1(h,nfft,fs)

#integracao numerica da serie de aceleracao z

acz_gx3 = z

#1 - retira a media
acz_gx3 = (acz_gx3 - np.mean(acz_gx3))

#calcula a primeira integral atraves de loop (metodos dos trapezios)
vz_gx3 = []
for i in range(len(acz_gx3)-1):
	vz_gx3.append( (acz_gx3[i] + acz_gx3[i+1])  )
vz_gx3 = np.array(vz_gx3 - np.mean(vz_gx3))

#calcula a segunda integral
eta_gx3 = []
for i in range(len(vz_gx3)-1):
	eta_gx3.append( (vz_gx3[i] + vz_gx3[i+1])  )
eta_gx3 = np.array(eta_gx3 - np.mean(eta_gx3))

# =============================================================================== #

#coloca zeros nos 2 ultimos indices (que ficou sem devido a intgracao)
eta_gx3 = np.concatenate((eta_gx3,([0,0])))

aan = espec.espec1(eta_gx3,nfft,fs)
