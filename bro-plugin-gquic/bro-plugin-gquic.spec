%global     distname GQUIC_Protocol_Analyzer
%global     commit0 89b7b45043db496e64ea9189b8ddfc681d0c77a7
%global     shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global     commitdate 20190816

Name:       bro-plugin-gquic
Version:    1.0
Release:    1.%{commitdate}git%{shortcommit0}%{?dist}
Summary:    Protocol analyzer that detects, dissects, fingerprints, and logs GQUIC traffic

License:    BSD
URL:        https://github.com/salesforce/%{distname}
Source0:    https://github.com/salesforce/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake >= 2.8
BuildRequires:  bro-devel = 2.6.3
BuildRequires:  bifcl = 1:1.1
BuildRequires:  binpac-devel = 1:0.53
BuildRequires:  binpac = 1:0.53
BuildRequires:  gcc-c++
Requires:       bro-core  = 2.6.3

%description
Protocol analyzer that detects, dissects, fingerprints, and logs GQUIC traffic.

%prep
%setup -n %{distname}-%{commit0}

%build
mkdir build; cd build
%cmake \
  -DCMAKE_MODULE_PATH=/usr/share/bro/cmake \
  -DBRO_CONFIG_CMAKE_DIR=/usr/share/bro/cmake \
  -DBRO_CONFIG_PLUGIN_DIR=/usr/lib64/bro/plugins \
  -DBRO_CONFIG_PREFIX=/usr \
  -DBRO_CONFIG_INCLUDE_DIR=/usr/include/bro \
  ..
%make_build

%install
%make_install

%files

%dir %{_libdir}/bro/plugins/Salesforce_GQUIC
%{_libdir}/bro/plugins/Salesforce_GQUIC/*

%doc README.md VERSION
%license LICENSE.txt

%changelog
* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 1.0-1
- Initial RPM packaging.
