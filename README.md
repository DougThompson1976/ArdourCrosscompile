# Python script for cross compiling Ardour DAW from Arch Linux targeting Windows

WIP, lots of steps to cross compile Ardour.

This script will work best on a Arch Linux distribution, it can work on other based distros like Manjaro, however I offer no support for those.

I'm guessing this will install at least 5 GB of MinGW dependencies and lots of packages, see `pacman.py` file for a complete list.

Installing the dependencies is the longest and hardest part while compiling and bundling Ardour itself is pretty straightforward; it took me about 2 to 3 hours of total compile time for all `mingw-*` packages including optional ones on a mainstream CPU.

## CONSIDER SUPPORTING ARDOUR DEVELOPMENT, BUY THEIR PRODUCT OR A SUBSCRIPTION.

#### Why Arch?

Out of Ubuntu, Fedora, OpenSUSE and Arch Linux, I was only successful cross compiling on Arch.

If you're on Windows, consider running this on WSL (Windows Subsystem for Linux), but you really should just use Linux, we have many free (as in price and freedom) plugins, such as Calf Studio Gear, ZynFusion, Disthro ports of LV2 / VST, TAL Plugins, and many others honorable mentions.

Compiling Ardour for Windows IS hard, under the penguin it is a lot more simple and straightforward.

# Roadmap

- [x] Basic shell functions (rmdir, sed a file, mkdir, etc)

- [ ] Download sources, urls simple way

- [ ] Manually patch files (mainly two PKGBUILDS)

- [x] Pacman wrapper for installing dependencies, needed ones, etc.
 
- [ ] From a finished build, package ardour

And others I might add as development goes on.

# Legal, disclaimer

### Ardour developers offer NO SUPPORT and WARRANTY on DIY builds and third party.

Only the files that comes with this repo are under the MIT license, downloaded files and sources licenses have their own license, own creators, etc.

If you find something wrong (like me downloading a file the user should do by hand because distribution problems), let me know!!

## Security / warranty

I do have to use some stuff like calling `shell=True` under Python's subprocess module, mainly for using `yay` for installing tha AUR packages.

I do not take responsibility for malicious AUR PKGBUILDS (I personally never had issues with them, just don't use something very deep and dark on it).

Most packages are from the mingw group and / or community / extra repositories (like `base-devel` package).

# Running / contributing / issues

Please before compiling have `yay` installed and run `yay -Syu python` for upgrading / syncing the system and installing python.

This script only uses native python modules / packages.

Edit `config.py` to your needs, run `python main.py`, if you want to install some packages by hand (or all) see file `pacman.py`, Requirements class.

Any issues with the scripts create a issue or contact me, any issues with AUR PKGBUILDs we can try solving together as well.

## CONSIDER SUPPORTING ARDOUR DEVELOPMENT, BUY THEIR PRODUCT OR A SUBSCRIPTION.
