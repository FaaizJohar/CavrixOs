import urllib.request
import json
import sys

def check(pkg):
    url = f"https://archlinux.org/packages/search/json/?name={pkg}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data.get('results'):
                print(f"FOUND: {pkg}")
            else:
                print(f"NOT FOUND: {pkg}")
    except Exception as e:
        print(f"Error checking {pkg}: {e}")

check('kvantum')
check('papirus-icon-theme')
check('plasma-desktop')
check('plasma-browser-integration')
check('xwaylandvideobridge')
check('appmenu-gtk-module')
check('breeze-gtk')
check('python-pyqt6')
