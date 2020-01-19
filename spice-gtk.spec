%global _hardened_build 1

#define _version_suffix

Name:           spice-gtk
Version:        0.34
Release:        3%{?dist}.2
Summary:        A GTK+ widget for SPICE clients

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.spice-space.org/
#VCS:           git:git://anongit.freedesktop.org/spice/spice-gtk
Source0:        https://www.spice-space.org/download/gtk/%{name}-%{version}%{?_version_suffix}.tar.bz2

Patch0001:      0001-canvas-base-Fix-width-computation-for-palette-images.patch
Patch0002:      0002-Revert-channel-usbredir-Fix-crash-on-channel-up.patch
Patch0003:      0003-channel-usbredir-Fix-crash-on-channel-up.patch
Patch0004:      0004-Fix-flexible-array-buffer-overflow.patch
Patch1000:      1000-gtk-Makefile.am-add-PIE-flags-to-libspice-client-gli.patch

BuildRequires: intltool
BuildRequires: usbredir-devel >= 0.6-8
BuildRequires: libusb1-devel >= 1.0.9
BuildRequires: libgudev1-devel
BuildRequires: pixman-devel openssl-devel libjpeg-turbo-devel
BuildRequires: celt051-devel pulseaudio-libs-devel
BuildRequires: zlib-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libcacard-devel
BuildRequires: gobject-introspection-devel
BuildRequires: dbus-glib-devel
BuildRequires: libacl-devel
BuildRequires: polkit-devel
BuildRequires: gtk-doc
BuildRequires: vala-tools
BuildRequires: usbutils
BuildRequires: libepoxy-devel
BuildRequires: lz4-devel
BuildRequires: gtk3-devel
BuildRequires: gstreamer1-devel gstreamer1-plugins-base-devel
# keep me to get gendeps magic happen
BuildRequires: spice-protocol >= 0.12.12-1
# Hack because of bz #613466
BuildRequires: libtool
BuildRequires: opus-devel
BuildRequires: pyparsing python-six
Requires: spice-glib%{?_isa} = %{version}-%{release}


%description
Client libraries for SPICE desktop servers.

%package -n spice-glib
Summary: A GObject for communicating with Spice servers
Group: Development/Libraries
Requires: usbredir >= 0.6-8

%description -n spice-glib
spice-client-glib-2.0 is a SPICE client library for GLib2.

%package -n spice-glib-devel
Summary: Development files to build Glib2 applications with spice-glib-2.0
Group: Development/Libraries
Requires: spice-glib%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel
Obsoletes: spice-gtk-python < 0.32

%description -n spice-glib-devel
spice-client-glib-2.0 is a SPICE client library for GLib2.

Libraries, includes, etc. to compile with the spice-glib-2.0 libraries

%package -n spice-gtk3
Summary: A GTK3 widget for SPICE clients
Group: Development/Libraries
Requires: spice-glib%{?_isa} = %{version}-%{release}
Obsoletes: spice-gtk < 0.32

%description -n spice-gtk3
spice-client-glib-3.0 is a SPICE client library for Gtk3.

%package -n spice-gtk3-devel
Summary: Development files to build GTK3 applications with spice-gtk-3.0
Group: Development/Libraries
Requires: spice-gtk3%{?_isa} = %{version}-%{release}
Requires: spice-glib-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk3-devel
Obsoletes: spice-gtk-devel < 0.32

%description -n spice-gtk3-devel
spice-client-gtk-3.0 provides a SPICE viewer widget for GTK3.

Libraries, includes, etc. to compile with the spice-gtk3 libraries

%package -n spice-gtk3-vala
Summary: Vala bindings for the spice-gtk-3.0 library
Group: Development/Libraries
Requires: spice-gtk3%{?_isa} = %{version}-%{release}
Requires: spice-gtk3-devel%{?_isa} = %{version}-%{release}

%description -n spice-gtk3-vala
A module allowing use of the spice-gtk-3.0 widget from vala

%package tools
Summary: Spice-gtk tools
Group: Applications/Internet
Requires: spice-gtk3%{?_isa} = %{version}-%{release}
Requires: spice-glib = %{version}-%{release}

%description tools
Simple clients for interacting with SPICE servers.
spicy is a client to a SPICE desktop server.
spicy-screenshot is a tool to capture screen-shots of a SPICE desktop.


