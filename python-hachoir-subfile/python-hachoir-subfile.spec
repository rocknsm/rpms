# Created by pyp2rpm-3.2.2
%global pypi_name hachoir-subfile

Name:           python-%{pypi_name}
Version:        0.5.3
Release:        1%{?dist}
Summary:        Find subfile in any binary stream

License:        GNU GPL v2
URL:            http://hachoir.org/wiki/hachoir-subfile
Source0:        https://files.pythonhosted.org/packages/source/h/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
hachoirsubfile is a tool based on hachoirparser to find subfiles in any binary
stream.Website: Version 0.5.3 (20080401): * Catch StreamError on file copy *
Use "!/usr/bin/env python" as shebang for FreeBSDVersion 0.5.2 (20070713): *
Fix shebang: use "!/usr/bin/python" * Only import hachoir_core.profiler with
profiler command line option is used, so hachoirsubfile do not depends on
'profiler'...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
hachoirsubfile is a tool based on hachoirparser to find subfiles in any binary
stream.Website: Version 0.5.3 (20080401): * Catch StreamError on file copy *
Use "!/usr/bin/env python" as shebang for FreeBSDVersion 0.5.2 (20070713): *
Fix shebang: use "!/usr/bin/python" * Only import hachoir_core.profiler with
profiler command line option is used, so hachoirsubfile do not depends on
'profiler'...


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build

%install
%py2_install
cp %{buildroot}/%{_bindir}/hachoir-subfile %{buildroot}/%{_bindir}/hachoir-subfile-%{python2_version}
ln -s %{_bindir}/hachoir-subfile-%{python2_version} %{buildroot}/%{_bindir}/hachoir-subfile-2


%files -n python2-%{pypi_name}
%doc 
%{_bindir}/hachoir-subfile
%{_bindir}/hachoir-subfile-2
%{_bindir}/hachoir-subfile-%{python2_version}
%{python2_sitelib}/hachoir_subfile
%{python2_sitelib}/hachoir_subfile-%{version}-py?.?.egg-info

%changelog
* Thu Nov 30 2017 Derek Ditch <derek@rocknsm.io> - 0.5.3-1
- Initial package.