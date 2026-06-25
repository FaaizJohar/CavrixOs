import urllib.request
import zipfile
import sys
import io

run_id = sys.argv[1]
url = f'https://api.github.com/repos/FaaizJohar/CavrixOS/actions/runs/{run_id}/logs'

try:
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/vnd.github.v3+json')
    # This will redirect to a zip file URL. urllib handles redirects automatically.
    response = urllib.request.urlopen(req)
    zip_data = response.read()
    
    with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
        for filename in z.namelist():
            if 'Build Packages' in filename or 'build' in filename.lower():
                print(f"--- {filename} ---")
                content = z.read(filename).decode('utf-8', errors='replace')
                # print last 50 lines to find the error
                lines = content.splitlines()[-50:]
                for line in lines:
                    print(line)
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} {e.reason}")
    print(e.read().decode())
except Exception as e:
    print(f"Error: {e}")
