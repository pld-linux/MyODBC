#
# Conditional build:
%bcond_with	iodbc	# build with libiodbc instead of unixODBC
#
Summary:	MyODBC: an ODBC driver for MySQL
Summary(pl):	MyODBC: driver ODBC dla MySQL
Name:		MyODBC
%define	sver	3.51
Version:	%{sver}.07
Release:	1
License:	Public Domain
Vendor:		MySQL AB
Group:		Applications/Databases
#Source0:	http://www.mysql.com/Downloads/MyODBC/%{name}-%{version}.tar.gz
Source0:	ftp://sunsite.icm.edu.pl/pub/unix/mysql/Downloads/MyODBC3/%{name}-%{version}.tar.gz
# Source0-md5:	80cda1784319505941c56aad5d7ac2a9
URL:		http://www.mysql.com/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with iodbc}
BuildRequires:	libiodbc-devel
%else
BuildRequires:	unixODBC-devel
%endif
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	mysql-devel >= 4.0.10
Requires(post):	/usr/bin/odbcinst
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MyODBC: an ODBC driver for MySQL.

%description -l pl
MyODBC: sterownik ODBC dla MySQL.

%prep
%setup -q -n myodbc-%{sver}

%build
rm -rf autom4te.cache
%{__libtoolize}
%{__aclocal}
%{__automake} -i
%{__autoconf}
%{__autoheader}
%configure \
%if %{with iodbc}
	--with-iODBC=/usr \
	--with-odbc-ini=/etc/odbc.ini
%else
	--with-unixODBC=/usr
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
# install text driver
/usr/bin/odbcinst -i -d -r <<EOF
[MySQL]
Description = ODBC for MySQL
Driver = %{_libdir}/libmyodbc3.so
FileUsage = 1
EOF

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc INSTALL ChangeLog
%attr(755,root,root) %{_libdir}/libmyodbc*
