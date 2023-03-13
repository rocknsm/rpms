%global     distname GQUIC_Protocol_Analyzer
%global     commit0 12d9dfe468f4774d6d57edf2758fa293fe5d5f42
%global     shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global     commitdate 20200511

%global BIFCL_VER 1:1.7.0
%global BINPAC_VER 1:0.60.0
%global ZEEK_VER 5.0.7

%if 0%{?rhel} < 8
%global scl devtoolset-8
%global scl_prefix devtoolset-8-
%global scl_enable cat << EOSCL | scl enable %{scl} -
%global scl_disable EOSCL
%endif

Name:       zeek-plugin-gquic
Version:    1.0
Release:    6.%{commitdate}git%{shortcommit0}%{?dist}
Summary:    Protocol analyzer that detects, dissects, fingerprints, and logs GQUIC traffic

License:    BSD
URL:        https://github.com/salesforce/%{distname}
Source0:    https://github.com/salesforce/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Patch0:     https://github.com/salesforce/GQUIC_Protocol_Analyzer/compare/master...dcode:master.patch#/01-%{name}-%{shortcommit0}-zeek3.1-fixes.patch

%if 0%{?rhel} < 8
BuildRequires:    cmake3  >= 3.0.0
%global cmake %cmake3
%else
BuildRequires:    cmake   >= 3.0.0
%endif
BuildRequires:  zeek-devel = %{ZEEK_VER}
BuildRequires:  bifcl = %{BIFCL_VER}
BuildRequires:  binpac-devel = %{BINPAC_VER}
BuildRequires:  binpac = %{BINPAC_VER}
BuildRequires:  %{?scl_prefix}gcc-c++ >= 8
BuildRequires:  git
Requires:       zeek-core  = %{ZEEK_VER}

Obsoletes:      bro-plugin-gquic < 1.0-3
Provides:       bro-plugin-gquic = %{version}-%{release}

%description
Protocol analyzer that detects, dissects, fingerprints, and logs GQUIC traffic.

%prep
%autosetup -n %{distname}-%{commit0} -S git

%build
mkdir build; cd build
%{?scl_enable}
%cmake \
  -DCMAKE_MODULE_PATH=%{_datadir}/zeek/cmake \
  -DBRO_CONFIG_CMAKE_DIR=%{_datadir}/zeek/cmake \
  -DBRO_CONFIG_PLUGIN_DIR=%{_libdir}/zeek/plugins \
  -DBRO_CONFIG_PREFIX=%{_prefix} \
  -DBRO_CONFIG_INCLUDE_DIR=%{_includedir}/zeek \
  ..
%{?scl_disable}

%{?scl_enable}
%make_build
%{?scl_disable}

%install
cd build
%{?scl_enable}
%make_install
%{?scl_disable}

%files

%dir %{_libdir}/zeek/plugins/Salesforce_GQUIC
%{_libdir}/zeek/plugins/Salesforce_GQUIC/*

%doc README.md VERSION
%license LICENSE.txt

%changelog
* Thu Jun 11 2020 Derek Ditch <derek@rocknsm.io> 1.0-6
- Recompile against Zeek 3.1.4

* Thu May 21 2020 Derek Ditch <derek@rocknsm.io> 1.0-5
- Bump to upstream latest
- Recompile with g++ > 8 and cmake 3

* Mon Dec 16 2019 Derek Ditch <derek@rocknsm.io> 1.0-4
- Recompile against Zeek 3.0.1

* Tue Sep 24 2019 Derek Ditch <derek@rocknsm.io> 1.0-3
- Recompile against Zeek 3.0.0

* Thu Sep 5 2019 Derek Ditch <derek@rocknsm.io> 1.0-2
- Recompile against Bro 2.6.4

* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 1.0-1
- Initial RPM packaging.
