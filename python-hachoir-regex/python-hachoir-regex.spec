# Created by pyp2rpm-3.2.2
%global pypi_name hachoir-regex

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

Name:           python-%{pypi_name}
Version:        1.0.5
Release:        1%{?dist}
Summary:        Manipulation of regular expressions (regex)

License:        GNU GPL v2
URL:            http://bitbucket.org/haypo/hachoir/wiki/hachoir-regex
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
Hachoir regex hachoirregex is a Python library for regular expression (regex or
regexp) manupulation. You can use a|b (or) and a+b (and) operators. Expressions
are optimized during the construction: merge ranges, simplify repetitions, etc.
It also contains a class for pattern matching allowing to search multiple
strings and regex at the same time.

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Hachoir regex hachoirregex is a Python library for regular expression (regex or
regexp) manupulation. You can use a|b (or) and a+b (and) operators. Expressions
are optimized during the construction: merge ranges, simplify repetitions, etc.
It also contains a class for pattern matching allowing to search multiple
strings and regex at the same time.

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Hachoir regex hachoirregex is a Python library for regular expression (regex or
regexp) manupulation. You can use a|b (or) and a+b (and) operators. Expressions
are optimized during the construction: merge ranges, simplify repetitions, etc.
It also contains a class for pattern matching allowing to search multiple
strings and regex at the same time.
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
%doc 
%{python2_sitelib}/hachoir_regex
%{python2_sitelib}/hachoir_regex-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name}
%doc 
%{python3_sitelib}/hachoir_regex
%{python3_sitelib}/hachoir_regex-%{version}-py?.?.egg-info
%endif

%changelog
* Thu Nov 30 2017 Derek Ditch <derek@rocknsm.io> - 1.0.5-1
- Initial package.
