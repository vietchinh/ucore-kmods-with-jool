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

%setup -c
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
# Cleanup the BUILDROOT
%{__rm} -rf${RPM_BUILD_ROOT}

# For each kernel version we are targeting
for kernel_version in %{?kernel_versions}; do
  # Make the directory the kernel module will be installed into in the BUILDROOT folder
  mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  # Install the previously built kernel module (This moves and compresses the .ko file to the directory created above)
  install -D -m 755 _kmod_build_${kernel_version%%___*}/jool_common.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/jool_common.ko
  install -D -m 755 _kmod_build_${kernel_version%%___*}/jool.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/jool.ko
  install -D -m 755 _kmod_build_${kernel_version%%___*}/jool_siit.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/jool_siit.ko
  # Make the installed kernel module executable for all users
  chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done

# AKMOD magic I guess?
%{?akmod_install}

%clean
# Cleanup the BUILDROOT
%{__rm} -rf${RPM_BUILD_ROOT}
