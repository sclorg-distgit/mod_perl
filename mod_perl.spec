%{?scl:%scl_package mod_perl}

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%define use_system_apr 1
%else
%define use_system_apr 0
%endif

%if 0%{?scl:1}
%{!?_httpd24_apxs:       %{expand: %%global _httpd24_apxs       %%{_sbindir}/apxs}}
%{!?_httpd24_mmn:        %{expand: %%global _httpd24_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd24_confdir:    %{expand: %%global _httpd24_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd24_modconfdir: %{expand: %%global _httpd24_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd24_moddir:    %{expand: %%global _httpd24_moddir    %%{_libdir}/httpd/modules}}
%else
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}
%endif

%global regenerate_xs 0

Name:           %{?scl:%scl_prefix}mod_perl
Version:        2.0.9
Release:        6%{?dist}
Summary:        An embedded Perl interpreter for the Apache HTTP Server

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://perl.apache.org/
Source0:        http://www.apache.org/dist/perl/mod_perl-%{version}.tar.gz
Source1:        perl.conf
Source2:        perl.module.conf
Patch1:         mod_perl-2.0.4-inline.patch
#Patch2:         mod_perl-2.0.5-nolfs.patch
#Patch3:         mod_perl-short-name.patch

BuildRequires:  %{?scl_prefix}perl-devel, %{?scl_prefix}perl-generators, %{?scl_prefix}perl(ExtUtils::Embed)
BuildRequires:  %{?scl:httpd24-}httpd-devel >= 2.4.0, %{?scl:httpd24-}httpd, gdbm-devel
%if %{use_system_apr}
BuildRequires:  apr-devel >= 1.2.0, apr-util-devel
%else
BuildRequires:  %{?scl:httpd24-}apr-devel >= 1.2.0, %{?scl:httpd24-}apr-util-devel
%endif
BuildRequires:  %{?scl_prefix}perl(Data::Dumper)
BuildRequires:  %{?scl_prefix}perl(Data::Flow)
BuildRequires:  %{?scl_prefix}perl(Tie::IxHash)
BuildRequires:  %{?scl_prefix}perl(Test)
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
%if 0%{?scl:1}
Requires:       %{?scl:httpd24-}httpd-mmn = %{_httpd24_mmn}
%else
Requires:       %{?scl:httpd24-}httpd-mmn = %{_httpd_mmn}
%endif
# For Apache::SizeLimit::Core
Requires:       %{?scl_prefix}perl(Linux::Pid)

Conflicts:      perl516-mod_perl
Conflicts:      rh-perl520-mod_perl

%if 0%{?rhel} < 7
# RPM 4.8 style
%{?filter_setup:
%filter_from_provides /^%{?scl_prefix}perl(Apache2::Connection)$/d
%filter_from_provides /^%{?scl_prefix}perl(Apache2::RequestRec)$/d
%filter_from_provides /^%{?scl_prefix}perl(warnings)$/d
%filter_from_provides /^%{?scl_prefix}perl(HTTP::Request::Common)$/d
%filter_from_provides /^mod_perl\.so(.*$/d
%filter_from_provides /^mod_perl\.so$/d
%filter_from_requires /^%{?scl_prefix}perl(Apache::Test.*)/d
%filter_from_requires /^%{?scl_prefix}perl(Data::Flow)/d
%filter_from_requires /^%{?scl_prefix}perl(Apache2::FunctionTable)/d
%filter_from_requires /^%{?scl_prefix}perl(Apache2::StructureTable)/d
# Hide dependencies on broken provides
%filter_from_requires /^%{?scl_prefix}perl(Apache2::MPM)/d
%{?perl_default_filter}
}
%else
# RPM 4.9 style
%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Apache2::Connection\\)$
%global __provides_exclude %__provides_exclude|perl\\(Apache2::RequestRec\\)$
%global __provides_exclude %__provides_exclude|perl\\(warnings\\)$
%global __provides_exclude %__provides_exclude|perl\\(HTTP::Request::Common\\)$
%global __provides_exclude %__provides_exclude|mod_perl\\.so\\(.*$
%global __provides_exclude %__provides_exclude|mod_perl\\.so$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Apache::Test.*\\)
%global __requires_exclude %__requires_exclude|perl\\(Data::Flow\\)
%global __requires_exclude %__requires_exclude|perl\\(Apache2::FunctionTable\\)
%global __requires_exclude %__requires_exclude|perl\\(Apache2::StructureTable\\)
# Hide dependencies on broken provides
%global __requires_exclude %__requires_exclude|^%{?scl_prefix}perl\\(Apache2::MPM\\)
%endif

%description
Mod_perl incorporates a Perl interpreter into the Apache web server,
so that the Apache web server can directly execute Perl code.
Mod_perl links the Perl run-time library into the Apache web server and
provides an object-oriented Perl interface for Apache's C language
API.  The end result is a quicker CGI script turnaround process, since
no external Perl interpreter has to be started.

Install mod_perl if you're installing the Apache web server and you'd
like for it to directly incorporate a Perl interpreter.


%package devel
Summary:        Files needed for building XS modules that use mod_perl
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}, %{?scl:httpd24-}httpd-devel%{?_isa}

%description devel 
The mod_perl-devel package contains the files needed for building XS
modules that use mod_perl.


%prep
%setup -q -n mod_perl-%{version}
%patch1 -p1
%{?scl:sed -i 's|@scl@|%{_scl_root}|' %{SOURCE1}}
%{!?scl:sed -i 's|@scl@||' %{SOURCE1}}

# Remove docs/os. It's only win32 info with non ASL-2.0 license.
rm -rf docs/os

%build

for i in Changes SVN-MOVE; do
    iconv --from=ISO-8859-1 --to=UTF-8 $i > $i.utf8
    mv $i.utf8 $i
done

cd docs
for i in devel/debug/c.pod devel/core/explained.pod user/Changes.pod; do
    iconv --from=ISO-8859-1 --to=UTF-8 $i > $i.utf8
    mv $i.utf8 $i
done
cd ..

%if 0%{?scl:1}
. /opt/rh/httpd24/enable
. /opt/rh/%scl/enable

%if %{use_system_apr}
CFLAGS="$RPM_OPT_FLAGS -fpic" %{__perl} Makefile.PL </dev/null \
         PREFIX=$RPM_BUILD_ROOT/%{_prefix} \
         INSTALLDIRS=vendor \
         MP_APXS=%{_httpd24_apxs} \
         MP_APR_CONFIG=%{_root_bindir}/apr-1-config
%else
CFLAGS="$RPM_OPT_FLAGS -fpic" %{__perl} Makefile.PL </dev/null \
         PREFIX=$RPM_BUILD_ROOT/%{_prefix} \
         INSTALLDIRS=vendor \
         MP_APXS=%{_httpd24_apxs} \
         MP_APR_CONFIG=/opt/rh/httpd24/root/usr/bin/apr-1-config
%endif
%else
CFLAGS="$RPM_OPT_FLAGS -fpic" %{__perl} Makefile.PL </dev/null \
         PREFIX=$RPM_BUILD_ROOT/%{_prefix} \
         INSTALLDIRS=vendor \
         MP_APXS=%{_httpd_apxs} \
         MP_APR_CONFIG=%{_bindir}/apr-1-config
%endif

# This is not needed now when we are using httpd24 branch, but I will keep
# it here in case someone will have to regenerate *.xs files again.
%if %{regenerate_xs}0
make source_scan
make xs_generate
CFLAGS="$RPM_OPT_FLAGS -fpic" %{__perl} Makefile.PL </dev/null \
         PREFIX=$RPM_BUILD_ROOT/%{_prefix} \
         INSTALLDIRS=vendor \
         MP_APXS=%{?scl:%{_httpd24_apxs}}%{!?scl:%{_httpd_apxs}} \
         MP_APR_CONFIG=$(type -P apr-1-config)
%endif

make -C src/modules/perl %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS -fpic"
make %{?_smp_mflags}

%install
%if 0%{?scl:1}
. /opt/rh/httpd24/enable
. /opt/rh/%scl/enable

install -d -m 755 $RPM_BUILD_ROOT%{_httpd24_moddir}
make install \
    MODPERL_AP_LIBEXECDIR=$RPM_BUILD_ROOT%{_httpd24_moddir} \
    MODPERL_AP_INCLUDEDIR=$RPM_BUILD_ROOT%{_includedir}/httpd
%else
install -d -m 755 $RPM_BUILD_ROOT%{_httpd_moddir}
make install \
    MODPERL_AP_LIBEXECDIR=$RPM_BUILD_ROOT%{_httpd_moddir} \
    MODPERL_AP_INCLUDEDIR=$RPM_BUILD_ROOT%{_includedir}/httpd
%endif

# Remove the temporary files.
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'

# Fix permissions to avoid strip failures on non-root builds.
chmod -R u+w $RPM_BUILD_ROOT/*

%if 0%{?scl:1}
# Install the config file
install -d -m 755 $RPM_BUILD_ROOT%{_httpd24_confdir}
install -d -m 755 $RPM_BUILD_ROOT%{_httpd24_modconfdir}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd24_confdir}
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_httpd24_modconfdir}/02-perl.conf
%else
# Install the config file
install -d -m 755 $RPM_BUILD_ROOT%{_httpd_confdir}
install -d -m 755 $RPM_BUILD_ROOT%{_httpd_modconfdir}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_httpd_modconfdir}/02-perl.conf
%endif

# Move set of modules to -devel
devmods="ModPerl::Code ModPerl::BuildMM ModPerl::CScan \
          ModPerl::TestRun ModPerl::Config ModPerl::WrapXS \
          ModPerl::BuildOptions ModPerl::Manifest \
          ModPerl::MapUtil ModPerl::StructureMap \
          ModPerl::TypeMap ModPerl::FunctionMap \
          ModPerl::ParseSource ModPerl::MM \
          Apache2::Build Apache2::ParseSource Apache2::BuildConfig \
          Bundle::ApacheTest"
for m in $devmods; do
   test -f $RPM_BUILD_ROOT%{_mandir}/man3/${m}.3pm &&
     echo "%{_mandir}/man3/${m}.3pm*"
   fn=${m//::/\/}
   test -f $RPM_BUILD_ROOT%{perl_vendorarch}/${fn}.pm &&
        echo %{perl_vendorarch}/${fn}.pm
   test -d $RPM_BUILD_ROOT%{perl_vendorarch}/${fn} && 
        echo %{perl_vendorarch}/${fn}
   test -d $RPM_BUILD_ROOT%{perl_vendorarch}/auto/${fn} && 
        echo %{perl_vendorarch}/auto/${fn}
done | tee devel.files | sed 's/^/%%exclude /' > exclude.files
echo "%%exclude %{_mandir}/man3/Apache::Test*.3pm*" >> exclude.files

# perl build script generates *.orig files, they get installed and later they
# break provides so mod_perl requires mod_perl-devel. We remove them here.
find "$RPM_BUILD_ROOT" -type f -name *.orig -exec rm -f {} \;

%files -f exclude.files
%doc Changes LICENSE NOTICE README* STATUS SVN-MOVE docs/
%if 0%{?scl:1}
%config(noreplace) %{_httpd24_confdir}/perl.conf
%config(noreplace) %{_httpd24_modconfdir}/02-perl.conf
%else
%config(noreplace) %{_httpd_confdir}/perl.conf
%config(noreplace) %{_httpd_modconfdir}/02-perl.conf
%endif
%{_bindir}/*
%if 0%{?scl:1}
%{_httpd24_moddir}/mod_perl.so
%else
%{_httpd_moddir}/mod_perl.so
%endif
%{perl_vendorarch}/auto/*
%dir %{perl_vendorarch}/Apache/
%{perl_vendorarch}/Apache/Reload.pm
%{perl_vendorarch}/Apache/SizeLimit*
%{perl_vendorarch}/Apache2/
%{perl_vendorarch}/Bundle/
%{perl_vendorarch}/APR/
%{perl_vendorarch}/ModPerl/
%{perl_vendorarch}/*.pm
%{_mandir}/man3/*.3*

%files devel -f devel.files
%if 0%{?scl:1}
%dir %{_includedir}/httpd/
%endif
%{_includedir}/httpd/*
%{perl_vendorarch}/Apache/Test*.pm
%{_mandir}/man3/Apache::Test*.3pm*

%changelog
* Thu Jul 21 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.9-6
- Fixed file conflict with others Perl SCLs
- Update local path in default perl.conf
- Resolves: rhbz#1227192, rhbz#1210621

* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 2.0.9-5
- SCL

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.9-4
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 19 2015 Jan Kaluza <jkaluza@redhat.com> - 2.0.9-2
- fix #1272901 - add perl(Test) to BuildRequires

* Fri Jun 19 2015 Jan Kaluza <jkaluza@redhat.com> - 2.0.9-1
- update to 2.0.9

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-14.20150311svn1665777
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.8-13.20150311svn1665777
- Perl 5.22 rebuild

* Wed Mar 11 2015 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-12.20150311svn1665777
- update to latest revision from trunk to backport latest upstream fixes

* Fri Mar 06 2015 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-11.20140624svn1602105
- remove docs/os from documentation because of its license (#1199044)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.8-10.20140624svn1602105
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-9.20140624svn1602105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-8.20140624svn1602105
- update to latest revision from trunk to backport latest upstream fixes

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-7.20140430svn1590627
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-6.20140430svn1590627
- update to latest revision of httpd24threading branch to backport latest upstream fixes

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 2.0.8-5.20131031svn1537408
- fix _httpd_mmn expansion in absence of httpd-devel

* Mon Oct 21 2013 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-3.20131031svn1537408
- update to latest revision of httpd24 branch to backport new upstream fixes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-3.20130709svn1498417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.0.8-2.20130709svn1498417
- Perl 5.18 rebuild

* Tue Jul 09 2013 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-1.20130709svn1498417
- update to latest revision of httpd24 branch to backport important fixes
  in httpd-2.4 compatibility

* Thu Feb 21 2013 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-12.20130221svn1448242
- update to httpd24 svn branch which provides much more better compatibility
  with httpd-2.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-10
- do not install .orig file generated by make xs_generate
- filter unversioned mod_perl.so from provides

* Mon Nov 19 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-9
- clean up spec file
- do not require -devel when installing main package

* Mon Nov 19 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-8
- add wrappers for new fields added in httpd-2.4 structures

* Wed Jul 25 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-7
- updated httpd-2.4 patch

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.0.7-5
- Hide dependencies on broken provides

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 2.0.7-4
- Perl 5.16 rebuild

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 2.0.7-3
- Rebuild to fix Apache2::MPM dependency on i686

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 2.0.7-2
- Perl 5.16 rebuild

* Fri Jun 29 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-1
- update to 2.0.7 (#830501)

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 2.0.5-11
- Perl 5.16 rebuild

* Thu Apr 19 2012 Petr Pisar <ppisar@redhat.com> - 2.0.5-10
- Fix dependency declaration on Data::Dumper

* Wed Apr 18 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.5-9
- fix compilation with httpd-2.4 (#809142)

* Tue Mar 06 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.5-8
- filter perl(HTTP::Request::Common) Provide from -devel (#247250)
- use short_name as argv[0] (#782369)

* Thu Jan  5 2012 Ville Skyttä <ville.skytta@iki.fi> - 2.0.5-7
- Ship Apache::Reload and Apache::SizeLimit in main package (#748362).
- Require Linux::Pid for Apache::SizeLimit (#766568).
- Move Apache::Test* man pages to -devel.
- Don't filter Module::Build dependency.

* Wed Nov  9 2011 Joe Orton <jorton@redhat.com> - 2.0.5-6
- fudge the LFS test (#730832)

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 2.0.5-5
- RPM 4.9 dependency filtering added

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.0.5-4
- Perl mass rebuild

* Mon Apr 11 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.0.5-3
- filter warnings from provides

* Sat Mar 26 2011 Joe Orton <jorton@redhat.com> - 2.0.5-2
- ship NOTICE file

* Sat Mar 26 2011 Joe Orton <jorton@redhat.com> - 2.0.5-1
- update to 2.0.5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.0.4-13
- fix missing requirements, add filter_setup macro, remove double provides

* Thu Nov 04 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 2.0.4-12
- Spec cleanup for the merge review

* Fri May 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.0.4-11
- Mass rebuild with perl-5.12.0

* Tue Dec  8 2009 Joe Orton <jorton@redhat.com> - 2.0.4-10
- add security fix for CVE-2009-0796 (#544455)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 17 2008 Joe Orton <jorton@redhat.com> 2.0.4-7
- fix inline abuse (#459351)

* Wed Aug  6 2008 Joe Orton <jorton@redhat.com> 2.0.4-5
- rebuild to fix patch fuzz (#427758)

* Mon Jul 14 2008 Joe Orton <jorton@redhat.com> 2.0.4-4
- rebuild for new BDB

* Tue May 13 2008 Joe Orton <jorton@redhat.com> 2.0.4-3
- trim changelog; rebuild

* Fri Apr 18 2008 Joe Orton <jorton@redhat.com> 2.0.4-2
- update to 2.0.4

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.3-21
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.3-20
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Joe Orton <jorton@redhat.com> 2.0.3-19
- further fixes for perl 5.10 (upstream r480903, r615751)

* Wed Jan 30 2008 Joe Orton <jorton@redhat.com> 2.0.3-18
- fix build with perl 5.10 (upstream r480890)

* Tue Jan 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.3-17
- fix perl BR

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.3-16
- rebuild for new perl

* Thu Dec  6 2007 Joe Orton <jorton@redhat.com> 2.0.3-15
- rebuild for new OpenLDAP

* Wed Sep  5 2007 Joe Orton <jorton@redhat.com> 2.0.3-14
- filter perl(HTTP::Request::Common) Provide from -devel (#247250)

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 2.0.3-13
- rebuild for fixed 32-bit APR

* Thu Aug 23 2007 Joe Orton <jorton@redhat.com> 2.0.3-12
- rebuild for expat soname bump

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 2.0.3-11
- rebuild for libdb soname bump

* Mon Aug 20 2007 Joe Orton <jorton@redhat.com> 2.0.3-10
- fix License

* Fri Apr 20 2007 Joe Orton <jorton@redhat.com> 2.0.3-8
- filter provide of perl(warnings) (#228429)

* Wed Feb 28 2007 Joe Orton <jorton@redhat.com> 2.0.3-7
- also restore Apache::Test to devel
- add BR for perl-devel

* Tue Feb 27 2007 Joe Orton <jorton@redhat.com> 2.0.3-6
- filter more Apache::Test requirements

* Mon Feb 26 2007 Joe Orton <jorton@redhat.com> 2.0.3-5
- repackage set of trimmed modules, but only in -devel

* Wed Jan 31 2007 Joe Orton <jorton@redhat.com> 2.0.3-4
- restore ModPerl::MM

* Tue Dec  5 2006 Joe Orton <jorton@redhat.com> 2.0.3-3
- trim modules even more aggressively (#197841)

* Mon Dec  4 2006 Joe Orton <jorton@redhat.com> 2.0.3-2
- update to 2.0.3
- remove droplet in buildroot from multilib patch
- drop build-related ModPerl:: modules and Apache::Test (#197841)
- spec file cleanups

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Thu Jun 15 2006 Joe Orton <jorton@redhat.com> 2.0.2-6
- fix multilib conflicts in -devel (#192733)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.2-5.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.2-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Joe Orton <jorton@redhat.com> 2.0.2-3
- rebuild for httpd 2.2

* Wed Oct 26 2005 Joe Orton <jorton@redhat.com> 2.0.2-2
- update to 2.0.2

* Thu Oct 20 2005 Joe Orton <jorton@redhat.com> 2.0.1-2
- rebuild

* Fri Jun 17 2005 Warren Togami <wtogami@redhat.com> 2.0.1-1
- 2.0.1

* Fri May 20 2005 Warren Togami <wtogami@redhat.com> 2.0.0-3
- dep changes (#114651 jpo and ville)

* Fri May 20 2005 Joe Orton <jorton@redhat.com> 2.0.0-1
- update to 2.0.0 final

* Mon Apr 18 2005 Ville Skyttä <ville.skytta@iki.fi> - 2.0.0-0.rc5.3
- Fix sample configuration.
- Explicitly disable the test suite. (#112563)

* Mon Apr 18 2005 Joe Orton <jorton@redhat.com> 2.0.0-0.rc5.2
- fix filter-requires for new Apache2:: modules

* Sat Apr 16 2005 Warren Togami <wtogami@redhat.com> - 2.0.0-0.rc5.1
- 2.0.0-RC5

* Sun Apr 03 2005 Jose Pedro Oliveira <jpo@di.uminho.pt> - 2.0.0-0.rc4.1
- Update to 2.0.0-RC4.
- Specfile cleanup. (#153236)
