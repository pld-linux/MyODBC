#
# Conditional build:
%bcond_with	iodbc	# build with libiodbc instead of unixODBC
#
Summary:	MyODBC: an ODBC driver for MySQL
Summary(pl):	MyODBC: driver ODBC dla MySQL
Name:		MyODBC
Version:	3.51.10
Release:	1
License:	GPL v2+
Vendor:		MySQL AB
Group:		Libraries
#Source0:	http://www.mysql.com/Downloads/MyODBC/%{name}-%{version}.tar.gz
Source0:	ftp://sunsite.icm.edu.pl/pub/unix/mysql/Downloads/MyODBC3/%{name}-%{version}.tar.gz
# Source0-md5:	34334272eb6f60dffc793c9aa3d29154
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

%description -l pl
MyODBC: sterownik ODBC dla MySQL.

%package qt
Summary:	MyODBC - Qt-based setup library
Summary(pl):	MyODBC - Oparta o Qt biblioteka konfiguracyjna
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description qt
MyODBC - Qt-based setup library.

%description qt -l pl
MyODBC - Oparta o Qt biblioteka konfiguracyjna.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__automake} -i
%{__autoconf}
%{__autoheader}
LDFLAGS="%{rpmldflags} -L/usr/X11R6/%{_lib}"
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

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

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
%doc ChangeLog INSTALL README
%attr(755,root,root) %{_libdir}/libmyodbc3-*.so
%attr(755,root,root) %{_libdir}/libmyodbc3.so
%attr(755,root,root) %{_libdir}/libmyodbc3_r-*.so
%attr(755,root,root) %{_libdir}/libmyodbc3_r.so

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmyodbc3S-*.so
%attr(755,root,root) %{_libdir}/libmyodbc3S.so
