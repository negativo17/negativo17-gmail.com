%global appstream_id com.libretro.%{name}

Name:           RetroArch
Epoch:          1
Version:        1.12.0
Release:        1%{?dist}
Summary:        Cross-platform, sophisticated frontend for the libretro API
License:        GPLv3+ and GPLv2 and CC-BY and CC0 and BSD and ASL 2.0 and MIT
URL:            https://www.libretro.com/

Source0:        https://github.com/libretro/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  lua-devel
BuildRequires:  mbedtls-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  mesa-libOSMesa-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(caca)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(jack) >= 0.120.1
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libavcodec) >= 57
BuildRequires:  pkgconfig(libavdevice) >= 57
BuildRequires:  pkgconfig(libavformat) >= 57
BuildRequires:  pkgconfig(libavutil) >= 55
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libswresample) >= 2
BuildRequires:  pkgconfig(libswscale) >= 4
BuildRequires:  pkgconfig(libusb-1.0) >= 1.0.13
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(Qt5Concurrent) >= 5.2
BuildRequires:  pkgconfig(Qt5Core) >= 5.2
BuildRequires:  pkgconfig(Qt5Gui) >= 5.2
BuildRequires:  pkgconfig(Qt5Network) >= 5.2
BuildRequires:  pkgconfig(Qt5Widgets) >= 5.2
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-egl) >= 10.1.0
BuildRequires:  pkgconfig(wayland-cursor) >= 1.12
BuildRequires:  pkgconfig(wayland-protocols) >= 1.15
BuildRequires:  pkgconfig(wayland-scanner) >= 1.15
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  systemd-devel

%if 0%{?fedora}
BuildRequires:  pkgconfig(check) >= 0.15
BuildRequires:  pkgconfig(libdecor-0)
%endif

# Required at runtime:
Requires:       perl(Net::DBus)
Requires:       perl(X11::Protocol)

Provides:       bundled(7zip) = 9.20
Provides:       bundled(discord-rpc)
Provides:       bundled(dr)
# Fails with undefined references with packaged glslang:
Provides:       bundled(glslang)
Provides:       bundled(ibxm)
# https://github.com/libretro/RetroArch/issues/8153:
Provides:       bundled(lua)
Provides:       bundled(rcheevos) = 7.0.2
Provides:       bundled(SPIRV-Cross)
Provides:       bundled(stb)

# Lowercase provide
Obsoletes:      retroarch <= %{epoch}:%{version}-%{release}
Provides:       retroarch == %{epoch}:%{version}-%{release}
Obsoletes:      retroarch-assets <= %{epoch}:%{version}-%{release}
Provides:       retroarch-assets == %{epoch}:%{version}-%{release}
Obsoletes:      retroarch-database <= %{epoch}:%{version}-%{release}
Provides:       retroarch-database == %{epoch}:%{version}-%{release}
Obsoletes:      retroarch-filters <= %{epoch}:%{version}-%{release}
Provides:       retroarch-filters == %{epoch}:%{version}-%{release}

%description
libretro is an API that exposes generic audio/video/input callbacks. A frontend
for libretro (such as %{name}) handles video output, audio output, input and
application lifecycle. A libretro core written in portable C or C++ can run
seamlessly on many platforms with very little to no porting effort.

While %{name} is the reference frontend for libretro, several other projects
have used the libretro interface to include support for emulators and/or game
engines. libretro is completely open and free for anyone to use.

%prep
%autosetup -p1

# Remove bundles
pushd deps
rm -rf \
  libfat \
  libFLAC \
  libiosuhax \
  libvita2d \
  libz \
  mbdetls \
  miniupnpc \
  peglib \
  pthreads \
  wayland-protocols
popd

