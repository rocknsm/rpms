# Created by pyp2rpm-3.2.2
%global pypi_name ctypescrypto

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

Name:           python-%{pypi_name}
Version:        0.4.2
Release:        1%{?dist}
Summary:        CTypes-based interface for some OpenSSL libcrypto features

License:        None
URL:            https://github.com/vbwagner/ctypescrypto
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
 
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
ctypescrypto
============

Python interface to some openssl function based on
ctypes module

This module is based on works from
http://code.google.com/p/ctypescrypto/

most recent version can be checked out
from

https://github.com/vbwagner/ctypescrypto.git

Rationale
---------

Why
have yet another crypto extension for Python? There is pyopenssl,
m2crypto,
hashlib in the standard library and...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
ctypescrypto
============

Python interface to some openssl function based on
ctypes module

This module is based on works from
http://code.google.com/p/ctypescrypto/

most recent version can be checked out
from

https://github.com/vbwagner/ctypescrypto.git

Rationale
---------

Why
have yet another crypto extension for Python? There is pyopenssl,
m2crypto,
hashlib in the standard library and...

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
ctypescrypto
============

Python interface to some openssl function based on
ctypes module

This module is based on works from
http://code.google.com/p/ctypescrypto/

most recent version can be checked out
from

https://github.com/vbwagner/ctypescrypto.git

Rationale
---------

Why
have yet another crypto extension for Python? There is pyopenssl,
m2crypto,
hashlib in the standard library and...
%endif

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%if %{with python3}
%py3_install
%endif

%py2_install


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Sun Dec 17 2017 Derek Ditch <derek@rocknsm.io> - 0.4.2-1
- Initial package.
