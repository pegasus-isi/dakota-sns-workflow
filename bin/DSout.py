#!/usr/bin/env python

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import sys
import re
def grep(var):
    with open("DS.out") as origin_file:
        for line in origin_file:
            if not var in line:
                continue
            opt = line.split()[0]
    return float(opt)

sys.path.append("/opt/Mantid/bin")

from mantid.simpleapi import *

data = Load('LiCl_290K.nxs')
x2=data.readX(0)
x = []
for i in range(len(x2)-1):
    x.append( (x2[i]+x2[i+1])*0.5)
y=data.readY(0)
data_smooth=SmoothData(InputWorkspace=data, NPoints=5)
y0 = grep('y0')
y1 = grep('y1')
print "Optimal parameters: ", y0, y1
y2=data_smooth.readY(0)
y2=y0+y1*y2
fig, ax = plt.subplots()
line1, = ax.plot(x, y,
                 label='Experimental data')
line2, = ax.plot(x, y2, '--', linewidth=2,
                 label='Model data')
ax.legend(loc='lower right')

#plt.show()
plt.savefig('DSout.png')
