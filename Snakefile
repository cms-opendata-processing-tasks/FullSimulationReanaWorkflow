totalEvents=1000
eventsPerJob=10

jobIndex = list(range(1, int(totalEvents / eventsPerJob) + 1))

rule all:
    input:
        expand("results/sim_{jobIndex}.root", jobIndex=jobIndex)

rule gen:
    input:
        frag="Configuration/GenProduction/python/SMP-RunIISummer20UL16GEN-00010-fragment.py"
    output:
        "results/gen_{jobIndex}.root"
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
        scram b # command used to build and compile code for the CMS Software (CMSSW) environment

        eval `scramv1 runtime -sh`

        mkdir -p $WORKDIR/results

        echo "Running cmsDriver"
        cmsDriver.py Configuration/GenProduction/python/SMP-RunIISummer20UL16GEN-00010-fragment.py \\
        --python_filename gen_cfg_{wildcards.jobIndex}.py \\
        --eventcontent RAWSIM \\
        --datatier GEN \\
        --fileout file:$WORKDIR/{output} \\
        --conditions 106X_mcRun2_asymptotic_v13 \\
        --beamspot Realistic25ns13TeV2016Collision \\
        --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(100)" \\
        --step GEN \\
        --geometry DB:Extended \\
        --era Run2_2016 \\
        --no_exec \\
        --mc \\
        -n {eventsPerJob}

        echo "Running cmsRun"
        cmsRun gen_cfg_{wildcards.jobIndex}.py > cmsRun.log 2>&1 || true

        echo "Listing directories, to better understand what it looks like:"
        ls -lh 

        if ! ls *.root 1> /dev/null 2>&1; then
            echo "[ERROR] cmsRun exited, but no .root file was created!"
            echo "[ERROR] Dumping the cmsRun log to see the exact CMS physics error:"
            cat cmsRun.log
            exit 1
        fi

        mv *.root $WORK_DIR/{output}

        sync
        sleep 5

        rm -rf $JOB_DIR
        """   

rule sim:
    input:
        "results/gen_{jobIndex}.root"
    output:
        "results/sim_{jobIndex}.root"
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

        scram b
        eval `scramv1 runtime -sh`

        echo "Running SIM workflow"

        echo "Running cmsDriver for SIM"
        cmsDriver.py --python_filename sim_cfg_{wildcards.jobIndex}.py \\
        --eventcontent RAWSIM \\
        --datatier GEN-SIM \\
        --fileout file:$WORKDIR/{output} \\
        --conditions 106X_mcRun2_asymptotic_v13 \\
        --beamspot Realistic25ns13TeV2016Collision \\
        --step SIM \\
        --geometry DB:Extended \\
        --filein file:$WORKDIR/{input} \\
        --era Run2_2016 \\
        --runUnscheduled \\
        --no_exec \\
        --mc \\
        -n {eventsPerJob}

        echo "Running cmsRun"
        cmsRun gen_cfg_{wildcards.jobIndex}.py > cmsRun.log 2>&1 || true

        echo "Listing directories, to better understand what it looks like:"
        ls -lh 

        if ! ls *.root 1> /dev/null 2>&1; then
            echo "[ERROR] cmsRun exited, but no .root file was created!"
            echo "[ERROR] Dumping the cmsRun log to see the exact CMS physics error:"
            cat cmsRun.log
            exit 1
        fi

        mv *.root $WORK_DIR/{output}

        sync
        sleep 5

        rm -rf $JOB_DIR
        """

