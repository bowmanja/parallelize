###############################################################################
### MASTER RUN BUNDLE
##
##
##
##
##
##
##
##

import subprocess
import tempfile

# Stata command inputs:
# need to use python_plugin (see https://github.com/jrfiedler/python-in-stata)
# in order to call local macros, need to use plugin call python_plugin syntax
request = st_local("request")
remoteDir = st_local("remoteDir")
nrep = st_local("nrep")
jobname = st_local("jobname")
jobID = st_local("jobID")
callBack = st_local("callBack")
email = st_local("email")
nodes = st_local("nodes")
ppn = st_local("ppn")
pmem = st_local("pmem")
walltime = st_local("walltime")
wFName = st_local("wFName")
cFName = st_local("cFName")
mFName = st_local("mFName")
argPass = st_local("argPass")
monInstructions = st_local("monInstructions")


### remember to find+replace these in everything copied from _runBundle.do!!!

###############################################################################
# Define functions
###############################################################################


########################
# MASTER submission program


# compose the master submit
masterHeader = ("cd "+remoteDir+"/logs`=char(10)'qsub << \EOF1`=char(10)'#PBS "
                "-N mas_`jobname'`=char(10)'#PBS -S /bin/bash`=char(10)'")
masterResources = "#PBS -l nodes=1:ppn=1,pmem=1gb,walltime=12:00:00`=char(10)'"
spoolerHeader = ("cd "+remoteDir+"/logs`=char(10)'qsub << \EOF2`=char(10)'#PBS"
                 "-N spo_`jobname'`=char(10)'#PBS -S /bin/bash`=char(10)'")
spoolerWork = ("cd "+remoteDir+"/logs`=char(10)'module load "
               "stata/15`=char(10)'stata-mp -b "+remoteDir+""
               "/scripts/_runBundle.do spool "+remoteDir+" `nrep' `jobname' "
               "0 `callBack' `email' `nodes' `ppn' `pmem' `walltime' "
               "`wFName' 0 0 `argPass'`=char(10)'")
spoolerTail = "EOF2`=char(10)'"
monitorHeader = ("cd "+remoteDir+"/logs`=char(10)'qsub << \EOF3`=char(10)'"
                 "#PBS -N mon_`jobname'`=char(10)'#PBS -S "
                 "/bin/bash`=char(10)'")
monitorResources = ("#PBS -l nodes=1:ppn=1,pmem=1gb,"
                    "walltime=120:00:00`=char(10)'")
monitorEmail = "#PBS -m e`=char(10)'#PBS -M `email'`=char(10)'"
monitorWork = ("cd "+remoteDir+"/logs`=char(10)'module load stata/15`=char(10)"
               "'module load moab`=char(10)'stata-mp -b "+remoteDir+""
               "/scripts/_runBundle.do monitor "+remoteDir+" `nrep' "
               "`jobname' 0 `callBack' `email' `nodes' `ppn' `pmem' "
               "`walltime' `wFName' `cFName' `mFName' `argPass'`=char(10)'")
monitorTail = "EOF3`=char(10)'"
masterTail = "EOF1`=char(10)'"


# combine all parts
if "`email'" == "0":
    masterFileContent = ("`masterHeader'`masterResources'`spoolerHeader'"
                         "`spoolerResources'`spoolerWork'`spoolerTail'"
                         "`monitorHeader'`monitorResources'`monitorWork'"
                         "`monitorTail'`masterTail'")
else:
    masterFileContent = ("`masterHeader'`masterResources'`spoolerHeader'"
                         "`spoolerResources'`spoolerWork'`spoolerTail'"
                         "`monitorHeader'`monitorResources'`monitorEmail'"
                         "`monitorWork'`monitorTail'`masterTail'")


# initialize tempfile and submit to shell with it
##is this needed? maybe can submit directly to shell using a string##
with tempfile.TemporaryFile() as ms:
    ms.write(masterFileContent)
    # shell command goes here (maybe)

# submit to shell
subprocess.run([masterFileContent], capture_output=True)


########################
# WORK submission program

# compose the submit file
pbsHeader = ("cd "+remoteDir+"/logs`=char(10)'qsub << \EOF`=char(10)'#PBS "
             "-N wor_`jobname'`=char(10)'#PBS -S /bin/bash`=char(10)'")
pbsResources = ("#PBS -l nodes=`nodes':ppn=`ppn',pmem=`pmem',"
                "walltime=`walltime'`=char(10)'")
pbsCommands = "module load stata/15`=char(10)'cd "+remoteDir+"/logs`=char(10)'"
# this is written like this so that Stata can write it properly!
pbsDofile = ("stata-mp -b "+remoteDir+"/scripts/_runBundle.do work "
             ""+remoteDir+" 0 na $")
# pbsEnd = '"PBS_JOBID 0 0 0 0 0 0 `wFName' 0 0 0 "`monInstructions'"`=char(10)'EOF`=char(10)'"'

# combine all parts
# pbsFileContent `"`pbsTitle'`pbsHeader'`pbsResources'`pbsCommands'`pbsDofile'"'
