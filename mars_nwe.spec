Summary:     NetWare file/print server that runs under Linux
Summary(de): NetWare-Datei/Druckserver unter Linux 
Summary(fr): Serveur Netware de fichiers/impression tournant sous Linux
Summary(pl): Serwer Netware plików/drukarek dzia³aj±cy pod Linuxem
Summary(tr): Linux altýnda çalýþan NetWare dosya/yazýcý sunucusu
Name:        mars_nwe
Version:     0.99.pl12
Release:     2
Copyright:   GPL
Source0:     ftp://ftp.gwdg.de/pub/linux/misc/ncpfs/mars_nwe-%{PACKAGE_VERSION}.tgz
Source1:     mars_nwe.cnv.tgz
Source2:     nwserv.init
Source3:     nwserv.log
Patch0:      mars_nwe.patch
Group:       Networking/Daemons
Prereq:      /sbin/chkconfig
Buildroot:   /tmp/%{name}-%{version}-root

%description
MARS is a NetWare compatible file and printer server. It lets you use
a Linux machine as a file and print server for NetWare based clients
using NetWare's native IPX protocol suite.

%description -l de
MARS ist ein NetWare-kompatibler Datei- und Druckerserver. Er gestattet 
die Verwendung eines Linux-Rechners als ein Datei- und Druckserver für 
NetWare-basierende Clients unter Verwendung der NetWare-eigenen 
IPX-Protokollserie. 

%description -l fr
MARS est un serveur de fichiers et d'impression compatible NetWare. Il
permet d'utiliser une machine Linux comme serveur de fichiers et
d'imoression pour des clients NetWare utilisant le protocole IPX
natif de NetWare.

%description -l pl
MARS jest kompatyblinym z Netware serwer plików i drukarek. Pozwala
stworzyæ z komputera z Linuxem serwer plików i drukarek dla klientów
Netware, przy u¿yciu podstawowego protoko³u Netware -- IPX.

%description -l tr
MARS, NetWare uyumlu bir dosya ve yazýcý sunucusudur. Bu program bir Linux
makinenin, NetWare in doðal IPX protokol takýmýný kullanan NetWare
istemcilerinin dosya ve yazýcý sunucusu olarak kullanýlmasýný saðlar.

%prep
%setup0 -q -n mars_nwe
%patch0 -p1
%setup1 -q -n mars_nwe -D -T -a 1
rm -rf $RPM_BUILD_ROOT

%build
make; make; make routed

cd examples
for I in unxcomm unxsendm; do
    gcc $RPM_OPT_FLAGS $I.c -o $I
done
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{nwserv,rc.d/init.d,logrotate.d}
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT/var/nwserv/{sys/{public/sources,login,system,mail},pipe,bindery,attrib,trustees}
install -d $RPM_BUILD_ROOT/var/{run,log,spool/nwserv/{.volcache,.locks}}

install -s {nwserv,nwconn,ncpserv,nwclient,nwbind,nwrouted} $RPM_BUILD_ROOT%{_sbindir}

touch $RPM_BUILD_ROOT/var/log/nw.log
touch $RPM_BUILD_ROOT/var/log/nw.routes

install examples/nwserv.stations $RPM_BUILD_ROOT/etc/nwserv/nwserv.stations

install examples/nw.ini $RPM_BUILD_ROOT/etc/nwserv/nwserv.conf
for I in examples/nw.ini.cnv.*; do
    install $I $RPM_BUILD_ROOT/etc/nwserv/nwserv${I##examples/nw.ini}
done
ln -s nwserv.cnv.437 $RPM_BUILD_ROOT/etc/nwserv/nwserv.cnv

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/nwserv.init
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/nwserv.log

install examples/comm.exe $RPM_BUILD_ROOT/var/nwserv/sys/public/comm.exe
install examples/{sendm,comm}.c $RPM_BUILD_ROOT/var/nwserv/sys/public/sources/

install -s examples/{unxcomm,unxsendm} $RPM_BUILD_ROOT/var/nwserv/pipe

%post
/sbin/chkconfig --add nwserv.init

%postun
/sbin/chkconfig --del nwserv.init

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(644, root, root, 755)
%doc README doc examples/{*.c,README.important}
%dir /var/nwserv
%dir /var/nwserv/bindery
%dir /var/nwserv/attrib
%dir /var/nwserv/trustees
%dir /var/nwserv/pipe
%dir /var/nwserv/sys
%dir /var/nwserv/sys/public
%dir /var/nwserv/sys/login
%dir /var/nwserv/sys/mail
%dir /var/nwserv/sys/system
%dir /var/nwserv/sys/public/sources
%dir /var/spool/nwserv
%dir /var/spool/nwserv/.volcache
%dir /var/spool/nwserv/.locks
%dir /etc/nwserv
%attr(600, root, root) %ghost /var/log/*
%attr(600, root, root) %verify(not md5 mtime) %config /etc/nwserv/nwserv.conf
%attr(600, root, root) %verify(not md5 mtime) %config /etc/nwserv/nwserv.stations
%attr(644, root, root) /etc/nwserv/nwserv.cnv*
%attr(700, root, root) %config /etc/rc.d/init.d/nwserv.init
%attr(600, root, root) %config /etc/logrotate.d/nwserv.log 
%attr(700, root, root) %{_sbindir}/*
%attr(644, root, root) /var/nwserv/sys/public/comm.exe
%attr(644, root, root) /var/nwserv/sys/public/sources/*
%attr(755, root, root) /var/nwserv/pipe/*

%changelog
* Sun Nov 1 1998 Przemys³aw Czerpak <druzus@polbox.com>
  [0.99.pl12-2]
- added reload option to init script,
- added logrotate config file.

* Wed Aug 12 1998 Marcin Korzonek <mkorz@shadow.eu.org>
- build against GNU libc-2.1
- added pl translations

* Mon Jun 1 1998 Przemys³aw Czerpak <druzus@polbox.com>
- DO_IPX_SEND_TEST deactivated - linux/net/ipx/af_ipx.c have to be patched
  for all known kernels prior 2.0.32 (see README.important) - mars works
  faster now,
- volume PIPE-FS added with simple programs for executing unx cmd from
  novell client (/var/nwserv/pipe),
- /etc/rc.d/init.d/mars-nwe changed - sleeps for some seconds
  (defined in section 210 of nwserv.conf) - time for shut down server,
  and name changed to nwserv.init
- trustees information moved to /var/nwserv/trustees,
- attrib information moved to /var/attrib/attribs,
- spool directory moved to /var/spool/nwserv,
- conversion tables for DOS<->Unix file names translation & upper/lowercase
  translations (cp1250,iso2,852,maz for polish characters only),
- nwrouted added,
- simple patch for PIPE-FS added (now PIPE-FS works o.k.),

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Feb 11 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda>
- removed macro %config from /etc/rc.d/init.d/mars-nwe,
- spec file rewrited for using Buildroot,
- added %clean section,
- added %verify(not md5 mtime) for %config files:
  /etc/nwserv.{conf,/etc/nwserv.stations},
- added %%{PACKAGE_VERSION} to Source url,
- added %attr macros in %files (allows building package from non-root
  account).

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- updated for chkconfig
- doesn't start by default
- added status, restart options to init script
