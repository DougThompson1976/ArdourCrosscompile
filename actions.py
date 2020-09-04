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

from bs4 import BeautifulSoup
import urllib.request
from config import *
import shutil
import os

class Actions:
    def __init__(self, main):
        self.main = main

    def run(self):

        # Clone the repository of ardour
        if CLONE_ARDOUR:
            self.main.utils.sprint("CLONE_ARDOUR", 'a')
            self.main.download.git_clone("https://github.com/Ardour/ardour", self.main.directories.ardour)
        
        # Pull latest commit, overwrite local made changes
        if RESET:
            self.main.utils.sprint("RESET", 'a')
            gitshell = self.main.get_subprocess_utils()
            gitshell.from_string((
                f"cd \"{self.main.directories.ardour}\" && "
                "git fetch --all && "
                "git reset --hard origin/master"
            ))
            gitshell.run(shell=True)
    
        # Get installed packages
        self.main.pacman.get_installed_packages()

        # Get a list of installed packages
        if CHECK_NEEDED_PACKAGES:
            self.main.utils.sprint("CHECK_NEEDED_PACKAGES", 'a')
            self.main.pacman.requirements.check_installed()

        if INSTALL_AUR_PACKAGES:
            self.main.utils.sprint("INSTALL_AUR_PACKAGES", 'a')
            for package in self.main.pacman.requirements.requirements.keys():
                if self.main.pacman.requirements.requirements[package]["from"] == "aur":
                    self.main.pacman.install_package(package)
        
        # Compile for x86_64 (64 bit)
        if XARCH_X86_64:

            mingw_pfx = "x86_64-w64-mingw32"
            plugin_arch = "w64"
            bundle_directory = self.main.directories.bundle_64
            lv2_bundle_directory = self.main.directories.lv2_bundled_64

            self.main.utils.sprint("SET XARCH to x86_64", 'a')

            for file in ["/tools/x-win/compile.sh", "/tools/x-win/package.sh"]:
                self.main.utils.sed_replace(
                    ": ${XARCH=i686}",
                    ": ${XARCH=x86_64}",
                    self.main.directories.ardour + file
                )
        else:
            self.main.utils.sprint("SET XARCH to default i686", 'a')

            mingw_pfx = "i686-w64-mingw32"
            plugin_arch = "w32"
            bundle_directory = self.main.directories.bundle_32
            lv2_bundle_directory = self.main.directories.lv2_bundled_32

        
        # Set audio backends we will compile
        self.main.utils.sprint(f"SET AUDIO BACKENDS TO [{AUDIO_BACKENDS}]", 'a')
        
        for line in ["--with-backends=dummy,wavesaudio", "--with-backends=jack,dummy"]:
            self.main.utils.sed_replace(
                line,
                f"--with-backends={AUDIO_BACKENDS}",
                self.main.directories.ardour + "/tools/x-win/compile.sh"
            )

        # Enable Windows VST
        self.main.utils.sprint("ENABLE WINDOWS VST", 'a')
        self.main.utils.sed_replace(
            "--dist-target=mingw \\",
            f"--dist-target=mingw \\\n	--windows-vst \\",
            self.main.directories.ardour + "/tools/x-win/compile.sh"
        )
        
        if OPTIMIZED:
            self.main.utils.sprint("OPTIMIZED", 'a')
            self.main.utils.sed_replace(
                "--dist-target=mingw \\",
                f"--dist-target=mingw \\\n	--optimize \\",
                self.main.directories.ardour + "/tools/x-win/compile.sh"
            )
            
        # Get mingw binaries filenames
        pkgconfig = mingw_pfx + "-pkg-config"
        mingw_gcc = mingw_pfx + "-gcc"
        mingw_gpp = mingw_pfx + "-g++"
        mingw_ld =  mingw_pfx + "-ld"


        # Doesn't really work, TODO
        if INSTALL_MINGW_JACK:

            raise RuntimeError("Mingw Jack is finicky, prefer not to")

            self.main.utils.sprint("INSTALL_MINGW_JACK", 'a')
            
            jack2_repo_path = self.main.directories.workspace + "jack_mingw"
            self.main.download.git_clone("https://github.com/jackaudio/jack2", jack2_repo_path)

            cmd = (
                f"cd \"{jack2_repo_path}\" && "
                f"IS_WINDOWS=true LD=/usr/bin/{mingw_ld} CC=/usr/bin/{mingw_gcc} CXX=/usr/bin/{mingw_gpp} PKGCONFIG=/usr/bin/{pkgconfig} ./waf configure && "
                "./waf build"
            )
            
            self.main.utils.sprint(f"Running command [{cmd}]", 'i')
            os.system(cmd)
        else:
            # Remove --with-backends=jack from ARDOURCFG
            self.main.utils.sed_replace(
                "--with-backends=jack,",
                "--with-backends=",
                self.main.directories.ardour + "/tools/x-win/compile.sh"
            )
            

        if INSTALL_AUBIO:
            self.main.utils.sprint("INSTALL_AUBIO", 'a')

            # This was the latest version I could compile successfully
            version = "0.4.8"

            aubio_source_code = self.main.directories.workspace + f"aubio-{version}.zip"
            
            self.main.download.wget(
                url = f"https://github.com/aubio/aubio/archive/{version}.zip",
                save = aubio_source_code,
                name = "Aubio Source Code",
            )
            self.main.utils.unzip(
                aubio_source_code,
                self.main.directories.workspace
            )

            aubio_folder = self.main.directories.workspace + f"aubio-{version}/"

            # Need Python2 on this version of aubios
            self.main.utils.sed_replace(
                "  ./waf", # We add trailing spaces as if we run the program again and re-overwrite
                "  python2 ./waf",
                f"{aubio_folder}/scripts/build_mingw"
            )

            self.main.utils.sed_replace(
                "WAFCMD=python waf", # We add trailing spaces as if we run the program again and re-overwrite
                "WAFCMD=python2 waf",
                f"{aubio_folder}/Makefile"
            )

            # Build aubio
            cmd = (
                f"cd \"{self.main.directories.workspace}aubio-{version}\" && "
                "chmod +x scripts/* && " # Mark scripts as executable
                "bash scripts/build_mingw"
            )
            self.main.utils.sprint(f"Running command [{cmd}]", 'i')
            os.system(cmd)

            # We compiled aubio and it gifts us two zips: "aubio-{version}-win32-ffmpeg.zip" and "aubio-{version}-win64-ffmpeg.zip"

            for arch in ["32", "64"]:
                self.main.utils.unzip(
                    aubio_folder + f"aubio-{version}-win{arch}-ffmpeg.zip",
                    aubio_folder,
                )

            aubio64 = aubio_folder + f"aubio-{version}-win64-ffmpeg"
            aubio32 = aubio_folder + f"aubio-{version}-win32-ffmpeg"

            # We copy the files to /usr/(mingw arch)/*

            # 64 bit
            sub = self.main.get_subprocess_utils()
            sub.from_string((
                f"sudo cp -var \"{aubio64}/.\" \"/usr/x86_64-w64-mingw32\""
            ))
            sub.run(shell=True)

            # 32 bit
            sub = self.main.get_subprocess_utils()
            sub.from_string((
                f"sudo cp -var \"{aubio32}/.\" \"/usr/i686-w64-mingw32\""
            ))
            sub.run(shell=True)


            # f"sudo cp \"{self.main.directories.workspace}aubio-{version}/build/src/libaubio.so\" /usr/{mingw_pfx}/"

        # Fix undefined reference on mingw, things seem not to blow if we just return false
        if FIX_CREATE_HARD_LINK_A:
            self.main.utils.sprint("FIX_CREATE_HARD_LINK_A", 'a')
            self.main.utils.sed_replace(
                "return CreateHardLinkA (new_path.c_str(), existing_file.c_str(), NULL);",
                "return false;",
                self.main.directories.ardour + "/libs/pbd/file_utils.cc"
            )

        # Add to LDFLAGS
        if FIX_LD_FLAG_FFTW:
            self.main.utils.sprint("FIX_LD_FLAG_FFTW", 'a')
            self.main.utils.sed_replace(
                'LDFLAGS="-L${PREFIX}/lib"',
                'LDFLAGS="-L${PREFIX}/lib -lfftw3 -lfftw3f"',
                self.main.directories.ardour + "/tools/x-win/compile.sh"
            )
        
        # FFTW threads can't be imported with -lfftw3_threads
        if FIX_FFTW_FFTWF_MAKE_PLANNER_THREAD_SAFE:
            self.main.utils.sprint("FIX_FFTW", 'a')
            self.main.utils.sed_replace(
                "fftwf_make_planner_thread_safe ();",
                "void fftwf_make_planner_thread_safe ();",
                self.main.directories.ardour + "libs/ardour/globals.cc"
            )


        # Configure CONCURRENCY
        if COMPILE_THREADS:
            self.main.utils.sed_replace(
                "./waf ${CONCURRENCY}",
                f"./waf build -j {COMPILE_THREADS}",
                self.main.directories.ardour + "/tools/x-win/compile.sh"
            )
        

        # Compile Ardour with their script
        if COMPILE:
            self.main.utils.sprint("COMPILE", 'a')
            
            # PKGCONFIG use mingw libs
            env = self.main.utils.custom_env({
                "PKGCONFIG": f"/usr/bin/{pkgconfig}"
            })

            sub = self.main.get_subprocess_utils()
            sub.from_string((
                "/usr/bin/bash"
                f" \"{self.main.directories.ardour}tools/x-win/compile.sh\""
            ))
            sub.run(env = env, shell=True)

        if BUNDLE_TEST:
            self.main.utils.sprint("BUNDLE_TEST", 'a')
            self.main.utils.mkdir_dne(bundle_directory)

            # Copy every .exe we created
            src = f"{self.main.directories.ardour}build"
            dst = bundle_directory
            match = "*.exe"

            self.main.utils.sprint(f"Copy every file matching \"{match}\" from {src} to {dst}", 'i')

            os.system("find \"%s\" -name '%s' -exec cp -v {} \"%s\" \\;" % (src, match, dst))


            # Copy every dll we build
            src = f"{self.main.directories.ardour}build"
            match = "*.dll"

            self.main.utils.sprint(f"Copy every file matching \"{match}\" from {src} to {bundle_directory}", 'i')

            os.system("find \"%s\" -name '%s' -exec cp -v {} \"%s\" \\;" % (src, match, bundle_directory))


            # Copy mingw dlls
            src = f"/usr/{mingw_pfx}/bin"
            match = "*.dll"

            self.main.utils.sprint(f"Copy every file matching \"{match}\" from {src} to {bundle_directory}", 'i')

            os.system("find \"%s\" -name '%s' -exec cp -v {} \"%s\" \\;" % (src, match, bundle_directory))
        

        # Reading ardour/tools/x-win/package.sh I found how to "build" those urls
        
        harrison = f"https://rsrc.harrisonconsoles.com/plugins/releases/public/harrison_lv2s-n.{plugin_arch}.zip"
        x42 = "http://x42-plugins.com/x42/win/"

        

        # mkdir dne path to bundled lv2 plugins
        self.main.utils.mkdir_dne(lv2_bundle_directory)

        # # # Bundle plugins

        # x42 plugins
        if GET_X42_PLUGINS:
            self.main.utils.sprint("GET_X42_PLUGINS", 'a')
            self.main.utils.sprint("DOWNLOADING PLUGINS ZIPS", 'w')
            
            x42_plugins_zip = self.main.directories.workspace + "x42-plugins/"
            self.main.utils.mkdir_dne(x42_plugins_zip)

            html = urllib.request.urlopen(x42)
            soup = BeautifulSoup(html, "html.parser")

            for link in soup.findAll('a'):
                href = link.get('href')
                if f"lv2-{plugin_arch}" in href:
                    download_url = x42 + href

                    self.main.download.wget(
                        url = download_url,
                        save = x42_plugins_zip + href,
                        name = href,
                    )
        
            self.main.utils.sprint("EXTRACTING PLUGINS ZIPS TO BUNDLE", 'a')

            # Extract contents to Ardour bundle
            for file in os.listdir(x42_plugins_zip):
                self.main.utils.unzip(
                    f"{x42_plugins_zip}/{file}",
                    lv2_bundle_directory,
                    mkdir_dne = False,
                )

        if GET_HARRISON_PLUGINS:
            self.main.utils.sprint("GET_HARRISON_PLUGINS", 'a')
            self.main.utils.sprint("DOWNLOADING PLUGINS ZIPS", 'w')
            
            harrison_plugins_zip = self.main.directories.workspace + "harrison-plugins"
            self.main.utils.mkdir_dne(harrison_plugins_zip)

            self.main.download.wget(
                url = harrison,
                save = harrison_plugins_zip + f"/harrison_lv2s-n.{plugin_arch}.zip",
                name = href,
            )

            self.main.utils.sprint("EXTRACTING PLUGINS ZIPS TO BUNDLE", 'a')

            # Extract contents to Ardour bundle
            for file in os.listdir(harrison_plugins_zip):
                self.main.utils.unzip(
                    f"{harrison_plugins_zip}/{file}",
                    lv2_bundle_directory,
                    mkdir_dne = False,
                )
        # 7z a -mmt bundle.7z -m0=lzma2 -mx=9 ardour_bundle/


            
