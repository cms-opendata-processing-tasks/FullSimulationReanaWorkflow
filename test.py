import sys
import json
import re
import subprocess
import urllib.request

subprocess.run("curl --help")

metadata_json = sys.argv[1]
cmsDriver_command_path = sys.argv[2]
fragment_path = sys.argv[3]

with open(metadata_json, "r") as f:
    metadata = json.load(f)

script_content = metadata["methodology"]["steps"][0]["configuration_files"][0]["script"]


curl_command = r"(curl.*? -o\s+(\S+))"
curl_match = re.search(curl_command, script_content)
if curl_match:
    curl_command = curl_match.group(1)
    print(curl_command)
    frag = re.search(r"-o\s+Configuration\S+", curl_command).group(0)
    fragment_name = frag.split("/")[-1]
else:
    raise ValueError("Fragment URL not found")