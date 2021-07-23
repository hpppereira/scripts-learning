# Aprendendo WAFO

import wafo.spectrum.models as wsm
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

D = wsm.Spreading('cos2s',s_a=10.0)


# Make directionale spectrum
S = wsm.Jonswap().tospecdata()

SD = D.tospecdata2d(S)

w = np.linspace(0,3,257)

theta = np.linspace(-np.pi,np.pi,129)

# Make frequency dependent direction spreading
theta0 = lambda w: w*np.pi/6.0

D2 = wsm.Spreading('cos2s',theta0=theta0)

h = SD.plot()
# t = plt.contour(D(theta,w)[0].squeeze())

# t = plt.contour(D2(theta,w)[0])

# # Plot all spreading functions
# alltypes = ('cos2s','box','mises','poisson','sech2','wrap_norm')
# for ix in range(len(alltypes)):
#     D3 = wsm.Spreading(alltypes[ix])
#     t = plt.figure(ix)
#     t = plt.contour(D3(theta,w)[0])
#     t = plt.title(alltypes[ix])

plt.show()



    # wp = w[s == s.max()]
    # theta0 = lambda w: w*np.pi/6.0
    # theta0 = lambda w: w_interp
    # theta0 = lambda w:dp_rad

    # S = wsm.SpecData1D(s, omegai)
    # S2 = wsm.SpecData2D(s, freqi)

    # D12 = wsm.Spreading(type='cos-2s', theta0=0, method='mitsuyasu') # frequency dependent

    # SD12 = D12.tospecdata2d(S, wc=1, nt=51)
    # SD12.plot()#linestyle='dashdot')

    # ============================================= #
    ## curva normal
    # mu = 0.0
    # sigma = 60.0/2.35
    # bins = np.linspace(-120,120,10000)
    # a = norm.pdf(bins, mu, sigma)
    # plt.plot(bins, a, linewidth=2, color='r')
    # plt.plot([bins[0],bins[-1]], [a.max()/2,a.max()/2])
    # plt.plot([mu, mu], [0,max(a)])
    # plt.grid()
    # plt.show()
    # sys.exit()
    # ============================================= #

    # ============================================= #
    ## Calcula do D_theta
    # bins = np.linspace(0,360,360)
    # mu = d[0]
    # sigma = spr[0]/2.35 # para calular em 3db
    # Dt = norm.pdf(bins, mu, sigma)
    # plt.figure()
    # plt.plot(bins, Dt)
    # plt.plot([bins[0],bins[-1]], [Dt.max()/2,Dt.max()/2])
    # plt.plot([mu, mu], [0,max(Dt)])
    # plt.grid()
    # plt.show()
    # sys.exit()
    # ============================================= #

