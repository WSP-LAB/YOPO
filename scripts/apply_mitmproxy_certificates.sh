#!/bin/bash

cd /yopo-artifact/mitmproxy
source /yopo-artifact/mitmproxy/venv/bin/activate

# Run mitmdump in the background
mitmdump &
MITMDUMP_PID=$!

sleep 3
kill $MITMDUMP_PID

# Deactivate the virtual environment
deactivate
cd /yopo-artifact/

mkdir -p ~/.pki/nssdb
certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n "mitmproxy" -i /root/.mitmproxy/mitmproxy-ca-cert.pem

echo "Applying mitmproxy certificates is completed!"
