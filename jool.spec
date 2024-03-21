%global buildforkernels akmod
%global debug_package %{nil}

Name:             jool
Version:          4.1.11
Release:          1%{?dist}
Summary:          Open Source SIIT and NAT64 Translator for Linux
License:          GPL-2.0-or-later
URL:              http://jool.mx/

Source:          https://github.com/NICMx/Jool/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: kmodtool
BuildRequires: gcc
BuildRequires: make

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This module contains the kmod module from %{URL} and overclocks the GameCube USB adapter.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

# For each kernel version we are targeting
for kernel_version in %{?kernel_versions} ; do
  # Make a copy of the source code that was downloaded by running spectool and automatically extracted
  %{__cp} -a %{name}-%{version} _kmod_build_${kernel_version%%___*}
done

%build
# For each kernel version we are targeting
for kernel_version in %{?kernel_versions}; do
  # Make/Build the kernel module (by running make in the directories previous copied) (This makes the .ko files in each of those respective directories)
  make V=1 -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done


%install
%{__rm} -rf ${RPM_BUILD_ROOT}

# For each kernel version we are targeting
for kernel_version in %{?kernel_versions}; do
    make install DESTDIR=${RPM_BUILD_ROOT} KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} ${kernel_version%%___*}/%{kmodinstdir_postfix}/kmodname/
done
chmod u+x ${RPM_BUILD_ROOT}/lib/modules/*/extra/*/*

# AKMOD magic I guess?
%{?akmod_install}

%clean
# Cleanup the BUILDROOT
%{__rm} -rf ${RPM_BUILD_ROOT}
