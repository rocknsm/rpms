%global     distname bro-community-id

Name:       bro-plugin-communityid
Version:    1.2
Release:    1%{?dist}
Summary:    Zeek support for "community ID" flow hashing

License:    BSD
URL:        https://github.com/corelight/%{distname}
Source0:    https://github.com/corelight/%{distname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 2.8
BuildRequires:  bro-devel = 2.6.3
BuildRequires:  bifcl = 1:1.1
BuildRequires:  binpac-devel = 1:0.53
BuildRequires:  binpac = 1:0.53
BuildRequires:  gcc-c++
BuildRequires:  openssl-devel
Requires:       bro-core  = 2.6.3

%description
Protocol analyzer that detects, dissects, fingerprints, and logs GQUIC traffic.

%prep
%setup -n %{distname}-%{version}

%build
mkdir build; cd build
%cmake \
  -DCMAKE_MODULE_PATH=/usr/share/bro/cmake \
  -DBRO_CONFIG_CMAKE_DIR=/usr/share/bro/cmake \
  -DBRO_CONFIG_PLUGIN_DIR=/usr/lib64/bro/plugins \
  -DBRO_CONFIG_PREFIX=/usr \
  -DBRO_CONFIG_INCLUDE_DIR=/usr/include/bro \
  -DBRO_HAS_OLD_DIGEST_CODE=True \
  ..
%make_build

%install
%make_install

%files
%dir %{_libdir}/bro/plugins/Corelight_CommunityID

%{_libdir}/bro/plugins/Corelight_CommunityID/*

%doc README.md CHANGES VERSION
%license COPYING

%changelog
* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 1.2-1
- Initial RPM packaging.
