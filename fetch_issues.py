import urllib.request
import json

url = "https://api.github.com/repos/FaaizJohar/CavrixOS/issues?state=all"
req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    print(f"Issues found: {len(data)}")
    for d in data:
        print(f"Issue #{d['number']}: {d['title']}")
        print(d.get('body', ''))
        print('-'*40)
