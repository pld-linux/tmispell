Summary:	Ispell compatible front-end for spell-checking modules
Summary(pl.UTF-8):	Zgodny z Ispellem frontend dla modułów sprawdzających pisownię
Name:		tmispell
Version:	0.5.0
Release:	1
License:	GPL v2+
Group:		Applications/Text
#Source0Download: https://github.com/voikko/tmispell/releases
Source0:	https://github.com/voikko/tmispell/archive/rel-0.5.0/%{name}-%{version}.tar.gz
# Source0-md5:	d7f745f3618c2f480faa36fd4fb0fe72
Patch0:		%{name}-glibmm.patch
URL:		http://voikko.puimula.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	enchant-devel >= 1.1.6
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	glibmm-devel >= 2.4.0
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	libtool >= 2:1.5
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tmispell is a transparent wrapper around Ispell. Many programs (e.g.
mail clients and document processors) use Ispell for spell-checking.
Since Tmispell imitates Ispell, these programs use automatically
Tmispell (and therefore e.g. Voikko) without any changes needed.
Additionally Tmispell can launch the real Ispell if there is no module
for the selected language.

%description -l pl.UTF-8
Tmispell to przezroczysty wrapper na Ispella. Wiele programów (np.
klientów pocztowych czy procesorów tekstu) wykorzystuje Ispella do
sprawdzania pisowni. Ponieważ Tmispell imituje Ispella, programy te
automatycznie używają Tmispella (i poprzez niego np. Voikko) bez
potrzeby żadnych zmian. Ponadto Tmispell potrafi uruchomić prawdziwego
Ispella, jeśli nie ma modułu dla wybranego języka.

%prep
%setup -q -n tmispell-rel-%{version}
%patch -P0 -p1

# force system glibmm
%{__rm} -r src/glibmm

# missing file
grep -l -e '\<_\>' src/*.cc enchant/*.cc > po/POTFILES.in

%build
%{__glib_gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CXXFLAGS="%{rpmcxxflags} -std=c++0x"
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# voikko module already included in enchant sources
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/enchant

%find_lang tmispell-voikko

%clean
rm -rf $RPM_BUILD_ROOT

%files -f tmispell-voikko.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%lang(fi) %doc LUEMINUT NEWS.fi
%attr(755,root,root) %{_bindir}/tmispell
%{_mandir}/man1/tmispell.1*
%{_mandir}/man5/tmispell.conf.5*
