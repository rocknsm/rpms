%global distname broker
Name:           libbroker
Version:        1.2.0
Release:        1%{?dist}
Summary:        Zeek’s messaging library.

License:        BSD
URL:            https://docs.zeek.org/projects/broker/en/stable/
Source0:        https://www.zeek.org/downloads/%{distname}-%{version}.tar.gz

BuildRequires:  sqlite-devel
BuildRequires:  caf-devel
BuildRequires:  openssl-devel
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  python2-devel
Requires:       libcaf_core
Requires:       libcaf_io
Requires:       libcaf_openssl
Requires:       openssl

%description
Broker is a library for type-rich publish/subscribe communication in Bro’s data
model.

################################################################################
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

################################################################################
%package        python
Summary:        Pything bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    python
The %{name}-python package contains Python bindings for
developing applications that use %{name}.

Requires:       python2

%prep
%setup -q -n %{distname}-%{version}

%build
mkdir build; cd build
%cmake \
  -DCAF_ROOT_DIR=%{_prefix} \
  -DBROKER_ROOT_DIR=%{_prefix} \
  -DPY_MOD_INSTALL_DIR=%{python_sitearch} \
  -DPYTHON_INCLUDE_DIR=%{_includedir} \
  -DPYTHON_LIBRARIES=%{_libdir} \
  -DINSTALL_LIB_DIR=%{_libdir} \
  ..
%make_build

%install
rm -rf $RPM_BUILD_ROOT
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%check
ctest -V %{?_smp_mflags}

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

%files python
%doc
%dir %{python_sitearch}/broker
%{python_sitearch}/broker/*


%changelog

* Wed Feb 13 2019 Derek Ditch <derek@rocknsm.io> 1.1.2
- Initial RPM packaging
