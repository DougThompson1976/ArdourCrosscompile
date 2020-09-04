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

# # # Package manager

NOCONFIRM = True


# # #

# Get source code

CLONE_ARDOUR = True
RESET = True  # Hard reset, overwrite local changes on SOURCE CODE

# Packages

CHECK_NEEDED_PACKAGES = True
INSTALL_AUR_PACKAGES = True

# "Manual" installed package
INSTALL_MINGW_JACK = False
INSTALL_AUBIO = True  # Their website expired certificates

# Fixes on Ardour scripts

FIX_CREATE_HARD_LINK_A = True
FIX_LD_FLAG_FFTW = True
FIX_FFTW_FFTWF_MAKE_PLANNER_THREAD_SAFE = True

# 

XARCH_X86_64 = False  # Compile for Windows 64 bit, 32 bit if False

if INSTALL_MINGW_JACK:
    AUDIO_BACKENDS = "portaudio,jack,dummy"
else:
    AUDIO_BACKENDS = "portaudio,dummy"

CXX_11 = True
OPTIMIZED = True  # Build a optimized executable of Ardour


# Compile options

COMPILE_THREADS = 4
COMPILE = True


BUNDLE_TEST = True


GET_X42_PLUGINS = True
GET_HARRISON_PLUGINS = True




