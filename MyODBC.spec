%define myodbc_version		2.50.37
%define release			1

Name:		MyODBC
Summary:	MyODBC: an ODBC driver for MySQL
Group:		Applications/Databases
Version:	%{myodbc_version}
Release:	%{release}
Copyright:	Public Domain
Source0:	MyODBC-%{myodbc_version}.tar.gz
URL:		http://www.mysql.com/
Vendor:		MySQL AB
Packager:	Matt Wagner <matt@mysql.com>

# Think about what you use here since the first step is to
# run a rm -rf
BuildRoot:	/var/tmp/myodbc

# From the manual
%description
MyODBC: an ODBC driver for MySQL

%prep
%setup -n MyODBC-%{myodbc_version}

%build
./configure \
	--prefix=${RPM_BUILD_ROOT}/usr/local \
	--with-iodbc=/usr/local
make

%clean 
rm -rf $RPM_BUILD_ROOT

%install
make PREFIX=$RPM_BUILD_ROOT install

find ${RPM_BUILD_ROOT}/usr/local -type f -print | sed "s@^${RPM_BUILD_ROOT}@@g" > myodbc-filelist
find ${RPM_BUILD_ROOT}/usr/local -type l -print | sed "s@^${RPM_BUILD_ROOT}@@g" >> myodbc-filelist

%files -f myodbc-filelist
%defattr(-,root,root)

%doc INSTALL
%doc ChangeLog
%doc odbc.ini
