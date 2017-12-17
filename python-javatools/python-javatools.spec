# Created by pyp2rpm-3.2.2
%global pypi_name javatools

Name:           python-%{pypi_name}
Version:        1.3
Release:        1%{?dist}
Summary:        Tools for finding meaningful deltas in Java class files and JARs

License:        GNU Lesser General Public License
URL:            https://github.com/obriencj/python-javatools
Source0:        https://files.pythonhosted.org/packages/source/j/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
UNKNOWN

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
UNKNOWN


%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py2_build

%install
%py2_install
cp %{buildroot}/%{_bindir}/manifest %{buildroot}/%{_bindir}/manifest-%{python2_version}
ln -s %{_bindir}/manifest-%{python2_version} %{buildroot}/%{_bindir}/manifest-2
cp %{buildroot}/%{_bindir}/distdiff %{buildroot}/%{_bindir}/distdiff-%{python2_version}
ln -s %{_bindir}/distdiff-%{python2_version} %{buildroot}/%{_bindir}/distdiff-2
cp %{buildroot}/%{_bindir}/classinfo %{buildroot}/%{_bindir}/classinfo-%{python2_version}
ln -s %{_bindir}/classinfo-%{python2_version} %{buildroot}/%{_bindir}/classinfo-2
cp %{buildroot}/%{_bindir}/distinfo %{buildroot}/%{_bindir}/distinfo-%{python2_version}
ln -s %{_bindir}/distinfo-%{python2_version} %{buildroot}/%{_bindir}/distinfo-2
cp %{buildroot}/%{_bindir}/jarinfo %{buildroot}/%{_bindir}/jarinfo-%{python2_version}
ln -s %{_bindir}/jarinfo-%{python2_version} %{buildroot}/%{_bindir}/jarinfo-2
cp %{buildroot}/%{_bindir}/classdiff %{buildroot}/%{_bindir}/classdiff-%{python2_version}
ln -s %{_bindir}/classdiff-%{python2_version} %{buildroot}/%{_bindir}/classdiff-2
cp %{buildroot}/%{_bindir}/jardiff %{buildroot}/%{_bindir}/jardiff-%{python2_version}
ln -s %{_bindir}/jardiff-%{python2_version} %{buildroot}/%{_bindir}/jardiff-2


%files -n python2-%{pypi_name}
%doc 
%{_bindir}/manifest
%{_bindir}/manifest-2
%{_bindir}/manifest-%{python2_version}
%{_bindir}/distdiff
%{_bindir}/distdiff-2
%{_bindir}/distdiff-%{python2_version}
%{_bindir}/classinfo
%{_bindir}/classinfo-2
%{_bindir}/classinfo-%{python2_version}
%{_bindir}/distinfo
%{_bindir}/distinfo-2
%{_bindir}/distinfo-%{python2_version}
%{_bindir}/jarinfo
%{_bindir}/jarinfo-2
%{_bindir}/jarinfo-%{python2_version}
%{_bindir}/classdiff
%{_bindir}/classdiff-2
%{_bindir}/classdiff-%{python2_version}
%{_bindir}/jardiff
%{_bindir}/jardiff-2
%{_bindir}/jardiff-%{python2_version}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Thu Nov 30 2017 Derek Ditch <derek@rocknsm.io> - 1.3-1
- Initial package.
