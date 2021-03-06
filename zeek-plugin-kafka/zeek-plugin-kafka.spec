%global     distname metron-bro-plugin-kafka
%global     commit0 8da1637a50815d6093e482bdb7a1a0882e02df3a
%global     shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global     commitdate 20200519

%global BIFCL_VER 1:1.2
%global BINPAC_VER 1:0.55.1
%global ZEEK_VER 3.1.4
%global LIBRDKAFKA_VER 1.4.0

%if 0%{?rhel} < 8
%global scl devtoolset-8
%global scl_prefix devtoolset-8-
%global scl_enable cat << EOSCL | scl enable %{scl} -
%global scl_disable EOSCL
%endif

Name:       zeek-plugin-kafka
Version:    0.3.0
Release:    9.%{commitdate}git%{shortcommit0}%{?dist}
Epoch:      1
Summary:    A Zeek log writer plugin that sends logging output to Kafka.

License:    ASL 2.0
URL:        https://github.com/apache/%{distname}
Source0:    https://github.com/apache/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

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
BuildRequires:  librdkafka-devel = %{LIBRDKAFKA_VER}
BuildRequires:  openssl-devel
Requires:       zeek-core  = %{ZEEK_VER}
Requires:       librdkafka = %{LIBRDKAFKA_VER}
Requires:       openssl

Obsoletes:      bro-plugin-kafka < 0.3-5
Provides:       bro-plugin-kafka = %{version}-%{release}

%description
A Bro log writer plugin that sends logging output to Kafka.

%prep
%autosetup -n %{distname}-%{commit0}

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
%{_libdir}/zeek/plugins/APACHE_KAFKA

%doc README.md COPYING MAINTAINER VERSION CHANGES

%changelog
* Thu Jun 11 2020 Derek Ditch <derek@rocknsm.io> 0.3-8
- Recompile against Zeek 3.1.4

* Thu May 21 2020 Derek Ditch <derek@rocknsm.io> 0.3-8
- Bump to latest upstream commit
- Recompile against Zeek 3.1.3
- Build with cmake 3 and g++ > 8

* Mon Dec 16 2019 Derek Ditch <derek@rocknsm.io> 0.3-7
- Recompile against Zeek 3.0.1

* Tue Sep 24 2019 Derek Ditch <derek@rocknsm.io> 0.3-6
- Recompile against Zeek 3.0.0

* Thu Sep 5 2019 Derek Ditch <derek@rocknsm.io> 0.3-5
- Recompile against Bro 2.6.4

* Fri Aug 23 2019 Bradford Dabbs <brad@dabbs.io> 0.3-4
- Updated to latest commit upstream
- Updated Bro requirement to 2.6.3

* Thu Feb 14 2019 Derek Ditch <derek@rocknsm.io> 0.3-3
- Updated to latest commit upstream (technically pre-0.3)
- Fix segfault on plugin exit
- Allow sending log to multiple topics

* Fri Oct 26 2018 Derek Ditch <derek@rocknsm.io> 0.3-2
- Update librdkafka requirement to 0.11.5

* Wed Oct 24 2018 Derek Ditch <derek@rocknsm.io> 0.3-1
- Updating to upstream version
- Update to link against Bro 2.5.5

* Mon Aug 13 2018 Derek Ditch <derek@rocknsm.io> 0.2-3
- Rebuilding to lock against librdkafka 0.11.4

* Thu Apr 05 2018 Derek Ditch <derek@rocknsm.io> 0.2-2
- Rebuilding to link against librdkafka 0.11.4

* Thu Apr 05 2018 Derek Ditch <derek@rocknsm.io> 0.2-1
- Updated to latest upstream
- Integrates configurable JSON timestamps
- Removes "send all logs by default" option
