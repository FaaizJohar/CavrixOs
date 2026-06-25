import sys
import urllib.request
import json
import zipfile
import io

run_id = sys.argv[1]
url = f"https://api.github.com/repos/FaaizJohar/CavrixOS/actions/runs/{run_id}/jobs"
req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    for job in data['jobs']:
        print(f"Job: {job['name']} - {job['conclusion']}")
        if job['conclusion'] == 'failure':
            log_url = f"https://api.github.com/repos/FaaizJohar/CavrixOS/actions/jobs/{job['id']}/logs"
            print(f"  Log URL: {log_url}")
            try:
                req_log = urllib.request.Request(log_url)
                with urllib.request.urlopen(req_log) as log_res:
                    log_content = log_res.read().decode('utf-8', errors='ignore')
                    lines = log_content.splitlines()[-200:]
                    print("  --- LAST 200 LINES OF LOG ---")
                    for line in lines:
                        print(line)
            except Exception as e:
                print(f"  Could not download log: {e}")
