%define major   0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Name:			rtl-sdr
URL:			https://sdr.osmocom.org/trac/wiki/rtl-sdr
Version:		2.0.2
Release:		1
License:		GPL-2.0-or-later
Group:			Communications/Radio
Summary:		SDR utilities for Realtek RTL2832 based DVB-T dongles
Source0:		https://github.com/osmocom/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildSystem:	cmake
BuildOption(prep):	-p1
BuildOption:	-DDETACH_KERNEL_DRIVER=ON
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(libusb)
Requires(pre):	shadow-utils

%description
This package can turn your RTL2832 based DVB-T dongle into an SDR receiver.

%package -n %{libname}
Summary:	Library files for rtl-sdr
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
Library files for rtl-sdr.

%package -n %{devname}
Summary:	Development files for rtl-sdr
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for rtl-sdr.

%prep -a
rm -rf src/getopt

%install -a
# remove static libs
rm -f %{buildroot}%{_libdir}/*.a

# Fix udev rules and allow access only to users in rtlsdr group
sed -i 's/MODE:="0666"/MODE:="0660", ENV{ID_SOFTWARE_RADIO}="1"/' rtl-sdr.rules
install -Dpm 644 rtl-sdr.rules %{buildroot}%{_udevrulesdir}/10-rtl-sdr.rules

# Fix Version string in librtlsdr.pc
sed -i '/Version/c Version: %{version}' %{buildroot}%{_libdir}/pkgconfig/librtlsdr.pc

%files
%doc AUTHORS
%{_bindir}/rtl_{adsb,biast,eeprom,fm,power,sdr,tcp,test}
%{_udevrulesdir}/10-rtl-sdr.rules

%files -n %{libname}
%{_libdir}/*.so.%{major}{,.*}

%files -n %{devname}
%{_includedir}/rtl-sdr*.h
%{_libdir}/librtlsdr.so
%{_libdir}/pkgconfig/librtlsdr.pc
