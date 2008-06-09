%define name bioapi
%define version 1.2.2
%define release %mkrel 2
%define major 1
%define libname %mklibname %name %{major}

Summary: The BioAPI reference implementation 
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://www.qrivy.net/~michael/blua/bioapi/%{name}-%{version}.tar.bz2
Source1: http://www.qrivy.net/~michael/blua/bioapi/bioapi-errors.html
Source2: fingerprint.rules
Patch0: bioapi-c++.patch.bz2
License: BSD
Group: Sciences/Other 
Url: http://www.qrivy.net/~michael/blua/bioapi/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:       %{libname} = %{version}-%{release}, udev, qt3-common
Buildrequires: qt3-devel

%description
This package contains the BioAPI reference implementation for Unix-based
platforms (in particular Linux and Solaris). The Unix-based reference
implementation was developed by the Convergent Information Division (CISD),
Information Technology Laboratory (ITL) of the National Institute of Standards
and Technology (NIST). The Unix-based reference implementation is based
directly on the BioAPI Consortium's Windows reference implementation and the
Common Data Security Architecture (CDSA) reference implementation. The
Unix-based reference implementation includes the Sample application and the
MdsEdit utility from code provided by the International Biometric Group
(IBG). Although this distribution has only been tested on Linux and Solaris,it
is anticipated that porting it to other Unix-based platforms should be fairly
straight-forward.

%package -n %{libname}
Summary:        Bioapi libraries
Group:          System/Libraries
Provides:       libbioapi

%description -n %{libname}
This package contains the bioapi libraries

%package -n %{libname}-devel
Summary:        Bioapi Development files
Group:          Development/C
Provides:       libbioapi-devel
Requires:       %{libname} = %{version}-%{release}

%description -n %{libname}-devel
This package contains the development files for bioapi
 
%prep
%setup -q
%patch0 -p1
cp %SOURCE1 .

%build
%configure 
%make

%install
rm -rf $RPM_BUILD_ROOT
# /var/lib/bioapi is created by the rpm
# mds_install will be called on post and will install some files in this directory
mkdir -p $RPM_BUILD_ROOT/%{_var}/lib/%{name}/
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/port
#mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/udev/rules.d/
#install -m 644 %SOURCE2 $RPM_BUILD_ROOT/%{_sysconfdir}/udev/rules.d/
%makeinstall
install -m 644 imports/cdsa/v2_0/inc/port/*.h $RPM_BUILD_ROOT/%{_includedir}/port
install -m 644 imports/cdsa/v2_0/inc/*.h $RPM_BUILD_ROOT/%{_includedir}/
install -m 644 include/port/* $RPM_BUILD_ROOT/%{_includedir}/port
install -m 644 include/*.h $RPM_BUILD_ROOT/%{_includedir}/
pushd addins/qtpwbsp
%makeinstall
popd

%clean
rm -rf $RPM_BUILD_ROOT

#%pre
#%_pre_useradd bioapi
#%_pre_groupadd usbfs

#%postun
#%_postun_userdel bioapi
#%_postun_groupdel usbfs 

%post
%{_bindir}/mds_install -s %{_libdir}
%{_bindir}/mod_install -fi %{_libdir}/libbioapi100.so
%{_bindir}/mod_install -fi %{_libdir}/libbioapi_dummy100.so
%{_bindir}/mod_install -fi %{_libdir}/libqtpwbsp.so
# Reloading usb devices to apply udev rules to the fingerprint reader
#find /sys/devices -name uevent | grep usb | while read u; do echo 1 > $u; done

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc bioapi-errors.html
%{_bindir}/*
%{_var}/lib/%{name}/
#%attr(770,bioapi,usbfs) %{_var}/lib/%{name}/
#%{_sysconfdir}/udev/rules.d

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*
