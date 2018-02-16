Name:           confd
Version:        0.14.0
Release:        2%{?dist}
Epoch:          1
Summary:        confd is a lightweight configuration management tool

License:        MIT
URL:            https://github.com/kelseyhightower/%{name}/
Source0:        https://github.com/kelseyhightower/%{name}/archive/v%{version}.tar.gz
Patch0:         https://github.com/dcode/confd/commit/d84d8908a18f021fcb9389a2ff4d40a63f4aec03.patch#/01_add_atoi_templ_func.patch

BuildRequires:  golang
BuildRequires:  golang(github.com/BurntSushi/toml)
BuildRequires:  git

%description
confd is a lightweight configuration management tool. It supports the following backends:
etcd, consul, vault, environment variables, redis, zookeeper, dynamodb, rancher, 
ssm (AWS Simple Systems Manager Parameter Store)

%prep
%autosetup -n %{name}-%{version} -S git

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

* Thu Feb 15 2018 Derek Ditch <derek@rocknsm.io> 0.14.0-2
- Added patch to support atoi in templates

* Mon Jan 15 2018 Derek Ditch <derek@rocknsm.io> 0.14.0-1
- Initial RPM for v0.14.0

