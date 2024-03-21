%global buildforkernels akmod
%global debug_package %{nil}
%global prjname jool

Name:             %{prjname}
Version:          4.1.11
Release:          1%{?dist}
Summary:          Open Source SIIT and NAT64 Translator for Linux
License:          GPL-2.0-or-later
URL:              http://jool.mx/

Source:          https://github.com/NICMx/Jool/releases/download/v%{version}/%{prjname}-%{version}.tar.gz
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: kmodtool
BuildRequires: gcc
BuildRequires: make

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
TODO

%prep
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null


%setup -q -c -T -a 0

# For each kernel version we are targeting
for kernel_version in %{?kernel_versions} ; do
  # Make a copy of the source code that was downloaded by running spectool and automatically extracted
  %{__cp} -a %{prjname}-%{version} _kmod_build_${kernel_version%%___*}
done

%build
# For each kernel version we are targeting
for kernel_version in %{?kernel_versions}; do
  # Make/Build the kernel module (by running make in the directories previous copied) (This makes the .ko files in each of those respective directories)
  make V=1 -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
rm -rf /root/rpmbuild
# AKMOD magic I guess?
%{?akmod_install}
