Summary:	NetWare file/print server that runs under Linux
Summary(de):	NetWare-Datei/Druckserver unter Linux 
Summary(fr):	Serveur Netware de fichiers/impression tournant sous Linux
Summary(pl):	Serwer Netware plików/drukarek dzia³aj±cy pod Linuxem
Summary(tr):	Linux altýnda çalýþan NetWare dosya/yazýcý sunucusu
Name:		mars_nwe
Version:	0.99.pl17
Release:	2
Copyright:	GPL
URL:		http://www.compu-art.de/mars_nwe/index.html
Source0:	http://www.compu-art.de/download/%{name}-%{version}.tgz
Source1:	mars_nwe.cnv.tgz
Source2:	nwserv.init
Source3:	nwserv.logrotate
Source4:	pipefs-scripts.tgz
Patch0:		mars_nwe.patch
Group:		Networking/Daemons
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
OPT="$RPM_OPT_FLAGS"; export OPT
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
install -d $RPM_BUILD_ROOT/var/lib/nwserv/{sys/{public/sources,login,system,mail},pipe,bindery,attrib,trustees}
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
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/nwserv

tar -xzf %{SOURCE4} -C $RPM_BUILD_ROOT/var/lib/nwserv/pipe

for I in comm comm32; do
	install -m644 examples/$I.exe $RPM_BUILD_ROOT/var/lib/nwserv/sys/public/$I.exe
done

for I in sendm comm; do
	install -m644 examples/$I.c $RPM_BUILD_ROOT/var/lib/nwserv/sys/public/sources/$I.c
done

for I in unxcomm unxsendm; do
	install -s examples/$I $RPM_BUILD_ROOT/var/lib/nwserv/pipe
done
    
gzip -9nf README doc/* examples/README.important

%post
/sbin/chkconfig --add nwserv.init

%postun
/sbin/chkconfig --del nwserv.init

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz doc examples/README.important.gz examples/*.c
%dir /var/lib/nwserv
%dir /var/lib/nwserv/bindery
%dir /var/lib/nwserv/attrib
%dir /var/lib/nwserv/trustees
%dir /var/lib/nwserv/pipe
%dir /var/lib/nwserv/sys
%dir /var/lib/nwserv/sys/public
%dir /var/lib/nwserv/sys/login
%dir /var/lib/nwserv/sys/mail
%dir /var/lib/nwserv/sys/system
%dir /var/lib/nwserv/sys/public/sources
%dir /var/spool/nwserv
%dir /var/spool/nwserv/.volcache
%dir /var/spool/nwserv/.locks
%dir /etc/nwserv
%attr(600,root,root) %ghost /var/log/*
%attr(600,root,root) %verify(not md5 mtime) %config /etc/nwserv/nwserv.conf
%attr(600,root,root) %verify(not md5 mtime) %config /etc/nwserv/nwserv.stations
%attr(644,root,root) /etc/nwserv/nwserv.cnv*
%attr(754,root,root) %config /etc/rc.d/init.d/nwserv.init
%attr(600,root,root) %config /etc/logrotate.d/nwserv
%attr(755,root,root) %{_sbindir}/*
%attr(644,root,root) /var/lib/nwserv/sys/public/comm.exe
%attr(644,root,root) /var/lib/nwserv/sys/public/sources/*
%attr(755,root,root) /var/lib/nwserv/pipe/*
