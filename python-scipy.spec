%define module	scipy
%define name	python-%{module}
%define version 0.6.0
%define release 3

Summary:	Scientific tools for Python
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Source0:	%{module}-%{version}.tar.bz2
Source1:	randomkit.tar.bz2
Patch0:		sandbox-setup.patch
Patch1:		montecarlo-setup.py.patch
Patch2:		montecarlo.py.patch
Patch3:		umfpack-setup.py.patch
Source2:	enabled_packages.txt
License:	BSD
Group:		Development/Python
BuildRoot:	%{_tmppath}/%{name}-buildroot
Url:		http://www.scipy.org
Obsoletes:	python-SciPy
Requires:	python, python-numpy >= 1.0
BuildRequires:	swig
BuildRequires:	python-devel, fftw-devel, blas-devel, lapack-devel 
BuildRequires:	python-numpy-devel >= 1.0, python-numpy >= 1.0
BuildRequires:	gcc >= 4.0, gcc-gfortran >= 4.0
BuildRequires:	libumfpack5-devel, libamd2-devel
BuildRequires:	libx11-devel, netcdf-devel

%description
SciPy is an open source library of scientific tools for Python. SciPy
supplements the popular numpy module, gathering a variety of high level
science and engineering modules together as a single package.

SciPy includes modules for graphics and plotting, optimization, integration,
special functions, signal and image processing, genetic algorithms, ODE 
solvers, and others.

%prep
%setup -n %{module}-%{version} -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0

%__tar jfx %SOURCE1 -C ./scipy/sandbox/montecarlo/src
%__cp %SOURCE2 ./scipy/sandbox/

%build

# Use netlib BLAS/LAPACK:
export BLAS=%{_libdir}/libblas.a
export LAPACK=%{_libdir}/liblapack.a
export ATLAS=None

# Make sure that gcc 4 is being used to build the package:
GCC_VERSION=`gcc --version | awk 'NR == 1 {print $3}'`
if echo $GCC_VERSION | grep ^4 > /dev/null; then
   export CC=gcc-$GCC_VERSION
else
   echo "Need GCC 4 to build"
   exit 1
fi

export CC=gcc-$GCC_VERSION

CFLAGS="-fPIC" %__python setup.py config_fc --fcompiler=gnu95 build

%install
%__rm -rf %{buildroot}

export BLAS=%{_libdir}/libblas.a
export LAPACK=%{_libdir}/liblapack.a
export ATLAS=None

%__python setup.py config_fc --fcompiler=gnu95 install --root=%{buildroot} --record=INSTALLED_FILES.tmp

# Don't include original test files:
%__grep -Ev "\\.orig$" INSTALLED_FILES.tmp > INSTALLED_FILES

## Uncomment the following once the scipy tests are stable ##
#%check
#export PYTHONPATH=%{buildroot}/%{_libdir}/python%{pyver}/site-packages/
#echo $PYTHONPATH
# python -c "import scipy; scipy.test(level=1, verbosity=2)"

%clean
%__rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc *.txt




