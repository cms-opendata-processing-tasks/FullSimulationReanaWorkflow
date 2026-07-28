
# rule test:
#     output:
#         touch("results/test_job.done")
#     container:
#         BASE_CONTAINER
#     resources:
#         kerberos=True
#     shell:
#         r"""
#         set -ex

#         source /cvmfs/cms.cern.ch/cmsset_default.sh

#         export SCRAM_ARCH=slc7_amd64_gcc700
#         scram p CMSSW CMSSW_10_6_17_patch1
#         cd CMSSW_10_6_17_patch1/src
#         eval "$(scram runtime -sh)"

#         echo hello > hello.txt

#         cp hello.txt /eos/user/k/kabuquti/FullSimulationReanaWorkflow/test/
#         mkdir -p results
#         touch {output}
#         """

# rule test:
#     output:
#         "results/test_job.done"
#     container:
#         BASE_CONTAINER
#     resources:
#         # kerberos=True,
#         voms_proxy=True,
#         compute_backend="htcondorcern",
#         htcondor_max_runtime="espresso"
#     shell:
#         """
#         set -x

#         echo "===== ENV ====="
#         env | sort

#         echo "===== X509 ====="
#         echo "X509_USER_PROXY=${{X509_USER_PROXY:-<unset>}}"

#         if [ -n "${{X509_USER_PROXY}}" ]; then
#             ls -l "${{X509_USER_PROXY}}" || true
#         fi

#         echo "===== Search ====="
#         find /tmp -maxdepth 2 -name 'x509*' 2>/dev/null || true

#         echo "===== Proxy ====="
#         voms-proxy-info -all || true

#         mkdir results
#         touch results/{output}
        
#         """

        
# echo "X509_USER_PROXY=$X509_USER_PROXY"
# ls -l $X509_USER_PROXY || true

# voms-proxy-info -all

# source /cvmfs/cms.cern.ch/cmsset_default.sh

# export X509_CERT_DIR=/cvmfs/grid.cern.ch/etc/grid-security/certificates

# export SCRAM_ARCH=slc7_amd64_gcc700

# scram p CMSSW CMSSW_10_6_17_patch1

# cd CMSSW_10_6_17_patch1/src

# eval `scram runtime -sh`

# echo hello > hello.txt

# xrdcp -f -p hello.txt \
# root://eosuser.cern.ch//eos/user/k/kabuquti/FullSimulationReanaWorkflow/test/hello.txt

#         echo "Before mv command"
#         ls -lh

#         echo "Before scram b"
#         scram b
#         cd ../..