# Created by pyp2rpm-3.2.2
%global pypi_name hachoir-core

Name:           python-%{pypi_name}
Version:        1.3.3
Release:        1%{?dist}
Summary:        Core of Hachoir framework: parse and edit binary files

License:        GNU GPL v2
URL:            http://bitbucket.org/haypo/hachoir/wiki/hachoir-core
Source0:        https://files.pythonhosted.org/packages/source/h/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
Hachoir project Hachoir is a Python library used to represent of a binary file
as a tree of Python objects. Each object has a type, a value, an address, etc.
The goal is to be able to know the meaning of each bit in a file.Why using slow
Python code instead of fast hardcoded C code? Hachoir has many interesting
features: * Autofix: Hachoir is able to open invalid / truncated files * Lazy:
Open...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Hachoir project Hachoir is a Python library used to represent of a binary file
as a tree of Python objects. Each object has a type, a value, an address, etc.
The goal is to be able to know the meaning of each bit in a file.Why using slow
Python code instead of fast hardcoded C code? Hachoir has many interesting
features: * Autofix: Hachoir is able to open invalid / truncated files * Lazy:
Open...


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build

%install
%py2_install


%files -n python2-%{pypi_name}
%doc 
%{python2_sitelib}/hachoir_core
%{python2_sitelib}/hachoir_core-%{version}-py?.?.egg-info

%changelog
* Thu Nov 30 2017 Derek Ditch <derek@rocknsm.io> - 1.3.3-1
- Initial package.
