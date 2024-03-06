#!/bin/sh

set -oeux pipefail

dnf copr enable -y dasskelett/jool
dnf install -y jool

dkms status

ls /var/lib/dkms/jool
ls /usr/src/