# Created by pyp2rpm-3.2.2
%global pypi_name czipfile

Name:           python-%{pypi_name}
Version:        1.0.0
Release:        1%{?dist}
Summary:        A replacement for the builtin zipfile module, with fast, C-based zipfile decryption

License:        Python Software Foundation License
URL:            http://pypi.python.org/pypi/czipfile
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
czipfile is a replacement for Python's builtin "zipfile" module, and provides
much faster, Cbased zipfile decryption. The code is actually 95% identical to
Python 2.6.5's Lib/zipfile.py, with some very minor modifications to allow it
to compile in Cython, and the _ZipDecrypter class adapted to take advantage of
native C datatypes.Many thanks to _habnabit from python in Freenode for
pointing me...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
czipfile is a replacement for Python's builtin "zipfile" module, and provides
much faster, Cbased zipfile decryption. The code is actually 95% identical to
Python 2.6.5's Lib/zipfile.py, with some very minor modifications to allow it
to compile in Cython, and the _ZipDecrypter class adapted to take advantage of
native C datatypes.Many thanks to _habnabit from python in Freenode for
pointing me...


%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py2_build

%install
%py2_install


%files -n python2-%{pypi_name}
%license LICENSE
%doc 
%{python2_sitearch}/czipfile.so
%{python2_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Sun Dec 17 2017 Derek Ditch <derek@rocknsm.io> - 1.0.0-1
- Initial package.
