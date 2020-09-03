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

from requirements import Requirements
from config import *
import subprocess


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
