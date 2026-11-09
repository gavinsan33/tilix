# Based on the Fedora tilix package spec
%global gtkd_version 3.11.0

# Package notes writer does not support the gold linker, used for D packages.
# See rhbz: 2043178, 2064996
%undefine _package_note_file

# ldc doesn't support -specs=... in LDFLAGS
%undefine _annotated_build
%undefine _hardened_build

Name:           tilix
# snapshot (commit count + hash) is prepended by .copr/Makefile
Version:        1.9.7^%{?snapshot}%{!?snapshot:0}
Release:        1%{?dist}
Summary:        Tiling terminal emulator

# The tilix source code is MPL-2.0,
# source/gx/gtk/x11.d is GPL-2.0-or-later,
# source/secret is LGPL-3.0-or-later,
# source/x11 is LGPL-3.0-only
# data/gsettings/com.gexperts.Tilix.gschema.xml is GPL-3.0-or-later
# data/scripts/tilix_int.sh is GPL-3.0-or-later
# data/icons are LGPL-3.0-or-later OR CC-BY-SA-3.0.
# This makes the combined license:
License:        MPL-2.0 AND GPL-2.0-or-later AND LGPL-3.0-or-later AND LGPL-3.0-only AND GPL-3.0-or-later AND (LGPL-3.0-or-later OR CC-BY-SA-3.0)
URL:            https://github.com/gavinsan33/tilix
Source0:        tilix.tar.gz

ExclusiveArch:  %{ldc_arches}

BuildRequires:  gettext-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  glib2-devel
BuildRequires:  ldc
BuildRequires:  meson
BuildRequires:  pkgconfig(gtkd-3) >= %{gtkd_version}
BuildRequires:  pkgconfig(vted-3) >= %{gtkd_version}
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(libunwind)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  /usr/bin/appstreamcli
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/desktop-file-validate
BuildRequires:  /usr/bin/po4a-translate

# For directory ownership
Requires:       dbus
Requires:       hicolor-icon-theme

Requires:       gtkd%{?_isa} >= %{gtkd_version}

%description
Fork of Tilix (gavinsan33/tilix) with session drag-to-split and custom keybindings.

Tilix is a tiling terminal emulator with the following features:

 - Layout terminals in any fashion by splitting them horizontally or vertically
 - Terminals can be re-arranged using drag and drop both within and between
   windows
 - Terminals can be detached into a new window via drag and drop
 - Input can be synchronized between terminals so commands typed in one
   terminal are replicated to the others
 - The grouping of terminals can be saved and loaded from disk
 - Terminals support custom titles
 - Color schemes are stored in files and custom color schemes can be created by
   simply creating a new file
 - Transparent background
 - Supports notifications when processes are completed out of view

The application was written using GTK 3 and an effort was made to conform to
GNOME Human Interface Guidelines (HIG).


%package        nautilus
Summary:        Tilix extension for Nautilus
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       nautilus-python%{?_isa}

%description    nautilus
This package provides a Nautilus extension that adds the 'Open in Tilix'
option to the right-click context menu in Nautilus.


%prep
%autosetup -n tilix


%build
export DFLAGS="%{_d_optflags} --allinst"
%meson
%meson_build

# Rename license files so that we can include them in %%license
cp -a data/icons/LICENSE LICENSE-data-icons
cp -a source/x11/LICENSE LICENSE-source-x11


%install
%meson_install

%find_lang tilix --with-man


%check
%meson_test

appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/metainfo/com.gexperts.Tilix.appdata.xml
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/com.gexperts.Tilix.desktop


%files -f tilix.lang
%license LICENSE*
%doc README.md
%{_bindir}/tilix
%{_datadir}/applications/com.gexperts.Tilix.desktop
%{_datadir}/dbus-1/services/com.gexperts.Tilix.service
%{_datadir}/glib-2.0/schemas/com.gexperts.Tilix.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/com.gexperts.Tilix.svg
%{_datadir}/icons/hicolor/symbolic/apps/com.gexperts.Tilix-symbolic.svg
%{_datadir}/metainfo/com.gexperts.Tilix.appdata.xml
%{_datadir}/tilix/
%{_mandir}/man1/tilix.1*

%files nautilus
%{_datadir}/nautilus-python/extensions/open-tilix.py*


%changelog
* Mon Nov 09 2026 Gavin Sanders <gavinsan33@gmail.com> - 1.9.7^0-1
- Fork snapshot build for COPR
