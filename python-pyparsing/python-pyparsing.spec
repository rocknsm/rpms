%global srcname pyparsing

%global build_wheel 1

%global python_wheelname %{srcname}-%{version}-py2.py3-none-any.whl

# when bootstrapping Python 3, pyparsing needs to be rebuilt before sphinx
%bcond_without doc

Summary:        Python package with an object-oriented approach to text processing
Name:           pyparsing
Version:        2.4.2
Release:        1%{?dist}

License:        MIT
URL:            https://github.com/pyparsing/pyparsing
Source0:        https://github.com/%{name}/%{name}/archive/%{name}_%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  dos2unix
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%if %{with doc}
BuildRequires:  python3-sphinx
%endif

%if 0%{?build_wheel}
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
%endif

%description
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.


%if %{with doc}
%package        doc
Summary:        Documentation for pyparsing python package

%description    doc
The package contains documentation for pyparsing.
%endif


%package -n python2-%{srcname}
Summary:       %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
Provides:      pyparsing = %{version}-%{release}
Obsoletes:     pyparsing < 2.1.10-5

%description -n python2-pyparsing
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.


%package -n python3-pyparsing
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-pyparsing
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

This is the Python 3 version.


%prep
%setup -q -n %{name}-%{name}_%{version}
dos2unix -k CHANGES LICENSE


%build
%py2_build
%if 0%{?build_wheel}
%py3_build_wheel
%else
%py3_build
%endif

%if %{with doc}
# build docs
pushd docs
# Theme is not available
sed -i '/alabaster/d' conf.py
sphinx-build -b html . html
popd
%endif

%install
%py2_install
%if 0%{?build_wheel}
%py3_install_wheel %{python_wheelname}
%else
%py3_install
%endif


%check
%{__python2} unitTests.py
%{__python3} unitTests.py
%{__python3} simple_unit_tests.py


%files -n python2-pyparsing
%license LICENSE
%doc CHANGES README.rst
%{python2_sitelib}/pyparsing.py*
%{python2_sitelib}/pyparsing-*-info/

%files -n python3-pyparsing
%license LICENSE
%doc CHANGES README.rst
%{python3_sitelib}/pyparsing.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/pyparsing-*-info/

%if %{with doc}
%files doc
%license LICENSE
%doc CHANGES README.rst docs/html examples
%endif
