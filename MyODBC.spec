# --with iodbs  build with libiodbc not with unixODBC
Summary:	MyODBC: an ODBC driver for MySQL
Summary(pl):	MyODBC: driver ODBC dla MySQL
Name:		MyODBC
Version:	3.51.05
Release:	2
License:	Public Domain
Vendor:		MySQL AB
Group:		Applications/Databases
#Source0:	http://www.mysql.com/Downloads/MyODBC/%{name}-%{version}.tar.gz
Source0:	ftp://sunsite.icm.edu.pl/pub/unix/mysql/Downloads/MyODBC3/%{name}-%{version}.tar.gz
URL:		http://www.mysql.com/
%if %{?_with_iodbc:0}%{!?_with_iodbc:1}
BuildRequires:	unixODBC-devel
%else
BuildRequires:	libiodbc-devel
%endif
BuildRequires:	mysql-devel >= 4.0.10
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MyODBC: an ODBC driver for MySQL.

%description -l pl
MyODBC: sterownik ODBC dla MySQL.

%prep
%setup -q

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__automake} -i
%{__autoconf}
%{__autoheader}
%configure \
	%{!?_with_iodbc:--with-unixODBC=/usr} \
	%{?_with_iodbc:--with-iODBC=/usr --with-odbc-ini=/etc/odbc.ini} 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(644,root,root,755)
%doc INSTALL ChangeLog
%attr(755,root,root) %{_libdir}/libmyodbc*
