# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

#define _version_suffix -f256

Name:           spice-gtk
Version:        0.26
Release:        4%{?dist}
Summary:        A GTK+ widget for SPICE clients

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://spice-space.org/page/Spice-Gtk
Source0:        http://www.spice-space.org/download/gtk/%{name}-%{version}%{?_version_suffix}.tar.bz2
#Patch0001:      patch-name.patch
Patch0001:      0001-smartcard-connect-object-signal-handlers-with-spice-.patch
Patch0002:      0002-smartcard-add-reader-and-cards-on-channel-up.patch
Patch0003:      0003-channel-smartcard-Add-missing-USE_SMARTCARD-checks.patch

BuildRequires: intltool
#New enough glib is needed for proxy support
BuildRequires: glib2-devel >= 2.28
BuildRequires: gtk2-devel >= 2.20.0
BuildRequires: usbredir-devel >= 0.5
BuildRequires: libusb1-devel >= 1.0.9
BuildRequires: libgudev1-devel
BuildRequires: pixman-devel openssl-devel libjpeg-devel
BuildRequires: celt051-devel pulseaudio-libs-devel
BuildRequires: pygtk2-devel python-devel zlib-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libcacard-devel
BuildRequires: libacl-devel
BuildRequires: polkit-devel
BuildRequires: usbutils
# needed for bz 799112
BuildRequires: spice-protocol
# Hack because of bz #613466
BuildRequires: libtool
Requires: spice-glib%{?_isa} = %{version}-%{release}
Requires: gtk2 >= 2.20.0
Requires: glib2 >= 2.28

ExclusiveArch: %{ix86} x86_64

%description
Client libraries for SPICE desktop servers.

%package devel
Summary: Development files to build GTK2 applications with spice-gtk-2.0
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: spice-glib-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk2-devel

%description devel
spice-client-gtk-2.0 provides a SPICE viewer widget for GTK2.

Libraries, includes, etc. to compile with the spice-gtk2 libraries

%package -n spice-glib
Summary: A GObject for communicating with Spice servers
Group: Development/Libraries
# Ensure we have a new enough libusb for usbredir
Requires: libusb1 >= 1.0.9

%description -n spice-glib
spice-client-glib-2.0 is a SPICE client library for GLib2.

%package -n spice-glib-devel
Summary: Development files to build Glib2 applications with spice-glib-2.0
Group: Development/Libraries
Requires: spice-glib%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel
Requires: spice-protocol

%description -n spice-glib-devel
spice-client-glib-2.0 is a SPICE client library for GLib2.

Libraries, includes, etc. to compile with the spice-glib-2.0 libraries

%package python
Summary: Python bindings for the spice-gtk-2.0 library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description python
SpiceClientGtk module provides a SPICE viewer widget for GTK2.

A module allowing use of the spice-gtk-2.0 widget from python

%package tools
Summary: Spice-gtk tools
Group: Applications/Internet
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Simple clients for interacting with SPICE servers.
spicy is a client to a SPICE desktop server.
spicy-screenshot is a tool to capture screen-shots of a SPICE desktop.

%prep
%setup -q -n spice-gtk-%{version}%{?_version_suffix} -c

if [ -n '%{?_version_suffix}' ]; then
  mv spice-gtk-%{version}%{?_version_suffix} spice-gtk-%{version}
fi

pushd spice-gtk-%{version}
#%patch0001 -p1
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1

find . -name '*.stamp' | xargs touch
popd


%build
cd spice-gtk-%{version}
%configure --disable-gtk-doc --with-gtk=2.0 --disable-introspection --enable-pie --with-usb-acl-helper-dir=%{_libexecdir}/spice-gtk-%{_arch}/
make %{?_smp_mflags} LDFLAGS="-Wl,-z,relro -Wl,-z,now" V=1
cd ..

%install
cd spice-gtk-%{version}
make install DESTDIR=%{buildroot} V=1
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.a
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.la
%find_lang %{name}
cd ..

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n spice-glib -p /sbin/ldconfig
%postun -n spice-glib -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc spice-gtk-%{version}/AUTHORS
%doc spice-gtk-%{version}/COPYING
%doc spice-gtk-%{version}/README
%doc spice-gtk-%{version}/NEWS
%{_libdir}/libspice-client-gtk-2.0.so.*
%{_mandir}/man1/spice-client.1*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libspice-client-gtk-2.0.so
%{_includedir}/spice-client-gtk-2.0
%{_libdir}/pkgconfig/spice-client-gtk-2.0.pc

