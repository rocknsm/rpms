# Created by pyp2rpm-3.2.2
%global pypi_name ssdeep

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

Name:           python-%{pypi_name}
Version:        3.2
Release:        1%{?dist}
Summary:        Python wrapper for the ssdeep library

License:        LGPLv3+
URL:            http://github.com/DinoTools/python-ssdeep
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
 
BuildRequires:  python2-devel
BuildRequires:  python-cffi
BuildRequires:  python-six >= 1.4.1
BuildRequires:  python-setuptools
BuildRequires:  ssdeep-devel
 
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-cffi
BuildRequires:  python3-six >= 1.4.1
BuildRequires:  python3-setuptools
%endif

%description
ssdeep Python Wrapper This is a straightforward Python wrapper for ssdeep by
Jesse Kornblum_, which is a library for computing context triggered piecewise
hashes (CTPH). Also called fuzzy hashes, CTPH can match inputs that have
homologies. Such inputs have sequences of identical bytes in the same order,
although bytes in between these sequences may be different in both content and
length. How...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python-cffi
Requires:       python-six >= 1.4.1
Requires:       ssdeep-libs
%description -n python2-%{pypi_name}
ssdeep Python Wrapper This is a straightforward Python wrapper for ssdeep by
Jesse Kornblum_, which is a library for computing context triggered piecewise
hashes (CTPH). Also called fuzzy hashes, CTPH can match inputs that have
homologies. Such inputs have sequences of identical bytes in the same order,
although bytes in between these sequences may be different in both content and
length. How...

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3-cffi
Requires:       python3-six >= 1.4.1
Requires:       ssdeep-libs
%description -n python3-%{pypi_name}
ssdeep Python Wrapper This is a straightforward Python wrapper for ssdeep by
Jesse Kornblum_, which is a library for computing context triggered piecewise
hashes (CTPH). Also called fuzzy hashes, CTPH can match inputs that have
homologies. Such inputs have sequences of identical bytes in the same order,
although bytes in between these sequences may be different in both content and
length. How...
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
%doc README.rst
%{python2_sitearch}/%{pypi_name}
%{python2_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name}
%doc README.rst
%{python3_sitearch}/%{pypi_name}
%{python3_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Sun Dec 17 2017 Derek Ditch <derek@rocknsm.io> - 3.2-1
- Initial package.
