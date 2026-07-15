import sys
import json
import re
import subprocess


metadata_json = sys.argv[1]
cmsDriver_command_path = sys.argv[2]

with open(metadata_json, "r") as f:
    metadata = json.load(f)

script_content = metadata["methodology"]["steps"][0]["configuration_files"][0]["script"]


curl_pattern = r"(curl.*? -o\s+(\S+))"
curl_match = re.search(curl_pattern, script_content)
if curl_match:
    curl_command = curl_match.group(1)
    print(curl_command)
else:
    raise ValueError("Fragment URL not found")

subprocess.run(curl_command, shell=True)

cmsDriver_pattern = "cmsDriver\.py.*?-n\s+\S+"
cmsDriver_match = re.search(cmsDriver_pattern, script_content, re.DOTALL)
if cmsDriver_match:
    print(cmsDriver_match.group(0))
    cmsDriver = cmsDriver_match.group(0)
else:
    raise ValueError("cmsDriver.py command not found")

cmsDriver_snakemake = cmsDriver.replace("--customise Configuration/DataProcessing/Utils.addMonitoring", "")
cmsDriver_snakemake = re.sub(r"--python_filename\s+\S+", "--python_filename gen_cfg_${JOB_INDEX}.py", cmsDriver_snakemake)
cmsDriver_snakemake = re.sub(r"--fileout\s+file:\S+", "--fileout file:gen_output.root", cmsDriver_snakemake)

with open(cmsDriver_command_path, "w") as f:
    f.write(cmsDriver_snakemake)