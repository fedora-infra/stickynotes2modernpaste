# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           stickynotes2modernpaste
Version:        1.0.0
Release:        1%{?dist}
Summary:        A (temporary) bridge from sticky-notes to modernpaste for the fpaste client

License:        MIT
URL:            https://github.com/fedora-infra/stickynotes2modernpaste
Source0:        https://github.com/fedora-infra/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       python-flask
Requires:       python-requests
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-flask

Requires:       python-sqlalchemy
BuildRequires:  python-sqlalchemy

%description
A (temporary) bridge from sticky-notes to modernpaste for the fpaste client.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# wsgi stuff
mkdir -p %{buildroot}%{_datadir}/%{name}/
cp stickynotes2modernpaste.wsgi %{buildroot}%{_datadir}/%{name}/

# configuration file
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install config.ini %{buildroot}%{_sysconfdir}/%{name}

%files
%doc README.md

%{python_sitelib}/*
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%changelog
* Wed Jan 4 2017 Ricky Elrod <relrod@redhat.com> - 1.0.0-1
- Initial build.
