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


class Requirements:
    def __init__(self, main):
        self.main = main

        debug_prefix = "[Requirements.__init__]"

        default = {"from": "aur", "installed": False, "skip": False}
        tremx_pkgbuild = {"from": "tremx_pkgbuild", "installed": False, "skip": False}

        # We're running on WSL so we use fakeroot-tcp not arch's fakeroot
        if "wsl" in self.main.flags:
            fakeroot_dep = "fakeroot-tcp"
            print(debug_prefix, f"RUNNING ON WSL, FAKEROOT DEP IS [{fakeroot_dep}]")
        else:
            # Default Arch fakeroot
            fakeroot_dep = "fakeroot"
            print(debug_prefix, f"NOT RUNNING ON WSL, FAKEROOT DEP IS [{fakeroot_dep}]")

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
            fakeroot_dep:                       default,
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
            "mingw-w64-freetype2":              default,
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
            # "mingw-w64-cairo-bootstrap":        default, # Finally we can install cairo
            "mingw-w64-cairo":                  default, 

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
            "mingw-w64-lilv":                   default,

            # Jack audio / "not specific" but needed, better audio support

            "mingw-w64-eigen":                  default,
            "mingw-w64-opus":                   default,
            "mingw-w64-opusfile":               default,
            "mingw-w64-portaudio":              default,
            "mingw-w64-ffmpeg-minimal":         default, # This takes a while but welp it's FFmpeg
            
            # For GST plugins
            "mingw-w64-orc":                    default,
            "mingw-w64-libtheora":              default,
            "mingw-w64-libvisual":              default,
            "mingw-w64-gstreamer":              default,
            "mingw-w64-gst-plugins-base":       default,
            "mingw-w64-gst-libav":              default,

            
            # Not needed but listed as optional deps, optimal for a full build
            
            "mingw-w64-vulkan-headers":         default,
            "mingw-w64-dbus":                   default,
            "mingw-w64-postgresql":             default,
            "mingw-w64-mariadb-connector-c":    default,
            "mingw-w64-libusb":                 default,
            "mingw-w64-pcre2":                  default,

            # You can safely remove those (probably), just trying to get everything ardour checks
            "mingw-w64-clang-git":              default,
            # "mingw-w64-libwebsockets":          default, # broken PKGBUILD 

            # We need aubio as well but that is done manually on actions


            # # # TREMESCHIN PKGBUILDS FOR 32 BIT # # #
            # "mingw-w32-vamp-sdk":               tremx_pkgbuild,
            # "mingw-w32-vamp-ladspa":            tremx_pkgbuild,
            # "mingw-w32-vamp-rubberband":        tremx_pkgbuild,
        }

        self.main.utils.sprint(f"Len of package dependencies: [{len(self.requirements.keys())}]", 'i')

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

