import urllib.request
import json
import sys

def search(q):
    url = f"https://archlinux.org/packages/search/json/?q={q}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            results = data.get('results', [])
            if results:
                print(f"Search for {q} found:")
                for r in results:
                    print(f" - {r['pkgname']}")
            else:
                print(f"Search for {q} found nothing.")
    except Exception as e:
        print(f"Error searching {q}: {e}")

search('xwaylandvideobridge')
