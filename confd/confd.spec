Name:           confd
Version:        0.14.0
Release:        1%{?dist}
Epoch:          1
Summary:        confd is a lightweight configuration management tool

License:        MIT
URL:            https://github.com/kelseyhightower/%{name}/
Source0:        https://github.com/kelseyhightower/%{name}/archive/v%{version}.tar.gz

BuildRequires:  golang
BuildRequires:  golang(github.com/BurntSushi/toml)

%description
confd is a lightweight configuration management tool. It supports the following backends:
etcd, consul, vault, environment variables, redis, zookeeper, dynamodb, rancher, 
ssm (AWS Simple Systems Manager Parameter Store)

%prep
%autosetup -n %{name}-%{version}

%build
# set up temporary build gopath, and put our directory there
mkdir -p ./_build/src/github.com/kelseyhightower/
ln -s $(pwd) ./_build/src/github.com/kelseyhightower/%{name}

# Build confd
export GOPATH=$(pwd)/_build:%{gopath}

# build with external linker to get a BuildID
GO_LDFLAGS="-linkmode=external"
go build -ldflags "${GO_LDFLAGS}" -o bin/%{name}

%install
rm -rf %{buildroot}

# Install binaries & scripts
install -d %{buildroot}%{_bindir}
install -p -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}

%files
%doc README.md LICENSE
%{_bindir}/%{name}

%changelog

* Mon Jan 15 2018 Derek Ditch <derek@rocknsm.io> 0.14.0-1
- Initial RPM for v0.14.0

