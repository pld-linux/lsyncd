Summary:	Live Syncing (Mirror) Daemon
Name:		lsyncd
Version:	1.26
Release:	0.1
License:	GPL v2+
Group:		Networking/Utilities
Source0:	http://lsyncd.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	ff06aed03a012c84c0526a4f892900fe
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
URL:		http://code.google.com/p/lsyncd/
Requires:	rsync
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lsyncd uses rsync to synchronize local directories with a remote machine
running rsyncd. Lsyncd watches multiple directories trees through inotify.
The first step after adding the watches is to rsync all directories with the
remote host, and then sync single file by collecting the inotify events. So
lsyncd is a light-weight live mirror solution that should be easy to install
and use while blending well with your system.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,logrotate.d,sysconfig},/var/log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

:> $RPM_BUILD_ROOT/var/log/%{name}

install lsyncd.conf.xml $RPM_BUILD_ROOT%{_sysconfdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
#%env_update
/sbin/chkconfig --add lsyncd
%service lsyncd restart "lsync server"

%preun
#%env_update
if [ "$1" = "0" ]; then
	%service lsyncd stop
	/sbin/chkconfig --del lsyncd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/lsyncd.conf.xml
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%attr(640,root,root) %ghost /var/log/%{name}
%attr(754,root,root) /etc/rc.d/init.d/lsyncd
%{_mandir}/man1/*.1*
