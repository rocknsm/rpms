%global     distname bro-af_packet-plugin
%global     commit0 9f9030b4b2a60736808d42afc97a2e2eeef74019
%global     shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global     commitdate 20170604

Name:       bro-plugin-af_packet
Version:    0
Release:    1.%{commitdate}git%{shortcommit0}%{?dist}
Epoch:      1
Summary:    Native AF_Packet support plugin for Bro.

License:    BSD
URL:        https://github.com/J-Gras/bro-af_packet-plugin/
Source0:    https://github.com/J-Gras/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Patch0:     https://github.com/J-Gras/bro-af_packet-plugin/compare/9f9030b...f385ca5.patch#/%{name}-%{shortcommit0}-fallback-headers.patch

BuildRequires:  cmake
BuildRequires:  kernel-devel
BuildRequires:  libpcap-devel
BuildRequires:  zlib-devel
BuildRequires:  bro-devel >= 2.5.0
Requires:       bro-core  >= 2.5.0
Requires:       libpcap
Requires:       zlib

%description
This plugin provides native AF_Packet support for Bro.

%prep
%setup -n %{distname}-%{commit0}

%patch0 -p1 -b .cmake

# ./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --program-prefix= --disable-dependency-tracking --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/var/lib --mandir=/usr/share/man --infodir=/usr/share/info --bro-dist=/usr/src/bro-2.5.1


%build
./configure --bro-dist=/usr/src/bro-2.5.1
make %{?_smp_mflags}


%install
%make_install

%files
%dir %{_libdir}/bro/plugins/Bro_AF_Packet
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/broctl
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/lib
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/lib/bif
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/scripts

%{_libdir}/bro/plugins/Bro_AF_Packet/__bro_plugin__
%{_libdir}/bro/plugins/Bro_AF_Packet/broctl/af_packet.py
%{_libdir}/bro/plugins/Bro_AF_Packet/lib/Bro-AF_Packet.linux-x86_64.so
%{_libdir}/bro/plugins/Bro_AF_Packet/lib/bif/*.bro
%{_libdir}/bro/plugins/Bro_AF_Packet/scripts/*.bro

%doc README COPYING MAINTAINER VERSION


%changelog
