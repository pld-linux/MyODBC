Name:		MyODBC
Summary:	MyODBC: an ODBC driver for MySQL
Summary(pl):	MyODBC: driver ODBC dla MySQL
Group:		Applications/Databases
Group(de):	Applikationen/Dateibanken
Group(pl):	Aplikacje/Bazy danych
Version:	2.50.37
Release:	1
License:	Public Domain
Source0:	http://www.mysql.com/Downloads/MyODBC/%{name}-%{version}.tar.gz
URL:		http://www.mysql.com/
Vendor:		MySQL AB
BuildRequires:	unixODBC-devel
BuildRequires:	mysql-devel >= 3.23.38-2
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MyODBC: an ODBC driver for MySQL.

%description -l pl
MyODBC: driver ODBC dla MySQL.

%prep
%setup -q

%build
rm -f missing
libtoolize --copy --force
aclocal
automake -a -c -i
autoconf
autoheader
%configure \
	--with-unixODBC=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

gzip -9fn INSTALL ChangeLog

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(644,root,root,755)
%doc {INSTALL,ChangeLog}.gz
%attr(755,root,root) %{_libdir}/libmyodbc*
