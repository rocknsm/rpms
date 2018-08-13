%global     distname bro-af_packet-plugin
%global     commit0 79edee2bf830becfe47cec11c1ce5eb24fc285dc
%global     shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global     commitdate 20171122

Name:       bro-plugin-af_packet
Version:    1
Release:    3.%{commitdate}git%{shortcommit0}%{?dist}
Epoch:      1
Summary:    Native AF_Packet support plugin for Bro.

License:    BSD
URL:        https://github.com/J-Gras/bro-af_packet-plugin/
Source0:    https://github.com/J-Gras/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

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

# ./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --program-prefix= --disable-dependency-tracking --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/var/lib --mandir=/usr/share/man --infodir=/usr/share/info --bro-dist=/usr/src/bro-2.5.1


%build
BRO_DIST=$(find /usr/src -name bro-config -exec /bin/sh {} --bro_dist \;)
./configure --bro-dist=${BRO_DIST} --with-latest-kernel
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
* Mon Aug 13 2108 Derek Ditch <derek@rocknsm.io> 1.3-1
- Rebuilding to lock against librdkafka 0.11.4