%files -n spice-glib -f spice-gtk-%{version}/%{name}.lang
%defattr(-,root,root,-)
%{_libdir}/libspice-client-glib-2.0.so.*
%{_libdir}/libspice-controller.so.*
%{_libexecdir}/spice-gtk-%{_arch}/spice-client-glib-usb-acl-helper
%{_datadir}/polkit-1/actions/org.spice-space.lowlevelusbaccess.policy

%files -n spice-glib-devel
%defattr(-,root,root,-)
%{_libdir}/libspice-client-glib-2.0.so
%{_libdir}/libspice-controller.so
%{_includedir}/spice-client-glib-2.0
%{_includedir}/spice-controller/*
%{_libdir}/pkgconfig/spice-client-glib-2.0.pc
%{_libdir}/pkgconfig/spice-controller.pc
%{_datadir}/vala/vapi/spice-protocol.vapi
%doc %{_datadir}/gtk-doc/html/*

%files python
%defattr(-,root,root,-)
%{_libdir}/python*/site-packages/SpiceClientGtk.so

%files tools
%defattr(-,root,root,-)
%{_bindir}/spicy
%{_bindir}/spicy-screenshot
%{_bindir}/spicy-stats

%changelog
* Fri Apr 10 2015 Christophe Fergeau <cfergeau@redhat.com> 0.26-4
- Fix smartcard issues after VM restart (virsh destroy/virsh start)
  Resolves: rhbz#1205171
- Remove obsolete patches
  Related: rhbz#1185434

* Fri Feb 27 2015 Christophe Fergeau <cfergeau@redhat.com> 0.26-3
- Add -Wl,-z,now as well to the link flags.  This flag was present in
  1002-gtk-Makefile.am-add-PIE-flags-to-libspice-client-gli.patch, and
  pkgwrangler still complains about:
  File /usr/lib/libspice-client-glib-2.0.so.8.5.0 lost GNU_RELRO security
  protection on i686
  Related: rhbz#1185434

* Thu Feb 26 2015 Christophe Fergeau <cfergeau@redhat.com> 0.26-2
- Add -Wl,-z,relro to the linker flags in order to fix a rpmdiff
  error. These flags used to be provided indirectly by openssl, and after
  openssl stopped exporting them, they were added by
  1002-gtk-Makefile.am-add-PIE-flags-to-libspice-client-gli.patch
  which was dropped during the rebase
  Related: rhbz#1185434

* Mon Feb 16 2015 Jonathon Jongsma <jjongsma@redhat.com> - 0.26-1
- Rebase to 0.26 release
  Resolves: rhbz#1185434

* Thu Jun 19 2014 Christophe Fergeau <cfergeau@redhat.com> 0.22-7
- Cherry-pick important fixes which were made after spice-gtk 0.22
  Related: rhbz#1097338

* Wed Jun 18 2014 Marc-Andre Lureau <marcandre.lureau@redhat.com> - 0.22-6
- Bump glib requirement. Resolves: rhbz#1097338

* Wed Jun 18 2014 Marc-Andre Lureau <marcandre.lureau@redhat.com> - 0.22-5
- Bump glib requirement. Resolves: rhbz#1097338

* Mon Jun 16 2014 Marc-Andre Lureau <marcandre.lureau@redhat.com> - 0.22-4
- Remove CAD rhel-only patches. Resolves: rhbz#1108628
- Add rhel-only SPICE_NOSCALE. Resolves: rhbz#1054757
- Check that clipboard request does not belong to remote. Resolves: rhbz#1108642
* Tue Jun  3 2014 Marc-Andre Lureau <marcandre.lureau@redhat.com> - 0.22-3
- Fix taking screenshots of secondary displays.
  Resolves: rhbz#1029765

* Tue Jun  3 2014 Marc-Andre Lureau <marcandre.lureau@redhat.com> - 0.22-2
- Use TLS version 1.0 or better
  Resolves: rhbz#1035728

* Tue May 13 2014 Jonathon Jongsma <jjongsma@redhat.com> - 0.22-1
- rebase to 0.22
  Resolves: rhbz#1097338

* Tue Oct 22 2013 Alon Levy <alevy@redhat.com> 0.20-11
- Fix failed RELRO test on spice-client-glib.
  Resolves: rhbz#998529 (previous version failed RELRO rpmdiff test)

* Mon Oct 21 2013 Alon Levy <alevy@redhat.com> 0.20-10
- Make mono invert only cursor properly contrast
  Resolves: rhbz#998529

* Thu Sep 12 2013 Christophe Fergeau <cfergeau@redhat.com> 0.20-9
- New build with correct patch for CVE-2013-4324

