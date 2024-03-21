#Build from base, simpley because it's the smallest image
ARG SOURCE_IMAGE="${SOURCE_IMAGE:-fedora-coreos}"
ARG BASE_IMAGE="quay.io/fedora/${SOURCE_IMAGE}"
ARG COREOS_VERSION="${COREOS_VERSION:-stable}"

FROM ${BASE_IMAGE}:${COREOS_VERSION} AS builder
ARG COREOS_VERSION="${COREOS_VERSION:-stable}"
ARG ZFS_MINOR_VERSION="${ZFS_MINOR_VERSION:-2.2}"

COPY build*.sh /tmp
COPY certs /tmp/certs
COPY zfs-kmod-spec-in.patch /tmp

ADD jool.spec \
        /tmp/jool/rpmbuild/SPECS/jool.spec
ADD ublue-os-ucore-addons.spec \
        /tmp/ublue-os-ucore-addons/ublue-os-ucore-addons.spec
ADD ublue-os-ucore-nvidia.spec \
        /tmp/ublue-os-ucore-nvidia/ublue-os-ucore-nvidia.spec
ADD files/usr/lib/systemd/system/ublue-nvctk-cdi.service \
        /tmp/ublue-os-ucore-nvidia/rpmbuild/SOURCES/ublue-nvctk-cdi.service
ADD files/usr/lib/systemd/system-preset/70-ublue-nvctk-cdi.preset \
        /tmp/ublue-os-ucore-nvidia/rpmbuild/SOURCES/70-ublue-nvctk-cdi.preset


RUN /tmp/build-prep.sh

RUN /tmp/build-kmod-jool.sh

RUN for RPM in $(find /var/cache/akmods/ -type f -name \*.rpm); do \
        cp "${RPM}" /var/cache/rpms/kmods/; \
    done

RUN find /var/cache/rpms

FROM scratch

COPY --from=builder /var/cache/rpms /rpms
