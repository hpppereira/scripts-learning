#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:06:53 2019

@author: piatam8
"""

import numpy as np
import matplotlib.pyplot as plt
import cmocean

############## Creating an artificial polar plot ##############################

# Creating the frequency and directions vector

freq_vec = np.zeros((1,25))
freq_vec[0,0]=0.0418

for b in range(1,25):
    freq_vec[0,b]=freq_vec[0,b-1]*1.1
    
dir_vec = np.arange(0,375,15).reshape((25,1))

my_freq, my_dir = np.meshgrid(freq_vec, dir_vec)

period = 1/my_freq
period = np.fliplr(period)

# For the polar plot, directions must be in radians, instead of degrees
my_rad = np.radians(my_dir)


################ Creating my artificial spectrum ##############################

my_spec = np.ones((24,25))

my_spec[5:10,20:25] = 40
my_spec[7:9,21:23] = 90
my_spec[0:4,20:25] = 23
my_spec[5:10,24:25] = 11
my_spec[0:14,14] = 32
my_spec[0:14,15] = 19.5
my_spec[:,1:13] = 7.3445
my_spec[15:24,14] = 7.445
my_spec[:,16:19] = 7.1115
my_spec[14:24,15:25] = 5
my_spec[11:13,20:25] = 3
my_spec[0:24,0] = 6
my_spec[0:24,24] = 3
my_spec[23,15] = 77
my_spec[0,23:24] = 123

####################### changing the spectrum #################################
# The spectrum must be changed in order to make the last (360º) row equals to
# the first (0º)

newline = my_spec[0,:]
newline = newline[np.newaxis, :]
my_spec = np.concatenate((my_spec, newline), axis=0)

####################### My Frequency Polar Plot ###############################

fig, sub = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 6))

# The plot variates the colorbar scale
sub.set_theta_direction(-1)
sub.set_theta_zero_location("N")
my_contourf = sub.contourf(my_rad, my_freq, my_spec, levels = 200, cmap='Spectral_r',\
                          vmin=np.min(my_spec), vmax=np.max(my_spec), extend='both') 
# cmap='Spectral_r', 'rainbow', 'gnuplot2', 'CMRmap', cmocean.cm.balance

# Special command to draw above the plot
fig.canvas.draw()

# Variable frequency resolution
freq_resolution = np.round(np.arange(0.05,0.40,0.05), decimals = 4)

# Variable frequency resolution labels
labels = []
for i in freq_resolution:
    labels.append(str(i) + 'Hz')

sub.set_yticklabels(labels)

# Customizing the grid
plt.yticks(freq_resolution, color='w')
plt.grid(color='w', linestyle='--', linewidth=0.5)
plt.title('2D Wave Spectrum', fontsize=16, pad=15)

# Customizing the colorbar
cbar = plt.colorbar(my_contourf)
cbar.set_label('Energy Density [$\\mathregular{m^{2}.hz^{-1}.deg^{-1}}$]', rotation =270, labelpad=18, fontsize=14)
dif = (np.max(my_spec) - np.min(my_spec))

# Fixed ticks
#cbar.set_ticks([10,40,80,120])
#cbar.set_ticklabels([10,40,80,120])

# Variable ticks
cbar.set_ticks([int(round(np.min(my_spec)+1)), int(round(dif*(1/4))), int(round(dif*(2/4))),\
                int(round(dif*(3/4))),  int(round(np.max(my_spec)-1))])
cbar.set_ticklabels([int(round(np.min(my_spec)+1)), int(round(dif*(1/4))), int(round(dif*(2/4))),\
                     int(round(dif*(3/4))), int(round(np.max(my_spec)-1))])
                    
plt.show()

######################### My Period Polar Plot ################################

# Preparing the reverse spectrum

reversed_spec = np.fliplr(my_spec)

fig2, sub = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 6))

# The plot variates the colorbar scale
sub.set_theta_direction(-1)
sub.set_theta_zero_location("N")
my_contourf = sub.contourf(my_rad, period, reversed_spec, levels = 200, cmap='Spectral_r',\
                          vmin=np.min(reversed_spec), vmax=np.max(reversed_spec), extend='both') 
# cmap='Spectral_r', 'rainbow', 'gnuplot2', 'CMRmap', cmocean.cm.balance

# Special command to draw above the plot
fig2.canvas.draw()

# Variable frequency resolution
per_resolution = np.round(np.arange(5,25,5), decimals = 4)
#per_resolution = [2.4, 4, 6, 8, 12, 18, 22]


# Variable frequency resolution labels
labels = []
for i in per_resolution:
    labels.append(str(i) + 's')

sub.set_yticklabels(labels)

# Customizing the grid
plt.yticks(per_resolution, color='w')
plt.grid(color='w', linestyle='--', linewidth=0.5)
plt.title('2D Wave Spectrum', fontsize=16, pad=15)

# Customizing the colorbar
cbar = plt.colorbar(my_contourf)
cbar.set_label('Energy Density [$\\mathregular{m^{2}.s.deg^{-1}}$]', rotation =270, labelpad=18, fontsize=14)
dif = (np.max(reversed_spec) - np.min(reversed_spec))

# Fixed ticks
#cbar.set_ticks([10,40,80,120])
#cbar.set_ticklabels([10,40,80,120])

# Variable ticks
cbar.set_ticks([int(round(np.min(reversed_spec)+1)), int(round(dif*(1/4))), int(round(dif*(2/4))),\
                int(round(dif*(3/4))),  int(round(np.max(reversed_spec)-1))])
cbar.set_ticklabels([int(round(np.min(reversed_spec)+1)), int(round(dif*(1/4))), int(round(dif*(2/4))),\
                     int(round(dif*(3/4))), int(round(np.max(reversed_spec)-1))])
                    
plt.show()


