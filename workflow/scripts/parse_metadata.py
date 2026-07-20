import sys
import json
import re
import subprocess


metadata_json = sys.argv[1]
cmsDriver_command_path = sys.argv[2]
step = sys.argv[3]
get_curl = sys.argv[4]

with open(metadata_json, "r") as f:
    metadata = json.load(f)

map_step = {
    "gen": 0,
    "sim": 1,
    "digi2raw": 2
}

script_content = metadata["methodology"]["steps"][map_step[step]]["configuration_files"][0]["script"]

if get_curl.lower() == "true":
    curl_pattern = r"(curl.*? -o\s+(\S+))"
    curl_match = re.search(curl_pattern, script_content)
    if curl_match:
        curl_command = curl_match.group(1)
        print(curl_command)
    else:
        raise ValueError("Fragment URL not found")

    subprocess.run(curl_command, shell=True)

cmsDriver_pattern = r"cmsDriver\.py.*?-n\s+\S+"
cmsDriver_match = re.search(cmsDriver_pattern, script_content, re.DOTALL)
if cmsDriver_match:
    print(cmsDriver_match.group(0))
    cmsDriver = cmsDriver_match.group(0)
else:
    raise ValueError("cmsDriver.py command not found")

cmsDriver_snakemake = cmsDriver.replace("--customise Configuration/DataProcessing/Utils.addMonitoring", "")
cmsDriver_snakemake = re.sub(r"--python_filename\s+\S+", f"--python_filename {step}_cfg_${{JOB_INDEX}}.py", cmsDriver_snakemake)
cmsDriver_snakemake = re.sub(r"--fileout\s+file:\S+", f"--fileout file:{step}_output.root", cmsDriver_snakemake)

if step != "gen":
    cmsDriver_snakemake = re.sub(r"--filein\s+file:\S+", "--filein file:${INPUT_FILE}", cmsDriver_snakemake)

if step == "sim":
    # get the pileup recordId
    print(metadata['pileup'])
    pileup_record_id = metadata['pileup']['links'][0]['recid']
    with open("pileup_record_id.txt", 'w') as f:
        f.write(pileup_record_id)
elif step == "digi2raw":
    cmsDriver_snakemake = re.sub(r"--pileup_input\s+\S+", "--pileup_input ${PILEUP_URL}", cmsDriver_snakemake)

with open(cmsDriver_command_path, "w") as f:
    f.write(cmsDriver_snakemake)