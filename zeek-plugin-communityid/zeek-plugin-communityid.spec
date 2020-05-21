%global     distname bro-community-id
%global BIFCL_VER 1:1.2
%global BINPAC_VER 1:0.55.1
%global ZEEK_VER 3.1.3

%if 0%{?rhel} < 8
%global scl devtoolset-8
%global scl_prefix devtoolset-8-
%global scl_enable cat << EOSCL | scl enable %{scl} -
%global scl_disable EOSCL
%endif

Name:       zeek-plugin-communityid
Version:    1.4
Release:    1%{?dist}
Summary:    Zeek support for "community ID" flow hashing

License:    BSD
URL:        https://github.com/corelight/%{distname}
Source0:    https://github.com/corelight/%{distname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

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
BuildRequires:  openssl-devel
Requires:       zeek-core  = %{ZEEK_VER}

Obsoletes:      bro-plugin-communityid < 2:1.2-3
Provides:       bro-plugin-communityid = %{version}-%{release}

%description
Extends Zeek to support for "community ID" flow hashing, a standardized way of
labeling traffic flows in network monitors

%prep
%autosetup -n %{distname}-%{version}

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
%{?scl_enable}
%make_install
%{?scl_disable}

%files
%dir %{_libdir}/zeek/plugins/Corelight_CommunityID

%{_libdir}/zeek/plugins/Corelight_CommunityID/*

%doc README.md CHANGES VERSION
%license COPYING

%changelog
* Thu May 21 2020 Derek Ditch <derek@rocknsm.io> 1.4-1
- Version bump upstream to 1.4
- Compile with g++ > 8 and cmake 3

* Mon Dec 16 2019 Derek Ditch <derek@rocknsm.io> 1.2-4
- Recompile against Zeek 3.0.1

* Tue Sep 24 2019 Derek Ditch <derek@rocknsm.io> 1.2-3
- Recompile against Zeek 3.0.0

* Thu Sep 5 2019 Derek Ditch <derek@rocknsm.io> 1.2-2
- Recompile against Bro 2.6.4

* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 1.2-1
- Initial RPM packaging.
