%global     distname bro-af_packet-plugin

Name:       zeek-plugin-af_packet
Version:    1.4.0
Release:    5%{?dist}
Epoch:      2
Summary:    Native AF_Packet support plugin for Zeek.

License:    BSD
URL:        https://github.com/J-Gras/%{distname}/
Source0:    https://github.com/J-Gras/%{distname}/archive/%{version}.tar.gz#/%{distname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  kernel-devel
BuildRequires:  libpcap-devel
BuildRequires:  zlib-devel
BuildRequires:  zeek-devel = 3.0.1
BuildRequires:  bifcl = 1:1.2
BuildRequires:  binpac-devel = 1:0.54
BuildRequires:  binpac = 1:0.54
BuildRequires:  gcc-c++
Requires:       zeek-core = 3.0.1
Requires:       libpcap
Requires:       zlib

Obsoletes:      bro-plugin-af_packet < 2:1.4.0-4
Provides:       bro-plugin-af_packet = %{version}-%{release}

%description
This plugin provides native AF_Packet support for Bro.

%prep
%autosetup -n %{distname}-%{version}

%build
mkdir build; cd build
%cmake \
  -DCMAKE_MODULE_PATH=%{_datadir}/zeek/cmake \
  -DBRO_CONFIG_CMAKE_DIR=%{_datadir}/zeek/cmake \
  -DBRO_CONFIG_PLUGIN_DIR=%{_libdir}/zeek/plugins \
  -DBRO_CONFIG_PREFIX=%{_prefix} \
  -DBRO_CONFIG_INCLUDE_DIR=%{_includedir}/zeek \
  -DKERNELHEADERS_LATEST:BOOL=ON \
  ..
%make_build

%install
%make_install

%files
%doc README MAINTAINER VERSION
%license COPYING

%dir %{_libdir}/zeek/plugins/Bro_AF_Packet
%dir %{_libdir}/zeek/plugins/Bro_AF_Packet/broctl
%dir %{_libdir}/zeek/plugins/Bro_AF_Packet/lib
%dir %{_libdir}/zeek/plugins/Bro_AF_Packet/lib/bif
%dir %{_libdir}/zeek/plugins/Bro_AF_Packet/scripts

%{_libdir}/zeek/plugins/Bro_AF_Packet/__bro_plugin__
%{_libdir}/zeek/plugins/Bro_AF_Packet/broctl/af_packet.p*
%{_libdir}/zeek/plugins/Bro_AF_Packet/lib/Bro-AF_Packet.linux-x86_64.so
%{_libdir}/zeek/plugins/Bro_AF_Packet/lib/bif/*.zeek
%{_libdir}/zeek/plugins/Bro_AF_Packet/scripts/*.bro

%{_libdir}/zeek/plugins/Bro_AF_Packet/README
%{_libdir}/zeek/plugins/Bro_AF_Packet/VERSION
%{_libdir}/zeek/plugins/Bro_AF_Packet/COPYING

%changelog
* Mon Dec 16 2019 Derek Ditch <derek@rocknsm.io> 1.4.0-5
- Recompile against Zeek 3.0.1

* Tue Sep 24 2019 Derek Ditch <derek@rocknsm.io> 1.4.0-4
- Recompile against Zeek 3.0.0

* Thu Sep 5 2019 Derek Ditch <derek@rocknsm.io> 1.4.0-3
- Recompile against Bro 2.6.4

* Fri Aug 23 2019 Bradford Dabbs <brad@dabbs.io> 1.4.0-2
- Change requirements to build against Bro 2.6.3

* Thu Feb 14 2019 Derek Ditch <derek@rocknsm.io> 1.4.0-1
- Version bump to 1.4.0
- Move to cmake build process against 2.6.1
* Wed Oct 24 2018 Derek Ditch <derek@rocknsm.io> 1.3-2
- Rebuilding to lock against bro 2.5.5
- Added gcc-c++ as build dependency

* Mon Aug 13 2018 Derek Ditch <derek@rocknsm.io> 1.3-1
- Rebuilding to lock against bro 2.5.4
