
# TODO:
# - support for new incompatibile quota version

Summary:	NetWare file/print server that runs under Linux
Summary(de.UTF-8):	NetWare-Datei/Druckserver unter Linux
Summary(es.UTF-8):	Servidor de archivos e impresión NetWare que se ejecuta en Linux
Summary(fr.UTF-8):	Serveur Netware de fichiers/impression tournant sous Linux
Summary(pl.UTF-8):	Serwer Netware plików/drukarek działający pod Linuksem
Summary(pt_BR.UTF-8):	Servidor de arquivos e impressão NetWare que roda no Linux
Summary(tr.UTF-8):	Linux altında çalışan NetWare dosya/yazıcı sunucusu
Name:		mars_nwe
Version:	0.99.pl20
Release:	13
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.compu-art.de/mars_nwe/%{name}-%{version}.tgz
# Source0-md5:	98b3bf022233035ce12a834c689605e5
Source1:	%{name}.cnv.tgz
# Source1-md5:	00add1da5f8e624c5c1d8d1b3351616a
Source2:	nwserv.init
Source3:	nwserv.logrotate
Source4:	pipefs-scripts.tgz
# Source4-md5:	940ec1baaea874d0c422eb0435a7b235
Patch0:		%{name}.patch
Patch1:		%{name}-rwlck.patch
Patch2:		%{name}-clean.patch
Patch3:		%{name}-gcc.patch
Patch4:		%{name}-dotfiles.patch
Patch5:		%{name}-trustees.patch
Patch6:		%{name}-lck.patch
Patch7:		%{name}-buffer.patch
Patch8:		%{name}-glibc21.patch
Patch9:		%{name}-format.patch
Patch10:	%{name}-gcc4.patch
Patch11:	%{name}-quota_off.patch
URL:		http://www.compu-art.de/mars_nwe/index.html
BuildRequires:	gdbm-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	ipxutils
Requires:	rc-scripts
Obsoletes:	mars-nwe
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nwserv

%description
MARS is a NetWare compatible file and printer server. It lets you use
a Linux machine as a file and print server for NetWare based clients
using NetWare's native IPX protocol suite.

%description -l de.UTF-8
MARS ist ein NetWare-kompatibler Datei- und Druckerserver. Er
gestattet die Verwendung eines Linux-Rechners als ein Datei- und
Druckserver für NetWare-basierende Clients unter Verwendung der
NetWare-eigenen IPX-Protokollserie.

%description -l es.UTF-8
MARS es un servidor de archivo y impresión compatible con NetWare.
Deja que uses una máquina Linux como un servidor de archivo y
impresión para clientes de NetWare usando el protocolo nativo IPX
NetWare.

%description -l fr.UTF-8
MARS est un serveur de fichiers et d'impression compatible NetWare. Il
permet d'utiliser une machine Linux comme serveur de fichiers et
d'imoression pour des clients NetWare utilisant le protocole IPX natif
de NetWare.

%description -l pl.UTF-8
MARS jest kompatybilnym z Netware serwer plików i drukarek. Pozwala
stworzyć z komputera z Linuksem serwer plików i drukarek dla klientów
Netware przy użyciu podstawowego protokołu Netware - IPX.

%description -l pt_BR.UTF-8
MARS é um servidor de arquivo e impressão compatível com NetWare. Ele
deixa você usar uma máquina Linux como um servidor de arquivo e
impressão para clientes de NetWare usando o protocolo nativo IPX
NetWare.

%description -l tr.UTF-8
MARS, NetWare uyumlu bir dosya ve yazıcı sunucusudur. Bu program bir
Linux makinenin, NetWare in doğal IPX protokol takımını kullanan
NetWare istemcilerinin dosya ve yazıcı sunucusu olarak kullanılmasını
sağlar.

%prep
%setup -q -n %{name} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%build
%{__make}
%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags} -D_GNU_SOURCE_ -DUSE_GDBM" \
	NDBMLIB="-lgdbm" \
	CRYPTLIB="-lcrypt"
%{__make} routed \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags} -D_GNU_SOURCE_ -DUSE_GDBM" \
	NDBMLIB="-lgdbm" \
	CRYPTLIB="-lcrypt"

cd examples
for I in unxcomm unxsendm; do
	%{__cc} %{rpmcflags} $I.c -o $I
done
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,logrotate.d}} \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT/var/lib/nwserv/{sys/{public/sources,login,system,mail},pipe,bindery,attrib,trustees} \
	$RPM_BUILD_ROOT/var/{run,log,spool/nwserv/{.volcache,.locks}}

install {nwserv,nwconn,ncpserv,nwclient,nwbind,nwrouted} $RPM_BUILD_ROOT%{_sbindir}

touch $RPM_BUILD_ROOT/var/log/nw.{log,routes}

install examples/nwserv.stations $RPM_BUILD_ROOT%{_sysconfdir}/nwserv.stations

install examples/nw.ini $RPM_BUILD_ROOT%{_sysconfdir}/nwserv.conf
#for I in examples/nw.ini.cnv.*; do
#	install $I $RPM_BUILD_ROOT%{_sysconfdir}/${I##examples/nw.ini}
#done
install examples/nw.ini.cnv.437 $RPM_BUILD_ROOT%{_sysconfdir}/nwserv.cnv.437

ln -sf nwserv.cnv.437 $RPM_BUILD_ROOT%{_sysconfdir}/nwserv.cnv

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/nwserv
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/nwserv

tar -xzf %{SOURCE4} -C $RPM_BUILD_ROOT/var/lib/nwserv/pipe

for I in comm comm32; do
	install examples/$I.exe $RPM_BUILD_ROOT/var/lib/nwserv/sys/public/$I.exe
done

for I in sendm comm; do
	install examples/$I.c $RPM_BUILD_ROOT/var/lib/nwserv/sys/public/sources/$I.c
done

for I in unxcomm unxsendm; do
	install examples/$I $RPM_BUILD_ROOT/var/lib/nwserv/pipe
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add nwserv
%service nwserv restart "MARS NetWare daemon"

%preun
if [ "$1" = "0" ]; then
	%service nwserv stop
	/sbin/chkconfig --del nwserv
fi

%files
%defattr(644,root,root,755)
%doc README doc examples/{README.important,nw.ini*,*.c}
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
%dir %{_sysconfdir}
%attr(600,root,root) %verify(not md5 mtime) %config %{_sysconfdir}/nwserv.conf
%attr(600,root,root) %verify(not md5 mtime) %config %{_sysconfdir}/nwserv.stations
%{_sysconfdir}/nwserv.cnv*
%attr(754,root,root) %config /etc/rc.d/init.d/nwserv
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/nwserv
%attr(755,root,root) %{_sbindir}/*
/var/lib/nwserv/sys/public/comm.exe
/var/lib/nwserv/sys/public/comm32.exe
/var/lib/nwserv/sys/public/sources/*
%attr(755,root,root) /var/lib/nwserv/pipe/*
%attr(600,root,root) %ghost /var/log/*
