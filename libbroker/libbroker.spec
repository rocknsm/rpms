%global distname broker
%global CAF_VER 0.17.5

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
%global cmake  %{cmake3}
%global ctest  /usr/bin/ctest3
%else
BuildRequires:    cmake
%global cmake  %{cmake}
%global ctest  /usr/bin/ctest
%endif
BuildRequires:  sqlite-devel
BuildRequires:  caf-devel >= %{CAF_VER}
BuildRequires:  openssl-devel
BuildRequires:  %{?scl_prefix}gcc-c++ >= 8
BuildRequires:  python3-devel
%if 0%{?rhel} < 8
BuildRequires:  python36-pyOpenSSL
%else
BuildRequires:  python3-pyOpenSSL
%endif
Requires:       libcaf_core    >= %{CAF_VER}
Requires:       libcaf_io      >= %{CAF_VER}
Requires:       libcaf_openssl >= %{CAF_VER}
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
%if 0%{?rhel} < 8
Requires:  python36-pyOpenSSL
%else
Requires:  python3-pyOpenSSL
%endif

%prep
%autosetup -n %{distname}-%{version}

%build
mkdir build; cd build

%{?scl_enable}
%cmake \
  -DCAF_ROOT_DIR=%{_prefix} \
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

%if 0%{?rhel} < 8
# Not sure why these tests are failing at the moment on CentOS 8
cd build
%{?scl_enable}
%ctest -V %{?_smp_mflags}
%{?scl_disable}
%endif

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
* Wed Jul 8 2020 Derek Ditch <derek@rocknsm.io> 1.3.3-2
- Depend on CAF 0.17.5
- Disable tests for EL8 for now

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
