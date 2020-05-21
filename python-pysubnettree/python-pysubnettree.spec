%global srcname pysubnettree

Name:           python-%{srcname}
Version:        0.33
Release:        1%{?dist}
Summary:        A Python Module for CIDR Lookups

License:        BSD
URL:            https://github.com/zeek/%{srcname}
Source0:        https://download.zeek.org/%{srcname}-%{version}.tar.gz

%global _description %{expand:
The PySubnetTree package provides a Python data structure SubnetTree which
maps subnets given in CIDR notation (incl. corresponding IPv6 versions) to
Python objects. Lookups are performed by longest-prefix matching. }

%description
%{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  gcc-c++

%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} setup.py test

%files -n python3-%{srcname}
%doc CHANGES README
%license COPYING
%{python3_sitearch}/%{srcname}/

%changelog
* Thu May 21 2020 Derek Ditch <derek@rocknsm.io> - 0.34-1
- Update to lastest upstream release 0.33

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
