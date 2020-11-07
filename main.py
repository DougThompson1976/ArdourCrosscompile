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

from directories import Directories
from utils import SubprocessUtils
from download import Download
from actions import Actions
from pacman import Pacman
from utils import Utils
import copy
import sys


class Main:
    """
    kwargs: {
        argv: expected sys.argv
            Tries breaking into arguments of flags and key flags
            flags are just texts like python script.py flag1 flag2 --flag3
            key flags have equal sign python script.py this=that --other_flag=that-one
            Not the best solution and doesn't work for spacer, easier for me to format

            flags:
                "wsl": Assume this is running on WSL Arch, changes one dependency (fakeroot -> fakeroot-tcp)
                "onego": Calls yay for installing ALL packages at once listed on requirements
    }
    """
    def __init__(self, **kwargs):
        debug_prefix = "[Main.__init__]"

        # Argv from shell
        self.argv = kwargs["argv"]

        # Empty list of flags and kflags
        self.flags = []
        self.kflags = {}

        if self.argv is not None:

            # Iterate in all args
            for arg in self.argv[1:]:
                
                # Is a kwarg
                if "=" in arg:
                    arg = arg.split("=")
                    self.kflags[arg[0]] = arg[1]

                # Is a flag
                else:
                    self.flags.append(arg)
        
        # Print user flags from the terminal
        print(debug_prefix, "Flags are:", self.flags)
        print(debug_prefix, "Keyword flags are:", self.kflags)

        # Create classes
        self.utils = Utils(self)
        self.subprocess_utils = SubprocessUtils(self)
        self.pacman = Pacman(self)
        self.directories = Directories(self)
        self.download = Download(self)
        self.actions = Actions(self)

        # Runs every action
        self.actions.run()

    def get_subprocess_utils(self):
        return copy.deepcopy(self.subprocess_utils)

Main(argv = sys.argv)
