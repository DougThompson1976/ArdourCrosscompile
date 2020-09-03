"""
MIT License

Copyright (c) 2020 Tremeschin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from config import *
import subprocess

class Requirements:
    def __init__(self, main):
        self.main = main

        default = {"from": "aur", "installed": False, "skip": False}

        # List of requirements (in order of installation probably)
        self.requirements = {
            # Just in case user doesn't have those
            "git":                              default,
            "waf":                              default,
            #"wine":                             default, # Some use different versions of wine
           

            # Base devek
            "autoconf":                         default,
            "automake":                         default,
            "binutils":                         default,
            "bison":                            default,
            "fakeroot":                         default,
            "file":                             default,
            "findutils":                        default,
            "flex":                             default,
            "gawk":                             default,
            "gcc":                              default,
            "gettext":                          default,
            "grep":                             default,
            "groff":                            default,
            "gzip":                             default,
            "libtool":                          default,
            "m4":                               default,
            "make":                             default,
            "pacman":                           default,
            "patch":                            default,
            "pkgconf":                          default,
            "sed":                              default,
            "sudo":                             default,
            "texinfo":                          default,
            "which":                            default,

            # Others we might need
            "python":                           default,
            "python2":                          default,

            # mingw-w64-toolchain group / base packages
            "mingw-w64-binutils":               default,
            "mingw-w64-crt":                    default,
            "mingw-w64-gcc":                    default,
            "mingw-w64-headers":                default,
            "mingw-w64-winpthreads":            default,

            # "Standard" / "isolated" mingw packages
            "mingw-w64-pkg-config":             default,
            "mingw-w64-environment":            default,
            "mingw-w64-configure":              default,
            "mingw-w64-bzip2":                  default,
            "mingw-w64-zlib":                   default,
            "mingw-w64-meson":                  default,
            "mingw-w64-make":                   default,
            "mingw-w64-cmake":                  default,
            "mingw-w64-wine":                   default,
            "mingw-w64-openssl":                default,
            "mingw-w64-xz":                     default,
            "mingw-w64-libxml2":                default,

            # Python
            "mingw-w64-libtre-git":             default,
            "mingw-w64-libsystre":              default,
            "mingw-w64-ncurses":                default,
            "mingw-w64-tcl":                    default,
            "mingw-w64-tk":                     default,
            "mingw-w64-mpdecimal":              default,
            "mingw-w64-sqlite":                 default,
            "mingw-w64-python":                 default,

            # GTK 2 / needed by

            "mingw-w64-libiconv":               default,  # libiconv usually gets stuck so just run the script again if that happens
            "mingw-w64-libjpeg-turbo":          default,
            "mingw-w64-pdcurses":               default,
            "mingw-w64-freetype2-bootstrap":    default,
            # Cairo
            "mingw-w64-libpng":                 default,
            "mingw-w64-pixman":                 default,
            "mingw-w64-libffi":                 default,
            "mingw-w64-pcre":                   default,
            "mingw-w64-readline":               default,
            "mingw-w64-termcap":                default,
            "mingw-w64-libunistring":           default,
            "mingw-w64-gettext":                default,
            "mingw-w64-glib2":                  default,
            "mingw-w64-expat":                  default,
            "mingw-w64-fontconfig":             default,
            "mingw-w64-lzo":                    default,
            "mingw-w64-cairo-bootstrap":        default, # Finally we can install cairo

            # For GTK 2
            "mingw-w64-atk":                    default,
            "mingw-w64-graphite":               default,
            "mingw-w64-harfbuzz":               default,
            "mingw-w64-fribidi":                default,
            "mingw-w64-libdatrie":              default,
            "mingw-w64-libthai":                default,
            "mingw-w64-libtiff":                default,
            "mingw-w64-lcms2":                  default,
            "mingw-w64-libssh2":                default,
            "mingw-w64-libidn2":                default,
            "mingw-w64-libpsl":                 default,
            "mingw-w64-curl":                   default,
            "mingw-w64-openjpeg2":              default,
            "mingw-w64-poppler":                default,
            "mingw-w64-pango":                  default,
            "mingw-w64-jasper":                 default,
            "mingw-w64-gdk-pixbuf2":            default,

            "mingw-w64-gtk2":                   default, # And gtk2

            # GTK2 bindings
            "mingw-w64-glibmm":                 default,
            "mingw-w64-cairomm":                default,
            "mingw-w64-pangomm":                default,
            "mingw-w64-atkmm":                  default,
            "mingw-w64-gtkmm":                  default,

            # Boost
            "mingw-w64-boost":                  default,

            # Packages Ardour need
            "mingw-w64-serd":                   default,
            "mingw-w64-sord":                   default,
            "mingw-w64-sratom":                 default,
            "mingw-w64-libsndfile":             default,
            "mingw-w64-libsamplerate":          default,
            "mingw-w64-lz4":                    default,
            "mingw-w64-gmp":                    default,
            "mingw-w64-nettle":                 default,
            "mingw-w64-libarchive":             default,
            "mingw-w64-liblo":                  default,
            "mingw-w64-cppunit":                default,
            "mingw-w64-taglib":                 default,
            "mingw-w64-vamp-plugin-sdk":        default,
            "mingw-w64-fftw":                   default,
            "mingw-w64-ladspa-sdk":             default,
            "mingw-w64-rubberband":             default,

            # Jack audio / "not specific" but needed, better
            "mingw-w64-eigen":                  default,
            "mingw-w64-opus":                   default,
            "mingw-w64-opusfile":               default,
            "mingw-w64-portaudio":              default,
            "mingw-w64-ffmpeg-minimal":         default,
            "mingw-w64-gst-libav":              default,
            "mingw-w64-gst-plugins-base":       default,


            
            
            # Not needed but listed as optional deps, optimal for a full build
            
            "mingw-w64-vulkan-headers":         default,
            "mingw-w64-dbus":                   default,
            "mingw-w64-postgresql":             default,
            "mingw-w64-mariadb-connector-c":    default,
            "mingw-w64-libusb":                 default,
            "mingw-w64-pcre2":                  default,

            # We need aubio as well but that is done manually on actions
        }

    def check_installed(self):
        self.main.utils.sprint(f"Checking already installed packages from requirements", 'i')

        for pkgname in self.requirements.keys():
            is_installed = self.main.pacman.is_package_installed(pkgname)
            self.requirements[pkgname]["installed"] = is_installed

        # Get number of installed packages and needed
        installed = 0

        for item in self.requirements.values():
            installed += item["installed"]

        needed = len(self.requirements.keys()) - installed

        self.main.utils.sprint(f"Status of packages: installed [{installed}], missing [{needed}]", 'i')



class Pacman:
    def __init__(self, main):
        self.main = main
        self.requirements = Requirements(self.main)

        # We run yay -Sy first time installing a package
        self.first_time = True

    # `pacman -Qq` --> Python list
    def get_installed_packages(self):
        self.main.utils.sprint(f"Getting / updating installed packages", 'c')
        
        # Pacman -Q to query, q to only show name, not version, decode the output and split on lines
        self.installed = subprocess.check_output(['pacman', '-Qq']).decode("utf-8").split("\n")

        self.main.utils.sprint(f"Got installed packages, len=({len(self.installed)})", 'o')

    # Is this package listed on installed packages on pacman?
    def is_package_installed(self, name):
        self.main.utils.sprint(f"Checking if package is installed [{name}]", 'c')
        
        exists = name in self.installed

        if exists:
            self.main.utils.sprint(f"Yes", 'o')
            return True
        else:
            self.main.utils.sprint(f"No", 'w')
            return False
    
    def has_noconfirm(self) -> str:
        if NOCONFIRM:
            return "--noconfirm"
        else:
            return ""
    
    def Syu(self):
        yay = self.main.get_subprocess_utils()
        yay.from_string(f"yay -Syu {self.has_noconfirm()}")
        yay.run(shell = True)
        yay.wait()

    # Install a package from Requirements class,
    # we also define how to install custom packages here namely aubio for mingw
    def install_package(self, name: str) -> None:
        self.main.utils.sprint(f"Installing package with name [{name}]", 'i')

        # Skip install if already installed
        if self.is_package_installed(name):
            self.main.utils.sprint(f"Package is already installed, skipping", 'o')
            return
            
        # Get Requirements info
        req_info = self.requirements.requirements[name]

        # Do we want to skip the package?
        skip = req_info.get("skip", None)
        if skip == True:
            self.main.utils.sprint(f"Skip installing package as configured on Requirements class", 'w')
        elif skip is None:
            self.main.utils.sprint(f"No skip argument found on dictionary, considering False", 'w')

        # Where the package is from?
        pkg_from = req_info.get("from", None)

        # Default to "AUR"
        if pkg_from is None:
            self.main.utils.sprint(f"No \"from\" argument found, defaulting to AUR", "w")

        self.main.utils.sprint(f"Package is from {pkg_from}", 'i')

        # Just for being safe
        if pkg_from in ["aur", "community", "extra"]:
            yay = self.main.get_subprocess_utils()
            # --needed because we install some package groups like base-devel
            yay.from_string(' '.join(["yay", "-S", self.has_noconfirm(), "--needed", name]))
            yay.run(shell = True) # YES shell=True is "dangerous", but we are using a package manager, there is no easier way
            
        # Update installed packages
        self.get_installed_packages()
