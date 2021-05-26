import os
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import linspace
from scipy import pi,sqrt,exp
from scipy.special import erf

total_degrees = 540
min_degrees = -360
max_degrees = 720

def pdf(norm_psd, x):
    return (100*norm_psd)/sqrt(2*pi) * exp(-x**2/2)

def cdf(x):
    return (1 + erf(x/sqrt(2))) / 2

def skew(x, e=0, w=1, a=0, norm_psd = 1):
    t = (x-e) / w
    return 2 / w * pdf(norm_psd,t) * cdf(a*t)
    # You can of course use the scipy.stats.norm versions
    # return 2 * norm.pdf(t) * norm.cdf(a*t)

def distribution(direction, spread, norm_psd, skewness):

    x = linspace(min_degrees, max_degrees, total_degrees) 

    p = skew(x, direction, spread, skewness, norm_psd)
    return p


files = { 'Buoy_Name':"example.spt"}

for buoy_name, file_path in files.items():
    max_psd = float(open(file_path).readlines()[3])
    spt = np.genfromtxt(file_path, delimiter=',', skip_header=12)
    complete_spt = spt
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylabel('Frequency (Hz)')
    ax.set_xlabel('Direction (degrees)')
    ax.yaxis.set_label_coords(0.75, 0.75)
    #y is frequency 
    yi = np.linspace(min(spt[:,0]), max(spt[:,0]),123)
    #x is direction
    xi = np.array(np.radians(np.linspace(min_degrees, max_degrees, 540)))
    X,Y = np.meshgrid(xi,yi)
    radian_directions = np.radians(complete_spt[:,2])
    orig_frequencies = spt[:,0]
    orig_norm_psds = spt[:,1] * max_psd
    orig_direction = spt[:,2]
    orig_spread = spt[:,3]
    orig_skew = spt[:,4]
    all_spreads = np.array([[],[],[]])
    for index, frequency in enumerate(orig_frequencies):
        norm_psd = orig_norm_psds[index]
        direction = orig_direction[index]
        spread = orig_spread[index]
        skewness = orig_skew[index]
        spread_distribution = np.array(distribution(direction, spread, norm_psd, skewness))
        spread_plus_dir = np.array([spread_distribution, xi, np.linspace(frequency,frequency,total_degrees)])
        all_spreads = np.concatenate((all_spreads, spread_plus_dir),axis=1)    
    Z = mlab.griddata(all_spreads[1], all_spreads[2], all_spreads[0], xi, yi, interp='linear')
    min_index = 180
    max_index = 360
    subset_Z = Z[:,np.arange(min_index,max_index)]
    Z_less_than_0 = Z[:,np.arange(0,180)]
    z_over_360 = Z[:,np.arange(360,540)]
    overlapping_z = subset_Z + Z_less_than_0 + z_over_360
    ax_im = ax.contourf(xi[min_index:max_index], yi, overlapping_z, cmap=cm.Reds)
    #ax_im.set_clim(0,1)
    fig.colorbar(ax_im)
    t = fig.text(0.5, 0.97, file_path.split(os.sep)[-1], 
                 horizontalalignment='center', fontsize=14)
    plt.savefig(buoy_name + ".png")