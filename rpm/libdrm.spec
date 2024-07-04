%define bcond_meson() %{lua: do
  local option = rpm.expand("%{1}")
  local with = rpm.expand("%{?with_" .. option .. "}")
  local value = (with ~= '') and "enabled" or "disabled"
  option = option:gsub('_', '-')
  print(string.format("-D%s=%s", option, value))
end}

%define bcond_meson_bool() %{lua: do
  local option = rpm.expand("%{1}")
  local with = rpm.expand("%{?with_" .. option .. "}")
  local value = (with ~= '') and "true" or "false"
  option = option:gsub('_', '-')
  print(string.format("-D%s=%s", option, value))
end}

%ifarch %{ix86} x86_64
%bcond_without intel
%else
%bcond_with    intel
%endif
%bcond_without radeon
%bcond_without amdgpu
%bcond_without nouveau
%bcond_without vmwgfx
%ifarch %{arm}
%bcond_without omap
%else
%bcond_with    omap
%endif
%ifarch %{arm} aarch64
#let's enable when we need to support them
%bcond_with    exynos
%bcond_with    freedreno
%bcond_with    tegra
%bcond_with    vc4
%bcond_with    etnaviv
%else
%bcond_with    exynos
%bcond_with    freedreno
%bcond_with    tegra
%bcond_with    vc4
%bcond_with    etnaviv
%endif
%bcond_with    cairo_tests
%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with    valgrind
%endif
%bcond_with    freedreno_kgsl
%bcond_with    install_test_programs
%bcond_without udev
%bcond_with    man_pages

Name:       libdrm
Summary:    Direct Rendering Manager runtime library
Version:    2.4.122
Release:    1
License:    MIT
URL:        https://dri.freedesktop.org/wiki/
Source0:    %{name}-%{version}.tar.bz2
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  meson >= 0.43
BuildRequires:  gcc
BuildRequires:  libatomic_ops-devel
BuildRequires:  kernel-headers
%if %{with intel}
BuildRequires:  pkgconfig(pciaccess) >= 0.10
%endif
%if %{with cairo_tests}
BuildRequires:  pkgconfig(cairo)
%endif
%if %{with man_pages}
BuildRequires:  %{_bindir}/xsltproc
BuildRequires:  %{_bindir}/sed
BuildRequires:  docbook-style-xsl
%endif
%if %{with valgrind}
BuildRequires:  valgrind-devel
%endif
%if %{with udev}
BuildRequires:  pkgconfig(udev)
%endif


%description
%{summary}

%if %{with omap}
%package omap
Summary:    Direct Rendering Manager omap api
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description omap
%{summary}.
%endif

%package radeon
Summary:    Direct Rendering Manager radeon api
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description radeon
%{summary}.


%package nouveau
Summary:    Direct Rendering Manager nouveau api
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description nouveau
%{summary}.

%package amdgpu
Summary:    Direct Rendering Manager amdgpu api
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description amdgpu
%{summary}.


%ifarch %{ix86} x86_64
%package intel
Summary:    Direct Rendering Manager intel api
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description intel
%{summary}.
%endif


%package devel
Summary:    Direct Rendering Manager development package
Requires:   %{name} = %{version}-%{release}
%if %{with omap}
Requires:   %{name}-omap = %{version}-%{release}
%endif
Requires:   %{name}-radeon = %{version}-%{release}
Requires:   %{name}-nouveau = %{version}-%{release}
%ifarch %{ix86} x86_64
Requires:   %{name}-intel = %{version}-%{release}
%endif
Requires:   kernel-headers

%description devel
%{summary}.

%if %{with install_test_programs}
%package -n drm-utils
Summary:        Direct Rendering Manager utilities
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n drm-utils
Utility programs for the kernel DRM interface.  Will void your warranty.
%endif


%prep
%autosetup -n %{name}-%{version}/upstream

%build
%meson \
  %{bcond_meson intel} \
  %{bcond_meson radeon} \
  %{bcond_meson amdgpu} \
  %{bcond_meson nouveau} \
  %{bcond_meson vmwgfx} \
  %{bcond_meson omap} \
  %{bcond_meson exynos} \
  %{bcond_meson freedreno}\
  %{bcond_meson tegra} \
  %{bcond_meson vc4} \
  %{bcond_meson etnaviv} \
  %{bcond_meson cairo_tests} \
  %{bcond_meson man_pages} \
  %{bcond_meson valgrind} \
  %{bcond_meson_bool freedreno_kgsl} \
  %{bcond_meson_bool install_test_programs} \
  %{bcond_meson_bool udev} \
  %{nil}
