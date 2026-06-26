#!/bin/bash
# Mock GPG Signing Key Generation for CI/CD Pipeline
# DO NOT USE IN PRODUCTION

set -e

echo "Generating Ephemeral CI/CD GPG Key..."

cat > /tmp/gpg-gen.conf <<EOF
%echo Generating a basic OpenPGP key
Key-Type: RSA
Key-Length: 2048
Subkey-Type: RSA
Subkey-Length: 2048
Name-Real: CavrixOS CI Pipeline
Name-Comment: Ephemeral Signing Key
Name-Email: ci@cavrixos.org
Expire-Date: 0
%no-protection
%commit
%echo done
EOF

gpg --batch --gen-key /tmp/gpg-gen.conf

KEY_ID=$(gpg --list-keys --with-colons ci@cavrixos.org | awk -F: '/^pub:/ { print $5 }')
echo "Key generated: $KEY_ID"

# Export public key for pacman
gpg --armor --export ci@cavrixos.org > /tmp/cavrixos-ci.pub
echo "Key exported to /tmp/cavrixos-ci.pub"
