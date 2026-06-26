import urllib.request
import json

try:
    url = 'https://api.github.com/repos/FaaizJohar/CavrixOS/issues'
    response = urllib.request.urlopen(url).read()
    issues = json.loads(response)
    for i in issues[:2]:
        with open('issue_body.txt', 'w', encoding='utf-8') as f:
            f.write(i['body'] or 'None')
        break
except Exception as e:
    print(e)