%meson_build

%install
%meson_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%if %{with omap}
%post omap -p /sbin/ldconfig

%postun omap -p /sbin/ldconfig
%endif

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
%{_libdir}/libdrm.so.2
%{_libdir}/libdrm.so.2.4.0
%dir %{_datadir}/libdrm

%if %{with omap}
%files omap
%{_libdir}/libdrm_omap.so.1
%{_libdir}/libdrm_omap.so.1.0.0
%endif

%files radeon
%{_libdir}/libdrm_radeon.so.*

%files nouveau
%{_libdir}/libdrm_nouveau.so.*

%files amdgpu
%{_libdir}/libdrm_amdgpu.so.*
%{_datadir}/libdrm/amdgpu.ids

%ifarch %{ix86} x86_64
%files intel
%{_libdir}/libdrm_intel.so.*
%endif

%files devel
%dir %{_includedir}/libdrm
%{_includedir}/libdrm/drm.h
%{_includedir}/libdrm/drm_fourcc.h
%{_includedir}/libdrm/drm_mode.h
%{_includedir}/libdrm/drm_sarea.h
%{_includedir}/libdrm/*_drm.h
%{_libdir}/libdrm.so
%{_libdir}/pkgconfig/libdrm.pc
%if %{with intel}
%{_includedir}/libdrm/intel_*.h
%{_libdir}/libdrm_intel.so
%{_libdir}/pkgconfig/libdrm_intel.pc
%endif
%if %{with radeon}
%{_includedir}/libdrm/radeon_*.h
%{_includedir}/libdrm/r600_pci_ids.h
%{_libdir}/libdrm_radeon.so
%{_libdir}/pkgconfig/libdrm_radeon.pc
%endif
%if %{with amdgpu}
%{_includedir}/libdrm/amdgpu.h
%{_libdir}/libdrm_amdgpu.so
%{_libdir}/pkgconfig/libdrm_amdgpu.pc
%endif
%if %{with nouveau}
%{_includedir}/libdrm/nouveau/
%{_libdir}/libdrm_nouveau.so
%{_libdir}/pkgconfig/libdrm_nouveau.pc
%endif
%if %{with omap}
%{_includedir}/libdrm/omap_*.h
%{_includedir}/omap/
%{_libdir}/libdrm_omap.so
%{_libdir}/pkgconfig/libdrm_omap.pc
%endif
%if %{with exynos}
%{_includedir}/libdrm/exynos_*.h
%{_includedir}/exynos/
%{_libdir}/libdrm_exynos.so
%{_libdir}/pkgconfig/libdrm_exynos.pc
%endif
%if %{with freedreno}
%{_includedir}/freedreno/
%{_libdir}/libdrm_freedreno.so
%{_libdir}/pkgconfig/libdrm_freedreno.pc
%endif
%if %{with tegra}
%{_includedir}/libdrm/tegra.h
%{_libdir}/libdrm_tegra.so
%{_libdir}/pkgconfig/libdrm_tegra.pc
%endif
%if %{with vc4}
%{_includedir}/libdrm/vc4_*.h
%{_libdir}/pkgconfig/libdrm_vc4.pc
%endif
%if %{with etnaviv}
%{_includedir}/libdrm/etnaviv_*.h
%{_libdir}/libdrm_etnaviv.so
%{_libdir}/pkgconfig/libdrm_etnaviv.pc
%endif
%{_includedir}/libsync.h
%{_includedir}/xf86drm.h
%{_includedir}/xf86drmMode.h
%if %{with man_pages}
%{_mandir}/man3/drm*.3*
%{_mandir}/man7/drm*.7*
%endif

%if %{with install_test_programs}
%files -n drm-utils
%if %{with amdgpu}
%{_bindir}/amdgpu_stress
%endif
%{_bindir}/drmdevice
%if %{with etnaviv}
%exclude %{_bindir}/etnaviv_*
%exclude %{_bindir}/exynos_*
%endif
%{_bindir}/modeprint
%{_bindir}/modetest
%{_bindir}/proptest
%{_bindir}/vbltest
%endif
