%define major   0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Name:             rtl-sdr
URL:              https://sdr.osmocom.org/trac/wiki/rtl-sdr
Version:          0.6.0
Release:          3
License:          GPLv2+
Group:            Communications/Radio
Summary:          SDR utilities for Realtek RTL2832 based DVB-T dongles
Source0:          https://github.com/osmocom/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:    cmake
BuildRequires:    pkgconfig(libusb)
Requires(pre):    shadow-utils

%description
This package can turn your RTL2832 based DVB-T dongle into an SDR receiver.

%package -n %{libname}
Summary:          Library files for rtl-sdr
Group:            System/Libraries
Requires:         %{name} = %{version}-%{release}

%description -n %{libname}
Library files for rtl-sdr.

%package -n %{devname}
Summary:          Development files for rtl-sdr
Group:            System/Libraries
Requires:         %{libname} = %{version}-%{release}
Provides:         %{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for rtl-sdr.

%prep
%autosetup -p1

rm -rf src/getopt

%build
%cmake -DDETACH_KERNEL_DRIVER=ON
%make_build

%install
%make_install -C build

# remove static libs
rm -f %{buildroot}%{_libdir}/*.a

# Fix udev rules and allow access only to users in rtlsdr group
sed -i 's/MODE:="0666"/MODE:="0660", ENV{ID_SOFTWARE_RADIO}="1"/' rtl-sdr.rules
install -Dpm 644 rtl-sdr.rules %{buildroot}%{_udevrulesdir}/10-rtl-sdr.rules

# Fix Version string in librtlsdr.pc
sed -i '/Version/c Version: %{version}' %{buildroot}%{_libdir}/pkgconfig/librtlsdr.pc

%files
%doc AUTHORS
%{_bindir}/*
%{_udevrulesdir}/10-rtl-sdr.rules

%files -n %{libname}
%{_libdir}/*.so.%{major}{,.*}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/librtlsdr.pc
