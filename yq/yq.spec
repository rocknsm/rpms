Name:           yq
Version:        2.3.0
Release:        1%{?dist}
Summary:        Process YAML documents from the CLI

License:        MIT
URL:            https://github.com/mikefarah/yq
Source0:        https://github.com/mikefarah/%{name}/archive/v%{version}.tar.gz

BuildRequires:  golang

%description
yq is a lightweight and portable command-line YAML processor.

The aim of the project is to be the jq or sed of yaml files.



%prep
%autosetup -n %{name}

%build

export GOPATH=$(pwd):%{gopath}

# Get go dependencies
go get -u github.com/kardianos/govendor
go install github.com/kardianos/govendor

# Build the yq binary
govendor sync;
go build -o %{name};

%install
rm -rf %{buildroot}

# Install binaries & scripts
install -d %{buildroot}%{_bindir}
install -p -m 755 %{name} %{buildroot}%{_bindir}

%files
%doc README.md LICENSE

%{_bindir}/%{name}


* Wed Jun 7 2017 Derek Ditch <derek@rocknsm.io>
- Added datestamp to allow for proper RPM progression
- Minor cleanups in SPEC file
- Added systemd as build-time dependency
