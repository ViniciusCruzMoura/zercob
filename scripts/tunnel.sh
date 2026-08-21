#!/bin/sh
set -xe
autossh -M 0 -N -T -v -C -c aes128-ctr -o "Compression yes" -o "ServerAliveInterval 60" -o "ServerAliveCountMax 3" -R 58002:127.0.0.1:8002 -p 2222 root@10.67.0.54
