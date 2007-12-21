%define major	1
%define libname %mklibname %{name} %{major}

%define epoch	1

Summary:	Portable Windows Library
Name:		pwlib
Version:	1.10.10
Release:	%mkrel 2
License:	GPL
Group:		System/Libraries
URL:		http://www.openh323.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0:		pwlib-1.8.0-libname.diff
Patch1:		pwlib-1.8.0-fix-libpt.so-symlink.diff
Patch2:		pwlib-1.9.2-lib64.patch

BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf2.5 
BuildRequires:	bison
BuildRequires:  expat-devel
BuildRequires:	flex
BuildRequires:	gcc-c++
BuildRequires:	libavc1394-devel
%if %mdkversion >= 200710
BuildRequires:  dc1394-devel >= 0.9.5
%else
BuildRequires:  libdc1394-devel = 1.2.1
%endif
BuildRequires:	libdv-devel
BuildRequires:	libraw1394-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	SDL-devel
BuildRequires:	sed
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildConflicts: libdc1394-devel >= 2.0.0

Epoch:		%epoch

%description
PWLib is a moderately large class library that has its genesis many
years ago asa method to product applications to run on both Microsoft
Windows and Unix X-Window systems. It also was to have a Macintosh
port as well but this never eventeated. Unfortunately this package
contains no GUI code.

%package -n	%{libname}
Summary:	Portable Windows Libary
Group:		System/Libraries
Provides:	%{name}%{major} = %{version}-%{release}
Obsoletes:	%{name}%{major}
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}
Requires:	%{libname}-plugins >= %{epoch}:%{version}-%{release}

%description -n	%{libname}
PWLib is a moderately large class library that has its genesis many
years ago asa method to product applications to run on both Microsoft
Windows and Unix X-Window systems. It also was to have a Macintosh
port as well but this never eventuated.  Unfortunately this package
contains no GUI code.

%package -n	%{libname}-devel
Summary:	Portable Windows Libary development files
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{name}%{major}-devel = %{version}-%{release}
Obsoletes:	%{name}%{major}-devel
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{libname}-devel
Header files and libraries for developing applications that use pwlib.

%package -n	%{libname}-plugins
Summary:	Main plugins for pwlib
Group:		System/Libraries
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-plugins = %{version}-%{release}
Obsoletes:	%{libname}-plugins-alsa 
Provides:	lib%{name}-plugins-alsa = %{version}-%{release}
Provides:	%{libname}-plugins-alsa = %{version}-%{release}
Provides:	%{name}-plugins-alsa = %{version}-%{release}
Obsoletes:	%{libname}-plugins-oss
Provides:	%{libname}-plugins-oss = %{version}-%{release}
Provides:	lib%{name}-plugins-oss = %{version}-%{release}
Provides:	%{name}-plugins-oss = %{version}-%{release}
Obsoletes:	%{libname}-plugins-v4l 
Provides:	%{libname}-plugins-v4l = %{version}-%{release}
Provides:	lib%{name}-plugins-v4l = %{version}-%{release}
Provides:	%{name}-plugins-v4l = %{version}-%{release}
Obsoletes:	%{libname}-plugins-v4l2
Provides:	%{libname}-plugins-v4l2 = %{version}-%{release}
Provides:	lib%{name}-plugins-v4l2 = %{version}-%{release}
Provides:	%{name}-plugins-v4l2 = %{version}-%{release}

%description -n	%{libname}-plugins
This package contains the oss, alsa, v4l1 and v4l2 plugins for pwlib

%package -n	%{libname}-plugins-dc
Summary:	Dc plugin for pwlib
Group:		System/Libraries
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-plugins-dc = %{version}-%{release}
Provides:	%{name}-plugins-dc = %{version}-%{release}

%description -n	%{libname}-plugins-dc
This package contains the dc plugin for pwlib

%package -n	%{libname}-plugins-avc
Summary:	AVC plugin for pwlib
Group:		System/Libraries
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{name}%{major}-plugins-avc = %{version}-%{release}
Obsoletes:	%{name}%{major}-plugins-avc
Provides:	lib%{name}-plugins-avc = %{version}-%{release}
Provides:	%{name}-plugins-avc = %{version}-%{release}

%description -n	%{libname}-plugins-avc
This package contains the AVC plugin for pwlib

%prep

%setup -q

%patch0 -p0 -b .libname
%patch1 -p0 -b .libptsymlink
%patch2 -p1 -b .lib64

#needed by patch2
autoconf

%build

%configure2_5x \
%if %mdkversion >= 1020
    --enable-v4l2 \
%endif
    --enable-plugins

%make OPTCCFLAGS="" RPM_OPT_FLAGS=""

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

%if %mdkversion >= 1020
%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/ptbuildopts.h
%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/ptlib/pluginmgr.h
%endif

#fix PWLIBDIR
perl -pi -e 's|(PWLIBDIR.*)=.*|\1= %{_datadir}/pwlib|' %{buildroot}%{_datadir}/pwlib/make/ptbuildopts.mak

#fix doc perms
chmod a+r *.txt

#remove unpackaged files
rm -f %{buildroot}%{_datadir}/pwlib/make/*.{pat,in,lib64,libname,pwlibdir,includesdir}

# fix ptlib-config
install -d %{buildroot}%{_bindir}
ln -snf %{_datadir}/pwlib/make/ptlib-config %{buildroot}%{_bindir}/ptlib-config

# fix strange perms
find %{buildroot} -type d -perm 0700 -exec chmod 755 {} \;
find %{buildroot} -type f -perm 0555 -exec chmod 755 {} \;
find %{buildroot} -type f -perm 0444 -exec chmod 644 {} \;
find %{buildroot}%{_libdir} -type f -name '*.so*' -exec chmod 755 {} \;

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc *.txt
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/ptlib-config
%attr(0755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_datadir}/pwlib

%files -n %{libname}-plugins
%defattr(-,root,root)
%dir %{_libdir}/pwlib
%dir %{_libdir}/pwlib/devices
%dir %{_libdir}/pwlib/devices/sound
%dir %{_libdir}/pwlib/devices/videoinput
%attr(0755,root,root) %{_libdir}/pwlib/devices/sound/alsa_pwplugin.so
%attr(0755,root,root) %{_libdir}/pwlib/devices/sound/oss_pwplugin.so
%attr(0755,root,root) %{_libdir}/pwlib/devices/videoinput/v4l_pwplugin.so
%if %mdkversion >= 1020
%attr(0755,root,root) %{_libdir}/pwlib/devices/videoinput/v4l2_pwplugin.so
%endif

%files -n %{libname}-plugins-dc
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/pwlib/devices/videoinput/dc_pwplugin.so

%files -n %{libname}-plugins-avc
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/pwlib/devices/videoinput/avc_pwplugin.so
