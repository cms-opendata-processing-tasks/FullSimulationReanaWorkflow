import glob

totalEvents=10
eventsPerJob=1
fragmentPath=glob.glob("Configuration/GenProduction/python/*.py")[0]

jobIndex = list(range(1, int(totalEvents/eventsPerJob)+1))

with open("cmsDriver_command.txt", "r") as f:
    cmsDriverCMD = f.read().strip()

rule all:
    input:
        expand("results/gen_{jobIndex}.root", jobIndex=jobIndex)

rule gen:
    input:
        frag=fragmentPath
    output:
        "results/gen_{jobIndex}.root"
    params:
        events=eventsPerJob
    container:
        "docker://cmssw/cc7:latest"
    shell:
        """
        set -e
        export WORKDIR=$(pwd)

        JOB_DIR=$(mktemp -d)
        cd $JOB_DIR

        echo "Sourcing CMS environment"
        export SCRAM_ARCH=slc7_amd64_gcc700

        source /cvmfs/cms.cern.ch/cmsset_default.sh

        scram p CMSSW CMSSW_10_6_30

        cd CMSSW_10_6_30/src/

        mkdir -p Configuration/GenProduction/python/
        cp $WORKDIR/{input.frag} Configuration/GenProduction/python/

        echo "Reached scramming"
        scram b 

        eval `scramv1 runtime -sh`

        mkdir -p $WORKDIR/results

        export EVENTS={params.events}
        export JOB_INDEX={wildcards.jobIndex}

        echo "Running cmsDriver"
        {cmsDriverCMD}
        
        ls -lh
        echo "Running cmsRun"

        cmsRun gen_cfg_{wildcards.jobIndex}.py > cmsRun.log 2>&1 || true

        echo "Listing directories, to better understand what it looks like:"
        ls -lh 

        if ! ls *.root 1> /dev/null 2>&1; then
            echo "[ERROR] cmsRun exited, but no .root file was created"
            echo "[ERROR] Dumping the cmsRun log to see the exact CMS physics error:"
            cat cmsRun.log
            exit 1
        fi

        cp cmsRun.log $WORKDIR/gen_{wildcards.jobIndex}.log


        mv gen_output.root $WORKDIR/{output}

        sync
        sleep 5

        rm -rf $JOB_DIR
        """   