* Wed Sep 11 2013 Christophe Fergeau <cfergeau@redhat.com> 0.20-8
- Fix race condition in policykit use (CVE-2013-4324)
  Resolves: CVE-2013-4324

* Wed Aug 28 2013 Alon Levy <alevy@redhat.com> 0.20-7
- Fix wrong local cursor rendering for mono cursors.
  Resolves: rhbz#998529

* Mon Aug 19 2013 Christophe Fergeau <cfergeau@redhat.com> 0.20-6
- Fix g_slist_free_full fallback implementation which was corrupting memory
  Resolves: rhbz#997893

* Tue Aug 13 2013 Christophe Fergeau <cfergeau@redhat.com> 0.20-5
- Fix gtk2 python bindings for USB widget
  Resolves: rhbz#996459

* Tue Aug 06 2013 Christophe Fergeau <cfergeau@redhat.com> 0.20-4
- Adjust BuildRequires to make sure new enough glib/gtk+ are used
  at build time as glib 2.26 is needed for proxy support
  Resolves: rhbz#948618

* Sun Jul 14 2013 Christophe Fergeau <cfergeau@redhat.com> 0.20-3
- Add versioned Requires for glib2/gtk2 as spice-gtk is using symbols
  which were added in these versions
  Resolves: rhbz#980400
- If software smartcard support is already initialized when creating a
  smartcard channel, don't consider this as a fatal error
  Resolves: rhbz#815639
- Convert text line-endings if necessary
  Resolves: rhbz#752350

