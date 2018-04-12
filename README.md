`eenvdir`: encryptable `envdir`
===============================

Like [envdir](http://cr.yp.to/daemontools/envdir.html), but with on-the-fly opt-in encryption.


## Requirements

* python3 (at least 3.6)
* openssl (supporting `enc -d -aes-256-cbc`)


## Installation

Copy/symlink eenvdir to somewhere on your path.

Or just `ln -s "$(pwd)/eenvdir" /usr/local/bin/eenvdir`


## Usage


```
Usage: eenvdir [--password-via-fd=N] DIR CMD [ARG] ...

Run CMD with environment modified according to files in DIR


    If DIR contains a file named KEY.aes it is decrypted and proceeds as if the
    file was named KEY. Decryption via: openssl enc -d -aes-256-cbc -salt

    If DIR contains a file named KEY whose first line is VAL, envdir removes an
    environment variable named KEY if one exists, and then adds an environment
    variable named KEY with value VAL. The name KEY must not contain =. Spaces
    and tabs at the end of VAL are removed. Nulls in VAL are changed to
    newlines in the environment variable.

    If the file KEY is completely empty (0 bytes long), envdir removes an
    environment variable named KEY if one exists, without adding a new
    variable.

    Exits 111 if it has trouble reading DIR, if it runs out of memory for
    environment variables, or if it cannot run child. Otherwise its exit code is
    the same as that of child.


Options:
    --password-via-fd=N     fd N is read and closed; password is the contents
```
