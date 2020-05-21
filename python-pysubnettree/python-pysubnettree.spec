%global srcname pysubnettree

%bcond_without with_python3

%if 0%{?fedora} < 6
%bcond_with with_python2
%else
%bcond_without with_python2
%endif

Name:           python-%{srcname}
Version:        0.33
Release:        1%{?dist}
Summary:        A Python Module for CIDR Lookups

License:        BSD
URL:            https://github.com/zeek/%{srcname}
Source0:        https://download.zeek.org/%{srcname}-%{version}.tar.gz

%if %{with python2}
BuildRequires:  python2-devel
%endif
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif
BuildRequires:  gcc-c++

%global common_desc The PySubnetTree package provides a Python data structure SubnetTree which \
maps subnets given in CIDR notation (incl. corresponding IPv6 versions) to \
Python objects. Lookups are performed by longest-prefix matching.

%description
%{common_desc}

%if %{with python2}
%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{common_desc}
%endif

%if %{with python3}
%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{common_desc}
%endif

%prep
%autosetup

%build
%if %{with python2}
%py2_build
%endif
%if %{with python3}
%py3_build
%endif

%install
%if %{with python2}
%py2_install
%endif
%if %{with python3}
%py3_install
%endif

%if %{with python2}
%files -n python2-%{srcname}
%doc CHANGES README
%license COPYING
%{python2_sitearch}/*
%endif

%if %{with python3}
%files -n python3-%{srcname}
%doc CHANGES README
%license COPYING
%{python3_sitearch}/*
%endif

%changelog
* Sun Feb 09 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.33-1
- Update to lastest upstream release 0.33

* Wed May 13 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.24-1
- Update to lastest upstream release 0.24

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.23-5
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.23-3
- Fix macro

* Sun Jun 22 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.23-2
- Use PyPI as SOURCE0 for now
- Fix permission

* Fri Jun 20 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.23-1
- Initial package
