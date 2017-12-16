#!/usr/bin/python
import struct
import sys
import os
import subprocess

def get_dev_size(device):
    with open(device, "rb") as f:
        f.seek(0, os.SEEK_END)
        return f.tell()

DATA_DEV = sys.argv[1]
DEV_SZ_BYTES = get_dev_size(DATA_DEV)

# from veritysetup output
SALT=        '<salt-goes-here>'
ROOT_DIGEST= '<root-hash-goes-here>'
VERITY_SB_SIZE = 32 * 1024

start = 0
size = DEV_SZ_BYTES / 512
target = 'verity'
hash_dev = DATA_DEV 
data_block_size = 4096
hash_block_size = data_block_size
num_blocks = DEV_SZ_BYTES / data_block_size
hash_offset = (DEV_SZ_BYTES + VERITY_SB_SIZE) / hash_block_size + 1

HASH_OFFSET_BYTES = (DEV_SZ_BYTES + VERITY_SB_SIZE)

print HASH_OFFSET_BYTES

hash_alg = 'sha256'

fmttab= "1 %s %s %d %d %d %d %s %s %s" 
table = fmttab % (DATA_DEV, hash_dev, data_block_size, hash_block_size, num_blocks, hash_offset, hash_alg, ROOT_DIGEST, SALT)

fmtcmd = "veritysetup --debug --hash-offset %d --data-blocks %d format %s %s"
veritycmd = fmtcmd % (HASH_OFFSET_BYTES, num_blocks, DATA_DEV, hash_dev)

print "DM verity table: \n" + table

print "DM verity command: \n" + veritycmd

f = open('dm-verity-table', 'wb')
f.write(buffer(table))
f.close()
