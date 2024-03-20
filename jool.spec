%global buildforkernels akmod
%global debug_package %{nil}

%define repo         rpmfusion

Name:             jool
Version:          4.1.11
Release:          1%{?dist}
Summary:          Open Source SIIT and NAT64 Translator for Linux
License:          GPL-2.0-or-later
URL:              http://jool.mx/

Source:          https://github.com/NICMx/Jool/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: kmodtool
BuildRequires: gcc
BuildRequires: make

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This module contains the kmod module from %{URL} and overclocks the GameCube USB adapter.

%prep
echo "PREP--------------------------------------------------"
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
echo "------------------------------------------------------"

%setup -q -c
echo "SETUP-------------------------------------------------"
# For each kernel version we are targeting
for kernel_version in %{?kernel_versions} ; do
  # Make a copy of the source code that was downloaded by running spectool and automatically extracted
  %{__cp} -a %{name}-%{commit} _kmod_build_${kernel_version%%___*}
done
echo "------------------------------------------------------"

%build
echo "BUILD-------------------------------------------------"
# For each kernel version we are targeting
for kernel_version in %{?kernel_versions}; do
  # Make/Build the kernel module (by running make in the directories previous copied) (This makes the .ko files in each of those respective directories)
  %{__make} %{?_smp_mflags} -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done
# Create gcadapter_oc.conf file needed for autoloading module at boot (will be installed into /etc/modules-load.d/ in install step)
cat > gcadapter_oc.conf <<EOF
gcadapter_oc
EOF
echo "------------------------------------------------------"

%install
echo "INSTALL-----------------------------------------------"
# For each kernel version we are targeting
for kernel_version in %{?kernel_versions}; do
  # Make the directory the kernel module will be installed into in the BUILDROOT folder
  mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  # Install the previously built kernel module (This moves and compresses the .ko file to the directory created above)
  install -D -m 755 _kmod_build_${kernel_version%%___*}/gcadapter_oc.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  # Make the installed kernel module executable for all users
  chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done
# Make the directory the .conf file will be installed into in the BUILDROOT folder
mkdir -p %{buildroot}/etc/modules-load.d/
# Install the previously built .conf file
install -m 755 gcadapter_oc.conf %{buildroot}/etc/modules-load.d/gcadapter_oc.conf
# AKMOD magic I guess?
%{?akmod_install}
echo "------------------------------------------------------"

%clean
echo "CLEAN-------------------------------------------------"
# Cleanup the BUILDROOT
%{__rm} -rf %{buildroot}
echo "------------------------------------------------------"

%changelog

