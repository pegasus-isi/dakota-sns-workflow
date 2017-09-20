#!/usr/bin/env python

import sys
sys.path.append("/opt/Mantid/bin")

from mantid.simpleapi import *
#We need to create some files
import mantid,os.path

# Dakota will execute this script as
#   DS.py params.in results.out
#  The command line arguments will be extracted by dakota.interfacing automatically.


# necessary python modules
import dakota.interfacing as di

# ----------------------------
# Parse Dakota parameters file
# ----------------------------

params, results = di.read_parameters_file()

# -------------------------------
# Convert and send to application
# -------------------------------

# set up the data structures the analysis code expects
# for this simple example, put all the variables into a single hardwired array
# The asv has to be mapped back into an integer
continuous_vars = [ params['y0'], params['y1'] ]
active_set_vector = 0
if results["obj_fn"].asv.function:
    active_set_vector += 1
if results["obj_fn"].asv.gradient:
    active_set_vector += 2
if results["obj_fn"].asv.hessian:
    active_set_vector += 4

# Alternatively, the ASV can be accessed by index in
# function, gradient, hessian order
#for i, bit in enumerate(results["obj_fn"].asv):
#    if bit:
#        active_set_vector += 1 << i

# set a dictionary for passing via Python kwargs
parms = {}
parms['cv'] = continuous_vars
parms['asv'] = [active_set_vector]
parms['functions'] = 1



print "Running DS..."
datafile='LiCl_290K.nxs'
simfile='DakotaChiSquared_sim.nxs'
chifile='results.out'

data=Load(datafile)
data_smooth=SmoothData(InputWorkspace=data, NPoints=5)
sim=continuous_vars[0]+continuous_vars[1]*data_smooth
SaveNexus('data',datafile)
SaveNexus('sim',simfile)

#clean up the workspaces
DeleteWorkspace("data")
DeleteWorkspace("sim")

#run the algorithm
result=DakotaChiSquared(datafile,simfile,chifile)

#Test to see if everything is ok
print "Chi squared is ",result[0]
#print "Residuals are ", result[1].dataY(0)
f = open(chifile,'r')
chistr=f.read()
f.close()


# ----------------------------
# Return the results to Dakota
# ----------------------------

# Insert functions from rosen into results
# Results iterator provides an index, response name, and response
for i, n, r in results:
    if r.asv.function:
        r.function = result[0]

results.write()

