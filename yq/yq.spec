%global git_org mikefarah

# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0

Name:           yq
Version:        3.3.2
Release:        1%{?dist}
Summary:        Process YAML documents from the CLI

License:        MIT
URL:            https://github.com/%{git_org}/%{name}
Source0:        https://github.com/%{git_org}/%{name}/archive/%{version}.tar.gz

BuildRequires:  golang
BuildRequires:  rsync

%description
yq is a lightweight and portable command-line YAML processor.

The aim of the project is to be the jq or sed of yaml files.

%prep
%autosetup -n %{name}-%{version}

%build

# Build the yq binary - requires internet for dependencies
go  build -o bin/%{name}

%install
rm -rf %{buildroot}

# Install binaries & scripts
install -d %{buildroot}%{_bindir}
install -p -m 755 bin/%{name} %{buildroot}%{_bindir}

%files
%doc README.md LICENSE

%license LICENSE

%{_bindir}/%{name}

%changelog
* Mon Jun 6 2020 Derek Ditch <derek@rocknsm.io> 3.3.2-1
- Update to latest version upstream

* Mon Mar 25 2019 Bradford Dabbs <brad@perched.io> 2.3.0-1
 - Initial creation of spec file