%prep
%setup -q -n spice-gtk-%{version}%{?_version_suffix}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch1000 -p1
find . -name '*.stamp' | xargs touch


%build
%configure \
    --with-gtk=3.0 \
    --enable-vala \
    --with-usb-acl-helper-dir=%{_libexecdir}/spice-gtk-%{_arch}/ \
    --enable-lz4 \
    --disable-werror
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la


%find_lang %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n spice-glib -p /sbin/ldconfig
%postun -n spice-glib -p /sbin/ldconfig

%post -n spice-gtk3 -p /sbin/ldconfig
%postun -n spice-gtk3 -p /sbin/ldconfig


%files -n spice-glib -f %{name}.lang
%{_libdir}/libspice-client-glib-2.0.so.*
%{_libdir}/libspice-controller.so.*
%{_libdir}/girepository-1.0/SpiceClientGLib-2.0.typelib
%dir %{_libexecdir}/spice-gtk-%{_arch}/
%attr(4755, root, root) %{_libexecdir}/spice-gtk-%{_arch}/spice-client-glib-usb-acl-helper
%{_datadir}/polkit-1/actions/org.spice-space.lowlevelusbaccess.policy

%files -n spice-glib-devel
%{_libdir}/libspice-client-glib-2.0.so
%{_libdir}/libspice-controller.so
%{_includedir}/spice-client-glib-2.0
%{_includedir}/spice-controller
%{_libdir}/pkgconfig/spice-client-glib-2.0.pc
%{_libdir}/pkgconfig/spice-controller.pc
%{_datadir}/gir-1.0/SpiceClientGLib-2.0.gir
%{_datadir}/vala/vapi/spice-protocol.vapi
%doc %{_datadir}/gtk-doc/html/*

%files -n spice-gtk3
%doc AUTHORS
%doc COPYING
%doc README
%doc NEWS
%{_mandir}/man1/spice-client.1*
%{_libdir}/libspice-client-gtk-3.0.so.*
%{_libdir}/girepository-1.0/SpiceClientGtk-3.0.typelib

%files -n spice-gtk3-devel
%{_libdir}/libspice-client-gtk-3.0.so
%{_includedir}/spice-client-gtk-3.0
%{_libdir}/pkgconfig/spice-client-gtk-3.0.pc
%{_datadir}/gir-1.0/SpiceClientGtk-3.0.gir

%files -n spice-gtk3-vala
%{_datadir}/vala/vapi/spice-client-glib-2.0.deps
%{_datadir}/vala/vapi/spice-client-glib-2.0.vapi
%{_datadir}/vala/vapi/spice-client-gtk-3.0.deps
%{_datadir}/vala/vapi/spice-client-gtk-3.0.vapi

%files tools
%{_bindir}/spicy
%{_bindir}/spicy-screenshot
%{_bindir}/spicy-stats

%changelog
* Thu Aug 09 2018 Frediano Ziglio <fziglio@redhat.com> - 0.34-3.2
- Fix flexible array buffer overflow
  Resolves: rhbz#1596008

* Wed Jun 13 2018 Victor Toso <victortoso@redhat.com> - 0.34-3.1
- Fix migration failure when USB is enabled
  Resolves: rhbz#1590412

* Thu Dec 21 2017 Frediano Ziglio <fziglio@redhat.com> - 0.34-3
- Fix stride misalignment
  Resolves: rhbz#1508847

* Tue Nov 14 2017 Victor Toso <victortoso@redhat.com> - 0.34-2
- Enable lz4
  Resolves: rhbz#1460198

* Tue Sep 12 2017 Victor Toso <victortoso@redhat.com> - 0.34-1
- Rebase to 0.34
  Resolves: rhbz#1472730

* Fri Jul 14 2017 Jonathon Jongsma <jjongsma@redhat.com> - 0.33-7
- build with opus support
  Resolves: rhbz#1456849

* Wed Jun 7 2017 Pavel Grunt <pgrunt@redhat.com> - 0.33-6
- Fix capslock regression
  Resolves: rhbz#1458730

* Thu May 25 2017 Pavel Grunt <pgrunt@redhat.com> - 0.33-5
- Enable hardened build flags
  Resolves: rhbz#1420778

* Wed May 10 2017 Pavel Grunt <pgrunt@redhat.com> - 0.33-4
- Make connection error message more clear
  Resolves: rhbz#1365736
- Improve audio debug
  Resolves: rhbz#1436249
- Fix wrong encoding of transferred files
  Resolves: rhbz#1440206

* Tue Apr 11 2017 Victor Toso <victortoso@redhat.com> - 0.33-3
- Avoid CRITICALs on copy-paste
  Resolves: rhbz#1440096
- Avoid assertions on file-xfer while agent disconnects
  Related: rhbz#1440096

* Mon Mar 27 2017 Pavel Grunt <pgrunt@redhat.com> - 0.33-2
- Add missing patch for rebase
  Resolves: rhbz#1402474
- Add obsoletes to the spec file to ease updates
  Resolves: rhbz#1432776
- Fix black screen in virt-manager
  Resolves: rhbz#1433242
- Make connection error message more clear
  Resolves: rhbz#1365736

* Mon Mar 13 2017 Pavel Grunt <pgrunt@redhat.com> - 0.33-1
- Rebase to 0.33
  Resolves: rhbz#1402474
- Rebuilt with correct hardening flags due to bug 1387475
  Resolves: rhbz#1420778
- Fix copy paste issues
  Resolve: rhbz#1409854

* Mon Dec 12 2016 Pavel Grunt <pgrunt@redhat.com> - 0.31-8
- Fix crash in spicy-stats
  Resolves: rhbz#1403820

* Fri Dec 9 2016 Pavel Grunt <pgrunt@redhat.com> - 0.31-7
- Avoid crash on clipboard due failure in text conversion
  Resolves: rhbz#1385225

* Fri Sep 9 2016 Pavel Grunt <pgrunt@redhat.com> - 0.31-6
- Improve clipboard handling for motif applications
  Resolves: rhbz#1348624

* Wed Aug 3 2016 Pavel Grunt <pgrunt@redhat.com> - 0.31-5
- Allow to connect to ipv6 without proxy
  Resolves: rhbz#1361478
- Silence a critical when migrating
  Resolves: rhbz#1356162
- Disable EPOXY / EGL usage
  Resolves: rhbz#1362460

* Fri Jul 1 2016 Pavel Grunt <pgrunt@redhat.com> - 0.31-4
- Fix SASL GSSAPI (kerberos authentication)
  Resolves: rhbz#1343361
- Allow to connect to ipv6 behind proxy
  Resolves: rhbz#1331777

* Wed Jun 8 2016 Victor Toso <victortoso@redhat.com> - 0.31-3
- Fix client's crash when agent is killed
  Resolves: rhbz#1336321
- Parse ipv6 address
  Resolves: rhbz#1335239
- Improving parsing of Smartcard messages
  Resolves: rhbz#1338727
- Fix hangs with "Connected to graphic server"
  Resolves: rhbz#1323092

* Mon May 2 2016 Pavel Grunt <pgrunt@redhat.com> - 0.31-2
- Rebase to 0.31, add back the PIE/relro patch.
  Resolves: rhbz#1329973

* Mon May 2 2016 Pavel Grunt <pgrunt@redhat.com> - 0.31-1
- Rebase to 0.31
  Resolves: rhbz#1329973
- Fix crash when migration fails
  Resolves: rhbz#1318574

* Mon Apr 18 2016 Pavel Grunt <pgrunt@redhat.com> - 0.26-8
- Check runtime usbredir version
  Resolves: rhbz#1320827
- Allow connection to password protected guests
  Resolves: rhbz#1320806
- Fix runtime warnings related to shared folders and usb redirection
  Resolves: rhbz#1319405
- Change runtime warning for empty monitor config to debug message
  Resolves: rhbz#1319405
- Fix 16 bpp LZ image decompression
  Resolves: rhbz#1285469

* Fri Mar 18 2016 Pavel Grunt <pgrunt@redhat.com> - 0.26-7
- Improve message for number of usb channels in usb device widget
  Resolves: rhbz#1299931
- Fix usbredir leak when redirecting a webcam
  Resolves: rhbz#1270363

* Thu Mar 17 2016 Victor Toso <victortoso@redhat.com> - 0.26-6
- Implements volume-sync from guest to client
  Resolves: rhbz#1264105
- Avoid crash in virt-manager
  Resolves: rhbz#1301863
- Fix focus in fullscreen mode
  Resolves: rhbz#1275231
- Add Client capability for Windows monitor_config message
  Resolves: rhbz#1248189
- Fix error message for file transfer
  Resolves: rhbz#1265562

* Mon Aug 31 2015 Fabiano Fidêncio <fidencio@redhat.com> - 0.26-5
- Connecting to VM changes its resolution
  Resolves: rhbz#1242602
- Cannot enable display 1 when it was disabled in previous session
  Resolves: rhbz#1247907
- Windows needs to send complete monitors_config message to client
  Resolves: rhbz#1244878
- High Resolution Multi-Monitor Windows Guest freeze
  Resolves: rhbz#1235442
- Print file transfer summary to the log
  Resolves: rhbz#1140512
- Enable proxy when requested
  Related: rhbz#1182252

* Thu Jul 9 2015 Fabiano Fidêncio <fidencio@redhat.com> - 0.26-4
- Disable default socket proxy
  Resolves: rhbz#1182252

* Wed May 6 2015 Marc-Andre Lureau <marcandre.lureau@redhat.com> - 0.26-3
- Rebase to 0.26, fix the PIE/relro patch.
  Resolves: rhbz#1214101

* Wed May 6 2015 Marc-Andre Lureau <marcandre.lureau@redhat.com> - 0.26-2
- Rebase to 0.26, add back the PIE/relro patch.
  Resolves: rhbz#1214101

* Tue May 5 2015 Marc-Andre Lureau <marcandre.lureau@redhat.com> - 0.26-1
- Rebase to 0.26
  Resolves: rhbz#1214101
- Allow to transfer multiple files at once
  Resolves: rhbz#1167829
- Fix smartcard cannot work after restart guest
  Resolves: rhbz#1205548

* Fri Sep 12 2014 Jonathon Jongsma <jjongsma@redhat.com> - 0.22-2
- Additional display pop out when restarting service spice-vdagentd in guest
  Resolves: rhbz#1043782
- Coverity scan fixes
  Resolves: rhbz#885719
- Send data message for file copy of 0 size
  Resolves: rhbz#1135104
- add spice_channel_get_error()
  Resolves: rhbz#1116048
- Prefix proxy lookup errors
  Resolves: rhbz#1116048

* Mon Jul  7 2014 Marc-Andre Lureau <marcandre.lureau@redhat.com> - 0.22-1
- Rebase to 0.22
  Resolves: rhbz#1109397
- Fix screenshot of secondary displays
  Resolves: rhbz#1029761
- Fix potential crash when freeing primary surface.
  Resolves: rhbz#1082555
- Add RHEL-only SPICE_NOSCALE to disable display scaling.
  Resolves: rhbz#1067346
- Fix connection to RHEL5 Spice server
  Resolves: rhbz#1017862
- Fix coroutine leak
  Resolves: rhbz#1007841
- Fix clipboard hang on clipboard loop
  Resolves: rhbz#1073364

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.20-8
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.20-7
- Mass rebuild 2013-12-27

* Fri Sep 13 2013 Christophe Fergeau <cfergeau@redhat.com> 0.20-6
- Add patch for CVE-2013-4324

* Fri Sep 13 2013 Hans de Goede <hdegoede@redhat.com> - 0.20-5
- Fix the spice-client-glib-usb-acl-helper no longer being suid root

* Fri Sep 13 2013 Christophe Fergeau <cfergeau@redhat.com> 0.20-4
- Add misc upstream patches fixing various 0.20 bugs

* Wed Aug 28 2013 Alon Levy <alevy@redhat.com> - 0.20-3
- Fix wrong mono cursor local rendering (rhbz#998529)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul  6 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.20-2
- Fix spice_channel_string_to_type symbol visibility (rhbz#981815)

* Wed Jun 26 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.20-1
- Update to spice-gtk 0.20

* Fri Apr 19 2013 Daniel Mach <dmach@redhat.com> - 0.19-1.1
- Rebuild for cyrus-sasl

* Thu Apr 11 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.19-1
- Update to spice-gtk 0.19

* Thu Mar 14 2013 Hans de Goede <hdegoede@redhat.com> - 0.18-2
- Fix "Warning no automount-inhibiting implementation available" warnings

* Wed Feb 13 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.18-1
- Update to spice-gtk 0.18

* Wed Feb  6 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.17-1
- Update to spice-gtk 0.17

* Thu Jan 31 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.16-2
- Remove perl-text-csv build requirement. (rhbz#873174)

* Sat Jan 12 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.16-1
- Update to spice-gtk 0.16

* Mon Dec 31 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.15.3-1
- Update to spice-gtk 0.15.3, fixes TLS & password regressions

* Fri Dec 21 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.15-2
- Update to spice-gtk 0.15

* Thu Oct 25 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-2
- Add various upstream patches

* Fri Sep 21 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-1
- Update to 0.14 release

* Fri Sep 14 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13.29-4
- Add patch fixing CVE 2012-4425

* Thu Sep 13 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13.29-3
- Run autoreconf after applying patch 2 as it only modifies Makefile.am

* Tue Sep 11 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13.29-2
- Add patch to fix symbol versioning

* Fri Sep  7 2012 Hans de Goede <hdegoede@redhat.com> - 0.13.29-1
- Update to the spice-gtk 0.13.29 development release
- Rebuild for new usbredir

* Mon Sep 03 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13-2
- Update to spice-gtk 0.13

* Tue Aug 07 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.12.101-1
- Update to the spice-gtk 0.12.101 development release (needed by Boxes
  3.5.5)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-4
- re-Add back spice-protocol BuildRequires to help some deps magic happen

* Thu May 10 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-3
- Fix Spice.Audio constructor Python binding
  https://bugzilla.redhat.com/show_bug.cgi?id=820335

* Wed May  2 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-2
- Fix virt-manager console not showing up, rhbz#818169

* Tue Apr 24 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-1
- New upstream release 0.12

* Tue Apr 10 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.11-5
- Fix build on PPC
- Remove ExclusiveArch. While spice-gtk will build on ARM and PPC, it
  hasn't been tested on these arch, so there may be some bugs.

* Tue Mar 20 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-4
- Add missing BuildRequires: usbutils, so that we get proper USB device
  descriptions in the USB device selection menu

* Wed Mar 14 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-3
- Fix a crash triggered when trying to view a usbredir enabled vm from
  virt-manager

* Mon Mar 12 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-2
- Add back spice-protocol BuildRequires to help some deps magic happen

* Fri Mar  9 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-1
- New upstream release 0.11
- Fix multilib conflict in spice-glib

* Thu Feb 23 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.10-1
- New upstream release 0.10

* Mon Jan 30 2012 Hans de Goede <hdegoede@redhat.com> - 0.9-1
- New upstream release 0.9

* Mon Jan 16 2012 Hans de Goede <hdegoede@redhat.com> - 0.8-1
- New upstream release 0.8
- Various small specfile improvements
- Enable vala bindings

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> 0.7.39-2
- Rebuild to break bogus libpng dependency
- Fix summaries for gtk3 subpackages to not talk about gtk2

* Fri Sep  2 2011 Hans de Goede <hdegoede@redhat.com> - 0.7.39-1
- Update to git snapshot 0.7.39-ab64, to add usbredir support

* Tue Jul 26 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.1-1
- Upstream version 0.7.1-d5a8 (fix libtool versionning)

* Tue Jul 19 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7-1
- Upstream release 0.7

* Wed May 25 2011 Christophe Fergeau <cfergeau@redhat.com> - 0.6-1
- Upstream release 0.6

* Tue Mar  1 2011 Hans de Goede <hdegoede@redhat.com> - 0.5-6
- Fix spice-glib requires in .pc file (#680314)

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-5
- Fix build against glib 2.28

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-4
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-2
- Rebuild against newer gtk

* Thu Jan 27 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.5-1
- Upstream release 0.5

* Fri Jan 14 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4-2
- Add support for parallel GTK3 build

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> - 0.4-2
- add ExclusiveArch as only x86 is supported

* Sun Jan 09 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.4-1
- Upstream release 0.4
- Initial release (#657403)

* Thu Nov 25 2010 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.1.0-1
- Initial packaging
