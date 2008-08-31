#
# Conditional build:
%bcond_with	iodbc	# build with libiodbc instead of unixODBC
#
Summary:	MyODBC: an ODBC driver for MySQL
Summary(pl.UTF-8):	MyODBC: driver ODBC dla MySQL
Name:		MyODBC
Version:	3.51.23
Release:	1
License:	GPL v2+ + MySQL FLOSS Exception
Vendor:		MySQL AB
Group:		Libraries
#Source0:	http://www.mysql.com/Downloads/MyODBC/%{name}-%{version}.tar.gz
Source0:	http://sunsite.icm.edu.pl/mysql/Downloads/Connector-ODBC/3.51/mysql-connector-odbc-%{version}r998.tar.gz
# Source0-md5:	74b02e2771529db36f98120f4308f9c9
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
BuildRequires:	qt-devel
Requires(post):	/usr/bin/odbcinst
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MyODBC: an ODBC driver for MySQL.

%description -l pl.UTF-8
MyODBC: sterownik ODBC dla MySQL.

%package qt
Summary:	MyODBC - Qt-based setup library
Summary(pl.UTF-8):	MyODBC - Oparta o Qt biblioteka konfiguracyjna
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description qt
MyODBC - Qt-based setup library.

%description qt -l pl.UTF-8
MyODBC - Oparta o Qt biblioteka konfiguracyjna.

%prep
%setup -q -n mysql-connector-odbc-%{version}r998

%build
%{__libtoolize}
%{__aclocal}
%{__automake} -i
%{__autoconf}
%{__autoheader}
%configure \
	--with-qt-libraries=%{_libdir} \
	--with-qt-dir=/usr \
	--with-qt-includes=/usr/include/qt \
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

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/mysql-connector-odbc

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

%post	qt -p /sbin/ldconfig
%postun	qt -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE.exceptions README
%attr(755,root,root) %{_bindir}/myodbc3*
%attr(755,root,root) %{_libdir}/libmyodbc3-*.so
%attr(755,root,root) %{_libdir}/libmyodbc3.so
%attr(755,root,root) %{_libdir}/libmyodbc3_r-*.so
%attr(755,root,root) %{_libdir}/libmyodbc3_r.so

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmyodbc3S-*.so
%attr(755,root,root) %{_libdir}/libmyodbc3S.so
