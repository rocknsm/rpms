# I'd rather use `jq -r '.sha' to parse this out, but can't get it into mock
%global commit0 d678531a3e5a87b321e9247ba60d0019768681de
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global builddate 20190326

# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0

Name:           stenographer
Version:        0
Release:        2.%{builddate}git%{shortcommit0}%{?dist}
Epoch:          1
Summary:        A high-speed packet capture solution that provides indexed access

License:        Apache License, 2.0
URL:            https://github.com/google/stenographer
Source0:        https://github.com/google/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{commit0}.tar.gz

BuildRequires:  libaio-devel, leveldb-devel, snappy-devel, gcc-c++, make
BuildRequires:  libpcap-devel, libseccomp-devel, git
BuildRequires:  golang


Requires:       libaio, leveldb, snappy, libpcap, libseccomp
Requires:       tcpdump, curl, rpmlib(FileCaps), jq, systemd
Requires(pre):  shadow-utils

%{?systemd_requires}
BuildRequires:  systemd

%description
Stenographer is a full-packet-capture utility for buffering packets to disk for
intrusion detection and incident response purposes. It provides a high-
performance implementation of NIC-to-disk packet writing, handles deleting those
files as disk fills up, and provides methods for reading back specific sets of
packets quickly and easily.

%prep
%autosetup -n %{name}-%{commit0}

%build
# Build stenographer

mkdir -p src/github.com/google/%{name}
export GOPATH=${PWD}
export PATH=${GOPATH}:${PATH}
rsync -az --exclude=src/ ./ src/github.com/google/%{name}

#Get go deps
go get -u golang.org/x/text/encoding
go get -u golang.org/x/text/transform
go get github.com/google/%{name}

go build -o %{name} -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n') -linkmode=external" -v -x "$@";

# Build stenotype
(cd stenotype; make %{?_smp_mflags} )

%install
rm -rf %{buildroot}

# Install binaries & scripts
install -d %{buildroot}%{_bindir}
install -p -m 755 %{name} %{buildroot}%{_bindir}
install -p -m 755 stenotype/stenotype %{buildroot}%{_bindir}
install -p -m 755 stenoread %{buildroot}%{_bindir}
install -p -m 755 stenocurl %{buildroot}%{_bindir}
install -p -m 755 stenokeys.sh %{buildroot}%{_bindir}

# Install configuration and service files
install -d %{buildroot}%{_sysconfdir}/%{name}/certs
install -p -m 644 configs/steno.conf   %{buildroot}%{_sysconfdir}/%{name}/config

install -d %{buildroot}%{_sysconfdir}/security/limits.d
install -p -m 644 configs/limits.conf  %{buildroot}%{_sysconfdir}/security/limits.d/stenographer.conf

install -d %{buildroot}%{_unitdir}
install -p -m 644 configs/systemd.conf %{buildroot}%{_unitdir}/stenographer.service

%files
%doc README.md DESIGN.md LICENSE

%attr(0500, stenographer, root) %{_bindir}/stenographer
%attr(0500, stenographer, root) %caps(cap_net_admin,cap_net_raw,cap_ipc_lock=ep) %{_bindir}/stenotype
%{_bindir}/stenoread
%{_bindir}/stenocurl
%{_bindir}/stenokeys.sh

%{_sysconfdir}/stenographer
%attr(0750, stenographer, stenographer) %{_sysconfdir}/stenographer/certs
%config(noreplace) %{_sysconfdir}/stenographer/*

%{_sysconfdir}/security/limits.d/stenographer.conf
%{_unitdir}/stenographer.service

%pre
getent group stenographer  || groupadd -r stenographer
getent passwd stenographer || useradd -r -g stenographer -d / -s /sbin/nologin \
  -c "Stenographer service account" stenographer
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog

* Tue Mar 26 2019 Bradford Dabbs <brad@perched.io> 0-2
- Update to latest git revision
- Cleanup go dependency imports

* Wed Jun 7 2017 Derek Ditch <derek@rocknsm.io>
- Added datestamp to allow for proper RPM progression
- Minor cleanups in SPEC file
- Added systemd as build-time dependency
