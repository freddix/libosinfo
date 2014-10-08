Summary:	A library for managing OS information for virtualization
Name:		libosinfo
Version:	0.2.11
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://fedorahosted.org/releases/l/i/libosinfo/%{name}-%{version}.tar.gz
# Source0-md5:	acfcddc6a3f577524fd705947fb5abbc
Patch0:		%{name}-destdir.patch
URL:		https://fedorahosted.org/libosinfo/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	intltool
BuildRequires:	libsoup-gnome-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	pkg-config
BuildRequires:	vala-vapigen
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libosinfo is a library that allows virtualization provisioning tools
to determine the optimal device settings for a hypervisor/operating
system combination.

%package tools
Summary:	libosinfo utilities
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	udev

%description tools
libosinfo utilities.

%package devel
Summary:	Header files for libosinfo library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libosinfo library.

%package apidocs
Summary:	libosinfo API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for libosinfo library.

%prep
%setup -q
#%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static	\
	--enable-udev		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	UDEV_RULESDIR="%{_prefix}/lib/udev/rules.d"

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	tools -p /usr/sbin/ldconfig
%postun	tools -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %ghost %{_libdir}/libosinfo-1.0.so.0
%attr(755,root,root) %{_libdir}/libosinfo-1.0.so.*.*.*
%{_libdir}/girepository-1.0/Libosinfo-1.0.typelib

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/osinfo-db-validate
%attr(755,root,root) %{_bindir}/osinfo-detect
%attr(755,root,root) %{_bindir}/osinfo-install-script
%attr(755,root,root) %{_bindir}/osinfo-query
%{_datadir}/libosinfo
%{_prefix}/lib/udev/rules.d/95-osinfo.rules
%{_mandir}/man1/osinfo-*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libosinfo-1.0.so
%{_datadir}/gir-1.0/Libosinfo-1.0.gir
%{_includedir}/libosinfo-1.0
%{_pkgconfigdir}/libosinfo-1.0.pc
%{_datadir}/vala/vapi/libosinfo-1.0.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/Libosinfo

