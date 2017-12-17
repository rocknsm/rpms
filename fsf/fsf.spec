%global commit0 7c5b201b2917a3c33b2be305c0223cbd226e6735
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%define _prefix /opt/fsf

Name:     fsf
Summary:  File Scanning Framework is a recursive file scanning solution that provides a service for static file analysis.
Version:  1.1
Release:  3.git.%{shortcommit0}%{?dist}
License:  Apache License, Version 2.0
Source0:  https://github.com/EmersonElectricCo/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{version}-%{shortcommit0}.tar.gz
Patch0:   https://raw.githubusercontent.com/akniffe1/fsf_rpm/master/SOURCES/0001-Adds-service-file-for-managing-fsf-server-daemon.patch
URL:      https://github.com/EmersonElectricCo/%{name}
Prefix:   %{_prefix}

Provides: fsf-server = %{version}

BuildRequires:    git
BuildRequires:    bash
BuildRequires:    systemd

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Requires: cabextract
Requires: libffi-devel
Requires: libtool
Requires: net-tools
Requires: openssl
Requires: python-concurrentloghandler
Requires: python-ctypescrypto
Requires: python-czipfile
Requires: python-hachoir-core
Requires: python-hachoir-metadata
Requires: python-hachoir-parser
Requires: python-hachoir-regex
Requires: python-hachoir-subfile
Requires: python-javatools
Requires: python-macholibre
Requires: python-oletools
Requires: python-pefile
Requires: python-pyelftools
Requires: python-pylzma
Requires: python-PyPDF2
Requires: python-rarfile
Requires: python-requests
Requires: python-ssdeep
Requires: python-xmltodict
Requires: python2-pyasn1
Requires: python2-pyasn1-modules
Requires: ssdeep
Requires: unrar
Requires: unzip
Requires: upx
Requires: yara

%description
The File Scanning Framework Server provides a daemonized python socket server and recursive file analysis capability.

%prep
%autosetup -n %{name}-%{commit0} -S git

%build
# nothing to do

%install

# Copy source files
mkdir -p %{buildroot}%{prefix}
cp -a fsf-client %{buildroot}%{_prefix}/fsf-client
cp -a fsf-server %{buildroot}%{_prefix}/fsf-server

# Make default log dirs
mkdir -p %{buildroot}/%{_sharedstatedir}/fsf/logs
mkdir -p %{buildroot}/%{_sharedstatedir}/fsf/archive

# Make dirs for yara rules
mkdir -p %{buildroot}/%{_sharedstatedir}
mv %{buildroot}%{_prefix}/fsf-server/yara %{buildroot}%{_sharedstatedir}/yara-rules

# Copy systemd service file
mkdir -p %{buildroot}/%{_unitdir}
%__install %{_builddir}/%{buildsubdir}/contrib/fsf.service %{buildroot}/%{_unitdir}

# Create symlinks on path
mkdir -p %{buildroot}/usr/bin/
ln -sf %{_prefix}/fsf-client/fsf_client.py %{buildroot}/usr/bin/fsfclient
ln -sf %{_prefix}/fsf-server/main.py %{buildroot}/usr/bin/fsfserver

%files
%attr(0664, root, root) %{_unitdir}/fsf.service
%defattr(-,fsf,fsf)
%dir %attr(0755, fsf, fsf) %{_sharedstatedir}/fsf/logs
%dir %attr(0755, fsf, fsf) %{_sharedstatedir}/fsf/archive

%config(noreplace) %attr(0664, fsf, fsf) %{_prefix}/fsf-client/conf/*.py
%attr(0755, fsf, fsf) %{_prefix}/fsf-client/conf/*.py[co]
%attr(0755, fsf, fsf) %{_prefix}/fsf-client/fsf_client.py
%attr(0755, fsf, fsf) %{_prefix}/fsf-client/fsf_client.py[co]

%config(noreplace) %attr(0664, fsf, fsf) %{_prefix}/fsf-server/conf/*.py

%attr(0664, fsf, fsf) %{_prefix}/fsf-server/conf/*.py[oc]
%attr(0755, fsf, fsf) %{_prefix}/fsf-server/modules/*.py[oc]
%attr(0755, fsf, fsf) %{_prefix}/fsf-server/modules/*.py
%attr(0755, fsf, fsf) %{_prefix}/fsf-server/*.py[oc]
%attr(0755, fsf, fsf) %{_prefix}/fsf-server/*.py

%attr(0664, fsf, fsf) %{_prefix}/fsf-server/jq/*.jq
%attr(0664, fsf, fsf) %{_sharedstatedir}/yara-rules/*.yara

# symlinks
/usr/bin/fsfserver
/usr/bin/fsfclient

%pre -p /bin/sh
#! /usr/bin/bash
#
# Add fsf user & group if doesn't exist
if ! getent group fsf; then
  groupadd --system fsf
fi
if ! getent passwd fsf; then
  useradd --no-create-home --no-user-group --gid fsf --system fsf
fi

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%changelog
* Sun Dec 17 2017 Derek Ditch <derek@rocknsm.io> 1.1-3.git7c5b201
- Removed BuildRequires that weren't needed

* Mon Nov 13 2017 Derek Ditch <derek@rocknsm.io> 1.1-2.git7c5b201
- Serious house cleaning
- Removed runtime requirements for devleopment packages

* Sun Feb 12 2017 Derek Ditch <derek@rocknsm.io> 1.1-1.git7c5b201
- Initial stab at specfile
- Packaged for RockNSM 2.0
