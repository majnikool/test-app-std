# Allow external override of 'version'
# i.e. if we run: rpmbuild --define "version 0.1.99" ...
%{!?version: %define version 0.1.0}

%define debug_package %{nil}
AutoReqProv: no

Name:           fastapi-app
Version:        %{version}
Release:        1%{?dist}
Summary:        FastAPI CRUD Application

License:        MIT
URL:            https://github.com/majnikool/test-app-std
Source0:        %{name}-%{version}.tar.gz

%description
A FastAPI CRUD application with PostgreSQL backend

%prep
# Expects a folder named "my_fastapi_app" at the root of your tarball.
%setup -q -n my_fastapi_app

%build
# No build steps needed for a Python/uvicorn setup.

%install
# Copy everything into /opt/fastapi-app
mkdir -p %{buildroot}/opt/fastapi-app
cp -r * %{buildroot}/opt/fastapi-app/

# Install the systemd service file
mkdir -p %{buildroot}/etc/systemd/system/
install -m 644 packaging/fastapi.service %{buildroot}/etc/systemd/system/fastapi.service

%files
/opt/fastapi-app
/etc/systemd/system/fastapi.service

%post
systemctl daemon-reload
systemctl enable fastapi.service

%preun
systemctl stop fastapi.service
systemctl disable fastapi.service

%postun
systemctl daemon-reload
