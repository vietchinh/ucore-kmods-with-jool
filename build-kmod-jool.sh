#!/bin/sh

set -oeux pipefail

dnf copr enable -y dasskelett/jool
dnf install -y jool

dkms status

ls /var/lib/dkms/jool/4.1.11/source
ls /var/lib/dkms/jool/4.1.11/build
ls /usr/src/jool-4.1.11/src