#!/usr/bin/env python

import sys
import os
from Pegasus.DAX3 import *

dax = ADAG("dakota_sns_pipeline")
dax.metadata("name", "Dakota SNS Workflow")
dax.metadata("createdby", "George Papadimitriou")

e_DakotaWrapper = Executable(name="DakotaWrapper", os="linux", arch="x86_64", installed=True)
e_DakotaWrapper.addPFN(PFN("file://" + os.getcwd() + "/bin/DakotaWrapper.sh", "condorpool"))
dax.addExecutable(e_DakotaWrapper)

e_DSout = Executable(name="DSout", os="linux", arch="x86_64", installed=True)
e_DSout.addPFN(PFN("file://" + os.getcwd() + "/bin/DSout.py", "condorpool"))
dax.addExecutable(e_DSout)

dakota_in = File("DS.in")
dakota_in.addPFN(PFN("file://" + os.getcwd() + "/input/DS.in", "local"))
dax.addFile(dakota_in)

sim_data = File("LiCl_290K.nxs")
sim_data.addPFN(PFN("file://" + os.getcwd() + "/input/LiCl_290K.nxs", "local"))
dax.addFile(sim_data)

sim_script = File("DS.py")
sim_script.addPFN(PFN("file://" + os.getcwd() + "/bin/DS.py", "local"))
dax.addFile(sim_script)

dakota_out = File("DS.out")
dakota_stdout = File("DS.stdout")
DSout_plot = File("DSout.png")
DSout_stdout = File("DSout.stdout")

dakota = Job("DakotaWrapper")
dakota.addArguments("-i", dakota_in, "-o", dakota_out, "-s", dakota_stdout)
dakota.uses(dakota_in, link=Link.INPUT)
dakota.uses(sim_data, link=Link.INPUT)
dakota.uses(sim_script, link=Link.INPUT)
dakota.uses(dakota_out, link=Link.OUTPUT, transfer=True, register=False)
dakota.uses(dakota_stdout, link=Link.OUTPUT, transfer=True, register=False)
dax.addJob(dakota)

DSout = Job("DSout")
DSout.setStdout(DSout_stdout)
DSout.uses(sim_data, link=Link.INPUT)
DSout.uses(dakota_out, link=Link.INPUT)
DSout.uses(DSout_plot, link=Link.OUTPUT, transfer=True, register=False)
DSout.uses(DSout_stdout, link=Link.OUTPUT, transfer=True, register=False)
dax.addJob(DSout)

f = open("DakotaSNS.dax","w")
dax.writeXML(f)
f.close()

