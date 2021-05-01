"""

Nome da variavel em .spc
BRMERENDES

"""

import numpy as np

f = open('../data/200610.spc')

freq = np.array([0.418E-01, 0.459E-01, 0.505E-01, 0.556E-01, 0.612E-01, 0.673E-01, 0.740E-01, 0.814E-01,
        0.895E-01, 0.985E-01, 0.108E+00, 0.119E+00, 0.131E+00, 0.144E+00, 0.159E+00, 0.174E+00,
        0.192E+00, 0.211E+00, 0.232E+00, 0.255E+00, 0.281E+00, 0.309E+00, 0.340E+00, 0.374E+00,
        0.411E+00])

dire = np.array([0.157E+01, 0.131E+01, 0.105E+01, 0.785E+00, 0.524E+00, 0.262E+00, 0.000E+00,
        0.602E+01, 0.576E+01, 0.550E+01, 0.524E+01, 0.497E+01, 0.471E+01, 0.445E+01,
        0.419E+01, 0.393E+01, 0.367E+01, 0.340E+01, 0.314E+01, 0.288E+01, 0.262E+01,
        0.236E+01, 0.209E+01, 0.183E+01]) * 180 / np.pi


spec = {}
lines = f.readlines()

cont = -1
for line in lines:

    cont += 1

    if len(line.split()) == 2:

        date = line.split()[0] + line.split()[1]

        print line

        # a = lines[cont:cont + 88]

        # stop

    if 'BRMERENDES' in line:

        # lista de strings
        a = lines[cont+1:cont + 86]

        # cria aray de float
        aa = []
        for l in a:
            aa.append(l.split())
        aa = np.array(aa).astype(float)

        # stop

        spec[date] = aa

        # print line

# stop

# stop

nf = 25
nd = 24

nl = int((nf*nd)/7)
rnl = int((nf*nd)-(int((nf*nd)/7)*7));

auxs = zeros((nf*nd),'f')
sdata = zeros(nt,'i')



for ic in range(0,nf):
    for il in range(0,nd):
        dspec[p,t,il,ic]=auxs[il*nf+ic]