* Thu Jul 11 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.20-2
- Fix spice_channel_string_to_type symbol visibility (rhbz#961452)

* Wed Jun 26 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.20-1
- Upstream release v0.20
  Resolves: rhbz#961452
- snappy has been renamed spicy-screenshot
- Adaptive video streaming support
  Resolves: rhbz#978405
- Disable auto-mount of devices when USB auto share is enabled and active
  Resolves: rhbz#812972
- Print actual host where spice-session.c connects
  Resolves: rhbz#879651
- Fix only one desktop effect to be disabled can be specified
  Resolves: rhbz#955277
- Accept CA certificate directly, not as a file
  Resolves: rhbz#882329
- Don't ignore secure channels controller messages
  Resolves: rhbz#879352
- Don't grab mouse cursor on client --> server mouse mode switch
  Resolves: rhbz#830760
- Fix crashes at first Shift-Ctrl-V in Microsoft Outlook
  Resolves: rhbz#906558
- Print list of channels usable on init
  Resolves: rhbz#834513
- Fix segfaults during spice migration with SSL when running from cli
  Resolves: rhbz#855870

* Thu Jan 10 2013 Hans de Goede <hdegoede@redhat.com> - 0.14-7
- Update agent monitor settings when closing a window
  Resolves: rhbz#881072

* Fri Dec 21 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-6
- Don't ask for root/admin password when users want to redirect USB
  devices
  Resolves: rhbz#859392

* Tue Oct 23 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.14-5
- Apply color conversion when creating image
  Resolves: rhbz#843134
- Show correct ungrab key combination in spicy
  Resolves: rhbz#851090
- Fix sending 00 scancodes to guests
  Resolves: rhbz#868237
- Improve open_host() debugging message
  Resolves: rhbz#858232
- Empty host subject from qemu should only validate hostname
  Resolves: rhbz#858228
- Fix disabling mouse acceleration on X11
  Resolves: rhbz#867885
- use more explicit SSL error message
  Resolves: rhbz#846666

* Mon Oct 15 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-4
- Fix application of Patch2, it includes the git commit log which
  contained a diff hunk which %patch happily applied, which caused
  https://bugzilla.redhat.com/show_bug.cgi?id=804187#c9
  Related: rhbz#804187

* Thu Oct 11 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-3
- Add info message when USB dialog is empty
  Resolves: rhbz#804187
- Properly reset usb channels after non-seamless migration
  Resolves: rhbz#861332
- Fix read error handling for USB redirection
  Related: rhbz#842354
- Auto-discover already plugged-in USB devices
  Resolves: rhbz#820964
- Add support for disabling Ctrl+Alt+Del
  Resolves: rhbz#807771

* Tue Sep 25 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-2
- Readd G_GNUC_DEPRECATED_FOR patch as this issue is not fixed upstream yet
  Related: rhbz#842354

* Fri Sep 21 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-1
- Rebase spice-gtk to 0.14
  Resolves: rhbz#842354

* Mon Sep 10 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13.29-3
- Add patch fixing CVE-2012-3524
  Resolves: rhbz#854825

* Tue Sep 4 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.13.29-2
- Rebase spice-gtk to latest upstream (with SPICE_DEPRECATED_FOR macro)
  Resolves: rhbz#842354

* Tue Sep 4 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.13.29-1
- Rebase spice-gtk to latest upstream
  Resolves: rhbz#842354

* Wed May 23 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.11-11
- Correctly track main channel, fix crash in some migration cases
  Resolves: rhbz#823874

* Thu May 17 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.11-10
- Fix channel caps not being reset correctly, and causing migration to fail
  Resolves: rhbz#821795

* Sun May 6 2012 Yonit Halperin     <yhalperi@redhat.com> - 0.11-9
- Introduce sized video frames, for fixing glitches in youtube movies.
  Resolves: rhbz#815426

* Mon Apr 16 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.11-8
- Fix switch-host migration error with ssl channels.
  Resolves: rhbz#802574

* Tue Apr 10 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.11-7
- Handle grab-broken event
  Resolves: rhbz#807292
- Fix segfault with large clipboard copy-paste
  Resolves: rhbz#809145
- Fix cursor not hidden
  Resolves: rhbz#810588
- Fix segfault when closing while recording
  Resolves: rhbz#810247
- Add USB support to controller
  Resolves: rhbz#807296
- Add WAN support to controller
  Resolves: rhbz#787449

* Tue Apr 03 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.11-6
- Fix blue-tinted video with old Spice server
  Resolves: rhbz#807389
- Fix segfault during switch-host migration
  Resolves: rhbz#807410
- Fix switch-host migration failure with SSL
  Resolves: rhbz#802574
- Fix crash during migration while playing video
  Resolves: rhbz#808567
- Requires gtk2 >= 2.18.9-10
  Resolves: rhbz#809033

* Thu Mar 22 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.11-5
- Fix memory leak when resizing guest
  Resolves: rhbz#805641

* Wed Mar 21 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.11-4
- Fix cursor is displayed on each guest screen when mouse is in server mode
  Resolves: rhbz#804308

* Wed Mar 21 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.11-3
- Fix cursor is displayed on each guest screen when mouse is in server mode
  Resolves: rhbz#804308
- Fix --spice-color-depth=16 does not seem to work.
  Resolves: rhbz#802898
- Fix cannot leave full-screen when mouse is grabbed in server mode mouse
  Resolves: rhbz#804307

* Wed Mar 14 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-2
- Fix a crash triggered when trying to view a usbredir enabled vm from
  virt-manager
  Related: rhbz#758100

* Thu Mar 08 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.11-1
- Rebase to 0.11 upstream release
  Related: rhbz#773642

* Wed Mar 07 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.10.6-3
- Add back spice-protocol BuildRequires to help some deps magic happen.
  Resolves: #799112

* Tue Mar 06 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.10.6-2
- spice-client-glib-devel requires spice-protocol.
  Resolves: #799112
- seam-less migration fix.

* Thu Mar 01 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.10.6-1
- Add foreign menu support.
  Related: rhbz#773642

* Fri Feb 24 2012 Hans de Goede <hdegoede@redhat.com> - 0.10-1
- Rebase to 0.10 upstream release
  Related: rhbz#773642

* Tue Jan 31 2012 Hans de Goede <hdegoede@redhat.com> - 0.9-1
- Rebase to 0.9 upstream release
  Related: rhbz#773642

* Wed Jan 25 2012 Hans de Goede <hdegoede@redhat.com> - 0.8-1
- Rebase to 0.8 upstream release
  Resolves: rhbz#773642
- This release add support for usbredirection
  Resolves: rhbz#758100
- This release fixes spice-gtk crashing on machines with no soundcard
  Resolves: rhbz#772118

* Mon Jul 18 2011 Christophe Fergeau <cfergeau@redhat.com> - 0.6-2
- Set release to -2 so that the EPEL package gets upgraded
- Related: rhbz#708417

* Mon Jul 18 2011 Christophe Fergeau <cfergeau@redhat.com> - 0.6-1
- Added spice-gtk-0.6-add-generated-files.patch to be able to build without
  perl-Text-CSV
- Initial import of spice-gtk in RHEL CVS based on the EPEL .spec
- Related: rhbz#708417

* Fri May 27 2011 Christophe Fergeau <cfergeau@redhat.com> - 0.6-1
- Initial EPEL release based on the rawhide .spec cleaned up from the parts
  that are not useful for EPEL (because the needed dependencies are not available)

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
