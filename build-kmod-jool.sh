#!/bin/sh

set -oeux pipefail

KERNEL="$(rpm -q kernel --queryformat '%{VERSION}-%{RELEASE}.%{ARCH}')"

mkdir -p /tmp/ublue-os-ucore-nvidia/rpmbuild/SOURCES/

cd /tmp/ublue-os-ucore-nvidia/rpmbuild/SOURCES/

ls /lib/modules/${KERNEL}/

curl -L -O https://github.com/NICMx/Jool/releases/download/v4.1.11/jool-4.1.11.tar.gz
tar -xzf jool-4.1.11.tar.gz
/sbin/dkms install --kernelsourcedir /lib/modules/${KERNEL}/build jool-4.1.11/



#install -D /etc/pki/akmods/certs/public_key.der /tmp/ublue-os-ucore-addons/rpmbuild/SOURCES/public_key.der
#rpmbuild -ba \
#    --define '_topdir /tmp/ublue-os-ucore-addons/rpmbuild' \
#    --define '%_tmppath %{_topdir}/tmp' \
#    /tmp/ublue-os-ucore-addons/jool.spec
#
#mkdir -p /var/cache/rpms/kmods
#
#mv /tmp/ublue-os-ucore-addons/rpmbuild/RPMS/*/*.rpm \
#   /var/cache/rpms/kmods/

#dnf copr enable -y dasskelett/jool
#dnf install -y jool
#
#dkms status
#
#ls /var/lib/dkms/jool/4.1.11/source
#ls /var/lib/dkms/jool/4.1.11/build
#ls /usr/src/jool-4.1.11/src