%build
%set_build_flags
# Not an autotools configure script:
./configure \
    --disable-builtinflac \
    --disable-builtinmbedtls \
    --disable-builtinzlib \
    --disable-cg \
    --disable-opengl_core \
    --enable-al \
    --enable-alsa \
    --enable-blissbox \
    --enable-builtinglslang \
    --enable-caca \
    --enable-cdrom \
    --enable-crtswitchres \
    --enable-dbus \
    --enable-dylib \
    --enable-dynamic_egl \
    --enable-egl \
    --enable-ffmpeg \
    --enable-flac \
    --enable-freetype \
    --enable-hid \
    --enable-jack \
    --enable-kms \
    --enable-libusb \
    --enable-lua \
    --enable-materialui \
    --enable-mmap \
    --enable-memfd_create \
    --enable-networkgamepad \
    --enable-networking \
    --enable-nvda \
    --enable-ozone \
    --enable-parport \
    --enable-plain_drm \
    --enable-pulse \
    --enable-qt \
    --enable-rgui \
    --enable-sdl2 \
    --enable-slang \
    --enable-spirv_cross \
    --enable-ssa \
    --enable-ssl \
    --enable-systemd \
    --enable-threads \
    --enable-thread_storage \
    --enable-udev \
    --enable-v4l2 \
    --enable-videoprocessor \
    --enable-vulkan \
    --enable-wayland \
    --enable-wifi \
    --enable-x11 \
    --enable-xinerama \
    --enable-xmb \
    --enable-xrandr \
    --enable-xshm \
    --enable-xvideo \
    --enable-zlib \
    --prefix=%{_prefix} \
%if 0%{?fedora}
    --enable-check \
    --enable-libdecor
%endif

%make_build

%install
%make_install

# Let RPM pick up docs in the files section
rm -fr %{buildroot}%{_docdir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/retroarch.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appstream_id}.appdata.xml

%files
%license COPYING
%doc CHANGES.md CONTRIBUTING.md README-exynos.md README-mali_fbdev_r4p0.md README.md README-OMAP.md
%{_bindir}/retroarch
%{_bindir}/retroarch-cg2glsl
%{_datadir}/applications/retroarch.desktop
%{_datadir}/pixmaps/retroarch.svg
%{_mandir}/man6/retroarch.6*
%{_mandir}/man6/retroarch-cg2glsl.6*
%{_metainfodir}/%{appstream_id}.appdata.xml
%config %{_sysconfdir}/retroarch.cfg

%changelog
* Tue Oct 25 2022 Simone Caronni <negativo17@gmail.com> - 1:1.12.0-1
- Update to 1.12.0.

* Wed Oct 05 2022 Simone Caronni <negativo17@gmail.com> - 1:1.11.1-1
- Update to 1.11.1.

* Sun Sep 25 2022 Simone Caronni <negativo17@gmail.com> - 1:1.10.3-2
- Update build requirements.

* Sun Apr 17 2022 Simone Caronni <negativo17@gmail.com> - 1:1.10.3-1
- Update to 1.10.3.

* Fri Apr 08 2022 Simone Caronni <negativo17@gmail.com> - 1:1.10.2-1
- Update to 1.10.2.

* Thu Dec 09 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.14-1
- Update to 1.9.14.

* Wed Nov 24 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.13.2-1
- Update to 1.9.13.2.

* Thu Nov 11 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.13.1-1
- Update to 1.9.13.1.
- Fix build on aarch64.

* Sun Nov 07 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.13-1
- Update to 1.9.13.

* Wed Oct 13 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.11-1
- Update to 1.9.11.

* Fri Sep 24 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.10-1
- Update to 1.9.10.

* Mon Sep 06 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.9-1
- Update to 1.9.9.

* Sun Aug 29 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.8-1
- Update to 1.9.8.

* Tue Aug 10 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.7-1
- Update to 1.9.7.
- Obsolete/provide Fedora's main packages.

* Thu Apr 22 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.1-1
- Update to 1.9.1.

* Fri Jan  8 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.0-1
- Update to 1.9.0.
- Revamp build.

* Mon Jun 15 2020 Simone Caronni <negativo17@gmail.com> - 1.8.8-1
- Update to 1.8.8.

* Sun Mar 29 2020 Simone Caronni <negativo17@gmail.com> - 1.8.5-1
- First build, pick some stuff from RPMFusion.
