# Created by pyp2rpm-3.2.2
%global pypi_name PyPDF2

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

Name:           python-%{pypi_name}
Version:        1.26.0
Release:        1%{?dist}
Summary:        PDF toolkit

License:        BSD
URL:            http://mstamy2.github.com/PyPDF2
Source0:        https://files.pythonhosted.org/packages/source/P/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
A PurePython library built as a PDF toolkit. It is capable of: extracting
document information (title, author, ...) splitting documents page by page
merging documents page by page cropping pages merging multiple pages into a
single page encrypting and decrypting PDF files and more!By being PurePython,
it should run on any Python platform without any dependencies on external
libraries. It can...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
A PurePython library built as a PDF toolkit. It is capable of: extracting
document information (title, author, ...) splitting documents page by page
merging documents page by page cropping pages merging multiple pages into a
single page encrypting and decrypting PDF files and more!By being PurePython,
it should run on any Python platform without any dependencies on external
libraries. It can...

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
A PurePython library built as a PDF toolkit. It is capable of: extracting
document information (title, author, ...) splitting documents page by page
merging documents page by page cropping pages merging multiple pages into a
single page encrypting and decrypting PDF files and more!By being PurePython,
it should run on any Python platform without any dependencies on external
libraries. It can...
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
%doc README.md Sample_Code/README.txt
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md Sample_Code/README.txt
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Tue Dec 19 2017 Derek Ditch <derek@rocknsm.io> - 1.26.0-1
- Initial package.
