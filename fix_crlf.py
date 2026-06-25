import os

def fix_crlf(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    if b'\r\n' in content:
        content = content.replace(b'\r\n', b'\n')
        with open(file_path, 'wb') as f:
            f.write(content)
        print(f"Fixed {file_path}")

for root, _, files in os.walk('e:\\archinstall\\CavrixOS'):
    if '.git' in root:
        continue
    for file in files:
        if file in ['PKGBUILD', 'Makefile'] or file.endswith(('.sh', '.py', '.yml', '.conf', '.x86_64', 'cavrix-ask')):
            fix_crlf(os.path.join(root, file))

print("Done converting CRLF to LF.")
