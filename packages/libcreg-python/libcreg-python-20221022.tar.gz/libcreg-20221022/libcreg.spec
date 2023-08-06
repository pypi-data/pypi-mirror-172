Name: libcreg
Version: 20221022
Release: 1
Summary: Library to access the Windows 9x/Me Registry File (CREG) format
Group: System Environment/Libraries
License: LGPLv3+
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libcreg
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
            
BuildRequires: gcc            

%description -n libcreg
Library to access the Windows 9x/Me Registry File (CREG) format

%package -n libcreg-static
Summary: Library to access the Windows 9x/Me Registry File (CREG) format
Group: Development/Libraries
Requires: libcreg = %{version}-%{release}

%description -n libcreg-static
Static library version of libcreg.

%package -n libcreg-devel
Summary: Header files and libraries for developing applications for libcreg
Group: Development/Libraries
Requires: libcreg = %{version}-%{release}

%description -n libcreg-devel
Header files and libraries for developing applications for libcreg.

%package -n libcreg-python3
Summary: Python 3 bindings for libcreg
Group: System Environment/Libraries
Requires: libcreg = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libcreg-python3
Python 3 bindings for libcreg

%package -n libcreg-tools
Summary: Several tools for reading Windows 9x/Me Registry Files (CREG)
Group: Applications/System
Requires: libcreg = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libcreg-tools
Several tools for reading Windows 9x/Me Registry Files (CREG)

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libcreg
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libcreg-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libcreg-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcreg.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libcreg-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libcreg-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Oct 22 2022 Joachim Metz <joachim.metz@gmail.com> 20221022-1
- Auto-generated

