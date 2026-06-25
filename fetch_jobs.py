import urllib.request
import json
import sys

run_id = sys.argv[1]
url = f'https://api.github.com/repos/FaaizJohar/CavrixOS/actions/runs/{run_id}/jobs'
req = urllib.request.Request(url)
req.add_header('Accept', 'application/vnd.github.v3+json')
try:
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    for job in data.get('jobs', []):
        print(f"Job: {job['name']} - {job['conclusion']}")
        for step in job.get('steps', []):
            if step['conclusion'] == 'failure':
                print(f"  FAILED STEP: {step['name']}")
                print(f"  Started: {step['started_at']}, Completed: {step['completed_at']}")
except Exception as e:
    print(f"Error: {e}")
