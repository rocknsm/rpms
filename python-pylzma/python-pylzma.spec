# Created by pyp2rpm-3.2.2
%global pypi_name pylzma

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

Name:           python-%{pypi_name}
Version:        0.4.9
Release:        1%{?dist}
Summary:        Python bindings for the LZMA library by Igor Pavlov

License:        LGPL
URL:            http://www.joachim-bauch.de/projects/pylzma/
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%if %{with python3} 
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
PyLZMA provides a platform independent way to read and write data that has been
compressed or can be decompressed by the LZMA library by Igor Pavlov.

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
PyLZMA provides a platform independent way to read and write data that has been
compressed or can be decompressed by the LZMA library by Igor Pavlov.

%if %{with python3} 
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
PyLZMA provides a platform independent way to read and write data that has been
compressed or can be decompressed by the LZMA library by Igor Pavlov.
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

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

%check
# These checks require manual download of some additional files 
#%{__python2} setup.py test
#%if %{with python3} 
#%{__python3} setup.py test
#%endif

%files -n python2-%{pypi_name}
%license LICENSE src/compat/copying.txt
%doc README.md

%{python2_sitearch}/py7zlib.py*
%{python2_sitearch}/pylzma.so
%{python2_sitearch}/%{pypi_name}-%{version}*-py?.?.egg-info

%if %{with python3} 
%files -n python3-%{pypi_name}
%license LICENSE src/compat/copying.txt
%doc README.md

%{python3_sitearch}/__pycache__/*
%{python3_sitearch}/py7zlib.py
%{python3_sitearch}/pylzma.so
%{python3_sitearch}/%{pypi_name}-%{version}*-py?.?.egg-info
%endif

%changelog
* Sun Dec 17 2017 Derek Ditch <derek@rocknsm.io> - 0.4.9-1
- Initial package.
