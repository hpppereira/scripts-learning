
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pywt
import pywt.data
plt.close('all')

# ecg = pywt.data.ecg()

pathname = os.environ['HOME'] + '/Documents/omega/dados/'
filename = 'dados_TMEs_cq.pkl'
d = pd.read_pickle(pathname + filename)

# ecg = d['ma_dt301_iv']['VelVenMedSup']['2018-07':'2018-12'].interpolate()
# ecg = d['ma_dt301_iv']['VelVenMedSup']['2017-01-01':'2020-05-18'].interpolate() #periodo completo
# ecg = d['ma_dt301_iv']['VelVenMedSup']['2017-01-01':'2017-12-31'].interpolate() #periodo completo
ecg = d['ma_dt301_iv']['VelVenMedSup']['2017-01-01':'2017-02-01'].interpolate() #periodo completo

# ecg = df.copy()

# for w in pywt.wavelist(kind='discrete'):
for w in ['db1']:

    # set trim_approx to avoid keeping approximation coefficients for all levels

    # set norm=True to rescale the wavelets so that the transform partitions the
    # variance of the input signal among the various coefficient arrays.

    coeffs = pywt.swt(ecg, wavelet=w, level=None, start_level=0, trim_approx=True, norm=True)
    ca = coeffs[0]
    details = coeffs[1:]

    print("Variance of the ecg signal = {}".format(np.var(ecg, ddof=1)))

    variances = [np.var(c, ddof=1) for c in coeffs]
    detail_variances = variances[1:]
    print("Sum of variance across all SWT coefficients = {}".format(
        np.sum(variances)))

    # Create a plot using the same y axis limits for all coefficient arrays to
    # illustrate the preservation of amplitude scale across levels when norm=True.
    ylim = [ecg.min(), ecg.max()]

    fig, axes = plt.subplots(len(coeffs) + 1, figsize=(12,25))
    axes[0].set_title("normalized SWT decomposition --  Wavelet: " + w)
    axes[0].plot(ecg)
    axes[0].set_ylabel('VelVenMedSup')
    # axes[0].set_xlim(0, len(ecg) - 1)
    # axes[0].set_ylim(ylim[0], ylim[1])

    for i, x in enumerate(coeffs):
        ax = axes[-i - 1]
        ax.plot(ecg.index, coeffs[i], 'g')
        # ax.set_ylim(-5, 5)
        if i == 0:
            ax.set_ylabel("A%d" % (len(coeffs) - 1))

        else:
            ax.set_ylabel("D%d" % (len(coeffs) - i))

        # Scale axes
        # ax.set_xlim(0, len(ecg) - 1)
        # ax.set_ylim(ylim[0], ylim[1])
    fig.savefig('swt_variance/' + 'normalized_SWT_decomposition_' + w + '.png',
                bbox_inches='tight')


    # reorder from first to last level of coefficients
    level = np.arange(1, len(detail_variances) + 1)

    # create a plot of the variance as a function of level
    # plt.figure(figsize=(8, 6))
    # fontdict = dict(fontsize=16, fontweight='bold')
    # plt.plot(level, detail_variances[::-1], 'k.')
    # plt.xlabel("Decomposition level", fontdict=fontdict)
    # plt.ylabel("Variance", fontdict=fontdict)
    # plt.title("Variances of detail coefficients -- Wavelet: " + w, fontdict=fontdict)
    # plt.savefig('swt_variance/' + 'decomposition_level_' + w + '.png',
    #             bbox_inches='tight')

# plt.close('all')
plt.show()