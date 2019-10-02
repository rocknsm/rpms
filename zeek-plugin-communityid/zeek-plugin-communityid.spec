%global     distname bro-community-id

Name:       zeek-plugin-communityid
Version:    1.2
Release:    3%{?dist}
Summary:    Zeek support for "community ID" flow hashing

License:    BSD
URL:        https://github.com/corelight/%{distname}
Source0:    https://github.com/corelight/%{distname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 2.8
BuildRequires:  zeek-devel = 3.0.0 
BuildRequires:  bifcl = 1:1.2
BuildRequires:  binpac-devel = 1:0.54
BuildRequires:  binpac = 1:0.54
BuildRequires:  gcc-c++
BuildRequires:  openssl-devel
Requires:       zeek-core  = 3.0.0

Obsoletes:      bro-plugin-communityid < 2:1.2-3
Provides:       bro-plugin-communityid = %{version}-%{release}

%description
Extends Zeek to support for "community ID" flow hashing, a standardized way of 
labeling traffic flows in network monitors

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
  ..
%make_build

%install
%make_install

%files
%dir %{_libdir}/zeek/plugins/Corelight_CommunityID

%{_libdir}/zeek/plugins/Corelight_CommunityID/*

%doc README.md CHANGES VERSION
%license COPYING

%changelog
* Tue Sep 24 2019 Derek Ditch <derek@rocknsm.io> 1.2-3
- Recompile against Zeek 3.0.0

* Thu Sep 5 2019 Derek Ditch <derek@rocknsm.io> 1.2-2
- Recompile against Bro 2.6.4

* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 1.2-1
- Initial RPM packaging.
