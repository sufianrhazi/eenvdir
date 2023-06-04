#!/usr/bin/env python3
import sys
import subprocess
import os
from getpass import getpass


def encrypt(path, password):
    print(f'Encrypting {repr(path)}...')
    out_path = path[:-4]
    pr, pw = os.pipe()
    os.set_inheritable(pr, True)
    fd_str = f'fd:{pr}'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-salt', '-pass', fd_str, '-in', path, '-out', path + '.aes'],
        stdout=subprocess.PIPE,
        pass_fds=[pr]
    )
    os.close(pr)
    os.write(pw, password)
    os.close(pw)
    stdout, stderr = proc.communicate()
    rc = proc.wait()
    if rc != 0:
        raise Exception(f'rc {rc} from openssl child; stderr={repr(stderr)}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'''
Usage: {sys.argv[0]} FILE [FILE2] [FILE3] [...]

Encrypt provided files with openssl aes-256-cbc, written to FILE.aes

    You will be prompted for an encryption passphrase, this is your decription
    passphrase for these files.

    Decryption via: openssl enc -d -aes-256-cbc -pbkdf2 -salt

    Once encrypted, the original files will still remain in your filesystem.
    Once verifying the files, it is safe to remove them.

    Any number of files may be encrypted at once, all using the same password.
        '''.strip())
        sys.exit(1)
    password = getpass().encode('ascii')
    for path in sys.argv[1:]:
        encrypt(path, password)
