%global distname broker

%if 0%{?rhel} < 8
%global scl devtoolset-8
%global scl_prefix devtoolset-8-
%global scl_enable cat << EOSCL | scl enable %{scl} -
%global scl_disable EOSCL
%endif

Name:           libbroker
Version:        1.3.3
Release:        1%{?dist}
Summary:        Zeek's messaging library.

License:        BSD
URL:            https://docs.zeek.org/projects/%{distname}/
Source0:        https://download.zeek.org/%{distname}-%{version}.tar.gz

%if 0%{?rhel} < 8
BuildRequires:    cmake3
%global cmake %cmake3
%else
BuildRequires:    cmake
%endif
BuildRequires:  sqlite-devel
BuildRequires:  caf-devel >= 0.17.3
BuildRequires:  openssl-devel
BuildRequires:  %{?scl_prefix}gcc-c++ >= 8
BuildRequires:  python3-devel
Requires:       libcaf_core >= 0.17.3
Requires:       libcaf_io >= 0.17.3
Requires:       libcaf_openssl >= 0.17.3
Requires:       openssl

%description
Broker is a library for type-rich publish/subscribe communication in Zeek's data
model.

################################################################################
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

################################################################################
%package     -n python3-%{distname}
Summary:        Python bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{distname}
The python3-%{distname} package contains Python bindings for
developing applications that use %{name}.

Requires:       python3

%prep
%autosetup -n %{distname}-%{version}

%build
mkdir build; cd build

%{?scl_enable} 
%cmake \
  -DCAF_ROOT_DIR=%{_prefix} \
  -DBROKER_ROOT_DIR=%{_prefix} \
  -DPY_MOD_INSTALL_DIR=%{python3_sitearch} \
  -DPYTHON_INCLUDE_DIR=%{_includedir} \
  -DPYTHON_LIBRARIES=%{_libdir} \
  -DINSTALL_LIB_DIR=%{_libdir} \
  ..
%{?scl_disable}

%{?scl_enable}
%make_build
%{?scl_disable}

%install
rm -rf %{buildroot}

%{?scl_enable} 
%make_install
%{?scl_disable}

find %{buildroot} -name '*.la' -delete

%check
%{?scl_enable}
ctest -V %{?_smp_mflags}
%{?scl_disable}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README
%doc CHANGES
%license COPYING
%{_libdir}/*.so.*

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so

%files -n python3-%{distname}
%doc
%dir %{python3_sitearch}/broker
%{python3_sitearch}/broker/*

%changelog
* Tue May 19 2020 Derek Ditch <derek@rocknsm.io> 1.3.3-1
- Version bump to 1.3.3
- Update download and docs links

* Mon Dec 16 2019 Derek Ditch <derek@rocknsm.io> 1.2.0-2
- Recompile against CAF 0.17.3

* Mon Sep 16 2019 Derek Ditch <derek@rocknsm.io> 1.2.0-1
- Version bump to 1.2.0 for Zeek 3.x
- Pin to CAF 0.17.x

* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 1.1.2-2
- Rename python package to RPM conventions
- Pinned CAF versions

* Wed Feb 13 2019 Derek Ditch <derek@rocknsm.io> 1.1.2-1
- Initial RPM packaging
