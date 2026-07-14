import requests
import json
import re 
import subprocess
import yaml
import os
import argparse


parser = argparse.ArgumentParser(description="Fetch and sanitize CMS Open Data fragment scripts.")
parser.add_argument("--record_id", type=str, help="The CERN Open Data record ID (e.g., 35755)", required=True)
args = parser.parse_args()

url = f"https://opendata.cern.ch/record/{args.record_id}/export/json"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    if "metadata" in data and "methodology" in data["metadata"]:
        script_content = data["metadata"]["methodology"]["steps"][0]["configuration_files"][0]["script"]

        curl_pattern = r"(curl.*? -o\s+(\S+))"
        curl_match = re.search(curl_pattern, script_content)
        
        if curl_match:
            print("curl match found")
            curl_command = curl_match.group(1)
            print(curl_command)
            fragment_path = curl_match.group(2)
            print(fragment_path)

            subprocess.run(curl_command, shell=True)


        else:
            print("curl command not found")

        cmsDriver_pattern = "cmsDriver\.py.*?-n\s+\S+"
        cmsDriver_match = re.search(cmsDriver_pattern, script_content, re.DOTALL)
        if cmsDriver_match:
            print("cmsDriver match found")
            print(cmsDriver_match.group(0))
            cmsDriver = cmsDriver_match.group(0)
        else:
            print("cmsDriver.py command not found")
    else:
        print("Could not find methodology in this record.")
else:
    print(f"Failed to fetch data: {response.status_code}")

cmsDriver_snakemake = cmsDriver.replace("--customise Configuration/DataProcessing/Utils.addMonitoring", "")
cmsDriver_snakemake = re.sub(r"--python_filename\s+\S+", "--python_filename gen_cfg_${JOB_INDEX}.py", cmsDriver_snakemake)
cmsDriver_snakemake = re.sub(r"--fileout\s+file:\S+", "--fileout file:gen_output.root", cmsDriver_snakemake)


with open("cmsDriver_command.txt", "w") as f:
    f.write(cmsDriver_snakemake)

reana_yaml_path = "reana.yaml"

if os.path.exists(reana_yaml_path):

    with open(reana_yaml_path, "r") as f:
        reana_config = yaml.safe_load(f)

    input_files = reana_config.get("inputs", {}).get("files", [])

    cleaned_files = [
        f for f in input_files if not (f.startswith("Configuration/GenProduction/python") and f.endswith(".py"))
    ]

    cleaned_files.append(fragment_path)

    reana_config["inputs"]["files"] = cleaned_files

    with open(reana_yaml_path, "w") as f: 
        yaml.dump(reana_config, f, default_flow_style=False)