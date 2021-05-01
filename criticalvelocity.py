import numpy as np
import matplotlib.pylab as pl
from scipy import stats
pl.close('all')

dd = np.loadtxt('dadossed.txt')
z, vel = dd.T

# figure
pl.figure()
pl.plot(np.log(z), vel, 'o')
# pl.xlabel('vel')
# pl.ylabel('z')

pl.show()

# mean
med = np.mean(dd, axis=0)
print (med)

# calculation z0
slope, intercept, r_value, p_value, std_err = stats.linregress(
    z, vel)


print (slope, intercept)
# equacao da reta para x=0
# y =
