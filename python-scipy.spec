%define enable_atlas 1
%{?_with_atlas: %global enable_atlas 1}

%define module	scipy
%define name	python-%{module}
%define version 0.8.0
%define release %mkrel 1

%define Werror_cflags %nil

Summary:	Scientific tools for Python
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{module}-%{version}.tar.gz
Patch0:		umfpack-setup.py.patch
License:	BSD
Group:		Development/Python
BuildRoot:	%{_tmppath}/%{name}-buildroot
Url:		http://www.scipy.org
Obsoletes:	python-SciPy
Obsoletes:	python-symeig
Requires:	python-numpy >= 1.4.1
BuildRequires:	swig
%if %enable_atlas
BuildRequires:	libatlas-devel
%else
BuildRequires:	blas-devel
%endif 
BuildRequires:	lapack-devel 
BuildRequires:	python-numpy-devel >= 1.4.1
BuildRequires:	gcc-gfortran >= 4.0
BuildRequires:	netcdf-devel
BuildRequires:	python-nose
%py_requires -d
%if %{mdkversion} <= 200800
# Needed to prevent older amd/umfpack devel packages from interfering with
# build on 2008.0:
BuildRequires:	amd-devel = 2.2.0, umfpack-devel = 5.2.0
%else
BuildRequires:	amd-devel umfpack-devel
%endif
BuildRequires:	python-sphinx
BuildRequires:	python-matplotlib

%description
SciPy is an open source library of scientific tools for Python. SciPy
supplements the popular numpy module, gathering a variety of high level
science and engineering modules together as a single package.

SciPy includes modules for graphics and plotting, optimization, integration,
special functions, signal and image processing, genetic algorithms, ODE 
solvers, and others.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p0 -b .umfpack

%build

# Make sure that gcc 4 is being used to build the package:
GCC_VERSION=`gcc --version | awk 'NR == 1 {print $3}'`
if echo $GCC_VERSION | grep ^4 > /dev/null; then
   export CC=gcc-$GCC_VERSION
else
   echo "Need GCC 4 to build"
   exit 1
fi

export CC=gcc-$GCC_VERSION

CFLAGS="%{optflags} -fPIC -O3" PYTHONDONTWRITEBYTECODE= %__python setup.py config_fc --fcompiler=gnu95 build

pushd doc
export PYTHONPATH=`dir -d ../build/lib.linux*`
%__make html
popd

%install
%__rm -rf %{buildroot}
CFLAGS="%{optflags} -fPIC -O3" PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot} 

# Remove doc files that should be in %doc:
%__rm -f %{buildroot}%{py_platsitedir}/%{module}/*.txt

%check
pushd doc &> /dev/null
PYTHONPATH=%{buildroot}%{py_platsitedir} python -c "import scipy; scipy.test()"
popd &> /dev/null

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.txt THANKS.txt LATEST.txt LICENSE.txt TOCHANGE.txt doc/build/html
%dir %{py_platsitedir}/%{module}
%{py_platsitedir}/%{module}/*
%{py_platsitedir}/%{module}-*.egg-info
