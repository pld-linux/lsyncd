Summary:	Lsyncd - Live Syncing (Mirror) Daemon
Name:		lsyncd
Version:	2.2.3
Release:	0.1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	https://github.com/axkibe/lsyncd/archive/release-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	25d36b73946bec822d5c7f258262d9f3
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
URL:		https://github.com/axkibe/lsyncd
BuildRequires:	cmake
BuildRequires:	libxml2-devel
Requires:	rsync >= 3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lsyncd uses rsync to synchronize local directories with a remote
machine running rsyncd. Lsyncd watches multiple directories trees
through inotify. The first step after adding the watches is to rsync
all directories with the remote host, and then sync single file by
collecting the inotify events. So lsyncd is a light-weight live mirror
solution that should be easy to install and use while blending well
with your system.

%prep
%setup -q -n %{name}-release-%{version}

%build
install -d build
cd build
%cmake \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,logrotate.d,sysconfig},/var/log,%{_mandir}/man1}
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT{%{_prefix}/''man/*.1,%{_mandir}/man1}

touch $RPM_BUILD_ROOT/var/log/%{name}
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add lsyncd
%service lsyncd restart "lsync server"

%preun
if [ "$1" = "0" ]; then
	%service lsyncd stop
	/sbin/chkconfig --del lsyncd
fi

%files
%defattr(644,root,root,755)
%doc README.md
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/lsyncd.1*
%attr(640,root,root) %ghost /var/log/%{name}
%attr(754,root,root) /etc/rc.d/init.d/lsyncd
