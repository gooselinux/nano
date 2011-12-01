Summary:         A small text editor
Name:            nano
Version:         2.0.9
Release:         7%{?dist}
License:         GPLv3+
Group:           Applications/Editors
URL:             http://www.nano-editor.org
Source:          http://www.nano-editor.org/dist/v2.0/%{name}-%{version}.tar.gz
Source2:         nanorc
Patch1:          nano-2.0.9-warnings.patch
Patch2:          nano-2.0.9-bz582434.patch
Patch3:          nano-2.0.9-bz582434-inc.patch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:   autoconf
BuildRequires:   gettext-devel
BuildRequires:   groff
BuildRequires:   ncurses-devel
BuildRequires:   sed
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

%description
GNU nano is a small and friendly text editor.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
for f in doc/man/fr/{nano.1,nanorc.5,rnano.1} ; do
  iconv -f iso-8859-1 -t utf-8 -o $f.tmp $f && mv $f.tmp $f
  touch $f.html
done

%build
%configure --enable-all --bindir=/bin
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR="%{buildroot}" install bindir=/bin
#ln -s nano %{buildroot}%{_bindir}/pico
rm -f %{buildroot}%{_infodir}/dir
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
ln -s ../../bin/nano ${RPM_BUILD_ROOT}%{_bindir}/nano
ln -s ../../bin/rnano ${RPM_BUILD_ROOT}%{_bindir}/rnano
cp %{SOURCE2} ./nanorc

# disable line wrapping by default
sed 's/# set nowrap/set nowrap/' doc/nanorc.sample >> ./nanorc
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 ./nanorc $RPM_BUILD_ROOT%{_sysconfdir}/nanorc

%find_lang %{name}

%post
if [ -f %{_infodir}/%{name}.info.gz ]; then
  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir
fi
exit 0

%preun
if [ $1 -eq 0 ]; then
  if [ -f %{_infodir}/%{name}.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir
  fi
fi
exit 0

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%doc doc/nanorc.sample
%doc doc/faq.html
/bin/*
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/nanorc
%{_mandir}/man*/*
%lang(fr) %{_mandir}/fr/man*/*
%{_infodir}/nano.info*
%{_datadir}/nano

%changelog
* Thu Aug 12 2010 Kamil Dudka <kdudka@redhat.com> - 2.0.9-7
- CVE-2010-1160, CVE-2010-1161 (#582740)

* Thu Apr 15 2010 Kamil Dudka <kdudka@redhat.com> - 2.0.9-6
- CVE-2010-1160, CVE-2010-1161 (#582740)

* Thu Nov 26 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-5
- sanitize specfile according to Fedora Packaging Guidelines 

* Wed Nov 18 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-4
- install a system-wide configuration file based on nanorc.sample
- disable line wrapping by default (#528359)

* Mon Sep 21 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-3
- suppress warnings for __attribute__((warn_unused_result)) (#523951)

* Fri Sep 18 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-2
- install binaries to /bin (#168340)

* Fri Sep 18 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-1
- new upstream release
- dropped patch no longer needed (possible change in behavior though negligible)
- fixed broken HTML doc in FR locales (#523951)

* Thu Sep 17 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.6-8
- do process install-info only without --excludedocs(#515943)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Apr  4 2008 Ville Skyttä <ville.skytta at iki.fi> - 2.0.6-5
- Mark localized man pages with %%lang, fix French nanorc(5) (#322271).

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.6-4
- Autorebuild for GCC 4.3

* Fri Dec 07 2007 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.0.6-3
- Pass rnano.1 through iconv to silence the final rpmlint complaint
  and finish up the merge review.

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> - 2.0.6-2
- Update licence
- Fix open(O_CREAT) calls without mode

* Sun Jun 03 2007 Florian La Roche <laroche@redhat.com> - 2.0.6-1
- update to 2.0.6

* Mon Feb 05 2007 Florian La Roche <laroche@redhat.com> - 2.0.3-1
- update to 2.0.3
- update spec file syntax, fix scripts rh#220527

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.12-1.1
- rebuild

* Mon Jul 10 2006 David Woodhouse <dwmw2@redhat.com> - 1.3.12-1
- Update to 1.3.12

* Tue May 16 2006 David Woodhouse <dwmw2@redhat.com> - 1.3.11-1
- Update to 1.3.11
- BuildRequires: groff (#191946)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.8-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.8-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 5 2005 David Woodhouse <dwmw2@redhat.com> 1.3.8-1
- 1.3.8

* Wed Mar 2 2005 David Woodhouse <dwmw2@redhat.com> 1.3.5-0.20050302
- Update to post-1.3.5 CVS tree to get UTF-8 support.

* Wed Aug 04 2004 David Woodhouse <dwmw2@redhat.com> 1.2.4-1
- 1.2.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 02 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.2.3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Aug 11 2003 Bill Nottingham <notting@redhat.com> 1.2.1-4
- build in different environment

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  6 2003 Bill Nottingham <notting@redhat.com> 1.2.1-2
- description tweaks

* Mon May  5 2003 Bill Nottingham <notting@redhat.com> 1.2.1-1
- initial build, tweak upstream spec file
