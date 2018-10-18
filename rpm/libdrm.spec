Name:       libdrm
Summary:    Direct Rendering Manager runtime library
Version:    2.4.96
Release:    1
Group:      System/Libraries
License:    MIT
URL:        http://dri.sourceforge.net
Source0:    http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.bz2
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(pciaccess) >= 0.10
BuildRequires:  pkgconfig(pthread-stubs)
BuildRequires:  pkgconfig(udev)
BuildRequires:  util-macros

%description
%{summary}

%package omap
Summary:    Direct Rendering Manager omap api
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description omap
%{summary}.


%package radeon
Summary:    Direct Rendering Manager radeon api
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description radeon
%{summary}.


%package nouveau
Summary:    Direct Rendering Manager nouveau api
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description nouveau
%{summary}.

%package amdgpu
Summary:    Direct Rendering Manager amdgpu api
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description amdgpu
%{summary}.


%package nouveau-devel
Summary:    Direct Rendering Manager nouveau api development files
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-nouveau = %{version}-%{release}
%description nouveau-devel
%{summary}.


%ifarch %{ix86} x86_64
%package intel
Summary:    Direct Rendering Manager intel api
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description intel
%{summary}.
%endif


%package devel
Summary:    Direct Rendering Manager development package
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-omap = %{version}-%{release}
Requires:   %{name}-radeon = %{version}-%{release}
Requires:   %{name}-nouveau = %{version}-%{release}
%ifarch %{ix86} x86_64
Requires:   %{name}-intel = %{version}-%{release}
%endif
Requires:   kernel-headers

%description devel
%{summary}.



%prep
%setup -q -n %{name}-%{version}/upstream

%build
unset LD_AS_NEEDED

%reconfigure --disable-static \
    --enable-omap-experimental-api

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post omap -p /sbin/ldconfig

%postun omap -p /sbin/ldconfig

%post radeon -p /sbin/ldconfig

%postun radeon -p /sbin/ldconfig

%post nouveau -p /sbin/ldconfig

%postun nouveau -p /sbin/ldconfig

%post amdgpu -p /sbin/ldconfig

%postun amdgpu -p /sbin/ldconfig


%ifarch %{ix86} x86_64
%post intel -p /sbin/ldconfig

%postun intel -p /sbin/ldconfig

%endif

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/libdrm.so.*
%{_libdir}/libkms.so.*

%files omap
%defattr(-,root,root,-)
%{_libdir}/libdrm_omap.so.*

%files radeon
%defattr(-,root,root,-)
%{_libdir}/libdrm_radeon.so.*

%files nouveau
%defattr(-,root,root,-)
%{_libdir}/libdrm_nouveau.so.*

%files nouveau-devel
%defattr(-,root,root,-)
%{_includedir}/libdrm/nouveau/*.h
%{_includedir}/libdrm/nouveau/nvif/*.h

%files amdgpu
%defattr(-,root,root,-)
%{_libdir}/libdrm_amdgpu.so.*
%{_datadir}/libdrm/amdgpu.ids

%ifarch %{ix86} x86_64
%files intel
%defattr(-,root,root,-)
%{_libdir}/libdrm_intel.so.*
%endif

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/libdrm
%{_includedir}/omap/omap_drm.h
%{_includedir}/libdrm/*.h
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libkms/*.h
