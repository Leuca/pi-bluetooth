# No binaries are built
%global debug_package %{nil}

Name:           {{{ git_dir_name }}}
Version:        {{{ git_dir_version lead=0.1 follow=19 }}}
Release:        1%{?dist}
Summary:        Load BCM43430A1 firmware on boot 

License:        BSD-3
URL:            https://github.com/RPi-Distro/pi-bluetooth
VCS:            {{{ git_dir_vcs }}}

ExclusiveArch:  aarch64 %{arm}

BuildRequires:  systemd-rpm-macros

Requires:       bluez
Requires:       bluez-deprecated
Requires:       bluez-firmware
Requires:       rpi-udev-rules

Source:         {{{ git_dir_pack }}}

%description
Load BCM43430A1 firmware on boot through systemd

%prep
{{{ git_dir_setup_macro }}}

%build
# Nothing to build

%install
# Install scripts
mkdir -p %{buildroot}%{_bindir}
install -m 0755 usr/bin/bthelper %{buildroot}%{_bindir}
install -m 0755 usr/bin/btuart %{buildroot}%{_bindir}

# Install systemd units
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 debian/pi-bluetooth.bthelper@.service %{buildroot}%{_unitdir}
install -m 0644 debian/pi-bluetooth.hciuart.service %{buildroot}%{_unitdir}

# Install udev rules
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
install -m 0644 lib/udev/rules.d/90-pi-bluetooth.rules %{buildroot}%{_prefix}/lib/udev/rules.d

%post
%systemd_post pi-bluetooth.bthelper@.service
%systemd_post pi-bluetooth.hciuart.service

%preun
%systemd_preun pi-bluetooth.bthelper@.service
%systemd_preun pi-bluetooth.hciuart.service

%postun
%systemd_postun_with_restart pi-bluetooth.bthelper@.service
%systemd_postun_with_restart pi-bluetooth.hciuart.service

%files
%license debian/copyright
%doc debian/control debian/changelog
%{_bindir}/bthelper
%{_bindir}/btuart
%{_unitdir}/pi-bluetooth.bthelper@.service
%{_unitdir}/pi-bluetooth.hciuart.service
%{_prefix}/lib/udev/rules.d/90-pi-bluetooth.rules

%changelog
* Fri Nov 04 2022 Luca Magrone <luca@magrone.cc> - 0.1.19-1
- Initial package
