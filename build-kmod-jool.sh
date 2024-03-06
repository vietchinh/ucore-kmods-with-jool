#!/bin/sh

set -oeux pipefail

dnf copr enable -y dasskelett/jool
dnf install -y jool

dkms status
dkms status

rm -f /etc/yum.repos.d/dasskelett-jool-fedora-39.repo