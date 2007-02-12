%define		dictname dalf
Summary:	Russian monolingual dictionary dalf for dictd
Summary(pl.UTF-8):   Słownik rosyjsko-rosyjski dalf dla dictd
Name:		dict-%{dictname}
Version:	1.0
Release:	2
License:	unknown
Group:		Applications/Dictionaries
Source0:	http://www.chat.ru/~muller_dic/dalf.gz
# Source0-md5:	395ca06b4e38399e1a91bf89d51ae289
Patch0:		%{dictname}.patch
URL:		http://www.chat.ru/~muller_dic/
BuildRequires:	dictfmt
BuildRequires:	dictzip
Requires:	%{_sysconfdir}/dictd
Requires:	dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Russian monolingual dictionary for dictd encoded in koi8-r. Start
server with --locale ru_RU.KOI8-R option in order to use it.

%description -l pl.UTF-8
Słownik rosyjsko-rosyjski dla dictd kodowany w koi8-r. Uruchom serwer
z opcją --locale ru_RU.KOI8-R, żeby móc go używać.

%description -l ru.UTF-8
Словарь Даля, переработанный из CD источника "Библиотека в Кармане".

%prep
%setup -q -c -T
%{__gzip} -dc %{SOURCE0} > dalf
%patch0 -p0

%build
LC_ALL=ru_RU.KOI8-R perl -ne 'use locale; /^(.*?)[\.,;\?]*  (.*)\n/; $def=$2; $word=$1; $word=~s/[\?,]+ /|/g; print ":".lc($word).":\n$def\n"' < dalf | \
	dictfmt -j -u http://www.chat.ru/~muller_dic/ -s %{dictname} --locale ru_RU.KOI8-R --headword-separator \| %{dictname}
dictzip %{dictname}.dict

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd,%{_sysconfdir}/dictd}

dictprefix=%{_datadir}/dictd/%{dictname}
echo "# dalf russian monolingual dictionary
database %{dictname} {
	data  \"$dictprefix.dict.dz\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}.dictconf
mv %{dictname}.* $RPM_BUILD_ROOT%{_datadir}/dictd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%postun
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2 || true
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dictd/%{dictname}.dictconf
%{_datadir}/dictd/%{dictname}.*
