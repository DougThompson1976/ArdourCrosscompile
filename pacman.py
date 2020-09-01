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

import subprocess

class Requirements:
    def __init__(self, main):
        self.main = main

        self.requirements = [
            # mingw-w64-toolchain group
            "binutils",
            "crt",
            "gcc",
            "headers",
            "winpthreads",

            # Special ones that either AUR broken, need manual installing
            "gtk2",
            "aubio", # Aubio will always be missing here
        ]

        self.requirements = {f"mingw-w64-{name}": False for name in self.requirements}

    def check_installed(self):
        self.main.utils.sprint(f"Checking already installed packages from requirements", 'i')

        for pkgname in self.requirements.keys():
            self.requirements[pkgname] = self.main.pacman.is_package_installed(pkgname)

        # Get number of installed packages and needed
        installed = sum(self.requirements.values())
        needed = len(self.requirements.keys()) - installed

        self.main.utils.sprint(f"Status of packages: installed [{installed}], missing [{needed}]", 'i')

class Pacman:
    def __init__(self, main):
        self.main = main
        self.requirements = Requirements(self.main)

    # `pacman -Qq` --> Python list
    def get_installed_packages(self):
        self.main.utils.sprint(f"Getting installed packages", 'c')
        
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
