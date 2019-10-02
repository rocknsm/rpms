%global     distname GQUIC_Protocol_Analyzer
%global     commit0 89b7b45043db496e64ea9189b8ddfc681d0c77a7
%global     shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global     commitdate 20190816

Name:       zeek-plugin-gquic
Version:    1.0
Release:    3.%{commitdate}git%{shortcommit0}%{?dist}
Summary:    Protocol analyzer that detects, dissects, fingerprints, and logs GQUIC traffic

License:    BSD
URL:        https://github.com/salesforce/%{distname}
Source0:    https://github.com/salesforce/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake >= 2.8
BuildRequires:  zeek-devel = 3.0.0
BuildRequires:  bifcl = 1:1.2
BuildRequires:  binpac-devel = 1:0.54
BuildRequires:  binpac = 1:0.54
BuildRequires:  gcc-c++
Requires:       zeek-core  = 3.0.0

Obsoletes:      bro-plugin-gquic < 1.0-3
Provides:       bro-plugin-gquic = %{version}-%{release}

%description
Protocol analyzer that detects, dissects, fingerprints, and logs GQUIC traffic.

%prep
%autosetup -n %{distname}-%{commit0}

%build
mkdir build; cd build
%cmake \
  -DCMAKE_MODULE_PATH=%{_datadir}/zeek/cmake \
  -DBRO_CONFIG_CMAKE_DIR=%{_datadir}/zeek/cmake \
  -DBRO_CONFIG_PLUGIN_DIR=%{_libdir}/zeek/plugins \
  -DBRO_CONFIG_PREFIX=%{_prefix} \
  -DBRO_CONFIG_INCLUDE_DIR=%{_includedir}/zeek \
  ..
%make_build

%install
%make_install

%files

%dir %{_libdir}/zeek/plugins/Salesforce_GQUIC
%{_libdir}/zeek/plugins/Salesforce_GQUIC/*

%doc README.md VERSION
%license LICENSE.txt

%changelog
* Tue Sep 24 2019 Derek Ditch <derek@rocknsm.io> 1.0-3
- Recompile against Zeek 3.0.0

* Thu Sep 5 2019 Derek Ditch <derek@rocknsm.io> 1.0-2
- Recompile against Bro 2.6.4

* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 1.0-1
- Initial RPM packaging.
