# --with iodbs  build with libiodbc not with unixODBC
Summary:	MyODBC: an ODBC driver for MySQL
Summary(pl):	MyODBC: driver ODBC dla MySQL
Name:		MyODBC
Version:	3.51.06
Release:	1
License:	Public Domain
Vendor:		MySQL AB
Group:		Applications/Databases
#Source0:	http://www.mysql.com/Downloads/MyODBC/%{name}-%{version}.tar.gz
Source0:	ftp://sunsite.icm.edu.pl/pub/unix/mysql/Downloads/MyODBC3/%{name}-%{version}.tar.gz
# Source0-md5:	5a59b4f01592fc9ec96e985bc7d6aada
URL:		http://www.mysql.com/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{?_with_iodbc:0}%{!?_with_iodbc:1}
BuildRequires:	unixODBC-devel
%else
BuildRequires:	libiodbc-devel
%endif
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	mysql-devel >= 4.0.10
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL ChangeLog
%attr(755,root,root) %{_libdir}/libmyodbc*
