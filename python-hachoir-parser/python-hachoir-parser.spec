# Created by pyp2rpm-3.2.2
%global pypi_name hachoir-parser

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

Name:           python-%{pypi_name}
Version:        1.3.4
Release:        1%{?dist}
Summary:        Package of Hachoir parsers used to open binary files

License:        GNU GPL v2
URL:            http://bitbucket.org/haypo/hachoir/wiki/hachoir-parser
Source0:        https://files.pythonhosted.org/packages/source/h/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-rpm-macros

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
hachoirparser is a package of most common file format parsers written for
Hachoir framework. Not all parsers are complete, some are very good and other
are poor: only parser first level of the tree for example.A perfect parser have
no "raw" field: with a perfect parser you are able to know *each* bit meaning.
Some good (but not perfect ;)) parsers: * Matroska video * Microsoft RIFF (AVI
video,...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
hachoirparser is a package of most common file format parsers written for
Hachoir framework. Not all parsers are complete, some are very good and other
are poor: only parser first level of the tree for example.A perfect parser have
no "raw" field: with a perfect parser you are able to know *each* bit meaning.
Some good (but not perfect ;)) parsers: * Matroska video * Microsoft RIFF (AVI
video,...

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
hachoirparser is a package of most common file format parsers written for
Hachoir framework. Not all parsers are complete, some are very good and other
are poor: only parser first level of the tree for example.A perfect parser have
no "raw" field: with a perfect parser you are able to know *each* bit meaning.
Some good (but not perfect ;)) parsers: * Matroska video * Microsoft RIFF (AVI
video,...
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


%files -n python2-%{pypi_name}
%doc README.py README.header
%{python2_sitelib}/hachoir_parser
%{python2_sitelib}/hachoir_parser-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name}
%doc README.py README.header
%{python3_sitelib}/hachoir_parser
%{python3_sitelib}/hachoir_parser-%{version}-py?.?.egg-info
%endif

%changelog
* Thu Nov 30 2017 Derek Ditch <derek@rocknsm.io> - 1.3.4-1
- Initial package.
