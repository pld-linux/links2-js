#
# Conditional build:
%bcond_without	javascript	# build without JavaScript interpreter
%bcond_without	graphics	# build without graphics support
%bcond_without	fb		# build without Linux Framebuffer graphics driver
%bcond_without	sdl		# build without SDL graphics driver
%bcond_without	svga		# build without svgalib graphics driver
%bcond_without	x		# build without X Window System graphics driver
#
Summary:	Lynx-like WWW browser
Summary(es.UTF-8):	El links es un browser para modo texto, similar a lynx
Summary(pl.UTF-8):	Podobna do Lynksa przeglądarka WWW
Summary(pt_BR.UTF-8):	O links é um browser para modo texto, similar ao lynx
Summary(ru.UTF-8):	Текстовый WWW броузер типа Lynx
Summary(uk.UTF-8):	Текстовий WWW броузер типу Lynx
Name:		links2
%define	pre	pre28
# XXX: stop using "pre" in Version after 2.1 release!
Version:	2.1%{pre}
Release:	2
Epoch:		1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://links.twibright.com/download/links-%{version}.tar.bz2
# Source0-md5:	815afe558dd548258eeb03b01cce01ce
Source1:	%{name}.desktop
Source2:	%{name}.1.pl
Source3:	%{name}.png
Source4:	glinks.desktop
Patch0:		%{name}-links-g_if_glinks.patch
Patch1:		%{name}-ac25x.patch
Patch2:		%{name}-img.patch
Patch3:		%{name}-convert-old-bookmarks.patch
Patch4:		%{name}-cookies-save.patch
Patch5:		%{name}-config-dirs.patch
Patch6:		%{name}-gzip_fallback.patch
Patch7:		%{name}-js-Date-getTime.patch
Patch8:		%{name}-js-submit-nodefer.patch
Patch9:		%{name}-segv.patch
Patch10:	%{name}-pl-update.patch
#Patch15:	%{name}-home_etc.patch
URL:		http://links.twibright.com/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
%{?with_javascript:BuildRequires:	bison}
BuildRequires:	bzip2-devel
%{?with_javascript:BuildRequires:	flex}
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel >= 5.1
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	zlib-devel
%if %{with graphics}
%{?with_fb:BuildRequires:	DirectFB-devel >= 0.9.17}
%{?with_sdl:BuildRequires:	SDL-devel >= 1.2.0}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
%{?with_svga:BuildRequires:	svgalib-devel}
%{?with_x:BuildRequires:	xorg-lib-libX11-devel}
%endif
Provides:	webclient
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Links is a WWW browser, at first look similiar to Lynx, but somehow
different:

- renders tables and frames,
- displays colors as specified in current HTML page,
- uses drop-down menu (like in Midnight Commander),
- can download files in background.

%{?with_graphics:This version can work in graphical mode.}
%{?with_javascript:This version has support for JavaScript.}

%description -l es.UTF-8
Links es un browser WWW modo texto, similar al Lynx. El links muestra
tablas, hace baja archivos en segundo plano, y usa conexiones HTTP/1.1
keepalive.

%description -l pl.UTF-8
Links jest przeglądarką WWW, na pierwszy rzut oka podobną do Lynksa,
ale mimo wszystko inną:

- renderuje tabelki i ramki,
- wyświetla kolory zgodnie z definicjami w oglądanej stronie HTML,
- używa opuszczanego menu (jak w Midnight Commanderze),
- może ściągać pliki w tle.

%{?with_graphics:Ta wersja może pracować w trybie graficznym.}
%{?with_javascript:Ta wersja obsługuje JavaScript.}

%description -l pt_BR.UTF-8
Links é um browser WWW modo texto, similar ao Lynx. O Links exibe
tabelas, faz baixa arquivos em segundo plano, e usa as conexões
HTTP/1.1 keepalive.

%description -l ru.UTF-8
Links - это текстовый WWW броузер, на первый взгляд похожий на Lynx,
но несколько отличающийся:

- отображает таблицы и (скоро) фреймы,
- показывает цвета как указано в HTML странице,
- использует выпадающие меню (как в Midnight Commander),
- может загружать файлы в фоне.

%description -l uk.UTF-8
Links - це текстовий WWW броузер, на перший погляд схожий на Lynx, але
трохи відмінний від нього:

- відображає таблиці та (незабаром) фрейми,
- показує кольори як вказано в HTML сторінці,
- використовує випадаючі меню (як в Midnight Commander),
- може завантажувати файли в фоні.

%prep
%setup -q -n links-%{version}
%{?with_graphics:%patch0 -p1}
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1
%patch -P9 -p1
%patch -P10 -p1

cd intl
./gen-intl

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--program-suffix=2 \
	%{?with_graphics:--enable-graphics} \
	%{?with_javascript:--enable-javascript} \
	%{!?with_fb:--without-fb} \
	%{!?with_sdl:--without-sdl} \
	%{!?with_svga:--without-svgalib} \
	%{!?with_x:--without-x}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_mandir}/pl/man1

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with graphics}
ln -sf links2 $RPM_BUILD_ROOT%{_bindir}/glinks
echo ".so links2.1" > $RPM_BUILD_ROOT%{_mandir}/man1/glinks.1
echo ".so links2.1" > $RPM_BUILD_ROOT%{_mandir}/pl/man1/glinks.1
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
%endif

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/pl/man1/links2.1
install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README SITES TODO
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{_mandir}/man*/*
%lang(pl) %{_mandir}/pl/man*/*
